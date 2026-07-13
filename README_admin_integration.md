# راهنمای اتصال پنل مدیریت اختصاصی

## پکیج‌های مورد نیاز

```bash
pip install django-import-export django-crispy-forms django-filter celery django-ckeditor
```

## اضافه کردن به INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'import_export',
    'crispy_forms',
    'django_filters',
    'custom_admin',
]
```

## اضافه کردن URL ها

```python
from django.urls import include, path

urlpatterns = [
    path('secure-panel/', include('custom_admin.urls')),
    path('admin/', admin.site.urls),
]
```

## نکات مهم

- بخش‌های اصلی products / orders / accounts / discounts پیاده‌سازی شده‌اند.
- برای عملیات async مثل ارسال ایمیل گروهی و گزارش‌گیری سنگین، باید Celery task تعریف شود.
- برای لاگ کامل تغییر قیمت و سفارشات، پیشنهاد می‌شود مدل‌های Log جداگانه اضافه شوند یا از django-simple-history استفاده شود.
- برای Role-based permissions می‌توان از Group و Permission جنگو استفاده کرد:
  - ادمین کل
  - مدیر فروش
  - مدیر محتوا
- برای Drag & Drop اسلایدر و بنر، در مرحله بعد SortableJS یا django-admin-sortable2 پیشنهاد می‌شود.
- برای خروجی Excel/CSV در ModelAdmin ها از import-export استفاده شده است.
```
