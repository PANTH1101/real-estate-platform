from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.accounts.permissions import IsBuyer, IsSeller
from apps.properties.models import Property

from .models import Enquiry


class EnquiryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "enquiry"

    def post(self, request):
        property_id = request.data.get("property_id")
        message = request.data.get("message", "").strip()
        if not property_id or not message:
            return Response({"detail": "property_id and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        prop = Property.objects.filter(id=property_id, is_approved=True).first()
        if not prop:
            return Response({"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        enquiry = Enquiry.objects.create(buyer=request.user, property=prop, message=message)

        # Email notification hook (configure email backend in prod)
        # send_mail(...)

        return Response(
            {"id": enquiry.id, "detail": "Enquiry created"},
            status=status.HTTP_201_CREATED,
        )


class SellerEnquiriesView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        qs = (
            Enquiry.objects.filter(property__owner=request.user)
            .select_related("buyer", "property")
            .order_by("-created_at")
        )
        return Response(
            [
                {
                    "id": e.id,
                    "property_id": str(e.property_id),
                    "property_title": e.property.title,
                    "buyer_id": str(e.buyer_id),
                    "buyer_email": e.buyer.email,
                    "message": e.message,
                    "is_read": e.is_read,
                    "created_at": e.created_at,
                }
                for e in qs
            ]
        )


