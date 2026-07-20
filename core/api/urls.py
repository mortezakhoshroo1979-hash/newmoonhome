from django.urls import path
from .views import Model3DUploadAPIView, SiteConfigAPIView

urlpatterns = [
    path('site-config', SiteConfigAPIView.as_view(), name='lovable_site_config'),
    path('models/upload', Model3DUploadAPIView.as_view(), name='lovable_models_upload'),
]
