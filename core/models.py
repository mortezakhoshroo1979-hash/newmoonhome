from __future__ import annotations

import uuid

from django.core.validators import EmailValidator
from django.db import models

from common_models import TimeStampedModel


class Slider(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    subtitle = models.CharField(max_length=255, blank=True, verbose_name='زیرعنوان')
    image = models.ImageField(upload_to='core/sliders/', verbose_name='تصویر')
    link = models.URLField(blank=True, verbose_name='لینک')
    button_text = models.CharField(max_length=100, blank=True, verbose_name='متن دکمه')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'
        ordering = ['sort_order', '-created_at']


class Banner(TimeStampedModel):
    POSITION_TOP = 'top'
    POSITION_MIDDLE = 'middle'
    POSITION_BOTTOM = 'bottom'
    POSITION_SIDEBAR = 'sidebar'
    POSITION_CHOICES = [(POSITION_TOP, 'بالا'), (POSITION_MIDDLE, 'میانی'), (POSITION_BOTTOM, 'پایین'), (POSITION_SIDEBAR, 'سایدبار')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    image = models.ImageField(upload_to='core/banners/', verbose_name='تصویر')
    link = models.URLField(blank=True, verbose_name='لینک')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name='جایگاه')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
        ordering = ['position', 'sort_order']


class Newsletter(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name='ایمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'خبرنامه'
        verbose_name_plural = 'خبرنامه‌ها'
        ordering = ['-created_at']


class ContactMessage(TimeStampedModel):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_ANSWERED = 'answered'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [(STATUS_NEW, 'جدید'), (STATUS_IN_PROGRESS, 'در حال بررسی'), (STATUS_ANSWERED, 'پاسخ داده شده'), (STATUS_CLOSED, 'بسته شده')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name='نام')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    subject = models.CharField(max_length=255, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='وضعیت')
    admin_note = models.TextField(blank=True, verbose_name='یادداشت ادمین')

    class Meta:
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'
        ordering = ['-created_at']


class SiteSetting(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site_name = models.CharField(max_length=255, default='NEW MOON HOME', verbose_name='عنوان سایت')
    site_description = models.TextField(blank=True, verbose_name='توضیحات سایت')
    logo = models.ImageField(upload_to='core/settings/', null=True, blank=True, verbose_name='لوگو')
    favicon = models.ImageField(upload_to='core/settings/', null=True, blank=True, verbose_name='فاوآیکون')
    primary_color = models.CharField(max_length=7, default='#1a3c2a', verbose_name='رنگ اصلی')
    secondary_color = models.CharField(max_length=7, default='#c9a84c', verbose_name='رنگ ثانویه')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن تماس')
    contact_email = models.EmailField(blank=True, verbose_name='ایمیل تماس')
    address = models.TextField(blank=True, verbose_name='آدرس')
    social_links = models.JSONField(default=dict, blank=True, verbose_name='شبکه‌های اجتماعی')
    seo_meta = models.JSONField(default=dict, blank=True, verbose_name='تنظیمات سئو')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'
        ordering = ['-created_at']

    def __str__(self):
        return self.site_name
