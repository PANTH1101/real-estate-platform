from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "property", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("seller__name", "seller__email", "property__title")


