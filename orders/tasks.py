from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation(customer_email, order_number):
    if customer_email:
        send_mail(
            'تایید سفارش',
            f'سفارش {order_number} با موفقیت ثبت شد.',
            None,
            [customer_email],
        )


@shared_task
def notify_admin_new_order(order_number):
    send_mail(
        'سفارش جدید',
        f'سفارش جدید با شماره {order_number} ثبت شد.',
        None,
        ['admin@newmoonhome.ir'],
    )
