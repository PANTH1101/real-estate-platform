from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from accounts.views import seller_login_required
from accounts.models import Seller

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
        prop = get_object_or_404(
            Property.objects.select_related("seller").prefetch_related(
                "images", "amenities"
            ),
            pk=pk,
            is_active=True,
        )
        return render(request, self.template_name, {"property": prop})


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
                "Property saved as draft. Complete payment to list it publicly.",
            )
            return redirect(f"{reverse('payment:create')}?property_id={prop.id}")
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


