from django.urls import path

from .views import (
    AdminAmenityCreateView,
    AdminPanelLoginView,
    AdminPanelLogoutView,
    ApprovePendingPropertyView,
    DeactivateLivePropertyView,
    PendingPropertyAdminView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyDetailView,
    PropertyListView,
    PropertyPreviewView,
    PropertyUpdateView,
)

app_name = "property"

urlpatterns = [
    path("admin/login/", AdminPanelLoginView.as_view(), name="admin_login"),
    path("admin/logout/", AdminPanelLogoutView.as_view(), name="admin_logout"),
    path("admin/pending/", PendingPropertyAdminView.as_view(), name="admin_pending"),
    path("admin/amenities/add/", AdminAmenityCreateView.as_view(), name="admin_add_amenity"),
    path(
        "admin/pending/<int:pk>/approve/",
        ApprovePendingPropertyView.as_view(),
        name="admin_approve_property",
    ),
    path(
        "admin/live/<int:pk>/deactivate/",
        DeactivateLivePropertyView.as_view(),
        name="admin_deactivate_property",
    ),
    path("", PropertyListView.as_view(), name="list"),
    path("<int:pk>/", PropertyDetailView.as_view(), name="detail"),
    path("<int:pk>/preview/", PropertyPreviewView.as_view(), name="preview"),
    path("create-form/", PropertyCreateView.as_view(), name="create_form"),
    path("<int:pk>/edit/", PropertyUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PropertyDeleteView.as_view(), name="delete"),
]
