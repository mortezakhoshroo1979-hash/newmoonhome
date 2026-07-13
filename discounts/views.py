from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.views.generic import TemplateView

from .models import Coupon, CategoryDiscount
from accounts.models import CustomerRank


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DiscountsDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "admin/discounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coupons"] = Coupon.objects.all().order_by("-created_at")[:10]
        context["coupon_usage_stats"] = Coupon.objects.values("code").annotate(uses=Count("orders"), total_discount=Sum("orders__discount_amount"))
        context["ranks"] = CustomerRank.objects.all()
        context["category_discounts"] = CategoryDiscount.objects.all()
        return context
