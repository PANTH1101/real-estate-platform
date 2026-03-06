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
        cleaned_data = super().clean()
        subcategory = cleaned_data.get('subcategory')
        
        # Validate based on property type
        if subcategory == Property.APARTMENT:
            # Apartment required fields
            if not cleaned_data.get('bhk'):
                self.add_error('bhk', 'BHK is required for apartments')
            if not cleaned_data.get('sqft'):
                self.add_error('sqft', 'Square feet is required for apartments')
            if not cleaned_data.get('floor'):
                self.add_error('floor', 'Floor number is required for apartments')
            if not cleaned_data.get('total_floors'):
                self.add_error('total_floors', 'Total floors is required for apartments')
                
        elif subcategory == Property.VILLA:
            # Villa required fields
            if not cleaned_data.get('bhk'):
                self.add_error('bhk', 'BHK is required for villas')
            if not cleaned_data.get('plot_area'):
                self.add_error('plot_area', 'Plot area is required for villas')
            if not cleaned_data.get('built_up_area'):
                self.add_error('built_up_area', 'Built-up area is required for villas')
                
        elif subcategory == Property.PLOT:
            # Plot required fields
            if not cleaned_data.get('plot_area'):
                self.add_error('plot_area', 'Plot area is required for plots')
            # Validate plot dimensions if provided
            plot_length = cleaned_data.get('plot_length')
            plot_width = cleaned_data.get('plot_width')
            if plot_length and plot_width:
                calculated_area = plot_length * plot_width
                plot_area = cleaned_data.get('plot_area')
                if plot_area and abs(calculated_area - plot_area) > (plot_area * 0.1):
                    self.add_error('plot_area', 
                        f'Plot area ({plot_area} sq ft) does not match calculated area from dimensions ({calculated_area:.2f} sq ft)')
                    
        elif subcategory == Property.OFFICE:
            # Office required fields
            if not cleaned_data.get('sqft'):
                self.add_error('sqft', 'Total area is required for offices')
            if not cleaned_data.get('floor'):
                self.add_error('floor', 'Floor number is required for offices')
                
        elif subcategory == Property.SHOP:
            # Shop required fields
            if not cleaned_data.get('sqft'):
                self.add_error('sqft', 'Shop area is required for shops')
            if not cleaned_data.get('floor'):
                self.add_error('floor', 'Floor number is required for shops')
        
        # Validate price is positive
        price = cleaned_data.get('price')
        if price and price <= 0:
            self.add_error('price', 'Price must be greater than zero')
        
        # Validate numeric fields are positive
        numeric_fields = ['bhk', 'sqft', 'total_floors', 'plot_area', 'plot_length', 
                         'plot_width', 'built_up_area', 'cabins', 'conference_rooms', 
                         'frontage_width', 'maintenance_charges']
        
        for field in numeric_fields:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, f'{field.replace("_", " ").title()} cannot be negative')
        
        # Validate BHK is reasonable (1-10)
        bhk = cleaned_data.get('bhk')
        if bhk and (bhk < 1 or bhk > 10):
            self.add_error('bhk', 'BHK must be between 1 and 10')
        
        # Validate floor number for apartments
        if subcategory == Property.APARTMENT:
            floor = cleaned_data.get('floor')
            total_floors = cleaned_data.get('total_floors')
            if floor and total_floors:
                try:
                    floor_num = int(floor)
                    if floor_num > total_floors:
                        self.add_error('floor', 'Floor number cannot be greater than total floors')
                except ValueError:
                    pass  # Floor might be "Ground" or "Basement"
        
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


