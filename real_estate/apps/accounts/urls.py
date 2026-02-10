from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    ProfileView,
    RefreshView,
    RegisterView,
    VerifyEmailView,
)


urlpatterns = [
    # AUTH
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/refresh/", RefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/verify-email/", VerifyEmailView.as_view()),
    path("auth/password-reset/", PasswordResetView.as_view()),
    # USER
    path("users/profile/", ProfileView.as_view()),
]


