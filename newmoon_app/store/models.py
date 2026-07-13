from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# ==========================================
# ۱. کاتالوگ (دسته‌بندی تودرتو و محصولات)
# ==========================================

class Category(models.Model):
    """ساختار درختی: اصلی و فرعی"""
    name_fa = models.CharField("نام فارسی", max_length=120)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="دسته مادر")
    slug = models.SlugField("نامک", max_length=140, unique=True, allow_unicode=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "۱. دسته‌بندی‌ها"

    def __str__(self):
        return f"{self.parent.name_fa} > {self.name_fa}" if self.parent else self.name_fa

class Product(models.Model):
    """مدل پیشرفته محصول ۳ زبانه با قیمت دلاری"""
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="دسته‌بندی")
    name_fa = models.CharField("نام فارسی", max_length=200)
    name_en = models.CharField("نام انگلیسی", max_length=200, blank=True)
    name_ar = models.CharField("نام عربی", max_length=200, blank=True)
    slug = models.SlugField("نامک (URL)", max_length=220, unique=True, allow_unicode=True)
    
    price = models.BigIntegerField("قیمت (ریال)", default=0)
    price_usd = models.DecimalField("قیمت دلاری ($)", max_digits=10, decimal_places=2, default=0, blank=True)
    old_price = models.BigIntegerField("قیمت قبل", default=0, blank=True)
    stock = models.PositiveIntegerField("موجودی", default=10)
    
    image = models.ImageField("تصویر اصلی", upload_to="products/", null=True, blank=True)
    background_image = models.ImageField("پس‌زمینه صفحه", upload_to="products/bg/", blank=True, null=True)
    description_fa = models.TextField("توضیحات فارسی", blank=True)
    
    is_featured = models.BooleanField("نمایش در هوم", default=True)
    is_active = models.BooleanField("وضعیت فعال", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "محصول"
        verbose_name_plural = "۲. محصولات"

    def __str__(self): return self.name_fa
    def get_absolute_url(self): return reverse("store:product_detail", kwargs={"slug": self.slug})

class ProductImage(models.Model):
    """گالری تصاویر چندتایی"""
    product = models.ForeignKey(Product, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField("تصویر گالری", upload_to="products/gallery/")

class ProductVariant(models.Model):
    """تنوع رنگ و متریال"""
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField("عنوان تنوع", max_length=100)
    price_extra = models.BigIntegerField("اختلاف قیمت", default=0)
    image = models.ImageField("تصویر تنوع", upload_to="products/variants/", blank=True, null=True)


# ==========================================
# ۲. سفارشات (سفارشی و نقدی)
# ==========================================

class CustomOrder(models.Model):
    """استعلام قیمت با ویس مدیر"""
    full_name = models.CharField("نام مشتری", max_length=100)
    phone = models.CharField("شماره تماس", max_length=11)
    width = models.PositiveIntegerField("عرض", default=0)
    height = models.PositiveIntegerField("ارتفاع", default=0)
    depth = models.PositiveIntegerField("عمق", default=0)
    color_scheme = models.CharField("رنگ مد نظر", max_length=100, blank=True)
    customer_image = models.ImageField("عکس مشتری", upload_to="custom_orders/", blank=True, null=True)
    description = models.TextField("توضیحات", blank=True)
    quoted_price = models.BigIntegerField("قیمت پیشنهادی", default=0)
    admin_notes = models.TextField("توضیحات مدیر", blank=True)
    admin_voice = models.FileField("ویس مدیر", upload_to="custom_orders/voices/", blank=True, null=True)
    status = models.CharField("وضعیت", max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    full_name = models.CharField("نام خریدار", max_length=100)
    phone = models.CharField("تماس", max_length=11)
    address = models.TextField("آدرس")
    total_price = models.BigIntegerField("جمع کل")
    created_at = models.DateTimeField(auto_now_add=True)


# ==========================================
# ۳. تنظیمات مرکز کنترل
# ==========================================

class SiteSetting(models.Model):
    brand_name_fa = models.CharField("نام برند", max_length=120, default="نیومون هوم")
    logo = models.ImageField("لوگو", upload_to="site/", blank=True, null=True)
    primary_color = models.CharField("رنگ اصلی", max_length=7, default="#0a1511")
    secondary_color = models.CharField("رنگ طلایی", max_length=7, default="#c9a84c")
    hero_title = models.CharField("تیتر هیرو", max_length=200, default="زیبایی")
    hero_subtitle = models.TextField("زیرعنوان هیرو", default="کالکشن جدید")
    hero_image = models.ImageField("عکس هیرو", upload_to="site/", blank=True, null=True)
    announcement_text = models.CharField("متن متحرک", max_length=255, blank=True)
    is_installment_enabled = models.BooleanField("قسطی فعال؟", default=False)
    whatsapp_number = models.CharField("واتس‌اپ", max_length=20, blank=True)
    phone = models.CharField("تلفن", max_length=20, default="۰۲۱")
    address = models.TextField("آدرس", blank=True)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)