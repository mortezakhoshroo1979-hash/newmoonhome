from django.urls import path
from . import manager_views as v

app_name = "manager"

urlpatterns = [
    path("login/",       v.manager_login,       name="login"),
    path("logout/",      v.manager_logout,      name="logout"),
    path("",             v.product_list,        name="dashboard"),
    path("create/",      v.product_create,      name="create"),
    path("edit/<int:pk>/", v.product_edit,      name="edit"),
    path("delete/<int:pk>/", v.product_delete,  name="delete"),
    path("settings/",    v.site_settings_edit,  name="site_settings"),
    path("custom-orders/", v.custom_order_list, name="custom_order_list"),
    path("order/<int:pk>/", v.order_detail,     name="order_detail"),
]