from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer
from .tokens import get_tokens_for_user


def _set_jwt_cookies(response: Response, access: str, refresh: str) -> None:
    cookie_kwargs = {
        "httponly": True,
        "secure": bool(getattr(settings, "JWT_COOKIE_SECURE", False)),
        "samesite": getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
        "path": "/",
    }
    response.set_cookie(getattr(settings, "JWT_COOKIE_NAME", "access"), access, **cookie_kwargs)
    response.set_cookie(getattr(settings, "JWT_REFRESH_COOKIE_NAME", "refresh"), refresh, **cookie_kwargs)


def _clear_jwt_cookies(response: Response) -> None:
    response.delete_cookie(getattr(settings, "JWT_COOKIE_NAME", "access"), path="/")
    response.delete_cookie(getattr(settings, "JWT_REFRESH_COOKIE_NAME", "refresh"), path="/")


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        tokens = get_tokens_for_user(user)
        resp = Response({"user": UserProfileSerializer(user).data}, status=status.HTTP_201_CREATED)
        _set_jwt_cookies(resp, tokens["access"], tokens["refresh"])
        return resp


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        s = LoginSerializer(data=request.data, context={"request": request})
        s.is_valid(raise_exception=True)
        user = s.validated_data["user"]
        tokens = get_tokens_for_user(user)
        resp = Response({"user": UserProfileSerializer(user).data})
        _set_jwt_cookies(resp, tokens["access"], tokens["refresh"])
        return resp


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.COOKIES.get(getattr(settings, "JWT_REFRESH_COOKIE_NAME", "refresh")) or request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh)
        access = str(token.access_token)
        resp = Response({"access": access})
        resp.set_cookie(
            getattr(settings, "JWT_COOKIE_NAME", "access"),
            access,
            httponly=True,
            secure=bool(getattr(settings, "JWT_COOKIE_SECURE", False)),
            samesite=getattr(settings, "JWT_COOKIE_SAMESITE", "Lax"),
            path="/",
        )
        return resp


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        resp = Response({"detail": "Logged out"})
        _clear_jwt_cookies(resp)
        return resp


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Placeholder: hook into email token verification later
        return Response({"detail": "Email verification endpoint (to be implemented)"}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Placeholder: hook into email-based password reset later
        return Response({"detail": "Password reset endpoint (to be implemented)"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    def put(self, request):
        s = UserProfileSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)


