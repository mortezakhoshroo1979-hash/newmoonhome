"""صفحه‌ی تشخیص خطا — برای عیب‌یابی روی گوشی.

به آدرس /diag/ برو تا ببینی چه چیزی درست است و چه چیزی خطا دارد.
"""
from django.http import HttpResponse
import traceback


def diag(request):
    out = []
    out.append("<html dir='rtl'><head><meta charset='utf-8'>")
    out.append("<style>body{font-family:Tahoma;padding:20px;line-height:2;background:#0a1511;color:#eee}"
               ".ok{color:#7CFC00}.bad{color:#ff6b6b}h2{color:#c9a84c}</style></head><body>")
    out.append("<h2>🌿 تشخیص وضعیت NEWMOON HOME</h2>")

    # نسخه Django
    try:
        import django
        out.append(f"<p>نسخه Django: <b>{django.get_version()}</b></p>")
    except Exception as e:
        out.append(f"<p class='bad'>خطای Django: {e}</p>")

    # دیتابیس و جدول‌ها
    try:
        from django.db import connection
        tables = connection.introspection.table_names()
        store_tables = [t for t in tables if t.startswith("store")]
        out.append(f"<p class='ok'>✔ دیتابیس متصل است. جدول‌های فروشگاه: {store_tables}</p>")
    except Exception as e:
        out.append(f"<p class='bad'>✗ خطای دیتابیس: {e}</p>")

    # محصولات
    try:
        from store.models import Product, SiteSetting
        out.append(f"<p class='ok'>✔ تعداد محصولات: {Product.objects.count()}</p>")
        SiteSetting.load()
        out.append("<p class='ok'>✔ تنظیمات سایت سالم است.</p>")
    except Exception as e:
        out.append(f"<p class='bad'>✗ خطای مدل: {e}</p>")

    # کاربر مدیر
    try:
        from django.contrib.auth import get_user_model
        U = get_user_model()
        admins = U.objects.filter(is_superuser=True).count()
        out.append(f"<p class='ok'>✔ تعداد کاربر مدیر: {admins}</p>")
        if admins == 0:
            out.append("<p class='bad'>⚠️ هیچ کاربر مدیری وجود ندارد!</p>")
    except Exception as e:
        out.append(f"<p class='bad'>✗ خطای کاربر: {e}</p>")

    # تست پنل مدیریت
    out.append("<h2>تست پنل مدیریت /manage/:</h2>")
    try:
        from store import manager_views, manager_urls, forms, utils, decorators
        out.append("<p class='ok'>✔ ماژول‌های manager_views / manager_urls / forms / utils لود شدند.</p>")
        # تست reverse
        from django.urls import reverse, resolve, get_resolver
        for name in ["store:manager_dashboard", "manager_dashboard"]:
            try:
                url = reverse(name)
                out.append(f"<p class='ok'>✔ reverse('{name}') = {url}</p>")
            except Exception as e:
                out.append(f"<p class='bad'>✗ reverse {name} خطا: {e}</p>")
        # تست resolve
        try:
            m = resolve("/manage/")
            out.append(f"<p class='ok'>✔ resolve('/manage/') → {m.view_name} / {m.func.__name__}</p>")
        except Exception as e:
            out.append(f"<p class='bad'>✗ resolve /manage/ خطا: {e}</p>")
        # لیست URLها
        try:
            resolver = get_resolver()
            urls = []
            def walk(patterns, prefix=""):
                from django.urls.resolvers import URLPattern, URLResolver
                for p in patterns:
                    if isinstance(p, URLPattern):
                        urls.append(prefix + str(p.pattern) + " → " + str(p.name))
                    elif isinstance(p, URLResolver):
                        walk(p.url_patterns, prefix + str(p.pattern))
            walk(resolver.url_patterns)
            out.append("<p>URL patterns:</p><pre style='direction:ltr;text-align:left'>" + "\n".join(urls[:40]) + "</pre>")
        except Exception as e:
            out.append(f"<p class='bad'>لیست URL خطا: {e}</p>")
        # تست Client
        from django.test import Client
        c = Client()
        r = c.get("/manage/")
        out.append(f"<p>Client GET /manage/ → {r.status_code} (302 یعنی نیاز به لاگین، طبیعی است)</p>")
    except Exception:
        out.append("<p class='bad'>✗ خطای لود پنل مدیریت:</p>")
        out.append(f"<pre style='color:#ff6b6b;white-space:pre-wrap'>{traceback.format_exc()}</pre>")

    # تست رندر صفحه ادمین
    out.append("<h2>تست بخش ادمین:</h2>")
    try:
        from django.test import Client
        c = Client()
        r = c.get("/admin/login/")
        if r.status_code == 200:
            out.append("<p class='ok'>✔ صفحه ورود ادمین درست کار می‌کند (200).</p>")
        else:
            out.append(f"<p class='bad'>✗ صفحه ادمین کد {r.status_code} داد.</p>")
    except Exception as e:
        out.append("<p class='bad'>✗ خطای رندر ادمین:</p>")
        out.append(f"<pre style='color:#ff6b6b;white-space:pre-wrap'>{traceback.format_exc()}</pre>")

    out.append("<hr><p>اگر همه ✔ سبز است، آدرس <b>/admin/</b> باید کار کند. "
               "اگر چیزی ✗ قرمز است، عکس همین صفحه را برای پشتیبان بفرست.</p>")
    out.append("</body></html>")
    return HttpResponse("\n".join(out))
