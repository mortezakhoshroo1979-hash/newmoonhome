from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.views.generic import FormView, ListView, TemplateView

from .filters import UserAdminFilter
from .forms import UserFilterEmailForm
from .models import ReferralTransaction, User


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class UserListAdminView(StaffRequiredMixin, ListView):
    model = User
    template_name = "admin/accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 30

    def get_queryset(self):
        queryset = User.objects.select_related("profile").annotate(
            orders_count=Count("orders", distinct=True),
            total_spent=Sum("orders__total_amount"),
        )
        self.filterset = UserAdminFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class UserEmailBulkView(StaffRequiredMixin, FormView):
    template_name = "admin/accounts/bulk_email.html"
    form_class = UserFilterEmailForm

    def form_valid(self, form):
        users = form.filtered_queryset().exclude(email="").exclude(email__isnull=True)
        # در فاز عملیاتی این کار باید از طریق Celery انجام شود.
        messages.info(self.request, f"{users.count()} کاربر برای ارسال ایمیل انتخاب شدند. این عملیات باید async اجرا شود.")
        return self.render_to_response(self.get_context_data(form=form, users=users))


class UserInsightsView(StaffRequiredMixin, TemplateView):
    template_name = "admin/accounts/user_insights.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.select_related("profile", "referral_code").get(pk=kwargs["pk"])
        context["target_user"] = user
        context["referrals"] = ReferralTransaction.objects.filter(referrer=user) | ReferralTransaction.objects.filter(referred_user=user)
        context["orders"] = user.orders.all()
        return context
