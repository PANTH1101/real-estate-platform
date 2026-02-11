import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from property.models import Property

from .models import BuyerLead


class BuyerLeadCreateView(View):
    def post(self, request: HttpRequest, property_id: int) -> HttpResponse:
        prop = get_object_or_404(Property, id=property_id, is_active=True)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        if not (name and email and phone):
            return JsonResponse({"error": "All fields are required."}, status=400)
        lead = BuyerLead.objects.create(
            property=prop,
            name=name,
            email=email,
            phone=phone,
        )
        seller = prop.seller
        data = {
            "message": "Lead submitted successfully.",
            "seller": {
                "name": seller.name,
                "email": seller.email,
                "phone": seller.phone,
            },
            "lead_id": lead.id,
        }
        return JsonResponse(data)


