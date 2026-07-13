from django.urls import path

from accounts.views import UserEmailBulkView, UserInsightsView, UserListAdminView
from core.views import AdminHomeView, ContentDashboardView
from discounts.views import DiscountsDashboardView
from orders.views import (
    InvoicePrintView,
    OrderListAdminView,
    OrderStatusBulkUpdateView,
    OrdersDashboardView,
    ShippingLabelPrintView,
)
from products.views import BulkPriceUpdatePreviewView, ProductListAdminView

app_name = "custom_admin"

urlpatterns = [
    path("", AdminHomeView.as_view(), name="dashboard"),
    path("products/", ProductListAdminView.as_view(), name="product_list"),
    path("products/bulk-price-update/", BulkPriceUpdatePreviewView.as_view(), name="bulk_price_update"),
    path("orders/", OrderListAdminView.as_view(), name="order_list"),
    path("orders/dashboard/", OrdersDashboardView.as_view(), name="orders_dashboard"),
    path("orders/bulk-status-update/", OrderStatusBulkUpdateView.as_view(), name="bulk_status_update"),
    path("orders/<uuid:pk>/invoice/", InvoicePrintView.as_view(), name="invoice_print"),
    path("orders/<uuid:pk>/shipping-label/", ShippingLabelPrintView.as_view(), name="shipping_label_print"),
    path("users/", UserListAdminView.as_view(), name="user_list"),
    path("users/bulk-email/", UserEmailBulkView.as_view(), name="bulk_email"),
    path("users/<uuid:pk>/insights/", UserInsightsView.as_view(), name="user_insights"),
    path("discounts/", DiscountsDashboardView.as_view(), name="discounts_dashboard"),
    path("content/", ContentDashboardView.as_view(), name="content_dashboard"),
]
