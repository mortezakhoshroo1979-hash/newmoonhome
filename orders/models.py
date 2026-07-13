from __future__ import annotations

import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from common_models import TimeStampedModel


class Order(TimeStampedModel):
    STATUS_REGISTERED = 'registered'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_PREPARING = 'preparing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELED = 'canceled'
    STATUS_RETURNED = 'returned'
    STATUS_CHOICES = [
        (STATUS_REGISTERED, 'ثبت'),
        (STATUS_CONFIRMED, 'تایید'),
        (STATUS_PREPARING, 'آماده‌سازی'),
        (STATUS_SHIPPED, 'ارسال'),
        (STATUS_DELIVERED, 'تحویل'),
        (STATUS_CANCELED, 'لغو'),
        (STATUS_RETURNED, 'مرجوعی'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='کاربر')
    order_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='شماره سفارش')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REGISTERED, verbose_name='وضعیت')
    shipping_method = models.ForeignKey('shipping.ShippingMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='روش ارسال')
    coupon = models.ForeignKey('discounts.Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='کوپن')
    subtotal_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='جمع جزء')
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='مبلغ تخفیف')
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه ارسال')
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='مبلغ نهایی')
    receiver_name = models.CharField(max_length=255, verbose_name='نام گیرنده')
    receiver_phone = models.CharField(max_length=20, verbose_name='شماره گیرنده')
    province = models.CharField(max_length=100, verbose_name='استان')
    city = models.CharField(max_length=100, verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='کد پستی')
    customer_note = models.TextField(blank=True, verbose_name='یادداشت مشتری')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['order_number', 'status'])]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"NMH-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orders:checkout')

    def recalculate_totals(self):
        subtotal = self.items.aggregate(total=Sum('total_price_snapshot'))['total'] or Decimal('0')
        self.subtotal_amount = subtotal
        self.total_amount = subtotal + self.shipping_amount - self.discount_amount
        if self.total_amount < 0:
            self.total_amount = Decimal('0')
        self.save(update_fields=['subtotal_amount', 'total_amount', 'updated_at'])


class OrderItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items', verbose_name='محصول')
    product_name = models.CharField(max_length=255, verbose_name='نام محصول')
    sku = models.CharField(max_length=100, blank=True, verbose_name='SKU')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    selected_options = models.JSONField(default=dict, blank=True, verbose_name='گزینه‌های انتخابی')
    unit_price_snapshot = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت واحد در لحظه ثبت')
    total_price_snapshot = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='قیمت کل در لحظه ثبت')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.total_price_snapshot:
            self.total_price_snapshot = self.unit_price_snapshot * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='status_history', verbose_name='سفارش')
    from_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name='از وضعیت')
    to_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name='به وضعیت')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='changed_order_statuses', verbose_name='تغییردهنده')
    note = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تاریخچه وضعیت سفارش'
        verbose_name_plural = 'تاریخچه وضعیت سفارش‌ها'
        ordering = ['-created_at']


class Invoice(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='invoice', verbose_name='سفارش')
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='شماره فاکتور')
    issue_date = models.DateField(default=timezone.localdate, verbose_name='تاریخ صدور')
    legal_name = models.CharField(max_length=255, blank=True, verbose_name='نام حقوقی/حقیقی')
    economic_code = models.CharField(max_length=50, blank=True, verbose_name='کد اقتصادی')
    national_id = models.CharField(max_length=50, blank=True, verbose_name='شناسه/کد ملی')
    amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='مبلغ')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتورها'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        if not self.amount and self.order_id:
            self.amount = self.order.total_amount
        super().save(*args, **kwargs)
