from datetime import timedelta
import random

from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View

from apps.accounts.models import UserRole
from property.models import Property

from .models import BuyerLead


class BuyerLeadCreateView(View):
    def post(self, request: HttpRequest, property_id: int) -> HttpResponse:
        if not request.user.is_authenticated or request.user.role != UserRole.BUYER:
            return JsonResponse(
                {"error": "Buyer login required to continue."},
                status=403,
            )

        prop = get_object_or_404(Property, id=property_id, is_active=True)
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        phone = (request.POST.get("phone") or "").strip()
        otp = (request.POST.get("otp") or "").strip()

        if not (name and email and phone):
            return JsonResponse({"error": "All fields are required."}, status=400)

        if email != (request.user.email or "").strip().lower():
            return JsonResponse(
                {"error": "Please enter the same email as your buyer account."},
                status=400,
            )

        session_key = f"lead_otp_{property_id}_{email}"

        if not otp:
            otp_code = f"{random.randint(0, 999999):06d}"
            expires_at = timezone.now() + timedelta(minutes=10)
            request.session[session_key] = {
                "code": otp_code,
                "name": name,
                "email": email,
                "phone": phone,
                "expires_at": expires_at.isoformat(),
            }

            try:
                send_mail(
                    subject="Your verification code for property enquiry",
                    message=(
                        f"Hi {name},\n\n"
                        f"Your 6-digit verification code is: {otp_code}\n"
                        "This code is valid for 10 minutes.\n\n"
                        f"Property: {prop.title}\n"
                    ),
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception:
                return JsonResponse(
                    {"error": "Could not send verification code. Please try again."},
                    status=500,
                )
            return JsonResponse(
                {"otp_required": True, "message": "Verification code sent to your email."}
            )

        otp_payload = request.session.get(session_key)
        if not otp_payload:
            return JsonResponse(
                {"error": "OTP expired or missing. Please request a new code."},
                status=400,
            )

        if len(otp) != 6 or not otp.isdigit():
            return JsonResponse({"error": "Enter a valid 6-digit code."}, status=400)

        expires_at_str = otp_payload.get("expires_at")
        expires_at = parse_datetime(expires_at_str) if expires_at_str else None
        if not expires_at or timezone.now() > expires_at:
            request.session.pop(session_key, None)
            return JsonResponse(
                {"error": "OTP has expired. Please request a new code."},
                status=400,
            )

        if otp != otp_payload.get("code"):
            return JsonResponse({"error": "Invalid verification code."}, status=400)

        lead = BuyerLead.objects.create(
            property=prop,
            name=otp_payload.get("name", name),
            email=otp_payload.get("email", email),
            phone=otp_payload.get("phone", phone),
        )
        request.session.pop(session_key, None)

        seller = prop.seller
        data = {
            "message": "Buyer verified successfully.",
            "seller": {
                "name": seller.name,
                "email": seller.email,
                "phone": seller.phone,
            },
            "lead_id": lead.id,
        }
        return JsonResponse(data)


