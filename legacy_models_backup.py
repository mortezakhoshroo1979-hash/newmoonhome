"""
مدل‌های اصلی پروژه فروشگاهی NEW MOON HOME

این فایل شامل مدل‌های تمام اپلیکیشن‌های درخواستی کاربر است تا به‌صورت
یکجا در اختیار باشد. در پیاده‌سازی واقعی، بهتر است هر بخش داخل فایل
models.py اپ مربوط به خودش قرار بگیرد.
"""

from __future__ import annotations

import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, Sum
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

try:
    # در صورتی که ckeditor نصب شده باشد از RichTextField استفاده می‌کنیم.
    from ckeditor.fields import RichTextField
except ImportError:  # pragma: no cover
    # جایگزین امن برای جلوگیری از خطای ایمپورت در محیطی که ckeditor ندارد.
    RichTextField = models.TextField


# -----------------------------------------------------------------------------
# مدل پایه
# -----------------------------------------------------------------------------
class TimeStampedModel(models.Model):
    """مدل پایه برای افزودن زمان ایجاد و آخرین بروزرسانی."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        abstract = True


# -----------------------------------------------------------------------------
# اپ accounts
# -----------------------------------------------------------------------------
class User(AbstractUser, TimeStampedModel):
    """مدل کاربر توسعه‌یافته."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="شناسه",
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="ایمیل",
    )
    phone = models.CharField(max_length=20, unique=True, verbose_name="شماره موبایل")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    national_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="کد ملی",
    )
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name() or self.username or self.phone


class CustomerRank(TimeStampedModel):
    """رتبه مشتری و مزایای وابسته به آن."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="نام رتبه")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="اسلاگ")
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
    )
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
    """پروفایل کاربر با امکان ذخیره چند آدرس."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر",
    )
    avatar = models.ImageField(
        upload_to="accounts/profiles/avatars/",
        null=True,
        blank=True,
        verbose_name="آواتار",
    )
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")
    score = models.PositiveIntegerField(default=0, verbose_name="امتیاز")
    rank = models.ForeignKey(
        CustomerRank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
        verbose_name="رتبه",
    )
    addresses = models.JSONField(
        default=list,
        blank=True,
        verbose_name="آدرس‌ها",
        help_text=(
            "ساختار پیشنهادی JSON برای آدرس‌ها: "
            "[{"
            "title": "خانه", "recipient_name": "...", "phone": "...", "province": "...", "city": "...", "address": "...", "postal_code": "...", "is_default": true}]"
        ),
    )

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"پروفایل {self.user}"


class ReferralCode(TimeStampedModel):
    """کد معرف اختصاصی هر کاربر."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referral_code",
        verbose_name="کاربر",
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="کد معرف")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="تعداد استفاده")
    total_reward_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مجموع پاداش",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "کد معرف"
        verbose_name_plural = "کدهای معرف"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - {self.user}"


class ReferralTransaction(TimeStampedModel):
    """ثبت هر بار استفاده از کد معرف."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="کد معرف",
    )
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referrals_made",
        verbose_name="معرف",
    )
    referred_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referrals_received",
        verbose_name="کاربر معرفی‌شده",
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referral_transactions",
        verbose_name="سفارش",
    )
    reward_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ پاداش",
    )
    note = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تراکنش معرفی"
        verbose_name_plural = "تراکنش‌های معرفی"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=~Q(referrer=models.F("referred_user")),
                name="referral_no_self_referral",
            )
        ]

    def __str__(self):
        return f"{self.referral_code.code} -> {self.referred_user}"


# -----------------------------------------------------------------------------
# اپ products
# -----------------------------------------------------------------------------
class Category(TimeStampedModel):
    """دسته‌بندی سلسله‌مراتبی محصولات."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="نام دسته")
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name="اسلاگ")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دسته والد",
    )
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(
        upload_to="products/categories/",
        null=True,
        blank=True,
        verbose_name="تصویر",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]
        unique_together = ("parent", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:category_detail", kwargs={"slug": self.slug})


class Brand(TimeStampedModel):
    """برند محصول."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name="نام برند")
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name="اسلاگ")
    logo = models.ImageField(upload_to="products/brands/", verbose_name="لوگو")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    website = models.URLField(blank=True, verbose_name="وب‌سایت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:brand_detail", kwargs={"slug": self.slug})


