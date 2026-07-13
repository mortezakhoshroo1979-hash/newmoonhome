from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.views.generic import FormView, ListView, TemplateView

from discounts.models import BulkPriceUpdate
from .filters import ProductFilter
from .forms import ProductBulkUpdateForm
from .models import Product


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProductListAdminView(StaffRequiredMixin, ListView):
    model = Product
    template_name = "admin/products/product_list.html"
    context_object_name = "products"
    paginate_by = 25

    def get_queryset(self):
        queryset = Product.objects.select_related("category", "brand").all()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class BulkPriceUpdatePreviewView(StaffRequiredMixin, FormView):
    template_name = "admin/products/bulk_price_update.html"
    form_class = ProductBulkUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("preview_rows", [])
        return context

    def _calculate_new_price(self, product, action_type, value, discount_percent):
        old_price = Decimal(product.base_price)
        if action_type == "percent_increase":
            new_price = old_price + ((old_price * Decimal(value)) / Decimal("100"))
        elif action_type == "percent_decrease":
            new_price = old_price - ((old_price * Decimal(value)) / Decimal("100"))
        elif action_type == "fixed_increase":
            new_price = old_price + Decimal(value)
        elif action_type == "fixed_decrease":
            new_price = old_price - Decimal(value)
        elif action_type == "set_price":
            new_price = Decimal(value)
        else:
            new_price = old_price

        special_price = product.special_price
        if action_type == "set_special_discount" and discount_percent is not None:
            special_price = old_price * (Decimal("100") - Decimal(discount_percent)) / Decimal("100")
        return max(new_price, Decimal("0")), max(Decimal(special_price or 0), Decimal("0")) if special_price is not None else None

    def form_valid(self, form):
        products = form.filter_queryset()
        action_type = form.cleaned_data["action_type"]
        value = form.cleaned_data.get("value") or 0
        discount_percent = form.cleaned_data.get("discount_percent")
        confirm = form.cleaned_data.get("confirm")
        reason = form.cleaned_data.get("reason", "")

        preview_rows = []
        with transaction.atomic():
            bulk_record = BulkPriceUpdate.objects.create(
                title=f"Bulk update by {self.request.user}",
                update_type="percent" if "percent" in action_type else "fixed",
                value=discount_percent or value or 0,
                status="applied" if confirm else "draft",
                note=reason,
            )
            for product in products:
                new_price, special_price = self._calculate_new_price(product, action_type, value, discount_percent)
                preview_rows.append({
                    "product": product,
                    "old_price": product.base_price,
                    "new_price": new_price,
                    "old_special_price": product.special_price,
                    "new_special_price": special_price,
                })
                bulk_record.products.add(product)
                if confirm:
                    product.base_price = new_price
                    if action_type == "set_special_discount":
                        product.special_price = special_price
                    product.save(update_fields=["base_price", "special_price", "updated_at"])

            if confirm:
                messages.success(self.request, "تغییرات قیمت با موفقیت اعمال شد.")
            else:
                messages.info(self.request, "پیش‌نمایش تغییرات آماده است. برای اعمال نهایی، تیک تایید را بزنید.")

        return self.render_to_response(self.get_context_data(form=form, preview_rows=preview_rows))
