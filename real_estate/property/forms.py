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
            "sqft",
            "bhk",
            "floor",
            "address",
            "city",
            "state",
            "price",
            "property_type",
            "facing",
            "parking",
            "balcony",
            "amenities",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select", "id": "id_category"}),
            "subcategory": forms.Select(
                attrs={"class": "form-select", "id": "id_subcategory"}
            ),
            "sqft": forms.NumberInput(attrs={"class": "form-control"}),
            "bhk": forms.NumberInput(attrs={"class": "form-control"}),
            "floor": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "property_type": forms.Select(attrs={"class": "form-select"}),
            "facing": forms.TextInput(attrs={"class": "form-control"}),
        }


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


