from django.urls import path

from .views import PaymentCallbackView, PaymentCreateView

app_name = "payment"

urlpatterns = [
    path("create/", PaymentCreateView.as_view(), name="create"),
    path("callback/", PaymentCallbackView.as_view(), name="callback"),
]


