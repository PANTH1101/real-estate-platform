from django.urls import path

from .views import (
    PropertyCreateView,
    PropertyDeleteView,
    PropertyDetailView,
    PropertyListView,
    PropertyUpdateView,
)

app_name = "property"

urlpatterns = [
    path("", PropertyListView.as_view(), name="list"),
    path("<int:pk>/", PropertyDetailView.as_view(), name="detail"),
    path("create-form/", PropertyCreateView.as_view(), name="create_form"),
    path("<int:pk>/edit/", PropertyUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PropertyDeleteView.as_view(), name="delete"),
]


