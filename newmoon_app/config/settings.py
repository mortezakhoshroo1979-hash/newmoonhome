"""تنظیمات پروژه NEWMOON HOME (نسخه سبک و خودکفا - SQLite)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-newmoon-home-dev-key-change-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- ثبت کامل خطاها در فایل خطا.txt برای عیب‌یابی روی گوشی ---
import os as _os
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "errorfile": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": _os.path.join(BASE_DIR, "خطا.txt"),
            "encoding": "utf-8",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {"handlers": ["errorfile", "console"], "level": "INFO"},
        "django.request": {"handlers": ["errorfile", "console"], "level": "ERROR", "propagate": False},
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

LANGUAGE_CODE = "fa-ir"
USE_I18N = True

# --- منطقه‌ی زمانی به‌صورت مقاوم ---
# روی اندروید/Pydroid معمولاً پکیج tzdata و دیتابیس مناطق زمانی سیستم وجود ندارد،
# و TIME_ZONE = "Asia/Tehran" باعث کرش‌شدن صفحاتی مثل ادمین می‌شود.
# این کد اول مطمئن می‌شود تهران قابل استفاده است؛ اگر نبود، امن به UTC برمی‌گردد.
try:
    import zoneinfo
    zoneinfo.ZoneInfo("Asia/Tehran")  # تست اینکه منطقه زمانی در دسترس است
    TIME_ZONE = "Asia/Tehran"
    USE_TZ = True
except Exception:
    # روی اندروید بدون tzdata: حالت امن
    TIME_ZONE = "UTC"
    USE_TZ = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# رفع مشکل OSError [Errno 38] در اندروید/Pydroid
import django.core.files.locks
from django.core.files import locks

def dummy_lock(f, flags):
    return True

def dummy_unlock(f):
    return True

django.core.files.locks.lock = dummy_lock
django.core.files.locks.unlock = dummy_unlock
CART_SESSION_ID = 'cart'