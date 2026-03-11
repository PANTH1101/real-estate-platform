from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, OuterRef, Q, Subquery, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from accounts.views import seller_login_required
from accounts.models import Seller
from apps.accounts.models import UserRole
from payment.models import Payment

from .forms import PropertyForm, PropertyImageFormSet
from .models import Amenity, Property


class HomeView(View):
    template_name = "property/home.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get("q", "")
        city = request.GET.get("city", "")
        bhk = request.GET.get("bhk", "")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        properties = Property.objects.active().select_related("seller").prefetch_related(
            "images"
        )
        if query:
            properties = properties.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(city__icontains=query)
            )
        if city:
            properties = properties.filter(city__icontains=city)
        if bhk:
            properties = properties.filter(bhk=bhk)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)

        latest_properties = properties[:8]

        return render(
            request,
            self.template_name,
            {
                "latest_properties": latest_properties,
            },
        )


class PropertyListView(View):
    template_name = "property/property_list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        qs = Property.objects.active().select_related("seller").prefetch_related(
            "images", "amenities"
        )
        category = request.GET.get("category")
        ptype = request.GET.get("type")
        city = request.GET.get("city")
        state = request.GET.get("state")
        bhk = request.GET.get("bhk")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        amenities = request.GET.getlist("amenities")
        sort = request.GET.get("sort")

        if category:
            qs = qs.filter(category=category)
        if ptype:
            qs = qs.filter(property_type=ptype)
        if city:
            qs = qs.filter(city__icontains=city)
        if state:
            qs = qs.filter(state__icontains=state)
        if bhk:
            qs = qs.filter(bhk=bhk)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if amenities:
            qs = qs.filter(amenities__id__in=amenities).distinct()

        if sort == "price_high":
            qs = qs.order_by("-price")
        elif sort == "price_low":
            qs = qs.order_by("price")
        else:
            qs = qs.order_by("-created_at")

        paginator = Paginator(qs, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        all_amenities = Amenity.objects.all()

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "amenities": all_amenities,
            },
        )


class PropertyDetailView(View):
    template_name = "property/property_detail.html"

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        # Allow a logged-in seller to view their own property's detail page without
        # needing a buyer login.
        seller_id = request.session.get("seller_id")
        if seller_id:
            seller_property = (
                Property.objects.select_related("seller")
                .prefetch_related("images", "amenities")
                .filter(pk=pk, seller_id=seller_id)
                .first()
            )
            if seller_property:
                if not seller_property.is_active:
                    messages.info(
                        request,
                        "This is a preview of your listing. It will be visible to buyers after an admin activates it.",
                    )
                return render(
                    request,
                    self.template_name,
                    {"property": seller_property, "is_seller_owner": True},
                )

        if not request.user.is_authenticated or request.user.role != UserRole.BUYER:
            messages.info(request, "Login required to view property details.")
            buyer_login_url = reverse("accounts:buyer_login")
            return redirect(f"{buyer_login_url}?next={request.path}")

        prop = get_object_or_404(
            Property.objects.select_related("seller").prefetch_related("images", "amenities"),
            pk=pk,
            is_active=True,
        )
        return render(
            request,
            self.template_name,
            {"property": prop, "is_seller_owner": False},
        )


class PropertyPreviewView(View):
    template_name = "property/property_detail.html"

    @seller_login_required
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        seller_id = request.session.get("seller_id")
        prop = get_object_or_404(
            Property.objects.select_related("seller").prefetch_related("images", "amenities"),
            pk=pk,
            seller_id=seller_id,
        )
        messages.info(
            request,
            "This is a preview of your listing. It will be visible to buyers after an admin activates it.",
        )
        return render(
            request,
            self.template_name,
            {"property": prop, "is_seller_owner": True},
        )


class PropertyCreateView(View):
    template_name = "property/property_form.html"

    @seller_login_required
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = PropertyForm()
        formset = PropertyImageFormSet()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        form = PropertyForm(request.POST)
        formset = PropertyImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            prop = form.save(commit=False)
            prop.seller = seller
            prop.is_active = False
            prop.save()
            form.save_m2m()
            images = formset.save(commit=False)
            for img in images:
                img.property = prop
                img.save()
            messages.info(
                request,
                "Property saved as draft. Complete payment so an admin can review and activate your listing.",
            )
            payment_url = f"{reverse('payment:create')}?property_id={prop.id}"
            return redirect(payment_url)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
            },
        )


