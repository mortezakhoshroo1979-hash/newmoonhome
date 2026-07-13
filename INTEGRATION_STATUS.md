# وضعیت یکپارچه‌سازی پروژه NEWMOON HOME

## انجام‌شده در این مرحله

- ایجاد `AppConfig` برای اپ‌ها
- ساخت `signals.py` برای ایجاد خودکار Profile و ReferralCode
- ساخت سرویس‌های:
  - `accounts/services.py`
  - `orders/services.py`
  - `payments/services/callbacks.py`
- افزودن `context_processors` برای:
  - تنظیمات سایت
  - خلاصه سبد خرید در هدر
- افزودن `SeoContextMixin`
- افزودن `SimpleRateLimitMiddleware`
- ساخت `models.py` در اپ‌ها به‌صورت wrapper روی فایل مرکزی برای جلوگیری از خطای import
- افزودن sitemap واقعی به `config/urls.py`
- داینامیک کردن title/description پایه
- اتصال هدر به تعداد و مبلغ سبد خرید
- تکمیل callback پرداخت با success/failed flow

## نکات مهم

در وضعیت فعلی، پروژه از نظر ساختاری بسیار نزدیک به اجرای واقعی است؛ اما برای یک محصول production-grade هنوز بهتر است این موارد در گام بعد نهایی شوند:

1. انتقال مدل‌ها از `models.py` مرکزی به فایل مستقل هر اپ
2. ایجاد migrationهای واقعی برای هر اپ
3. تکمیل OTP واقعی با مدل ذخیره کد و سرویس پیامک
4. تکمیل فرم‌ها و POST workflow سبد خرید / checkout
5. اتصال نهایی تمپلیت‌ها به داده‌های واقعی در همه صفحات
6. تست end-to-end برای پرداخت، سفارش و API
7. افزودن اعلان موجودی و ورود گوگل

## دستورهای پایه اجرا

```bash
cp .env.example .env
pip install -r requirements.txt
docker-compose up -d
python newmoonhome/manage.py makemigrations
python newmoonhome/manage.py migrate
python newmoonhome/manage.py runserver
```
