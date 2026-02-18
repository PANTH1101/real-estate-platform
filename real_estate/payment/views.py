import decimal

try:
    import razorpay
except ImportError:  # pragma: no cover - handled gracefully at runtime
    razorpay = None
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from accounts.models import Seller
from accounts.views import seller_login_required
from property.models import Property

from .models import Payment


class PaymentCreateView(View):
    template_name = "payment/checkout.html"

    @seller_login_required
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        property_id = request.GET.get("property_id")
        prop = get_object_or_404(Property, id=property_id)
        amount_rupees = decimal.Decimal("499.00")
        amount_paise = int(amount_rupees * 100)
        if razorpay is None:
            messages.error(
                request,
                "Razorpay SDK is not installed. Please install the 'razorpay' package.",
            )
            return redirect("accounts:dashboard")

        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            messages.error(
                request,
                "Razorpay API keys are not configured. "
                "Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables.",
            )
            return redirect("accounts:dashboard")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        try:
            order = client.order.create(
                {"amount": amount_paise, "currency": "INR", "payment_capture": 1}
            )
        except Exception as exc:  # pragma: no cover - external API failure
            messages.error(
                request,
                f"Could not initiate payment with Razorpay: {exc}",
            )
            return redirect("accounts:dashboard")
        seller = get_object_or_404(Seller, id=request.session.get("seller_id"))
        payment = Payment.objects.create(
            seller=seller,
            property=prop,
            amount=amount_rupees,
            razorpay_order_id=order["id"],
        )

        return render(
            request,
            self.template_name,
            {
                "property": prop,
                "payment": payment,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "amount_paise": amount_paise,
            },
        )


class PaymentCallbackView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        payment = get_object_or_404(Payment, razorpay_order_id=order_id)
        if razorpay is None:
            messages.error(
                request,
                "Razorpay SDK is not installed. Please install the 'razorpay' package.",
            )
            return render(
                request,
                "payment/failed.html",
                {"property": payment.property, "payment": payment},
            )

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        try:
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": order_id,
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                }
            )
        except razorpay.errors.SignatureVerificationError:
            payment.status = "FAILED"
            payment.save()
            messages.error(request, "Payment verification failed.")
            return render(
                request,
                "payment/failed.html",
                {"property": payment.property, "payment": payment},
            )

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "SUCCESS"
        payment.save()

        prop = payment.property
        prop.is_active = True
        prop.save(update_fields=["is_active"])

        messages.success(request, "Payment successful. Your property is now live.")
        return render(
            request,
            "payment/success.html",
            {"property": prop, "payment": payment},
        )


