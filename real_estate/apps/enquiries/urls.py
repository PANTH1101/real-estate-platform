from django.urls import path

from .views import EnquiryCreateView, SellerEnquiriesView


urlpatterns = [
    path("enquiries/", EnquiryCreateView.as_view()),
    path("enquiries/seller/", SellerEnquiriesView.as_view()),
]


