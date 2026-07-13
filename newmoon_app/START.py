import os
import sys
import subprocess

# --- تابع نصب خودکار برای کامپیوتر و گوشی ---
def ensure_installed(pkg):
    try:
        __import__(pkg.lower() if pkg != "Pillow" else "PIL")
    except ImportError:
        print(f"⏳ در حال نصب {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_installed("Django")
ensure_installed("Pillow")
ensure_installed("tzdata")

import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

print("\n" + "="*40)
print("🚀 در حال راه اندازی سیستم لوکس نیومون هوم...")
print("="*40)

# ۱. همگام‌سازی دیتابیس
call_command("makemigrations", "store", interactive=False)
call_command("migrate", interactive=False)

# ۲. ساخت کاربر مدیر (اگر نباشد)
from django.contrib.auth.models import User
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@test.com", "admin1234")
    print("✔ کاربر مدیر (admin / admin1234) ساخته شد.")

print("\n✅ سیستم با موفقیت روی پورت 8000 بالا آمد!")
print("👉 http://127.0.0.1:8000/")
call_command("runserver", "127.0.0.1:8000", use_reloader=False)