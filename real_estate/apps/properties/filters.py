import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    locality = django_filters.CharFilter(field_name="locality", lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    bedrooms = django_filters.NumberFilter(field_name="bedrooms")
    bathrooms = django_filters.NumberFilter(field_name="bathrooms")
    property_type = django_filters.CharFilter(field_name="property_type")
    listing_type = django_filters.CharFilter(field_name="listing_type")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Property
        fields = [
            "city",
            "locality",
            "price_min",
            "price_max",
            "bedrooms",
            "bathrooms",
            "property_type",
            "listing_type",
            "status",
        ]


