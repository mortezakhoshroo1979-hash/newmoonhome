from collections import Counter

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import FormView, ListView, TemplateView

from .filters import OrderFilter
from .forms import OrderStatusBulkUpdateForm
from .models import Invoice, Order, OrderStatusHistory


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class OrdersDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "admin/orders/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_counts = Order.objects.values("status").annotate(count=Count("id"))
        context["status_counts"] = list(status_counts)
        context["total_sales"] = Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0
        context["orders_count"] = Order.objects.count()
        return context


class OrderListAdminView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "admin/orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 25

    def get_queryset(self):
        queryset = Order.objects.select_related("user", "shipping_method").prefetch_related("transactions")
        self.filterset = OrderFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class OrderStatusBulkUpdateView(StaffRequiredMixin, FormView):
    template_name = "admin/orders/bulk_status_update.html"
    form_class = OrderStatusBulkUpdateForm

    def form_valid(self, form):
        orders = form.filtered_queryset()
        to_status = form.cleaned_data["to_status"]
        confirm = form.cleaned_data.get("confirm")
        preview_rows = []

        with transaction.atomic():
            for order in orders:
                preview_rows.append({
                    "order": order,
                    "old_status": order.status,
                    "new_status": to_status,
                })
                if confirm and order.status != to_status:
                    old_status = order.status
                    order.status = to_status
                    order.save(update_fields=["status", "updated_at"])
                    OrderStatusHistory.objects.create(
                        order=order,
                        from_status=old_status,
                        to_status=to_status,
                        changed_by=self.request.user,
                        note="تغییر گروهی از پنل مدیریت",
                    )

        if confirm:
            messages.success(self.request, "تغییر وضعیت گروهی سفارش‌ها انجام شد.")
        else:
            messages.info(self.request, "پیش‌نمایش تغییرات وضعیت آماده است.")
        return self.render_to_response(self.get_context_data(form=form, preview_rows=preview_rows))


class InvoicePrintView(StaffRequiredMixin, TemplateView):
    template_name = "admin/orders/invoice_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.select_related("user").prefetch_related("items").get(pk=kwargs["pk"])
        context["order"] = order
        context["invoice"] = getattr(order, "invoice", None)
        return context


class ShippingLabelPrintView(StaffRequiredMixin, TemplateView):
    template_name = "admin/orders/shipping_label_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.get(pk=kwargs["pk"])
        return context
