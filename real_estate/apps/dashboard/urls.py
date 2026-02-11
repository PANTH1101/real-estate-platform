from django.urls import path

from apps.properties.views import PropertyViewSet
from .views import AdminAnalyticsView, AdminUsersView


urlpatterns = [
    path("admin/users/", AdminUsersView.as_view()),
    path("admin/analytics/", AdminAnalyticsView.as_view()),
    # exact endpoint requested: PUT /api/admin/property/{id}/approve/
    path("admin/property/<uuid:pk>/approve/", PropertyViewSet.as_view({"put": "approve"})),
]


