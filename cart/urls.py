from django.urls import path
from .views_front import CartAddView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
    path('add/<uuid:product_id>/', CartAddView.as_view(), name='add'),
]
