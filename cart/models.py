from __future__ import annotations

import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models

from common_models import TimeStampedModel


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='carts', verbose_name='کاربر')
    session_key = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name='کلید سشن/کوکی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
        ordering = ['-updated_at']

    def __str__(self):
        return f'سبد {self.user}' if self.user else f'سبد مهمان {self.session_key}'

    @property
    def total_amount(self):
        total = Decimal('0')
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='cart_items', verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    selected_options = models.JSONField(default=dict, blank=True, verbose_name='گزینه‌های انتخاب‌شده')

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'

    @property
    def unit_price(self):
        return self.product.calculate_price(self.selected_options)

    @property
    def total_price(self):
        return self.unit_price * self.quantity
