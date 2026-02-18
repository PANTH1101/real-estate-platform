from django.db import models

from accounts.models import Seller


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class PropertyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_city(self, city: str):
        if city:
            return self.filter(city__icontains=city)
        return self

    def for_state(self, state: str):
        if state:
            return self.filter(state__icontains=state)
        return self


class PropertyManager(models.Manager):
    def get_queryset(self) -> PropertyQuerySet:  # type: ignore[name-defined]
        return PropertyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Property(models.Model):
    RESIDENTIAL = "RES"
    COMMERCIAL = "COM"
    CATEGORY_CHOICES = [
        (RESIDENTIAL, "Residential"),
        (COMMERCIAL, "Commercial"),
    ]

    TYPE_RENT = "RENT"
    TYPE_SELL = "SELL"
    TYPE_CHOICES = [
        (TYPE_RENT, "For Rent"),
        (TYPE_SELL, "For Sale"),
    ]

    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="properties"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bhk = models.PositiveIntegerField(default=1)
    sqft = models.PositiveIntegerField("Square feet")
    floor = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    facing = models.CharField(max_length=50, blank=True)
    parking = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    amenities = models.ManyToManyField(Amenity, related_name="properties", blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PropertyManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="property_images/")
    is_primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Image for {self.property_id}"



