import django_filters
from django.db.models import Q

from .models import Brand, Category, Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q", label="جستجو")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="دسته")
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), label="برند")
    is_active = django_filters.BooleanFilter(label="فعال")
    stock_status = django_filters.ChoiceFilter(
        choices=[("in_stock", "موجود"), ("out_of_stock", "ناموجود")],
        method="filter_stock_status",
        label="موجودی",
    )

    class Meta:
        model = Product
        fields = ["category", "brand", "is_active"]

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(sku__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_stock_status(self, queryset, name, value):
        if value == "in_stock":
            return queryset.filter(stock__gt=0)
        if value == "out_of_stock":
            return queryset.filter(stock=0)
        return queryset
