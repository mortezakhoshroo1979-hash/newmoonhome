from django.urls import path
from .views import CategoryListAPIView, ProductDetailAPIView, ProductListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='api_categories'),
    path('', ProductListAPIView.as_view(), name='api_products'),
    path('<slug:slug>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
]
