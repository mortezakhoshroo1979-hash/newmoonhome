from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from common_models import TimeStampedModel


class Wishlist(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist', verbose_name='کاربر')
    products = models.ManyToManyField('products.Product', blank=True, related_name='wishlists', verbose_name='محصولات')

    class Meta:
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'
        ordering = ['-created_at']


class Compare(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compare_list', verbose_name='کاربر')
    products = models.ManyToManyField('products.Product', blank=True, related_name='compare_lists', verbose_name='محصولات')

    class Meta:
        verbose_name = 'مقایسه'
        verbose_name_plural = 'مقایسه‌ها'
        ordering = ['-created_at']

    def clean(self):
        if self.pk and self.products.count() > 4:
            raise ValidationError('حداکثر ۴ محصول برای مقایسه مجاز است.')

    def add_product(self, product):
        if self.products.count() >= 4:
            raise ValidationError('حداکثر ۴ محصول برای مقایسه مجاز است.')
        self.products.add(product)