class Product(TimeStampedModel):
    """محصول اصلی فروشگاه."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته‌بندی",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="برند",
    )
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    slug = models.SlugField(max_length=280, unique=True, blank=True, verbose_name="اسلاگ")
    description = RichTextField(verbose_name="توضیحات")
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت پایه",
    )
    special_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="قیمت ویژه",
    )
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="وزن (کیلوگرم)",
    )
    dimensions = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="ابعاد",
        help_text="مثلاً: 200x90x75 سانتی‌متر",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی پایه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="تعداد فروش")
    customization_fields = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="فیلدهای شخصی‌سازی",
        help_text=(
            "ساختار پیشنهادی JSON: "
            "{" 
            "options": ["
            "{" 
            "group": "size", "label": "سایز", "type": "select", "required": true, "items": ["
            "{" 
            "value": "180x200", "label": "180x200", "price_adjustment": 5000000, "stock": 2, "sku_suffix": "SZ180""
            "}, "
            "{" 
            "value": "200x220", "label": "200x220", "price_adjustment": 8000000, "stock": 1, "sku_suffix": "SZ200""
            "}"
            "]}"
            ", {"
            "group": "wood_type", "label": "نوع چوب", "type": "select", "required": false, "items": [ ... ]"
            "}]"
            "}"
        ),
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active", "is_featured"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    @property
    def current_price(self):
        """قیمت جاری محصول را برمی‌گرداند."""
        if self.special_price is not None and self.special_price > 0:
            return self.special_price
        return self.base_price

    def calculate_price(self, selected_options: dict | None = None) -> Decimal:
        """
        محاسبه قیمت نهایی بر اساس گزینه‌های انتخاب‌شده.

        نمونه selected_options:
        {
            "size": "180x200",
            "wood_type": "oak",
            "fabric": "velvet-beige"
        }
        """
        selected_options = selected_options or {}
        total_price = Decimal(self.current_price or 0)
        config = self.customization_fields or {}
        options_groups = config.get("options", [])

        for group in options_groups:
            group_key = group.get("group")
            selected_value = selected_options.get(group_key)
            if selected_value is None:
                continue

            for item in group.get("items", []):
                if item.get("value") == selected_value:
                    adjustment = item.get("price_adjustment", 0) or 0
                    total_price += Decimal(str(adjustment))
                    break

        if total_price < 0:
            return Decimal("0")
        return total_price

    def get_option_stock(self, selected_options: dict | None = None) -> int:
        """
        موجودی گزینه‌های انتخابی را برمی‌گرداند.
        اگر چند گزینه دارای stock باشند، کمترین مقدار به‌عنوان موجودی قابل فروش در نظر گرفته می‌شود.
        """
        selected_options = selected_options or {}
        config = self.customization_fields or {}
        options_groups = config.get("options", [])
        stocks = []

        for group in options_groups:
            group_key = group.get("group")
            selected_value = selected_options.get(group_key)
            if selected_value is None:
                continue

            for item in group.get("items", []):
                if item.get("value") == selected_value and item.get("stock") is not None:
                    stocks.append(int(item.get("stock", 0)))
                    break

        if not stocks:
            return self.stock
        return min(stocks)


class ProductImage(TimeStampedModel):
    """گالری تصاویر محصول."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="محصول",
    )
    image = models.ImageField(upload_to="products/images/", verbose_name="تصویر")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="متن جایگزین")
    is_feature = models.BooleanField(default=False, verbose_name="تصویر شاخص")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return f"تصویر {self.product.name}"


class ProductVideo(TimeStampedModel):
    """ویدیوهای محصول."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="محصول",
    )
    title = models.CharField(max_length=255, blank=True, verbose_name="عنوان")
    video = models.FileField(upload_to="products/videos/", verbose_name="فایل ویدیو")
    thumbnail = models.ImageField(
        upload_to="products/videos/thumbnails/",
        null=True,
        blank=True,
        verbose_name="تصویر بندانگشتی",
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "ویدیوی محصول"
        verbose_name_plural = "ویدیوهای محصولات"
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return self.title or f"ویدیو {self.product.name}"


class ProductThreeD(TimeStampedModel):
    """فایل‌های سه‌بعدی محصول برای توسعه آینده."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="three_d_files",
        verbose_name="محصول",
    )
    title = models.CharField(max_length=255, blank=True, verbose_name="عنوان")
    file = models.FileField(upload_to="products/3d/", verbose_name="فایل سه‌بعدی")
    preview_image = models.ImageField(
        upload_to="products/3d/previews/",
        null=True,
        blank=True,
        verbose_name="تصویر پیش‌نمایش",
    )
    file_format = models.CharField(max_length=50, blank=True, verbose_name="فرمت فایل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "فایل سه‌بعدی محصول"
        verbose_name_plural = "فایل‌های سه‌بعدی محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"فایل سه‌بعدی {self.product.name}"


# -----------------------------------------------------------------------------
# اپ cart
# -----------------------------------------------------------------------------
class Cart(TimeStampedModel):
    """سبد خرید کاربران و مهمانان."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
        verbose_name="کاربر",
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="کلید سشن/کوکی",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"
        ordering = ["-updated_at"]

    def __str__(self):
        if self.user:
            return f"سبد {self.user}"
        return f"سبد مهمان {self.session_key}"

    @property
    def total_amount(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(TimeStampedModel):
    """آیتم‌های داخل سبد خرید."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="محصول",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    selected_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="گزینه‌های انتخاب‌شده",
        help_text=(
            "نمونه ساختار JSON: "
            "{" 
            "size": "180x200", "color": "dark-green", "wood_type": "oak", "fabric": "velvet""
            "}"
        ),
    )

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    @property
    def unit_price(self):
        return self.product.calculate_price(self.selected_options)

    @property
    def total_price(self):
        return self.unit_price * self.quantity


