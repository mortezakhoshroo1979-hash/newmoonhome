"""تنظیمات سبک برای اجرای پروژه روی اندروید / Pydroid / محیط‌های محدود."""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# در محیط اندروید معمولاً PostgreSQL/Redis در دسترس نیستند.
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# اپ‌ها و middlewareهای سنگین/اختیاری را حذف می‌کنیم تا اجرای اولیه ساده‌تر شود.
OPTIONAL_APPS_TO_REMOVE = {
    'debug_toolbar',
    'import_export',
    'ckeditor',
}
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in OPTIONAL_APPS_TO_REMOVE]

OPTIONAL_MIDDLEWARE_TO_REMOVE = {
    'debug_toolbar.middleware.DebugToolbarMiddleware',
}
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in OPTIONAL_MIDDLEWARE_TO_REMOVE]

# استاتیک‌ها در محیط سبک اندرویدی
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# کش ساده
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'android-cache',
    }
}

# امنیت در dev اندروید ساده‌تر
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
