from django.urls import path

from .views import (
    BuyerGoogleLoginCallbackView,
    BuyerGoogleLoginStartView,
    BuyerLoginView,
    BuyerSignupView,
    DashboardView,
    GoogleLoginCallbackView,
    GoogleLoginStartView,
    LoginChoiceView,
    LoginView,
    LogoutView,
    ProfileView,
    SignupChoiceView,
    SignupView,
)

app_name = "accounts"

urlpatterns = [
    path("login/options/", LoginChoiceView.as_view(), name="login_choice"),
    path("signup/options/", SignupChoiceView.as_view(), name="signup_choice"),
    path("buyer/login/", BuyerLoginView.as_view(), name="buyer_login"),
    path("buyer/google/login/", BuyerGoogleLoginStartView.as_view(), name="buyer_google_login"),
    path("buyer/google/callback/", BuyerGoogleLoginCallbackView.as_view(), name="buyer_google_callback"),
    path("buyer/signup/", BuyerSignupView.as_view(), name="buyer_signup"),
    path("seller/signup/", SignupView.as_view(), name="seller_signup"),
    path("seller/login/", LoginView.as_view(), name="seller_login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("google/login/", GoogleLoginStartView.as_view(), name="google_login"),
    path("google/callback/", GoogleLoginCallbackView.as_view(), name="google_callback"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),
]