# -----------------------------------------------------------------------------
# اپ orders
# -----------------------------------------------------------------------------
class Order(TimeStampedModel):
    """سفارش مشتری."""

    STATUS_REGISTERED = "registered"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PREPARING = "preparing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELED = "canceled"
    STATUS_RETURNED = "returned"

    STATUS_CHOICES = [
        (STATUS_REGISTERED, "ثبت"),
        (STATUS_CONFIRMED, "تایید"),
        (STATUS_PREPARING, "آماده‌سازی"),
        (STATUS_SHIPPED, "ارسال"),
        (STATUS_DELIVERED, "تحویل"),
        (STATUS_CANCELED, "لغو"),
        (STATUS_RETURNED, "مرجوعی"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="کاربر",
    )
    order_number = models.CharField(max_length=50, unique=True, verbose_name="شماره سفارش")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REGISTERED,
        verbose_name="وضعیت",
    )
    shipping_method = models.ForeignKey(
        "ShippingMethod",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="روش ارسال",
    )
    coupon = models.ForeignKey(
        "Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="کوپن",
    )
    subtotal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="جمع جزء",
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ تخفیف",
    )
    shipping_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="هزینه ارسال",
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ نهایی",
    )
    receiver_name = models.CharField(max_length=255, verbose_name="نام گیرنده")
    receiver_phone = models.CharField(max_length=20, verbose_name="شماره گیرنده")
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="کد پستی")
    customer_note = models.TextField(blank=True, verbose_name="یادداشت مشتری")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان پرداخت")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["order_number", "status"])]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.order_number = f"NMH-{timestamp}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"order_number": self.order_number})

    def recalculate_totals(self):
        subtotal = self.items.aggregate(total=Sum("total_price_snapshot"))["total"] or Decimal("0")
        self.subtotal_amount = subtotal
        self.total_amount = subtotal + self.shipping_amount - self.discount_amount
        if self.total_amount < 0:
            self.total_amount = Decimal("0")
        self.save(update_fields=["subtotal_amount", "total_amount", "updated_at"])


class OrderItem(TimeStampedModel):
    """آیتم‌های سفارش با قیمت ثبت‌شده در لحظه خرید."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name="محصول",
    )
    product_name = models.CharField(max_length=255, verbose_name="نام محصول")
    sku = models.CharField(max_length=100, blank=True, verbose_name="SKU")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    selected_options = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="گزینه‌های انتخابی",
        help_text="نمونه: {""size"": ""180x200"", ""wood_type"": ""oak""}",
    )
    unit_price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت واحد در لحظه ثبت",
    )
    total_price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت کل در لحظه ثبت",
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.total_price_snapshot:
            self.total_price_snapshot = self.unit_price_snapshot * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(TimeStampedModel):
    """تاریخچه تغییر وضعیت سفارش."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_history",
        verbose_name="سفارش",
    )
    from_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name="از وضعیت")
    to_status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name="به وضعیت")
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="changed_order_statuses",
        verbose_name="تغییردهنده",
    )
    note = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تاریخچه وضعیت سفارش"
        verbose_name_plural = "تاریخچه وضعیت سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order.order_number}: {self.from_status} -> {self.to_status}"


