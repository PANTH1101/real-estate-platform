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
    
    # Property subcategory types
    APARTMENT = "APARTMENT"
    VILLA = "VILLA"
    PLOT = "PLOT"
    OFFICE = "OFFICE"
    SHOP = "SHOP"
    SUBCATEGORY_CHOICES = [
        (APARTMENT, "Apartment"),
        (VILLA, "House / Villa"),
        (PLOT, "Plot / Land"),
        (OFFICE, "Commercial Office"),
        (SHOP, "Shop / Showroom"),
    ]
    
    # Furnishing types
    FURNISHED = "FURNISHED"
    SEMI_FURNISHED = "SEMI_FURNISHED"
    UNFURNISHED = "UNFURNISHED"
    FURNISHING_CHOICES = [
        (FURNISHED, "Fully Furnished"),
        (SEMI_FURNISHED, "Semi Furnished"),
        (UNFURNISHED, "Unfurnished"),
    ]

    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="properties"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, choices=SUBCATEGORY_CHOICES)
    property_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Common fields
    sqft = models.PositiveIntegerField("Square feet", null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    facing = models.CharField(max_length=50, blank=True)
    
    # Apartment/Villa specific fields
    bhk = models.PositiveIntegerField("BHK", null=True, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    parking = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, blank=True)
    maintenance_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Villa specific fields
    garden = models.BooleanField(default=False)
    built_up_area = models.PositiveIntegerField(null=True, blank=True, help_text="Built-up area in sq ft")
    
    # Plot specific fields
    plot_area = models.FloatField(null=True, blank=True, help_text="Plot area in sq ft")
    plot_length = models.FloatField(null=True, blank=True, help_text="Length in feet")
    plot_width = models.FloatField(null=True, blank=True, help_text="Width in feet")
    boundary_wall = models.BooleanField(default=False)
    corner_plot = models.BooleanField(default=False)
    
    # Commercial Office specific fields
    cabins = models.PositiveIntegerField(null=True, blank=True)
    conference_rooms = models.PositiveIntegerField(null=True, blank=True)
    pantry = models.BooleanField(default=False)
    
    # Shop specific fields
    frontage_width = models.FloatField(null=True, blank=True, help_text="Frontage width in feet")
    washroom = models.BooleanField(default=False)
    
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



