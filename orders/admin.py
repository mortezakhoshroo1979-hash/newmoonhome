from django.contrib import admin, messages
from import_export.admin import ExportMixin

from .models import Invoice, Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "sku", "quantity", "unit_price_snapshot", "total_price_snapshot", "selected_options")


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("from_status", "to_status", "changed_by", "note", "created_at")


@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "province", "total_amount", "paid_at", "created_at")
    list_filter = ("status", "province", "created_at")
    search_fields = ("order_number", "receiver_name", "receiver_phone", "address")
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    actions = ["mark_confirmed", "mark_preparing", "mark_shipped"]

    @admin.action(description="تغییر وضعیت به تایید")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_CONFIRMED)
        self.message_user(request, f"{updated} سفارش تایید شد.", messages.SUCCESS)

    @admin.action(description="تغییر وضعیت به آماده‌سازی")
    def mark_preparing(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_PREPARING)
        self.message_user(request, f"{updated} سفارش به آماده‌سازی رفت.", messages.INFO)

    @admin.action(description="تغییر وضعیت به ارسال")
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_SHIPPED)
        self.message_user(request, f"{updated} سفارش ارسال شد.", messages.WARNING)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "order", "amount", "issue_date", "created_at")
    search_fields = ("invoice_number", "order__order_number")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "from_status", "to_status", "changed_by", "created_at")
    list_filter = ("from_status", "to_status")