class Invoice(TimeStampedModel):
    """فاکتور رسمی سفارش."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name="سفارش",
    )
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="شماره فاکتور")
    issue_date = models.DateField(default=timezone.localdate, verbose_name="تاریخ صدور")
    legal_name = models.CharField(max_length=255, blank=True, verbose_name="نام حقوقی/حقیقی")
    economic_code = models.CharField(max_length=50, blank=True, verbose_name="کد اقتصادی")
    national_id = models.CharField(max_length=50, blank=True, verbose_name="شناسه/کد ملی")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مبلغ")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        if not self.amount and self.order_id:
            self.amount = self.order.total_amount
        super().save(*args, **kwargs)


# -----------------------------------------------------------------------------
# اپ payments
# -----------------------------------------------------------------------------
class PaymentGateway(TimeStampedModel):
    """درگاه پرداخت قابل تنظیم."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="نام درگاه")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="اسلاگ")
    provider = models.CharField(max_length=100, verbose_name="ارائه‌دهنده")
    settings_json = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات JSON",
        help_text=(
            "نمونه ساختار: "
            "{" 
            "merchant_id": "...", "terminal_id": "...", "callback_url": "...", "sandbox": true"
            "}"
        ),
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    priority = models.PositiveIntegerField(default=0, verbose_name="اولویت")

    class Meta:
        verbose_name = "درگاه پرداخت"
        verbose_name_plural = "درگاه‌های پرداخت"
        ordering = ["priority", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    """ثبت تمام تراکنش‌های مالی."""

    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_CANCELED = "canceled"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_PENDING, "در انتظار"),
        (STATUS_SUCCESS, "موفق"),
        (STATUS_FAILED, "ناموفق"),
        (STATUS_CANCELED, "لغو شده"),
        (STATUS_REFUNDED, "بازپرداخت شده"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="سفارش",
    )
    gateway = models.ForeignKey(
        PaymentGateway,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name="درگاه",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name="کاربر",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مبلغ")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="وضعیت",
    )
    authority = models.CharField(max_length=255, blank=True, verbose_name="Authority")
    reference_id = models.CharField(max_length=255, blank=True, verbose_name="Reference ID")
    tracking_code = models.CharField(max_length=255, blank=True, verbose_name="کد پیگیری")
    card_pan = models.CharField(max_length=30, blank=True, verbose_name="شماره کارت ماسک‌شده")
    raw_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="پاسخ خام درگاه",
        help_text="ساختار آزاد JSON برای ذخیره پاسخ کامل درگاه پرداخت",
    )
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان پرداخت")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "authority", "reference_id"])]

    def __str__(self):
        return f"{self.order.order_number} - {self.amount}"


# -----------------------------------------------------------------------------
# اپ shipping
# -----------------------------------------------------------------------------
class ShippingMethod(TimeStampedModel):
    """روش ارسال."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name="نام")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    base_cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="هزینه پایه")
    cost_per_kg = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="هزینه هر کیلوگرم",
    )
    min_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="حداقل وزن",
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="حداکثر وزن",
    )
    covered_cities = models.JSONField(
        default=list,
        blank=True,
        verbose_name="شهرهای تحت پوشش",
        help_text=(
            "نمونه ساختار JSON: "
            "["
            "{" 
            "province": "تهران", "cities": ["تهران", "ری", "شمیرانات"]"
            "}, "
            "{" 
            "province": "اصفهان", "cities": ["اصفهان"]"
            "}"
            "]"
        ),
    )
    delivery_time = models.CharField(max_length=150, verbose_name="زمان تحویل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "روش ارسال"
        verbose_name_plural = "روش‌های ارسال"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def calculate_cost(self, weight: Decimal | int | float = 0) -> Decimal:
        weight = Decimal(str(weight or 0))
        return Decimal(self.base_cost) + (weight * Decimal(self.cost_per_kg))


class ShippingRate(TimeStampedModel):
    """تعرفه ویژه ارسال برای استان‌ها/شهرهای خاص."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping_method = models.ForeignKey(
        ShippingMethod,
        on_delete=models.CASCADE,
        related_name="special_rates",
        verbose_name="روش ارسال",
    )
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, blank=True, verbose_name="شهر")
    extra_cost = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="هزینه اضافی",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تعرفه ویژه ارسال"
        verbose_name_plural = "تعرفه‌های ویژه ارسال"
        ordering = ["province", "city"]
        unique_together = ("shipping_method", "province", "city")

    def __str__(self):
        target = self.city or self.province
        return f"{self.shipping_method.name} - {target}"


