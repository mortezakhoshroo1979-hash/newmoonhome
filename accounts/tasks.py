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
