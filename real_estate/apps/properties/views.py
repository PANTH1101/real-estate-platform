from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsAdminRole, IsSeller

from .filters import PropertyFilter
from .models import Property
from .serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter

    def get_queryset(self):
        qs = Property.objects.all().select_related("owner").prefetch_related("media")
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and getattr(user, "role", None) == "ADMIN":
            return qs
        # public: only approved properties
        return qs.filter(is_approved=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve", "search"):
            return [permissions.AllowAny()]
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsSeller()]
        if self.action in ("approve",):
            return [permissions.IsAuthenticated(), IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_approved=False)

    def perform_update(self, serializer):
        # sellers can only edit their own properties
        if serializer.instance.owner_id != self.request.user.id:
            raise permissions.PermissionDenied("Cannot edit another seller's property")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.id:
            raise permissions.PermissionDenied("Cannot delete another seller's property")
        instance.delete()

    @action(detail=False, methods=["get"], url_path="search", permission_classes=[permissions.AllowAny])
    def search(self, request):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(PropertySerializer(page, many=True).data)
        return Response(PropertySerializer(qs, many=True).data)

    @action(detail=True, methods=["put"], url_path="approve", permission_classes=[permissions.IsAuthenticated, IsAdminRole])
    def approve(self, request, pk=None):
        prop = self.get_object()
        prop.is_approved = True
        prop.save(update_fields=["is_approved"])
        return Response({"detail": "Approved"})


