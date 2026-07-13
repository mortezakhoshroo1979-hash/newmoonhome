from django.db import transaction

from orders.services import OrderWorkflowService
from payments.models import Transaction


class PaymentCallbackService:
    """سرویس مدیریت callback و تایید تراکنش."""

    @staticmethod
    @transaction.atomic
    def mark_success(transaction: Transaction, raw_response=None):
        transaction.status = Transaction.STATUS_SUCCESS
        transaction.raw_response = raw_response or {}
        transaction.save(update_fields=['status', 'raw_response', 'updated_at'])

        order = transaction.order
        order.paid_at = transaction.created_at
        order.save(update_fields=['paid_at', 'updated_at'])
        OrderWorkflowService.change_status(order, 'confirmed', note='پرداخت موفق')
        return transaction

    @staticmethod
    @transaction.atomic
    def mark_failed(transaction: Transaction, raw_response=None):
        transaction.status = Transaction.STATUS_FAILED
        transaction.raw_response = raw_response or {}
        transaction.save(update_fields=['status', 'raw_response', 'updated_at'])
        return transaction
