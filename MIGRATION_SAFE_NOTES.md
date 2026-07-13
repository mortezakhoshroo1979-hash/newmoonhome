# Migration-safe status

در این مرحله، مدل‌ها از فایل مرکزی `models.py` به فایل‌های واقعی هر اپ منتقل شدند.

## انجام‌شده
- `common_models.py` برای مدل پایه ساخته شد.
- مدل‌های اپ‌های زیر به فایل مستقل منتقل شدند:
  - accounts
  - products
  - cart
  - orders
  - payments
  - shipping
  - discounts
  - blog
  - core
  - wishlist
- پوشه `migrations` برای همه اپ‌ها ساخته شد.

## نکات
- فایل مرکزی `models.py` هنوز در workspace وجود دارد اما دیگر مرجع اصلی اپ‌ها نیست.
- برای تولید migration واقعی، از همین ساختار جدید استفاده شود.
- اگر خواسته باشی، در مرحله بعد می‌توانم migrationهای اولیه را هم به‌صورت دستی بسازم.
