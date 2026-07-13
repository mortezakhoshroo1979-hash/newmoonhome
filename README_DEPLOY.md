# راهنمای اجرا و دیپلوی پروژه NEWMOON HOME

## 1) نصب وابستگی‌ها

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) آماده‌سازی محیط

```bash
cp .env.example .env
```

## 3) اجرای سرویس‌های مورد نیاز

```bash
docker-compose up -d
```

## 4) مایگریشن و ساخت سوپریوزر

```bash
python newmoonhome/manage.py makemigrations
python newmoonhome/manage.py migrate
python newmoonhome/manage.py createsuperuser
```

## 5) اجرای پروژه

```bash
python newmoonhome/manage.py runserver
```

## 6) اجرای Celery

```bash
celery -A newmoonhome worker -l info
```

## 7) جمع‌آوری فایل‌های استاتیک

```bash
python newmoonhome/manage.py collectstatic --noinput
```

## 8) دیپلوی با Gunicorn

```bash
gunicorn newmoonhome.config.wsgi:application --bind 0.0.0.0:8000
```

## 9) Nginx

- ترافیک را به Gunicorn پراکسی کنید.
- مسیر `/static/` را به `staticfiles` و `/media/` را به `media` متصل کنید.
- SSL را با Let's Encrypt فعال کنید.

## 10) نکات امنیتی

- در production از `production.py` استفاده کنید.
- مقادیر `.env` واقعی و امن قرار دهید.
- `DEBUG=False` باشد.
- `ALLOWED_HOSTS` را محدود کنید.

## 11) تست

```bash
python newmoonhome/manage.py test tests
```
