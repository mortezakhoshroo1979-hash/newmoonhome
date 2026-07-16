from __future__ import annotations

import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import FileExtensionValidator
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


class CustomOrderRequest(TimeStampedModel):
    STATUS_PENDING_REVIEW = 'pending_review'
    STATUS_QUOTED = 'quoted'
    STATUS_ACCEPTED = 'accepted'
    STATUS_WOOD_CUTTING = 'wood_cutting'
    STATUS_CARPENTRY = 'carpentry'
    STATUS_PAINTING = 'painting'
    STATUS_UPHOLSTERY = 'upholstery'
    STATUS_QUALITY_CONTROL = 'quality_control'
    STATUS_READY = 'ready'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_PENDING_REVIEW, 'در انتظار بررسی تیم مهندسی'),
        (STATUS_QUOTED, 'برآورد قیمت و اعلام به مشتری'),
        (STATUS_ACCEPTED, 'تایید مشتری و پرداخت بیعانه'),
        (STATUS_WOOD_CUTTING, 'مرحله ۱: انتخاب و برش چوب'),
        (STATUS_CARPENTRY, 'مرحله ۲: نجاری و کلاف‌بندی'),
        (STATUS_PAINTING, 'مرحله ۳: رنگ‌آمیزی و پرداخت سطح'),
        (STATUS_UPHOLSTERY, 'مرحله ۴: رویه‌کوبی و خیاطی پارچه'),
        (STATUS_QUALITY_CONTROL, 'مرحله ۵: کنترل کیفیت نهایی'),
        (STATUS_READY, 'آماده ارسال / تحویل'),
        (STATUS_CANCELED, 'لغو شده'),
    ]

    WOOD_CHOICES = [
        ('raash', 'چوب راش طبیعی درجه یک'),
        ('gerdoo', 'چوب گردوی آمریکایی ممتاز'),
        ('baloot', 'چوب بلوط اروپایی'),
        ('roosi', 'چوب روسی ساب‌خورده'),
        ('other', 'سایر موارد (طبق توضیحات)'),
    ]

    FINISH_CHOICES = [
        ('polyurethane', 'رنگ پلی‌اورتان مات/براق'),
        ('herbal_oil', 'روغن گیاهی طبیعی ضدآب'),
        ('patina', 'پاتینه و کهنه‌کاری دست‌ساز'),
        ('raw', 'بدون پوشش (چوب خام)'),
    ]

    FABRIC_CHOICES = [
        ('velvet', 'مخمل وارداتی درجه یک'),
        ('leather', 'چرم طبیعی/صنعتی ممتاز'),
        ('linen', 'کتان / گونی‌بافت لوکس'),
        ('boucle', 'بوکله بافت‌دار اروپایی'),
        ('none', 'بدون پارچه (تمام چوب)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_orders', verbose_name='کاربر')
    request_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='شماره استعلام')
    receiver_name = models.CharField(max_length=255, verbose_name='نام سفارش‌دهنده')
    receiver_phone = models.CharField(max_length=20, verbose_name='شماره تماس')
    inspiration_image = models.ImageField(
        upload_to='orders/custom_requests/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'pdf'])],
        verbose_name='تصویر نمونه/الهام‌بخش'
    )
    length_cm = models.PositiveIntegerField(null=True, blank=True, verbose_name='طول (سانتی‌متر)')
    width_cm = models.PositiveIntegerField(null=True, blank=True, verbose_name='عرض (سانتی‌متر)')
    height_cm = models.PositiveIntegerField(null=True, blank=True, verbose_name='ارتفاع (سانتی‌متر)')
    wood_type = models.CharField(max_length=50, choices=WOOD_CHOICES, default='raash', verbose_name='نوع چوب')
    finish_type = models.CharField(max_length=50, choices=FINISH_CHOICES, default='polyurethane', verbose_name='نوع رنگ/پوشش')
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, default='velvet', verbose_name='جنس پارچه')
    fabric_color_code = models.CharField(max_length=100, blank=True, verbose_name='کد/رنگ پارچه')
    customer_notes = models.TextField(blank=True, verbose_name='توضیحات تکمیلی مشتری')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING_REVIEW, verbose_name='وضعیت ساخت')
    quoted_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='مبلغ برآوردی (ریال)')
    prepayment_amount = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='مبلغ بیعانه (ریال)')
    admin_feedback = models.TextField(blank=True, verbose_name='پاسخ و برآورد مهندسی')

    class Meta:
        verbose_name = 'استعلام و سفارش اختصاصی'
        verbose_name_plural = 'استعلام‌ها و سفارش‌های اختصاصی'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['request_number', 'status'])]

    def __str__(self):
        return f"{self.request_number} - {self.receiver_name}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = f"REQ-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    @property
    def progress_percentage(self):
        steps = {
            self.STATUS_PENDING_REVIEW: 10,
            self.STATUS_QUOTED: 20,
            self.STATUS_ACCEPTED: 30,
            self.STATUS_WOOD_CUTTING: 45,
            self.STATUS_CARPENTRY: 60,
            self.STATUS_PAINTING: 75,
            self.STATUS_UPHOLSTERY: 85,
            self.STATUS_QUALITY_CONTROL: 95,
            self.STATUS_READY: 100,
            self.STATUS_CANCELED: 0,
        }
        return steps.get(self.status, 10)
