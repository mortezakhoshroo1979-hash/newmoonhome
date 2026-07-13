# چک‌لیست اجرای پروژه

## 1. نصب وابستگی‌ها
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. تنظیم env
```bash
cp .env.example .env
```

## 3. اجرای سرویس‌ها
```bash
docker-compose up -d
```

## 4. بررسی migrationها
```bash
python newmoonhome/manage.py makemigrations
python newmoonhome/manage.py migrate
```

## 5. اجرای پروژه
```bash
python newmoonhome/manage.py runserver
```

## 6. اجرای celery
```bash
celery -A newmoonhome worker -l info
```
