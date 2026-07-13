import django_filters

from payments.models import Transaction
from .models import Order


class OrderFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte", label="از تاریخ")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="date__lte", label="تا تاریخ")
    province = django_filters.CharFilter(field_name="province", lookup_expr="icontains", label="استان")
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES, label="وضعیت")
    payment_status = django_filters.ChoiceFilter(method="filter_payment_status", choices=Transaction.STATUS_CHOICES, label="وضعیت پرداخت")

    class Meta:
        model = Order
        fields = ["status", "province"]

    def filter_payment_status(self, queryset, name, value):
        if value:
            return queryset.filter(transactions__status=value).distinct()
        return queryset
