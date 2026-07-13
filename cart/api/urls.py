from django.urls import path
from .views import CartDetailAPIView

urlpatterns = [
    path('', CartDetailAPIView.as_view(), name='api_cart_detail'),
]
