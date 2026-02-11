from rest_framework import serializers

from .models import Property, PropertyMedia


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ("id", "file", "media_type")


class PropertySerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField(source="owner.id", read_only=True)
    media = PropertyMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "owner_id",
            "title",
            "description",
            "property_type",
            "listing_type",
            "price",
            "area_sqft",
            "bedrooms",
            "bathrooms",
            "city",
            "locality",
            "latitude",
            "longitude",
            "status",
            "is_approved",
            "created_at",
            "updated_at",
            "media",
        )
        read_only_fields = ("id", "owner_id", "is_approved", "created_at", "updated_at")


