#!/usr/bin/env python
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 55)
print("🚀 در حال آماده‌سازی و راه‌اندازی سرور لوکس NEWMOON HOME...")
print("=" * 55)

# 1. بررسی و نصب خودکار پکیج‌های ضروری
try:
    import django
    import decouple
    import import_export
except ImportError:
    print("⏳ در حال نصب خودکار پکیج‌های پروژه (لطفاً چند لحظه صبر کنید)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    import django

# 2. تنظیم کانفیگ جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newmoonhome.config.settings.development')

# 3. بررسی اتصال به دیتابیس PostgreSQL یا تغییر خودکار به SQLite در کامپیوتر شخصی
def check_or_setup_sqlite():
    settings_path = BASE_DIR / 'newmoonhome' / 'config' / 'settings' / 'base.py'
    if not settings_path.exists():
        return

    # بررسی آیا سرور پستگرس روی پورت 5432 محلی پاسخ می‌دهد
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect(('127.0.0.1', 5432))
        s.close()
        print("✔ سرور دیتابیس PostgreSQL متصل و فعال است.")
    except Exception:
        # اگر پستگرس نصب یا روشن نیست، فایل base.py را به طور خودکار روی SQLite می‌گذاریم
        content = settings_path.read_text(encoding='utf-8')
        if 'django.db.backends.postgresql' in content:
            print("⚡ دیتابیس PostgreSQL در این کامپیوتر یافت نشد؛ تنظیم خودکار پروژه روی دیتابیس محلی (SQLite)...")
            new_db_code = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
            new_content = re.sub(
                r'DATABASES\s*=\s*\{[^}]+\'default\'\s*:\s*\{[^\}]+\}\s*\}',
                new_db_code,
                content,
                flags=re.DOTALL
            )
            settings_path.write_text(new_content, encoding='utf-8')
            print("✔ دیتابیس پروژه به طور خودکار به SQLite تغییر یافت.")

check_or_setup_sqlite()

django.setup()
from django.core.management import call_command

# 4. اجرای مایگریشن‌ها و ساخت دیتای نمونه
print("\n⏳ در حال بررسی جداول دیتابیس و محصولات نمونه...")
call_command("migrate", interactive=False)
call_command("seed_demo_data")

# 5. ساخت خودکار سوپریوزر (admin / admin12345)
from accounts.models import User
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(username="admin", email="admin@newmoonhome.ir", password="admin12345")
    print("✔ کاربر مدیر (admin / admin12345) ساخته شد.")
elif not User.objects.get(username="admin").has_usable_password():
    u = User.objects.get(username="admin")
    u.set_password("admin12345")
    u.save()
    print("✔ رمز عبور کاربر مدیر روی admin12345 تنظیم شد.")

print("\n✅ سرور با موفقیت آماده و فعال شد!")
print("👉 آدرس ورود به سایت: http://127.0.0.1:8000/")
print("👉 آدرس پنل ادمین: http://127.0.0.1:8000/admin/")
print("=" * 55 + "\n")

call_command("runserver", "127.0.0.1:8000", use_reloader=False)
