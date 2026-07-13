from __future__ import annotations

import uuid
from decimal import Decimal

from django.db import models

from common_models import TimeStampedModel


class ShippingMethod(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name='نام')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    base_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه پایه')
    cost_per_kg = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه هر کیلوگرم')
    min_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='حداقل وزن')
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='حداکثر وزن')
    covered_cities = models.JSONField(default=list, blank=True, verbose_name='شهرهای تحت پوشش')
    delivery_time = models.CharField(max_length=150, verbose_name='زمان تحویل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'روش ارسال'
        verbose_name_plural = 'روش‌های ارسال'
        ordering = ['name']

    def __str__(self):
        return self.name

    def calculate_cost(self, weight=0):
        weight = Decimal(str(weight or 0))
        return Decimal(self.base_cost) + (weight * Decimal(self.cost_per_kg))


class ShippingRate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping_method = models.ForeignKey('shipping.ShippingMethod', on_delete=models.CASCADE, related_name='special_rates', verbose_name='روش ارسال')
    province = models.CharField(max_length=100, verbose_name='استان')
    city = models.CharField(max_length=100, blank=True, verbose_name='شهر')
    extra_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='هزینه اضافی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'تعرفه ویژه ارسال'
        verbose_name_plural = 'تعرفه‌های ویژه ارسال'
        ordering = ['province', 'city']
        unique_together = ('shipping_method', 'province', 'city')

    def __str__(self):
        target = self.city or self.province
        return f'{self.shipping_method.name} - {target}'
