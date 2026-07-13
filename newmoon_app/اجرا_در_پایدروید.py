# -*- coding: utf-8 -*-
"""
🌿 فایل اجرای آسان NEWMOON HOME برای Pydroid 3 / کامپیوتر

طرز استفاده در Pydroid 3:
  ۱) این فایل (START.py) را در Pydroid باز کن.
  ۲) دکمه‌ی زرد پخش (▶) پایین صفحه را بزن.
  ۳) صبر کن تا بنویسد: Starting development server at http://127.0.0.1:8000/
  ۴) بعد در مرورگر گوشی برو به:  http://127.0.0.1:8000/admin/
     ورود با:  admin  /  admin1234

⚠️ مهم: تا وقتی Pydroid باز است و این فایل اجراست، سایت روشن می‌ماند.
"""
import os
import sys
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
sys.path.insert(0, BASE)

print("=" * 52)
print("🌿  NEWMOON HOME — در حال آماده‌سازی...")
print("پوشه‌ی پروژه:", BASE)
print("=" * 52)


def ensure(pkg, import_name=None):
    import_name = import_name or pkg.lower()
    try:
        __import__(import_name)
        print(f"✔ {pkg} از قبل نصب است.")
    except ImportError:
        print(f"⏳ در حال نصب {pkg} ... (کمی صبر کن)")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])
        print(f"✔ {pkg} نصب شد.")


ensure("Django", "django")
ensure("Pillow", "PIL")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()
from django.core.management import call_command
from django.db import connection

# ---------- ۱) ساخت جدول‌های دیتابیس ----------
print("\n⏳ آماده‌سازی دیتابیس (migrate)...")
try:
    call_command("makemigrations", "store", interactive=False, verbosity=1)
except Exception as e:
    print("یادداشت makemigrations:", e)
call_command("migrate", interactive=False, verbosity=1)

# بررسی اینکه جدول‌ها واقعاً ساخته شدند
tables = connection.introspection.table_names()
if "store_sitesetting" not in tables or "store_product" not in tables:
    print("\n❌ جدول‌ها ساخته نشدند! دوباره تلاش می‌کنم...")
    call_command("migrate", "store", interactive=False, verbosity=2)
    tables = connection.introspection.table_names()

if "store_sitesetting" in tables and "store_product" in tables:
    print("✔ دیتابیس آماده شد. جدول‌ها ساخته شدند.")
else:
    print("⚠️ هشدار: ممکن است دیتابیس کامل آماده نشده باشد.")

# ---------- ۲) داده‌های نمونه + کاربر مدیر ----------
from django.contrib.auth import get_user_model
from store.models import Category, Product, SiteSetting

User = get_user_model()

# کاربر مدیر (همیشه مطمئن شو وجود دارد)
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@newmoonhome.ir", "admin1234")
    print("✔ کاربر مدیر ساخته شد:  admin / admin1234")
else:
    print("✔ کاربر مدیر از قبل وجود دارد:  admin / admin1234")

# تنظیمات سایت + عکس هیرو (اگر assets موجود بود)
s = SiteSetting.load()
from django.core.files import File
hero = os.path.join(BASE, "..", "assets", "forest_hero_real.png")
if os.path.exists(hero) and not s.hero_image:
    try:
        with open(hero, "rb") as f:
            s.hero_image.save("hero.png", File(f), save=False)
    except Exception:
        pass
s.save()

# دسته‌بندی‌ها و محصولات نمونه (فقط اگر هیچ محصولی نیست)
if Product.objects.count() == 0:
    cats = {}
    for i, name in enumerate(["نشیمن", "اتاق خواب", "ناهارخوری", "ورودی"]):
        c, _ = Category.objects.get_or_create(name=name, defaults={"order": i})
        cats[name] = c
    sample = [
        ("مبل وینتج مون", "نشیمن", "ترکیب بافت گرم، خطوط نرم و هویت لوکس برای نشیمن.", 385000000, "کالکشن ویژه", "prod_sofa.png"),
        ("کنسول اورورا", "ورودی", "حضور ظریف چوب و فلز برای ورودی و نشیمن.", 248000000, "پرفروش", "prod_console.png"),
        ("میز ناهارخوری اِستون", "ناهارخوری", "فرمی متین و باوقار با امکان سفارشی‌سازی.", 440000000, "امضای برند", "prod_table.png"),
        ("سرویس خواب نوآر", "اتاق خواب", "ترکیبی عمیق و مجلل برای اتاق‌های خاص.", 598000000, "جدید", "prod_bed.png"),
    ]
    for name, cat, desc, price, badge, img in sample:
        p = Product(name=name, category=cats.get(cat), short_desc=desc,
                    description=desc, price=price, badge=badge, is_featured=True)
        ipath = os.path.join(BASE, "media", "products", img)
        if not os.path.exists(ipath):
            ipath = os.path.join(BASE, "..", "assets", img)
        if os.path.exists(ipath):
            try:
                with open(ipath, "rb") as f:
                    p.image.save(img, File(f), save=False)
            except Exception:
                pass
        p.save()
    print(f"✔ {Product.objects.count()} محصول نمونه ساخته شد.")
else:
    print(f"✔ {Product.objects.count()} محصول از قبل وجود دارد.")

# ---------- ۳) روشن کردن سرور ----------
print("\n" + "=" * 52)
print("✅ همه چیز آماده است!")
print("حالا در مرورگر گوشی (Chrome/Brave) باز کن:")
print("    👉  http://127.0.0.1:8000/          (سایت)")
print("    👉  http://127.0.0.1:8000/admin/    (پنل مدیریت)")
print("    ورود:  admin  /  admin1234")
print("=" * 52)
print("(این پنجره را نبند تا سایت روشن بماند)\n")

call_command("runserver", "127.0.0.1:8000", use_reloader=False)
