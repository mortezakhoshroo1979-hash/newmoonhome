# نصب پنل مدیریت NEWMOON HOME

این پکیج شامل فایل‌های پنل مدیریت (`/manage/`) برای اپ `store` هست.
همه URLها با query string کار می‌کنن (مثلاً `/manage/edit/?id=5`) تا از باگ Pydroid با `<int:pk>` دور بمونیم.

## ۱) فایل‌ها رو در این مسیرها کپی کن

```
newmoon_app/
├── config/
│   └── urls.py                          ← فقط یک خط اضافه کن (پایین)
└── store/
    ├── manager_urls.py                  ← کپی از store/manager_urls.py
    ├── manager_views.py                 ← کپی از store/manager_views.py
    ├── manager_forms.py                 ← کپی از store/manager_forms.py
    ├── templatetags/
    │   ├── __init__.py                  ← کپی (فایل خالی)
    │   └── manager_extras.py            ← کپی
    └── templates/store/manager/
        ├── base.html
        ├── login.html
        ├── list.html
        ├── form.html
        ├── confirm_delete.html
        └── bulk_price.html
```

## ۲) به `config/urls.py` این خط رو اضافه کن

**مستقیم در config/urls.py** (نه در store/urls.py — چون include در آن مسیر روی Pydroid شکننده‌ست):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("manage/", include("store.manager_urls")),   # ← این خط
    path("", include("store.urls")),
]
```

ترتیب مهمه: `manage/` قبل از include ریشه‌ی store باشه.

## ۳) settings.py — مطمئن شو این‌ها هست

```python
LOGIN_URL = "/manage/login/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

و در `config/urls.py` انتهای فایل (فقط در حالت DEBUG):

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## ۴) مطمئن شو Pillow نصبه (برای ImageField)

```
pip install Pillow
```

## ۵) migrations

اگه مدل Product فیلد `old_price` نداره، اضافه‌ش کن و:
```
python manage.py makemigrations store
python manage.py migrate
```

## ۶) کاربر staff بساز

```
python manage.py createsuperuser
```

## ۷) تست

```
python manage.py runserver
```

برو به: `http://127.0.0.1:8000/manage/`

---

## مدل فرض‌شده

فرم‌ها با این فیلدها کار می‌کنن. اگه اسمشون فرق داره، `store/manager_forms.py` رو ادیت کن:

```python
class Product(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=220, unique=True, allow_unicode=True)
    price       = models.PositiveBigIntegerField(default=0)
    old_price   = models.PositiveBigIntegerField(null=True, blank=True)
    image       = models.ImageField(upload_to="products/", blank=True, null=True)
    stock       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
```

## قابلیت‌ها

- ✅ لیست محصولات با جستجو، صفحه‌بندی، چک‌باکس گروهی
- ✅ ساخت / ویرایش / حذف (تک و گروهی)
- ✅ آپلود عکس
- ✅ عملیات قیمت گروهی:
  - `inc_percent` / `dec_percent`
  - `inc_amount` / `dec_amount`
  - `set_exact`
  - `round_base` با mode: nearest / up / down
  - `move_to_old` (کپی price → old_price قبل از تغییر)
  - `reset_old` (خالی کردن old_price)
- ✅ پارس ارقام فارسی/عربی و کاما (`۱٬۲۵۰٬۰۰۰` → `1250000`)
- ✅ نمایش قیمت با جداکننده هزارگان
- ✅ فقط staff/superuser
- ✅ RTL کامل با Bootstrap 5 RTL
