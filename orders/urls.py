from django.urls import path
from .views_front import CheckoutView, CustomOrderRequestView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('custom-request/', CustomOrderRequestView.as_view(), name='custom_request'),
]
