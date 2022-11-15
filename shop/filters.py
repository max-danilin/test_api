from django_filters.rest_framework import FilterSet
from .models import Product, User


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'size': ['exact'],
            'color': ['exact'],
            'price': ['lt', 'gt']
        }


class CustomerFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'date_joined': ['lt', 'gt']
        }