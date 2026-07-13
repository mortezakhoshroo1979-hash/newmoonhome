from __future__ import annotations

import uuid
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from common_models import TimeStampedModel


class Coupon(TimeStampedModel):
    TYPE_PERCENT = 'percent'
    TYPE_FIXED = 'fixed'
    TYPE_CHOICES = [(TYPE_PERCENT, 'درصدی'), (TYPE_FIXED, 'ثابت')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    discount_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='نوع تخفیف')
    value = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مقدار تخفیف')
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='حداقل مبلغ سفارش')
    max_discount_amount = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='حداکثر مبلغ تخفیف')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضا')
    max_uses = models.PositiveIntegerField(default=1, verbose_name='حداکثر استفاده')
    used_count = models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        if self.used_count >= self.max_uses:
            return False
        return True

    def calculate_discount(self, amount):
        amount = Decimal(str(amount))
        if not self.is_valid or amount < self.min_order_amount:
            return Decimal('0')
        if self.discount_type == self.TYPE_PERCENT:
            discount = (amount * Decimal(self.value)) / Decimal('100')
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        return min(Decimal(self.value), amount)


class CategoryDiscount(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE, related_name='discounts', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=150, verbose_name='عنوان')
    percent = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخفیف')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'تخفیف دسته‌ای'
        verbose_name_plural = 'تخفیف‌های دسته‌ای'
        ordering = ['-created_at']


class BulkPriceUpdate(TimeStampedModel):
    TYPE_PERCENT = 'percent'
    TYPE_FIXED = 'fixed'
    TYPE_CHOICES = [(TYPE_PERCENT, 'درصدی'), (TYPE_FIXED, 'مبلغ ثابت')]
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_APPLIED = 'applied'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = [(STATUS_DRAFT, 'پیش‌نویس'), (STATUS_SCHEDULED, 'زمان‌بندی‌شده'), (STATUS_APPLIED, 'اعمال‌شده'), (STATUS_CANCELED, 'لغوشده')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    update_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='نوع تغییر')
    value = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مقدار')
    categories = models.ManyToManyField('products.Category', blank=True, related_name='bulk_price_updates', verbose_name='دسته‌بندی‌ها')
    brands = models.ManyToManyField('products.Brand', blank=True, related_name='bulk_price_updates', verbose_name='برندها')
    products = models.ManyToManyField('products.Product', blank=True, related_name='bulk_price_updates', verbose_name='محصولات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, verbose_name='وضعیت')
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان اجرا')
    note = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تغییر قیمت گروهی'
        verbose_name_plural = 'تغییرات قیمت گروهی'
        ordering = ['-created_at']
