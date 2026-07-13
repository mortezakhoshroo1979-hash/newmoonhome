import logging
from dataclasses import dataclass
from urllib.parse import urlencode

from django.conf import settings

logger = logging.getLogger('payments')


@dataclass
class PaymentResult:
    success: bool
    authority: str = ''
    redirect_url: str = ''
    raw_response: dict | None = None
    message: str = ''


class BaseGatewayService:
    slug = ''

    def start_payment(self, order, callback_url):
        raise NotImplementedError

    def verify_payment(self, transaction, data):
        raise NotImplementedError


class ZarinpalGatewayService(BaseGatewayService):
    slug = 'zarinpal'

    def start_payment(self, order, callback_url):
        authority = f'ZP-{order.order_number}'
        base_url = 'https://sandbox.zarinpal.com/pg/StartPay/' if settings.ZARINPAL_SANDBOX else 'https://www.zarinpal.com/pg/StartPay/'
        logger.info('Starting Zarinpal payment for order %s', order.order_number)
        return PaymentResult(
            success=True,
            authority=authority,
            redirect_url=f'{base_url}{authority}',
            raw_response={'authority': authority},
            message='زرین‌پال آماده انتقال است.',
        )

    def verify_payment(self, transaction, data):
        logger.info('Verifying Zarinpal payment for transaction %s', transaction.id)
        return PaymentResult(success=True, authority=transaction.authority, raw_response=data, message='پرداخت تایید شد.')


class MellatGatewayService(BaseGatewayService):
    slug = 'mellat'

    def start_payment(self, order, callback_url):
        ref = f'MELLAT-{order.order_number}'
        params = urlencode({'RefId': ref, 'CallBackUrl': callback_url})
        logger.info('Starting Mellat payment for order %s', order.order_number)
        return PaymentResult(
            success=True,
            authority=ref,
            redirect_url=f'https://bpm.shaparak.ir/pgwchannel/startpay.mellat?{params}',
            raw_response={'RefId': ref},
            message='درگاه ملت آماده انتقال است.',
        )

    def verify_payment(self, transaction, data):
        logger.info('Verifying Mellat payment for transaction %s', transaction.id)
        return PaymentResult(success=True, authority=transaction.authority, raw_response=data, message='تایید اولیه ملت انجام شد.')


GATEWAY_SERVICES = {
    'zarinpal': ZarinpalGatewayService(),
    'mellat': MellatGatewayService(),
}