# -----------------------------------------------------------------------------
# اپ discounts
# -----------------------------------------------------------------------------
class Coupon(TimeStampedModel):
    """کوپن تخفیف."""

    TYPE_PERCENT = "percent"
    TYPE_FIXED = "fixed"

    TYPE_CHOICES = [
        (TYPE_PERCENT, "درصدی"),
        (TYPE_FIXED, "ثابت"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, verbose_name="کد")
    discount_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="نوع تخفیف")
    value = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مقدار تخفیف")
    min_order_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="حداقل مبلغ سفارش",
    )
    max_discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="حداکثر مبلغ تخفیف",
    )
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضا")
    max_uses = models.PositiveIntegerField(default=1, verbose_name="حداکثر استفاده")
    used_count = models.PositiveIntegerField(default=0, verbose_name="تعداد استفاده")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپن‌ها"
        ordering = ["-created_at"]

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

    def calculate_discount(self, amount: Decimal) -> Decimal:
        amount = Decimal(str(amount))
        if not self.is_valid or amount < self.min_order_amount:
            return Decimal("0")

        if self.discount_type == self.TYPE_PERCENT:
            discount = (amount * Decimal(self.value)) / Decimal("100")
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        return min(Decimal(self.value), amount)


class CategoryDiscount(TimeStampedModel):
    """تخفیف دسته‌ای برای دسته‌بندی محصولات."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="discounts",
        verbose_name="دسته‌بندی",
    )
    title = models.CharField(max_length=150, verbose_name="عنوان")
    percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
    )
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تخفیف دسته‌ای"
        verbose_name_plural = "تخفیف‌های دسته‌ای"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.category.name}"


class BulkPriceUpdate(TimeStampedModel):
    """سیستم تغییر قیمت گروهی برای توسعه بعدی."""

    TYPE_PERCENT = "percent"
    TYPE_FIXED = "fixed"

    TYPE_CHOICES = [
        (TYPE_PERCENT, "درصدی"),
        (TYPE_FIXED, "مبلغ ثابت"),
    ]

    STATUS_DRAFT = "draft"
    STATUS_SCHEDULED = "scheduled"
    STATUS_APPLIED = "applied"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "پیش‌نویس"),
        (STATUS_SCHEDULED, "زمان‌بندی‌شده"),
        (STATUS_APPLIED, "اعمال‌شده"),
        (STATUS_CANCELED, "لغوشده"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    update_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="نوع تغییر")
    value = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مقدار")
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="bulk_price_updates",
        verbose_name="دسته‌بندی‌ها",
    )
    brands = models.ManyToManyField(
        Brand,
        blank=True,
        related_name="bulk_price_updates",
        verbose_name="برندها",
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="bulk_price_updates",
        verbose_name="محصولات",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="وضعیت",
    )
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان اجرا")
    note = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تغییر قیمت گروهی"
        verbose_name_plural = "تغییرات قیمت گروهی"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# اپ blog
# -----------------------------------------------------------------------------
class PostCategory(TimeStampedModel):
    """دسته‌بندی مقالات وبلاگ."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, verbose_name="نام")
    slug = models.SlugField(max_length=180, unique=True, blank=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی مقاله"
        verbose_name_plural = "دسته‌بندی‌های مقالات"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(TimeStampedModel):
    """تگ مقاله."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="نام")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(TimeStampedModel):
    """پست وبلاگ برای سئو و بازاریابی محتوایی."""

    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "پیش‌نویس"),
        (STATUS_PUBLISHED, "منتشر شده"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="نویسنده",
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="دسته‌بندی",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="تگ‌ها")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=280, unique=True, blank=True, verbose_name="اسلاگ")
    excerpt = models.TextField(blank=True, verbose_name="خلاصه")
    content = RichTextField(verbose_name="محتوا")
    featured_image = models.ImageField(
        upload_to="blog/posts/",
        null=True,
        blank=True,
        verbose_name="تصویر شاخص",
    )
    seo_title = models.CharField(max_length=255, blank=True, verbose_name="عنوان سئو")
    seo_description = models.TextField(blank=True, verbose_name="توضیحات سئو")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="وضعیت",
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان انتشار")

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})


class Comment(TimeStampedModel):
    """نظرات پست‌ها با تایید ادمین."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="پست",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_comments",
        verbose_name="کاربر",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="والد",
    )
    name = models.CharField(max_length=150, blank=True, verbose_name="نام")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    body = models.TextField(verbose_name="متن نظر")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ["created_at"]

    def __str__(self):
        return f"نظر برای {self.post.title}"


