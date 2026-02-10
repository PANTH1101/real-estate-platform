from django.urls import path

from .views import DashboardView, LoginView, LogoutView, ProfileView, SignupView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),
]


