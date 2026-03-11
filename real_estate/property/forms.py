from django import forms
from django.forms import inlineformset_factory

from .models import Amenity, Property, PropertyImage

PRICE_MIN = 1
PRICE_MAX = 1000000000
AREA_MIN = 100
AREA_MAX = 1000000
LENGTH_MIN = 1
LENGTH_MAX = 10000
COUNT_MAX = 200
BHK_MAX = 20


class PropertyForm(forms.ModelForm):
    FACING_CHOICES = [
        ("", "Select facing"),
        ("N", "North"),
        ("NE", "North East"),
        ("E", "East"),
        ("SE", "South East"),
        ("S", "South"),
        ("SW", "South West"),
        ("W", "West"),
        ("NW", "North West"),
    ]

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facing = forms.ChoiceField(
        choices=FACING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "category",
            "subcategory",
            "property_type",
            "price",
            "address",
            "city",
            "state",
            "latitude",
            "longitude",
            "facing",
            # Common fields
            "sqft",
            # Apartment/Villa fields
            "bhk",
            "floor",
            "total_floors",
            "parking",
            "balcony",
            "lift",
            "furnishing",
            "maintenance_charges",
            # Villa specific
            "garden",
            "built_up_area",
            # Plot fields
            "plot_area",
            "plot_length",
            "plot_width",
            "boundary_wall",
            "corner_plot",
            # Office fields
            "cabins",
            "conference_rooms",
            "pantry",
            # Shop fields
            "frontage_width",
            "washroom",
            "amenities",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select", "id": "id_category"}),
            "subcategory": forms.Select(attrs={"class": "form-select", "id": "id_subcategory"}),
            "property_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": PRICE_MIN,
                    "max": PRICE_MAX,
                }
            ),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(attrs={"id": "id_latitude"}),
            "longitude": forms.HiddenInput(attrs={"id": "id_longitude"}),
            "facing": forms.Select(attrs={"class": "form-select"}),
            # Common
            "sqft": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": AREA_MIN,
                    "max": AREA_MAX,
                }
            ),
            # Apartment/Villa
            "bhk": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": BHK_MAX,
                }
            ),
            "floor": forms.TextInput(attrs={"class": "form-control"}),
            "total_floors": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": COUNT_MAX,
                }
            ),
            "furnishing": forms.Select(attrs={"class": "form-select"}),
            "maintenance_charges": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "max": PRICE_MAX,
                }
            ),
            # Villa
            "built_up_area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": AREA_MIN,
                    "max": AREA_MAX,
                }
            ),
            # Plot
            "plot_area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": AREA_MIN,
                    "max": AREA_MAX,
                }
            ),
            "plot_length": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": LENGTH_MIN,
                    "max": LENGTH_MAX,
                }
            ),
            "plot_width": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": LENGTH_MIN,
                    "max": LENGTH_MAX,
                }
            ),
            # Office
            "cabins": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": COUNT_MAX,
                }
            ),
            "conference_rooms": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": COUNT_MAX,
                }
            ),
            # Shop
            "frontage_width": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": LENGTH_MIN,
                    "max": LENGTH_MAX,
                }
            ),
        }
    
    def clean(self):
        """
        Simplified validation so that valid choices from the UI
        can be submitted without overly strict subcategory-specific rules.
        """
        cleaned_data = super().clean()

        # Basic sanity checks only
        price = cleaned_data.get("price")
        if price is not None and price <= 0:
            self.add_error("price", "Price must be greater than zero")

        numeric_fields = [
            "bhk",
            "sqft",
            "total_floors",
            "plot_area",
            "plot_length",
            "plot_width",
            "built_up_area",
            "cabins",
            "conference_rooms",
            "frontage_width",
            "maintenance_charges",
        ]
        for field in numeric_fields:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, f"{field.replace('_', ' ').title()} cannot be negative")

        bhk = cleaned_data.get("bhk")
        if bhk is not None and (bhk < 0 or bhk > 20):
            self.add_error("bhk", "BHK value looks invalid")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_facing = getattr(self.instance, "facing", "") if self.instance else ""
        base_choices = list(self.FACING_CHOICES)
        if current_facing and current_facing not in {choice[0] for choice in base_choices}:
            base_choices = [
                ("", "Select facing"),
                (current_facing, current_facing),
                *[choice for choice in base_choices if choice[0]],
            ]
        self.fields["facing"].choices = base_choices


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ["image", "is_primary"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "multiple": False}
            ),
            "is_primary": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    extra=3,
    can_delete=True,
)


