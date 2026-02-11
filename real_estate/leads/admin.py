from django.contrib import admin

from .models import BuyerLead


@admin.register(BuyerLead)
class BuyerLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "property", "submitted_at")
    search_fields = ("name", "email", "phone", "property__title")
    list_filter = ("submitted_at",)


