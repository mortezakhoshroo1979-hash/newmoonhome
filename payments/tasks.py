try:
    from celery import shared_task
except ImportError:
    def shared_task(func=None, *args, **kwargs):
        if func:
            func.delay = func
            return func
        def decorator(inner_func):
            inner_func.delay = inner_func
            return inner_func
        return decorator

from payments.models import Transaction


@shared_task
def verify_payment_async(transaction_id, payload=None):
    transaction = Transaction.objects.select_related('order', 'gateway').get(id=transaction_id)
    transaction.raw_response = payload or {}
    transaction.save(update_fields=['raw_response', 'updated_at'])
    return transaction.status
