from decimal import Decimal
from django.db import transaction

from accounts.services import LoyaltyService, ReferralService
from cart.models import Cart
from orders.models import Order, OrderItem, OrderStatusHistory
from orders.tasks import notify_admin_new_order, send_order_confirmation


class OrderWorkflowService:
    """سرویس یکپارچه‌سازی جریان سفارش."""

    @staticmethod
    @transaction.atomic
    def build_order_from_cart(user, address_data):
        """ساخت سفارش از روی سبد خرید فعال کاربر."""
        if not user or not user.is_authenticated:
            return None

        cart = Cart.objects.filter(user=user, is_active=True).first()
        if not cart or not cart.items.exists():
            return None

        order = Order.objects.create(
            user=user,
            receiver_name=address_data.get('receiver_name', '').strip(),
            receiver_phone=address_data.get('receiver_phone', '').strip(),
            province=address_data.get('province', '').strip(),
            city=address_data.get('city', '').strip(),
            address=address_data.get('address', '').strip(),
            postal_code=address_data.get('postal_code', '').strip(),
            shipping_amount=Decimal('0'),
            status=Order.STATUS_REGISTERED,
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                selected_options=cart_item.selected_options,
                unit_price_snapshot=cart_item.unit_price,
            )

        order.recalculate_totals()

        cart.is_active = False
        cart.save(update_fields=['is_active', 'updated_at'])

        OrderWorkflowService.on_order_created(order)
        return order

    @staticmethod
    @transaction.atomic
    def on_order_created(order):
        customer_email = order.user.email if order.user and order.user.email else ''
        try:
            send_order_confirmation.delay(customer_email, order.order_number)
            notify_admin_new_order.delay(order.order_number)
        except Exception:
            try:
                send_order_confirmation(customer_email, order.order_number)
                notify_admin_new_order(order.order_number)
            except Exception:
                pass

    @staticmethod
    @transaction.atomic
    def change_status(order, to_status, changed_by=None, note=''):
        old_status = order.status
        if old_status == to_status:
            return order

        order.status = to_status
        order.save(update_fields=['status', 'updated_at'])
        OrderStatusHistory.objects.create(
            order=order,
            from_status=old_status,
            to_status=to_status,
            changed_by=changed_by,
            note=note,
        )

        if to_status == 'delivered':
            LoyaltyService.assign_points_for_order(order)
        return order

    @staticmethod
    def apply_referral(order, referral_code_value=None):
        return ReferralService.apply_referral_after_first_order(order, referral_code_value)
