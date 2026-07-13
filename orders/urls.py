from django.urls import path
from .views_front import CheckoutView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
