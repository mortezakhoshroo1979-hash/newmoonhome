from django.contrib import admin
from import_export.admin import ExportMixin

from .forms import CouponAdminForm
from .models import BulkPriceUpdate, CategoryDiscount, Coupon


@admin.register(Coupon)
class CouponAdmin(ExportMixin, admin.ModelAdmin):
    form = CouponAdminForm
    list_display = ("code", "discount_type", "value", "used_count", "max_uses", "expires_at", "is_active")
    list_filter = ("discount_type", "is_active", "expires_at")
    search_fields = ("code",)


@admin.register(CategoryDiscount)
class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "percent", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)


@admin.register(BulkPriceUpdate)
class BulkPriceUpdateAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("title", "update_type", "value", "status", "scheduled_at", "created_at")
    list_filter = ("update_type", "status")
    filter_horizontal = ("categories", "brands", "products")
    search_fields = ("title", "note")