# -----------------------------------------------------------------------------
# اپ core
# -----------------------------------------------------------------------------
class Slider(TimeStampedModel):
    """اسلایدر صفحه اصلی."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="زیرعنوان")
    image = models.ImageField(upload_to="core/sliders/", verbose_name="تصویر")
    link = models.URLField(blank=True, verbose_name="لینک")
    button_text = models.CharField(max_length=100, blank=True, verbose_name="متن دکمه")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title


class Banner(TimeStampedModel):
    """بنر تبلیغاتی."""

    POSITION_TOP = "top"
    POSITION_MIDDLE = "middle"
    POSITION_BOTTOM = "bottom"
    POSITION_SIDEBAR = "sidebar"

    POSITION_CHOICES = [
        (POSITION_TOP, "بالا"),
        (POSITION_MIDDLE, "میانی"),
        (POSITION_BOTTOM, "پایین"),
        (POSITION_SIDEBAR, "سایدبار"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="عنوان")
    image = models.ImageField(upload_to="core/banners/", verbose_name="تصویر")
    link = models.URLField(blank=True, verbose_name="لینک")
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name="جایگاه")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"
        ordering = ["position", "sort_order"]

    def __str__(self):
        return self.title


class Newsletter(TimeStampedModel):
    """عضویت در خبرنامه."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name="ایمیل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class ContactMessage(TimeStampedModel):
    """پیام تماس با ما."""

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_ANSWERED = "answered"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_NEW, "جدید"),
        (STATUS_IN_PROGRESS, "در حال بررسی"),
        (STATUS_ANSWERED, "پاسخ داده شده"),
        (STATUS_CLOSED, "بسته شده"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="نام")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name="وضعیت",
    )
    admin_note = models.TextField(blank=True, verbose_name="یادداشت ادمین")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject


class SiteSetting(TimeStampedModel):
    """تنظیمات عمومی سایت."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site_name = models.CharField(max_length=255, default="NEW MOON HOME", verbose_name="عنوان سایت")
    site_description = models.TextField(blank=True, verbose_name="توضیحات سایت")
    logo = models.ImageField(
        upload_to="core/settings/",
        null=True,
        blank=True,
        verbose_name="لوگو",
    )
    favicon = models.ImageField(
        upload_to="core/settings/",
        null=True,
        blank=True,
        verbose_name="فاوآیکون",
    )
    primary_color = models.CharField(max_length=7, default="#1a3c2a", verbose_name="رنگ اصلی")
    secondary_color = models.CharField(max_length=7, default="#c9a84c", verbose_name="رنگ ثانویه")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن تماس")
    contact_email = models.EmailField(blank=True, verbose_name="ایمیل تماس")
    address = models.TextField(blank=True, verbose_name="آدرس")
    social_links = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="شبکه‌های اجتماعی",
        help_text=(
            "نمونه ساختار JSON: "
            "{" 
            "instagram": "https://instagram.com/...", "telegram": "https://t.me/...", "linkedin": "...""
            "}"
        ),
    )
    seo_meta = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات سئو",
        help_text=(
            "نمونه ساختار JSON: "
            "{" 
            "default_title": "NEW MOON HOME", "default_description": "...", "default_keywords": ["مبلمان", "دکوراسیون"]"
            "}"
        ),
    )

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"
        ordering = ["-created_at"]

    def __str__(self):
        return self.site_name


# -----------------------------------------------------------------------------
# اپ wishlist
# -----------------------------------------------------------------------------
class Wishlist(TimeStampedModel):
    """علاقه‌مندی‌های کاربران."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
        verbose_name="کاربر",
    )
    products = models.ManyToManyField(Product, blank=True, related_name="wishlists", verbose_name="محصولات")

    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"علاقه‌مندی‌های {self.user}"


class Compare(TimeStampedModel):
    """مقایسه محصولات برای هر کاربر."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="compare_list",
        verbose_name="کاربر",
    )
    products = models.ManyToManyField(Product, blank=True, related_name="compare_lists", verbose_name="محصولات")

    class Meta:
        verbose_name = "مقایسه"
        verbose_name_plural = "مقایسه‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"مقایسه {self.user}"

    def clean(self):
        if self.pk and self.products.count() > 4:
            raise ValidationError("حداکثر ۴ محصول برای مقایسه مجاز است.")

    def add_product(self, product: Product):
        """افزودن محصول به لیست مقایسه با محدودیت ۴ عدد."""
        if self.products.count() >= 4:
            raise ValidationError("حداکثر ۴ محصول برای مقایسه مجاز است.")
        self.products.add(product)
