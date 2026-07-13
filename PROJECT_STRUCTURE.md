# ساختار نهایی پروژه NEWMOON HOME

## اپ‌های اصلی
- `accounts/`
- `products/`
- `cart/`
- `orders/`
- `payments/`
- `shipping/`
- `discounts/`
- `blog/`
- `core/`
- `wishlist/`
- `custom_admin/`

## هسته پروژه
- `newmoonhome/manage.py`
- `newmoonhome/config/settings/base.py`
- `newmoonhome/config/settings/development.py`
- `newmoonhome/config/settings/production.py`
- `newmoonhome/config/urls.py`
- `newmoonhome/config/celery.py`

## فایل‌های طراحی
- `templates/`
- `static/css/main.css`
- `static/js/main.js`
- `static/assets/logo.png`

## فایل‌های زیرساخت
- `requirements.txt`
- `.env.example`
- `docker-compose.yml`
- `README_DEPLOY.md`
- `scripts/backup_db.sh`

## یادداشت
- `legacy_models_backup.py` فقط نسخه آرشیوی فایل مدل قدیمی است و نباید در پروژه production import شود.
