from __future__ import annotations

import uuid
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from common_models import TimeStampedModel

try:
    from ckeditor.fields import RichTextField
except ImportError:  # pragma: no cover
    RichTextField = models.TextField


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="نام دسته")
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name="اسلاگ")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='دسته والد')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='products/categories/', null=True, blank=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['name']
        unique_together = ('parent', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_list')


class Brand(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name='نام برند')
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name='اسلاگ')
    logo = models.ImageField(upload_to='products/brands/', verbose_name='لوگو')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    website = models.URLField(blank=True, verbose_name='وب‌سایت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('products.Category', on_delete=models.PROTECT, related_name='products', verbose_name='دسته‌بندی')
    brand = models.ForeignKey('products.Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='برند')
    name = models.CharField(max_length=255, verbose_name='نام محصول')
    slug = models.SlugField(max_length=280, unique=True, blank=True, verbose_name='اسلاگ')
    description = RichTextField(verbose_name='توضیحات')
    base_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت پایه')
    special_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='قیمت ویژه')
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='وزن (کیلوگرم)')
    dimensions = models.CharField(max_length=255, blank=True, verbose_name='ابعاد')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی پایه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    sales_count = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')
    customization_fields = models.JSONField(default=dict, blank=True, verbose_name='فیلدهای شخصی‌سازی')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['slug']), models.Index(fields=['sku']), models.Index(fields=['is_active', 'is_featured'])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        if self.special_price is not None and self.special_price > 0:
            return self.special_price
        return self.base_price

    def calculate_price(self, selected_options=None):
        selected_options = selected_options or {}
        total_price = Decimal(self.current_price or 0)
        config = self.customization_fields or {}
        for group in config.get('options', []):
            selected_value = selected_options.get(group.get('group'))
            if selected_value is None:
                continue
            for item in group.get('items', []):
                if item.get('value') == selected_value:
                    total_price += Decimal(str(item.get('price_adjustment', 0) or 0))
                    break
        return max(total_price, Decimal('0'))

    def get_option_stock(self, selected_options=None):
        selected_options = selected_options or {}
        config = self.customization_fields or {}
        stocks = []
        for group in config.get('options', []):
            selected_value = selected_options.get(group.get('group'))
            if selected_value is None:
                continue
            for item in group.get('items', []):
                if item.get('value') == selected_value and item.get('stock') is not None:
                    stocks.append(int(item.get('stock', 0)))
                    break
        return min(stocks) if stocks else self.stock


class ProductImage(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = models.ImageField(upload_to='products/images/', verbose_name='تصویر')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='متن جایگزین')
    is_feature = models.BooleanField(default=False, verbose_name='تصویر شاخص')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'
        ordering = ['sort_order', 'created_at']


class ProductVideo(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='videos', verbose_name='محصول')
    title = models.CharField(max_length=255, blank=True, verbose_name='عنوان')
    video = models.FileField(upload_to='products/videos/', verbose_name='فایل ویدیو')
    thumbnail = models.ImageField(upload_to='products/videos/thumbnails/', null=True, blank=True, verbose_name='تصویر بندانگشتی')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'ویدیوی محصول'
        verbose_name_plural = 'ویدیوهای محصولات'
        ordering = ['sort_order', 'created_at']


class ProductThreeD(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='three_d_files', verbose_name='محصول')
    title = models.CharField(max_length=255, blank=True, verbose_name='عنوان')
    file = models.FileField(upload_to='products/3d/', verbose_name='فایل سه‌بعدی')
    preview_image = models.ImageField(upload_to='products/3d/previews/', null=True, blank=True, verbose_name='تصویر پیش‌نمایش')
    file_format = models.CharField(max_length=50, blank=True, verbose_name='فرمت فایل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'فایل سه‌بعدی محصول'
        verbose_name_plural = 'فایل‌های سه‌بعدی محصولات'
        ordering = ['-created_at']
