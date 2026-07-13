import os

# --- ۱. بازنویسی مدل‌ها (بدون ارور فاصله) ---
models_code = """from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import secrets

class Category(models.Model):
    name_fa = models.CharField("نام فارسی", max_length=120)
    name_en = models.CharField("نام انگلیسی", max_length=120, blank=True)
    name_ar = models.CharField("نام عربی", max_length=120, blank=True)
    slug = models.SlugField("نامک", max_length=140, unique=True, allow_unicode=True)
    image = models.ImageField("کاور", upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField("فعال", default=True)
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "۱. دسته‌بندی‌ها"
    def __str__(self): return self.name_fa

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name_fa = models.CharField("نام فارسی", max_length=200)
    name_en = models.CharField("نام انگلیسی", max_length=200, blank=True)
    name_ar = models.CharField("نام عربی", max_length=200, blank=True)
    slug = models.SlugField("نامک", max_length=220, unique=True, allow_unicode=True)
    price = models.BigIntegerField("قیمت پایه", default=0)
    old_price = models.BigIntegerField("قیمت قبل", default=0, blank=True)
    stock = models.PositiveIntegerField("موجودی", default=10)
    image = models.ImageField("تصویر اصلی", upload_to="products/", null=True, blank=True)
    background_image = models.ImageField("پس‌زمینه صفحه", upload_to="products/bg/", blank=True, null=True)
    description_fa = models.TextField("توضیحات فارسی", blank=True)
    description_en = models.TextField("توضیحات انگلیسی", blank=True)
    description_ar = models.TextField("توضیحات عربی", blank=True)
    is_featured = models.BooleanField("نمایش در هوم", default=True)
    is_active = models.BooleanField("وضعیت", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "محصول"
        verbose_name_plural = "۲. محصولات"
    def __str__(self): return self.name_fa
    def get_absolute_url(self): return reverse("store:product_detail", kwargs={"slug": self.slug})

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField("عنوان تنوع", max_length=100)
    price_extra = models.BigIntegerField("اختلاف قیمت", default=0)
    image = models.ImageField("تصویر تنوع", upload_to="products/variants/", blank=True, null=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField("تصویر گالری", upload_to="products/gallery/")

class Order(models.Model):
    full_name = models.CharField("نام مشتری", max_length=100)
    phone = models.CharField("شماره تماس", max_length=11)
    address = models.TextField("آدرس")
    total_price = models.BigIntegerField("مبلغ کل", default=0)
    is_paid = models.BooleanField("پرداخت شده", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomOrder(models.Model):
    full_name = models.CharField("نام مشتری", max_length=100)
    phone = models.CharField("شماره تماس", max_length=11)
    width = models.PositiveIntegerField("عرض", default=0)
    height = models.PositiveIntegerField("ارتفاع", default=0)
    depth = models.PositiveIntegerField("عمق", default=0)
    color_scheme = models.CharField("رنگ مد نظر", max_length=100, blank=True)
    customer_image = models.ImageField("عکس ارسالی", upload_to="custom_orders/", blank=True, null=True)
    description = models.TextField("توضیحات مشتری", blank=True)
    quoted_price = models.BigIntegerField("قیمت پیشنهادی", default=0, blank=True)
    admin_notes = models.TextField("توضیحات مدیر", blank=True)
    admin_voice = models.FileField("ویس مدیر", upload_to="custom_orders/voices/", blank=True, null=True)
    status = models.CharField("وضعیت", max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class SiteSetting(models.Model):
    brand_name_fa = models.CharField("نام برند", max_length=120, default="نیومون هوم")
    logo = models.ImageField("لوگو", upload_to="site/", blank=True, null=True)
    primary_color = models.CharField("رنگ اصلی", max_length=7, default="#0a1511")
    secondary_color = models.CharField("رنگ فرعی", max_length=7, default="#c9a84c")
    hero_title = models.CharField("تیتر هیرو", max_length=200, default="زیبایی")
    hero_subtitle = models.TextField("زیرعنوان هیرو", default="کالکشن جدید")
    hero_image = models.ImageField("عکس هیرو", upload_to="site/", blank=True, null=True)
    announcement_text = models.CharField("متن متحرک", max_length=255, blank=True)
    is_installment_enabled = models.BooleanField("قسطی فعال؟", default=False)
    whatsapp_number = models.CharField("واتس‌اپ", max_length=20, blank=True)
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
"""

print("🚀 شروع عملیات پاکسازی و بازسازی...")

# ساخت فایل مدل سالم
with open("store/models.py", "w", encoding="utf-8") as f:
    f.write(models_code)
print("✔ فایل models.py با موفقیت بازنویسی شد.")

# پاک کردن دیتابیس و میگریشن‌ها
if os.path.exists("db.sqlite3"):
    os.remove("db.sqlite3")
    print("✔ دیتابیس قدیمی پاک شد.")

for file in os.listdir("store/migrations/"):
    if file != "__init__.py" and file.endswith(".py"):
        os.remove(os.path.join("store/migrations/", file))
print("✔ تاریخچه میگریشن‌ها پاکسازی شد.")

# اجرای دستورات سیستمی
os.system("python manage.py makemigrations store")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser --noinput --username admin --email admin@test.com")
# تنظیم پسورد برای یوزر ادمین
os.system("python manage.py shell -c \"from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin1234'); u.save()\"")

print("\n✨ عملیات با موفقیت تمام شد!")
print("حالا فایل START.py را اجرا کنید. یوزر: admin / پسورد: admin1234")