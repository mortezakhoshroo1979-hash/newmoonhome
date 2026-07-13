# مراحل بعدی پیشنهادی

## برای اجرای واقعی روی سیستم یا سرور
1. نصب dependencyها:
   ```bash
   pip install -r requirements.txt
   ```
2. کپی env:
   ```bash
   cp .env.example .env
   ```
3. اجرای PostgreSQL و Redis:
   ```bash
   docker-compose up -d
   ```
4. اجرای migration:
   ```bash
   python newmoonhome/manage.py makemigrations
   python newmoonhome/manage.py migrate
   ```
5. اجرای پروژه:
   ```bash
   python newmoonhome/manage.py runserver
   ```

## برای بهبود بیشتر
- ساخت migrationهای نهایی با خود Django
- حذف فایل‌های آرشیوی غیرضروری
- افزودن smoke tests برای auth و payment
- تکمیل flow واقعی cart/checkout
