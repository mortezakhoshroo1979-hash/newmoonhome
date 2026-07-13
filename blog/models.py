from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from common_models import TimeStampedModel

try:
    from ckeditor.fields import RichTextField
except ImportError:  # pragma: no cover
    RichTextField = models.TextField


class PostCategory(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name='نام')
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی‌های مقالات'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='نام')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(TimeStampedModel):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [(STATUS_DRAFT, 'پیش‌نویس'), (STATUS_PUBLISHED, 'منتشر شده')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='نویسنده')
    category = models.ForeignKey('blog.PostCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='دسته‌بندی')
    tags = models.ManyToManyField('blog.Tag', blank=True, related_name='posts', verbose_name='تگ‌ها')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    slug = models.SlugField(max_length=280, unique=True, blank=True, verbose_name='اسلاگ')
    excerpt = models.TextField(blank=True, verbose_name='خلاصه')
    content = RichTextField(verbose_name='محتوا')
    featured_image = models.ImageField(upload_to='blog/posts/', null=True, blank=True, verbose_name='تصویر شاخص')
    seo_title = models.CharField(max_length=255, blank=True, verbose_name='عنوان سئو')
    seo_description = models.TextField(blank=True, verbose_name='توضیحات سئو')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, verbose_name='وضعیت')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان انتشار')

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:home')


class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='والد')
    name = models.CharField(max_length=150, blank=True, verbose_name='نام')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    body = models.TextField(verbose_name='متن نظر')
    is_approved = models.BooleanField(default=False, verbose_name='تایید شده')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['created_at']
