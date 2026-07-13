from django.urls import path
from .views_front import CartDetailView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='detail'),
]