class PropertyUpdateView(View):
    template_name = "property/property_form.html"

    @seller_login_required
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, request: HttpRequest, pk: int) -> Property:
        seller_id = request.session.get("seller_id")
        return get_object_or_404(Property, pk=pk, seller_id=seller_id)

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        prop = self.get_object(request, pk)
        form = PropertyForm(instance=prop)
        formset = PropertyImageFormSet(instance=prop)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
                "property": prop,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        prop = self.get_object(request, pk)
        form = PropertyForm(request.POST, instance=prop)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=prop)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Property updated.")
            return redirect("accounts:dashboard")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
                "property": prop,
            },
        )


class PropertyDeleteView(View):
    @seller_login_required
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        seller_id = request.session.get("seller_id")
        prop = get_object_or_404(Property, pk=pk, seller_id=seller_id)
        prop.delete()
        messages.info(request, "Property deleted.")
        return redirect("accounts:dashboard")


class AdminPanelLoginView(View):
    template_name = "property/admin_login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_staff:
            return redirect("property:admin_pending")
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=email, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, "Welcome to the admin panel.")
            return redirect("property:admin_pending")

        messages.error(request, "Invalid admin credentials.")
        return render(request, self.template_name, {"email": email})


class AdminPanelLogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        messages.info(request, "Admin panel session ended.")
        return redirect("property:admin_login")


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class PendingPropertyAdminView(View):
    template_name = "property/admin_pending_properties.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        latest_payment_status = (
            Payment.objects.filter(property_id=OuterRef("pk"))
            .order_by("-created_at")
            .values("status")[:1]
        )
        pending_properties = (
            Property.objects.filter(is_active=False)
            .annotate(payment_status=Subquery(latest_payment_status))
            .select_related("seller")
            .prefetch_related("images")
            .order_by("-created_at")
        )
        live_properties = (
            Property.objects.filter(is_active=True)
            .select_related("seller")
            .prefetch_related("images")
            .order_by("-updated_at")
        )
        payments = (
            Payment.objects.select_related("seller", "property")
            .order_by("-created_at")
        )
        successful_payments = payments.filter(status="SUCCESS")
        payment_success_amount = successful_payments.aggregate(total=Sum("amount"))["total"] or 0
        amenities = Amenity.objects.all()

        return render(
            request,
            self.template_name,
            {
                "pending_properties": pending_properties,
                "live_properties": live_properties,
                "payments": payments,
                "amenities": amenities,
                "total_properties": pending_properties.count() + live_properties.count(),
                "pending_count": pending_properties.count(),
                "live_count": live_properties.count(),
                "amenity_count": amenities.count(),
                "payment_count": payments.count(),
                "payment_success_count": successful_payments.count(),
                "payment_success_amount": payment_success_amount,
            },
        )


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class ApprovePendingPropertyView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        prop = get_object_or_404(Property, pk=pk, is_active=False)
        prop.is_active = True
        prop.save(update_fields=["is_active", "updated_at"])
        messages.success(request, f'"{prop.title}" is now live on the website.')
        return redirect("property:admin_pending")


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class DeactivateLivePropertyView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        prop = get_object_or_404(Property, pk=pk, is_active=True)
        prop.is_active = False
        prop.save(update_fields=["is_active", "updated_at"])
        messages.info(request, f'"{prop.title}" moved back to pending.')
        return redirect("property:admin_pending")


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class AdminAmenityCreateView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        amenity_name = (request.POST.get("amenity_name") or "").strip()
        if not amenity_name:
            messages.error(request, "Amenity name is required.")
            return redirect("property:admin_pending")

        existing = Amenity.objects.filter(name__iexact=amenity_name).first()
        if existing:
            messages.info(request, f'Amenity "{existing.name}" already exists.')
            return redirect("property:admin_pending")

        Amenity.objects.create(name=amenity_name)
        messages.success(request, f'Amenity "{amenity_name}" added successfully.')
        return redirect("property:admin_pending")


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class AdminAmenityDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        amenity = get_object_or_404(Amenity, pk=pk)
        amenity_name = amenity.name
        amenity.delete()
        messages.info(request, f'Amenity "{amenity_name}" deleted.')
        return redirect("property:admin_pending")


@method_decorator(staff_member_required(login_url="/properties/admin/login/"), name="dispatch")
class AdminPropertyDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        prop = get_object_or_404(Property, pk=pk)
        prop_title = prop.title
        prop.delete()
        messages.info(request, f'Property "{prop_title}" deleted.')
        return redirect("property:admin_pending")
