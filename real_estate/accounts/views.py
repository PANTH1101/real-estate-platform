from functools import wraps

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SellerLoginForm, SellerProfileForm, SellerSignupForm
from .models import Seller


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


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        request.session.flush()
        messages.info(request, "You have been logged out.")
        return redirect("home")


@method_decorator(seller_login_required, name="dispatch")
class DashboardView(View):
    template_name = "accounts/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        properties = seller.properties.all().prefetch_related("leads")
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


