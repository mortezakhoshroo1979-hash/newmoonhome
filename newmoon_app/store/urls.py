from django.urls import path, re_path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    re_path(r"^product/(?P<slug>[^/]+)/$", views.product_detail, name="product_detail"),
    
    # آدرس‌های سبد خرید و تسویه
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    
    # آدرس سفارش اختصاصی
    path("custom-order/", views.custom_order_request, name="custom_order"),
]