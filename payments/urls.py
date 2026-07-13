from django.urls import path
from .views import PaymentStartView, PaymentCallbackView

app_name = 'payments'

urlpatterns = [
    path('start/<uuid:order_id>/', PaymentStartView.as_view(), name='start'),
    path('callback/<slug:gateway_slug>/', PaymentCallbackView.as_view(), name='callback'),
]
