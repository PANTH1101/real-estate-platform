from django.urls import path

from .views import BuyerLeadCreateView

app_name = "leads"

urlpatterns = [
    path("create/<int:property_id>/", BuyerLeadCreateView.as_view(), name="create"),
]


