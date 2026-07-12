from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.api.urls")),
    path("products/", include("products.api.urls")),
    path("orders/", include("orders.api.urls")),
    path("cart/", include("cart.api.urls")),
]
