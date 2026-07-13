#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PATCH v6 - NEWMOON HOME
این اسکریپت فایل‌های urls را به‌صورت خودکار و سالم بازنویسی می‌کند
تا مشکل خراب شدن < > در ادیتور Pydroid دور زده شود.
محل اجرا: کنار START.py داخل پوشه newmoon_app
"""
import os
from pathlib import Path

BASE = Path(__file__).parent
print("BASE:", BASE)

# 1) config/urls.py
config_urls = r'''from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# وارد کردن ویوهای پنل مدیریت برای مسیر مستقیم
from store import manager_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # پنل مدیریت - مسیر مستقیم
    path("manage/", manager_views.manager_dashboard, name="manager_dashboard"),
    path("manage/products/", manager_views.manager_product_list, name="manager_product_list"),
    path("manage/products/new/", manager_views.manager_product_create, name="manager_product_create"),
    re_path(r"^manage/products/(?P<pk>\d+)/edit/$", manager_views.manager_product_edit, name="manager_product_edit"),
    re_path(r"^manage/products/(?P<pk>\d+)/delete/$", manager_views.manager_product_delete, name="manager_product_delete"),
    path("manage/products/bulk-action/", manager_views.manager_bulk_action, name="manager_bulk_action"),
    path("manage/products/bulk-price/", manager_views.manager_bulk_price, name="manager_bulk_price"),

    # سایت اصلی
    path("", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
p = BASE / "config" / "urls.py"
p.write_text(config_urls, encoding="utf-8")
print("✓ config/urls.py written", p)

# 2) store/urls.py - تمیز، بدون manage
store_urls = r'''from django.urls import path, re_path
from . import views
from . import diag

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("diag/", diag.diag, name="diag"),
    path("products/", views.product_list, name="product_list"),
    re_path(r"^product/(?P<slug>[^/]+)/$", views.product_detail, name="product_detail"),
    path("test-xyz-123/", views.home, name="test_xyz"),
]
'''
p2 = BASE / "store" / "urls.py"
p2.write_text(store_urls, encoding="utf-8")
print("✓ store/urls.py written", p2)

# 3) پاک کردن __pycache__
import shutil
for d in [BASE/"store"/"__pycache__", BASE/"config"/"__pycache__"]:
    if d.exists():
        shutil.rmtree(d)
        print("× cleared", d)

print("\n✅ PATCH تمام شد!")
print("حالا START.py را اجرا کن")
print("بعد تست کن: /diag/  سپس  /manage/")
