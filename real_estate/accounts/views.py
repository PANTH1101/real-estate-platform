from functools import wraps
import json
import secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from django.db.models import OuterRef, Subquery
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from apps.accounts.models import UserRole
from .forms import (
    BuyerLoginForm,
    BuyerSignupForm,
    SellerLoginForm,
    SellerProfileForm,
    SellerSignupForm,
)
from .models import Seller
from payment.models import Payment

User = get_user_model()


def seller_login_required(view_func):
    """
    Decorator that works for both function-based views and class-based views'
    dispatch methods. It checks for `seller_id` in session.
    """

    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        # When used on a CBV method via method_decorator, args[0] is self,
        # args[1] is request. For a normal function view, args[0] is request.
        if isinstance(args[0], HttpRequest):
            request = args[0]
            self = None
            remaining_args = args[1:]
        else:
            self = args[0]
            request = args[1]
            remaining_args = args[2:]

        if not request.session.get("seller_id"):
            return redirect(f"{reverse('accounts:login')}?next={request.path}")

        if self is None:
            return view_func(request, *remaining_args, **kwargs)
        return view_func(self, request, *remaining_args, **kwargs)

    return _wrapped


class SignupView(View):
    template_name = "accounts/signup.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = SellerSignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            seller = form.save()
            request.session["seller_id"] = seller.id
            messages.success(request, "Account created successfully.")
            return redirect("accounts:dashboard")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = SellerLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            seller = Seller.objects.filter(email=email, password=password).first()
            if seller:
                request.session["seller_id"] = seller.id
                messages.success(request, "Logged in successfully.")
                next_url = request.GET.get("next") or reverse("accounts:dashboard")
                return redirect(next_url)
            messages.error(request, "Invalid email or password.")
        return render(request, self.template_name, {"form": form})


class GoogleLoginStartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not settings.GOOGLE_OAUTH_CLIENT_ID or not settings.GOOGLE_OAUTH_CLIENT_SECRET:
            messages.error(request, "Google login is not configured yet.")
            return redirect("accounts:login")

        state = secrets.token_urlsafe(24)
        request.session["google_oauth_state"] = state

        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            request.session["google_login_next"] = next_url
        else:
            request.session["google_login_next"] = reverse("accounts:dashboard")

        redirect_uri = request.build_absolute_uri(reverse("accounts:google_callback"))
        params = {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "prompt": "select_account",
        }
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}")


class GoogleLoginCallbackView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        expected_state = request.session.pop("google_oauth_state", None)
        state = request.GET.get("state")
        code = request.GET.get("code")
        error = request.GET.get("error")

        if error:
            messages.error(request, "Google login was cancelled or failed.")
            return redirect("accounts:login")

        if not expected_state or state != expected_state:
            messages.error(request, "Invalid Google login state. Please try again.")
            return redirect("accounts:login")

        if not code:
            messages.error(request, "Google did not return an authorization code.")
            return redirect("accounts:login")

        redirect_uri = request.build_absolute_uri(reverse("accounts:google_callback"))

        try:
            token_data = urlencode(
                {
                    "code": code,
                    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            ).encode("utf-8")
            token_req = Request(
                "https://oauth2.googleapis.com/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with urlopen(token_req, timeout=10) as token_resp:
                token_payload = json.loads(token_resp.read().decode("utf-8"))

            access_token = token_payload.get("access_token")
            if not access_token:
                raise ValueError("Missing access token")

            userinfo_req = Request(
                f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}",
                method="GET",
            )
            with urlopen(userinfo_req, timeout=10) as userinfo_resp:
                user_info = json.loads(userinfo_resp.read().decode("utf-8"))
        except Exception:
            messages.error(request, "Unable to sign in with Google right now.")
            return redirect("accounts:login")

        email = (user_info.get("email") or "").strip().lower()
        name = (user_info.get("name") or "").strip()
        email_verified = bool(user_info.get("verified_email", False))

        if not email:
            messages.error(request, "Google account did not return an email.")
            return redirect("accounts:login")

        if not email_verified:
            messages.error(request, "Google account email is not verified.")
            return redirect("accounts:login")

        seller, created = Seller.objects.get_or_create(
            email=email,
            defaults={
                "name": name or email.split("@")[0],
                "phone": "",
                "password": "google_oauth",
            },
        )
        if not created and name and seller.name != name:
            seller.name = name
            seller.save(update_fields=["name"])

        request.session["seller_id"] = seller.id
        messages.success(request, "Logged in with Google successfully.")

        next_url = request.session.pop("google_login_next", reverse("accounts:dashboard"))
        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = reverse("accounts:dashboard")
        return redirect(next_url)


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        auth_logout(request)
        request.session.flush()
        messages.info(request, "You have been logged out.")
        return redirect("home")


class LoginChoiceView(View):
    template_name = "accounts/auth_choice.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "mode": "login",
                "title": "Login",
            },
        )


class SignupChoiceView(View):
    template_name = "accounts/auth_choice.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "mode": "signup",
                "title": "Signup",
            },
        )


