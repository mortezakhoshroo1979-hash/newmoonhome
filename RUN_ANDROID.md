# راهنمای اجرای پروژه روی اندروید

## 1) نصب پکیج‌های پایه
در همان محیط اندرویدی این دستورها را اجرا کن:

```bash
python -m pip install --upgrade pip
python -m pip install django pillow python-decouple whitenoise djangorestframework djangorestframework-simplejwt drf-spectacular django-filter django-crispy-forms django-import-export django-ckeditor
```

اگر بعضی پکیج‌ها خطا دادند، فعلاً فقط این‌ها را نصب کن:

```bash
python -m pip install django pillow python-decouple whitenoise
```

## 2) استفاده از تنظیمات مخصوص اندروید
این دستورها را با این متغیر محیطی اجرا کن:

### بررسی نسخه جنگو
```bash
python -c "import django; print(django.get_version())"
```

### check
```bash
DJANGO_SETTINGS_MODULE=newmoonhome.config.settings.android python newmoonhome/manage.py check
```

اگر محیطت از این نوع export پشتیبانی نمی‌کند، داخل خود `manage.py` موقتاً این خط را تغییر بده:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newmoonhome.config.settings.android')
```

## 3) ساخت migration
```bash
DJANGO_SETTINGS_MODULE=newmoonhome.config.settings.android python newmoonhome/manage.py makemigrations
```

## 4) migrate
```bash
DJANGO_SETTINGS_MODULE=newmoonhome.config.settings.android python newmoonhome/manage.py migrate
```

## 5) ساخت superuser
```bash
DJANGO_SETTINGS_MODULE=newmoonhome.config.settings.android python newmoonhome/manage.py createsuperuser
```

## 6) اجرای سرور
```bash
DJANGO_SETTINGS_MODULE=newmoonhome.config.settings.android python newmoonhome/manage.py runserver 0.0.0.0:8000
```

## 7) اگر export کار نکرد
در `newmoonhome/manage.py` این خط را موقتاً بگذار:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newmoonhome.config.settings.android')
```

## 8) اگر خطا گرفتی
فقط متن کامل خطا را بفرست تا مرحله بعدی دقیق اصلاح شود.
