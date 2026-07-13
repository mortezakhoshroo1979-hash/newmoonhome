"""اسکریپت پر کردن داده‌های اولیه + ساخت کاربر مدیر.

اجرا:  python manage.py shell < seed.py
"""
import os
import django
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
try:
    django.setup()
except Exception:
    pass

from django.contrib.auth import get_user_model
from store.models import Category, Product, SiteSetting

User = get_user_model()

# ---- کاربر مدیر ----
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@newmoonhome.ir", "admin1234")
    print("کاربر مدیر ساخته شد:  admin / admin1234")
else:
    print("کاربر مدیر از قبل وجود دارد.")

# ---- تنظیمات سایت ----
s = SiteSetting.load()
ASSETS = "../assets"  # نسبت به newmoon_app
hero_path = os.path.join(ASSETS, "forest_hero_real.png")
if os.path.exists(hero_path) and not s.hero_image:
    with open(hero_path, "rb") as f:
        s.hero_image.save("hero.png", File(f), save=False)
s.save()
print("تنظیمات سایت آماده شد.")

# ---- دسته‌بندی‌ها ----
cats = {}
for i, name in enumerate(["نشیمن", "اتاق خواب", "ناهارخوری", "ورودی"]):
    c, _ = Category.objects.get_or_create(name=name, defaults={"order": i})
    cats[name] = c
print("دسته‌بندی‌ها آماده شد.")

# ---- محصولات ----
products = [
    ("مبل وینتج مون", "نشیمن", "ترکیب بافت گرم، خطوط نرم و هویت لوکس برای نشیمن.",
     385000000, "کالکشن ویژه", "prod_sofa.png"),
    ("کنسول اورورا", "ورودی", "حضور ظریف چوب و فلز برای ورودی و نشیمن.",
     248000000, "پرفروش", "prod_console.png"),
    ("میز ناهارخوری اِستون", "ناهارخوری", "فرمی متین و باوقار با امکان سفارشی‌سازی.",
     440000000, "امضای برند", "prod_table.png"),
    ("سرویس خواب نوآر", "اتاق خواب", "ترکیبی عمیق و مجلل برای اتاق‌های خاص.",
     598000000, "جدید", "prod_bed.png"),
]
for name, cat, desc, price, badge, img in products:
    if Product.objects.filter(name=name).exists():
        continue
    p = Product(
        name=name, category=cats.get(cat), short_desc=desc,
        description=desc + "\n\nساخته‌شده از متریال ممتاز با اجرای دستی و امکان سفارشی‌سازی ابعاد و متریال.",
        price=price, badge=badge, is_featured=True,
    )
    ipath = os.path.join(ASSETS, img)
    if os.path.exists(ipath):
        with open(ipath, "rb") as f:
            p.image.save(img, File(f), save=False)
    p.save()
    print(f"محصول ساخته شد: {name}")

print("\n✅ همه چیز آماده است. وارد /admin/ شوید با  admin / admin1234")