class BuyerSignupView(View):
    template_name = "accounts/buyer_signup.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = BuyerSignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = BuyerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            request.session.pop("seller_id", None)
            messages.success(request, "Buyer account created successfully.")
            next_url = request.GET.get("next") or reverse("home")
            if not url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = reverse("home")
            return redirect(next_url)
        return render(request, self.template_name, {"form": form})


class BuyerLoginView(View):
    template_name = "accounts/buyer_login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = BuyerLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = BuyerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user and user.is_active and user.role == UserRole.BUYER:
                auth_login(request, user)
                request.session.pop("seller_id", None)
                messages.success(request, "Buyer login successful.")
                next_url = request.GET.get("next") or reverse("home")
                if not url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    next_url = reverse("home")
                return redirect(next_url)
            messages.error(request, "Invalid buyer credentials.")
        return render(request, self.template_name, {"form": form})


class BuyerGoogleLoginStartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not settings.GOOGLE_OAUTH_CLIENT_ID or not settings.GOOGLE_OAUTH_CLIENT_SECRET:
            messages.error(request, "Google login is not configured yet.")
            return redirect("accounts:buyer_login")

        state = secrets.token_urlsafe(24)
        request.session["buyer_google_oauth_state"] = state

        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            request.session["buyer_google_login_next"] = next_url
        else:
            request.session["buyer_google_login_next"] = reverse("home")

        redirect_uri = request.build_absolute_uri(reverse("accounts:buyer_google_callback"))
        params = {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "prompt": "select_account",
        }
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}")


class BuyerGoogleLoginCallbackView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        expected_state = request.session.pop("buyer_google_oauth_state", None)
        state = request.GET.get("state")
        code = request.GET.get("code")
        error = request.GET.get("error")

        if error:
            messages.error(request, "Google login was cancelled or failed.")
            return redirect("accounts:buyer_login")

        if not expected_state or state != expected_state:
            messages.error(request, "Invalid Google login state. Please try again.")
            return redirect("accounts:buyer_login")

        if not code:
            messages.error(request, "Google did not return an authorization code.")
            return redirect("accounts:buyer_login")

        redirect_uri = request.build_absolute_uri(reverse("accounts:buyer_google_callback"))

        try:
            token_data = urlencode(
                {
                    "code": code,
                    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            ).encode("utf-8")
            token_req = Request(
                "https://oauth2.googleapis.com/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with urlopen(token_req, timeout=10) as token_resp:
                token_payload = json.loads(token_resp.read().decode("utf-8"))

            access_token = token_payload.get("access_token")
            if not access_token:
                raise ValueError("Missing access token")

            userinfo_req = Request(
                f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}",
                method="GET",
            )
            with urlopen(userinfo_req, timeout=10) as userinfo_resp:
                user_info = json.loads(userinfo_resp.read().decode("utf-8"))
        except Exception:
            messages.error(request, "Unable to sign in with Google right now.")
            return redirect("accounts:buyer_login")

        email = (user_info.get("email") or "").strip().lower()
        name = (user_info.get("name") or "").strip()
        email_verified = bool(user_info.get("verified_email", False))

        if not email:
            messages.error(request, "Google account did not return an email.")
            return redirect("accounts:buyer_login")

        if not email_verified:
            messages.error(request, "Google account email is not verified.")
            return redirect("accounts:buyer_login")

        user = User.objects.filter(email=email).first()
        if user and user.role != UserRole.BUYER:
            messages.error(
                request,
                "This Google account is linked to a non-buyer profile. Use the correct login type.",
            )
            return redirect("accounts:buyer_login")

        if not user:
            user = User.objects.create_user(
                email=email,
                password=None,
                full_name=name or email.split("@")[0],
                phone_number="",
                role=UserRole.BUYER,
                is_active=True,
                is_email_verified=True,
            )
        elif name and user.full_name != name:
            user.full_name = name
            user.save(update_fields=["full_name"])

        auth_login(request, user)
        request.session.pop("seller_id", None)
        messages.success(request, "Logged in with Google successfully.")

        next_url = request.session.pop("buyer_google_login_next", reverse("home"))
        if not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = reverse("home")
        return redirect(next_url)


@method_decorator(seller_login_required, name="dispatch")
class DashboardView(View):
    template_name = "accounts/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        latest_payment_status = (
            Payment.objects.filter(property_id=OuterRef("pk"))
            .order_by("-created_at")
            .values("status")[:1]
        )
        properties = (
            seller.properties.all()
            .prefetch_related("leads")
            .annotate(payment_status=Subquery(latest_payment_status))
        )
        total_leads = sum(p.leads.count() for p in properties)
        return render(
            request,
            self.template_name,
            {
                "seller": seller,
                "properties": properties,
                "total_leads": total_leads,
            },
        )


@method_decorator(seller_login_required, name="dispatch")
class ProfileView(View):
    template_name = "accounts/profile.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        form = SellerProfileForm(instance=seller)
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        form = SellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form})


