from __future__ import annotations

import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

from common_models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """مدل کاربر توسعه‌یافته."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="شناسه")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, unique=True, verbose_name="شماره موبایل")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    national_code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="کد ملی")
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name() or self.username or self.phone


class CustomerRank(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="نام رتبه")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="اسلاگ")
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="درصد تخفیف")
    benefits = models.TextField(blank=True, verbose_name="مزایا")
    minimum_score = models.PositiveIntegerField(default=0, verbose_name="حداقل امتیاز")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "رتبه مشتری"
        verbose_name_plural = "رتبه‌های مشتریان"
        ordering = ["minimum_score", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Profile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile", verbose_name="کاربر")
    avatar = models.ImageField(upload_to="accounts/profiles/avatars/", null=True, blank=True, verbose_name="آواتار")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")
    score = models.PositiveIntegerField(default=0, verbose_name="امتیاز")
    rank = models.ForeignKey('accounts.CustomerRank', on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles", verbose_name="رتبه")
    addresses = models.JSONField(default=list, blank=True, verbose_name="آدرس‌ها")

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"پروفایل {self.user}"


class ReferralCode(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_code", verbose_name="کاربر")
    code = models.CharField(max_length=50, unique=True, verbose_name="کد معرف")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="تعداد استفاده")
    total_reward_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="مجموع پاداش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "کد معرف"
        verbose_name_plural = "کدهای معرف"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - {self.user}"


class ReferralTransaction(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referral_code = models.ForeignKey('accounts.ReferralCode', on_delete=models.CASCADE, related_name="transactions", verbose_name="کد معرف")
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referrals_made", verbose_name="معرف")
    referred_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referrals_received", verbose_name="کاربر معرفی‌شده")
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name="referral_transactions", verbose_name="سفارش")
    reward_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="مبلغ پاداش")
    note = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تراکنش معرفی"
        verbose_name_plural = "تراکنش‌های معرفی"
        ordering = ["-created_at"]
        constraints = [models.CheckConstraint(check=~Q(referrer=models.F("referred_user")), name="referral_no_self_referral")]

    def __str__(self):
        return f"{self.referral_code.code} -> {self.referred_user}"
