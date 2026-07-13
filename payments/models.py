from __future__ import annotations

import uuid

from django.db import models
from django.utils.text import slugify

from common_models import TimeStampedModel


class PaymentGateway(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='نام درگاه')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='اسلاگ')
    provider = models.CharField(max_length=100, verbose_name='ارائه‌دهنده')
    settings_json = models.JSONField(default=dict, blank=True, verbose_name='تنظیمات JSON')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    priority = models.PositiveIntegerField(default=0, verbose_name='اولویت')

    class Meta:
        verbose_name = 'درگاه پرداخت'
        verbose_name_plural = 'درگاه‌های پرداخت'
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CANCELED = 'canceled'
    STATUS_REFUNDED = 'refunded'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'در انتظار'),
        (STATUS_SUCCESS, 'موفق'),
        (STATUS_FAILED, 'ناموفق'),
        (STATUS_CANCELED, 'لغو شده'),
        (STATUS_REFUNDED, 'بازپرداخت شده'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='transactions', verbose_name='سفارش')
    gateway = models.ForeignKey('payments.PaymentGateway', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name='درگاه')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name='کاربر')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='وضعیت')
    authority = models.CharField(max_length=255, blank=True, verbose_name='Authority')
    reference_id = models.CharField(max_length=255, blank=True, verbose_name='Reference ID')
    tracking_code = models.CharField(max_length=255, blank=True, verbose_name='کد پیگیری')
    card_pan = models.CharField(max_length=30, blank=True, verbose_name='شماره کارت ماسک‌شده')
    raw_response = models.JSONField(default=dict, blank=True, verbose_name='پاسخ خام درگاه')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', 'authority', 'reference_id'])]

    def __str__(self):
        return f'{self.order.order_number} - {self.amount}'
