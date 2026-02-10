from django.contrib import admin

from .models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "joined_at")
    search_fields = ("name", "email", "phone")


