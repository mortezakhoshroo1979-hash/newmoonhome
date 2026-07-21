from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductSitemap, StaticViewSitemap

try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    spectacular_urls = [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
except ImportError:
    spectacular_urls = []

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('secure-panel/', include('custom_admin.urls')),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    path('api/', include('core.api.urls')),
    path('api/v1/', include('newmoonhome.config.api.v1.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + spectacular_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'frontend' / 'dist' / 'assets' if (settings.BASE_DIR / 'frontend' / 'dist' / 'assets').exists() else settings.BASE_DIR / 'frontend' / 'assets' if (settings.BASE_DIR / 'frontend' / 'assets').exists() else settings.BASE_DIR / 'static' / 'assets'}),
        re_path(r'^src/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'frontend' / 'src'}),
        re_path(r'^public/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'frontend' / 'public'}),
    ]

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        try:
            import debug_toolbar
            urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
        except ImportError:
            pass
