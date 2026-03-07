from django import forms
from django.forms import inlineformset_factory

from .models import Amenity, Property, PropertyImage


class PropertyForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
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
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(attrs={"id": "id_latitude"}),
            "longitude": forms.HiddenInput(attrs={"id": "id_longitude"}),
            "facing": forms.TextInput(attrs={"class": "form-control"}),
            # Common
            "sqft": forms.NumberInput(attrs={"class": "form-control"}),
            # Apartment/Villa
            "bhk": forms.NumberInput(attrs={"class": "form-control"}),
            "floor": forms.TextInput(attrs={"class": "form-control"}),
            "total_floors": forms.NumberInput(attrs={"class": "form-control"}),
            "furnishing": forms.Select(attrs={"class": "form-select"}),
            "maintenance_charges": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            # Villa
            "built_up_area": forms.NumberInput(attrs={"class": "form-control"}),
            # Plot
            "plot_area": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "plot_length": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "plot_width": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            # Office
            "cabins": forms.NumberInput(attrs={"class": "form-control"}),
            "conference_rooms": forms.NumberInput(attrs={"class": "form-control"}),
            # Shop
            "frontage_width": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
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


