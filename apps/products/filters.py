from django_filters import rest_framework as filters
from apps.products.models import Product
from django.db.models import Q


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter(label=("Цена от до"))

    class Meta:
        model = Product
        fields = ['price', ]
