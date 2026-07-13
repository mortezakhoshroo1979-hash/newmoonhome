import django_filters
from django.db.models import Count, Sum

from .models import CustomerRank, User


class UserAdminFilter(django_filters.FilterSet):
    date_joined_from = django_filters.DateFilter(field_name="date_joined", lookup_expr="date__gte", label="از تاریخ عضویت")
    date_joined_to = django_filters.DateFilter(field_name="date_joined", lookup_expr="date__lte", label="تا تاریخ عضویت")
    is_verified = django_filters.BooleanFilter(label="تایید شده")
    rank = django_filters.ModelChoiceFilter(field_name="profile__rank", queryset=CustomerRank.objects.all(), label="رتبه")
    min_score = django_filters.NumberFilter(field_name="profile__score", lookup_expr="gte", label="حداقل امتیاز")

    class Meta:
        model = User
        fields = ["is_verified"]
