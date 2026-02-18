from django.contrib import admin

from .models import Amenity, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "state", "price", "property_type", "is_active")
    list_filter = ("city", "state", "property_type", "category", "is_active")
    search_fields = ("title", "city", "state", "seller__name")
    inlines = [PropertyImageInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ("name",)


