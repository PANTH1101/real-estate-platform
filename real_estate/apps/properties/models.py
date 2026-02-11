import uuid

from django.conf import settings
from django.db import models

from .validators import validate_image_file, validate_video_file


class PropertyType(models.TextChoices):
    HOUSE = "HOUSE", "House"
    FLAT = "FLAT", "Flat"
    LAND = "LAND", "Land"
    COMMERCIAL = "COMMERCIAL", "Commercial"


class ListingType(models.TextChoices):
    SALE = "SALE", "Sale"
    RENT = "RENT", "Rent"


class PropertyStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    SOLD = "SOLD", "Sold"
    PENDING = "PENDING", "Pending"


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    listing_type = models.CharField(max_length=10, choices=ListingType.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area_sqft = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PropertyStatus.choices, default=PropertyStatus.AVAILABLE)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["locality"]),
            models.Index(fields=["price"]),
            models.Index(fields=["property_type"]),
            models.Index(fields=["listing_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_approved"]),
        ]

    def __str__(self) -> str:
        return self.title


class MediaType(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"


def property_media_upload_path(instance: "PropertyMedia", filename: str) -> str:
    return f"property_media/{instance.property_id}/{filename}"


class PropertyMedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to=property_media_upload_path)
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.media_type == MediaType.IMAGE:
            validate_image_file(self.file)
        elif self.media_type == MediaType.VIDEO:
            validate_video_file(self.file)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.media_type} for {self.property_id}"


