from celery import shared_task

from payments.models import Transaction


@shared_task
def verify_payment_async(transaction_id, payload=None):
    transaction = Transaction.objects.select_related('order', 'gateway').get(id=transaction_id)
    transaction.raw_response = payload or {}
    transaction.save(update_fields=['raw_response', 'updated_at'])
    return transaction.status
