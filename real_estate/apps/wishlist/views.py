from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsBuyer
from apps.properties.models import Property

from .models import Wishlist


class WishlistListView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        items = (
            Wishlist.objects.filter(user=request.user)
            .select_related("property")
            .order_by("-created_at")
        )
        return Response(
            [
                {
                    "property_id": str(i.property_id),
                    "created_at": i.created_at,
                    "title": i.property.title,
                    "price": i.property.price,
                    "city": i.property.city,
                    "locality": i.property.locality,
                }
                for i in items
            ]
        )


class WishlistAddView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        property_id = request.data.get("property_id")
        if not property_id:
            return Response({"detail": "property_id required"}, status=status.HTTP_400_BAD_REQUEST)
        prop = Property.objects.filter(id=property_id, is_approved=True).first()
        if not prop:
            return Response({"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        Wishlist.objects.get_or_create(user=request.user, property=prop)
        return Response({"detail": "Added"})


class WishlistRemoveView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def delete(self, request, property_id):
        Wishlist.objects.filter(user=request.user, property_id=property_id).delete()
        return Response({"detail": "Removed"})


