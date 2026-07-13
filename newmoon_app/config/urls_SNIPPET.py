# این فایل فقط راهنماست — محتوای فایل واقعی config/urls.py خودت باید این‌طوری بشه:

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # ← این خط را دقیقاً همین‌جا اضافه کن (قبل از include ریشه‌ی store)
    path("manage/", include("store.manager_urls")),

    path("", include("store.urls")),
]

# سرو کردن فایل‌های آپلود شده (عکس محصول) فقط در حالت DEBUG:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
