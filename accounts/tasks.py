from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_upgrade_congratulations(email, rank_name):
    if email:
        send_mail(
            'ارتقای سطح کاربری',
            f'تبریک! سطح شما به {rank_name} ارتقا یافت.',
            None,
            [email],
        )
