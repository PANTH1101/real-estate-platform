from rest_framework.permissions import BasePermission

from .models import UserRole


class IsBuyer(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.BUYER)


class IsSeller(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.SELLER)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)


