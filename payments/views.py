from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from orders.models import Order
from .models import PaymentGateway, Transaction
from .services.callbacks import PaymentCallbackService
from .services.gateways import GATEWAY_SERVICES
from .tasks import verify_payment_async


class PaymentStartView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        gateway = PaymentGateway.objects.filter(is_active=True).order_by('priority').first()
        if not gateway:
            messages.error(request, 'هیچ درگاه فعالی یافت نشد.')
            return redirect('orders:checkout')

        service = GATEWAY_SERVICES.get(gateway.slug)
        callback_url = request.build_absolute_uri(reverse('payments:callback', kwargs={'gateway_slug': gateway.slug}))
        result = service.start_payment(order, callback_url)
        transaction = Transaction.objects.create(
            order=order,
            gateway=gateway,
            user=order.user,
            amount=order.total_amount,
            authority=result.authority,
            raw_response=result.raw_response or {},
        )
        return redirect(result.redirect_url)


class PaymentCallbackView(View):
    def get(self, request, gateway_slug):
        authority = request.GET.get('Authority') or request.GET.get('RefId') or ''
        transaction = get_object_or_404(Transaction, authority=authority)
        status_flag = request.GET.get('Status', 'OK')
        payload = dict(request.GET.items())

        if status_flag in ['OK', '0', 'success', 'Success']:
            PaymentCallbackService.mark_success(transaction, payload)
            verify_payment_async.delay(str(transaction.id), payload)
            messages.success(request, 'پرداخت شما با موفقیت ثبت شد.')
        else:
            PaymentCallbackService.mark_failed(transaction, payload)
            messages.error(request, 'پرداخت ناموفق بود یا توسط کاربر لغو شد.')
        return redirect('accounts:profile')
