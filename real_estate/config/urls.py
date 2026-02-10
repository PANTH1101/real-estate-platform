from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

from property.views import HomeView, PropertyCreateView
from apps.dashboard.views import BuyerDashboardView, SellerDashboardView, AdminDashboardView


def render_template(request, template_name, context=None):
    return render(request, template_name, context or {})


urlpatterns = [
    # legacy UI + pages (kept)
    path("", HomeView.as_view(), name="home"),
    path("accounts/", include("accounts.urls")),
    path("properties/", include("property.urls")),
    path("property/create/", PropertyCreateView.as_view(), name="property_create"),
    path("leads/", include("leads.urls")),
    path("payment/", include("payment.urls")),
    path("admin/", admin.site.urls),
    # new API-first backend
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.properties.urls")),
    path("api/", include("apps.wishlist.urls")),
    path("api/", include("apps.enquiries.urls")),
    path("api/", include("apps.dashboard.urls")),
    # new frontend pages (API-based)
    path("auth/login/", lambda r: render_template(r, "auth/login_api.html"), name="auth_login"),
    path("auth/register/", lambda r: render_template(r, "auth/register_api.html"), name="auth_register"),
    path("properties/list/", lambda r: render_template(r, "properties/list_api.html"), name="properties_list_api"),
    path("properties/<uuid:pk>/", lambda r, pk: render_template(r, "properties/detail_api.html", {"property_id": pk}), name="property_detail_api"),
    path("dashboard/buyer/", BuyerDashboardView.as_view(), name="dashboard_buyer"),
    path("dashboard/seller/", SellerDashboardView.as_view(), name="dashboard_seller"),
    path("dashboard/admin/", AdminDashboardView.as_view(), name="dashboard_admin"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
