from django.db import transaction

from accounts.services import LoyaltyService, ReferralService
from orders.models import OrderStatusHistory
from orders.tasks import notify_admin_new_order, send_order_confirmation


class OrderWorkflowService:
    """سرویس یکپارچه‌سازی جریان سفارش."""

    @staticmethod
    @transaction.atomic
    def on_order_created(order):
        customer_email = order.user.email if order.user and order.user.email else ''
        send_order_confirmation.delay(customer_email, order.order_number)
        notify_admin_new_order.delay(order.order_number)

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
