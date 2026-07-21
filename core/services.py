import logging
from decouple import config

logger = logging.getLogger(__name__)


class SMSService:
    """سرویس پیامکی یکپارچه با پشتیبانی از کاوه‌نگار، ملی پیامک و قاصدک."""

    def __init__(self):
        self.provider = config('SMS_PROVIDER', default='console').lower()
        self.api_key = config('SMS_API_KEY', default='test_key')
        self.sender_number = config('SMS_SENDER_NUMBER', default='10008445')

    def send_pattern(self, phone, template_name, tokens=None):
        """ارسال پیامک پترن (کد تایید یا اطلاع‌رسانی وضعیت)."""
        tokens = tokens or {}
        if not phone:
            return False

        if self.provider == 'console':
            print(f"\n[📱 SMS CONSOLE ({template_name}) -> {phone}] Tokens: {tokens}\n")
            logger.info(f"SMS pattern sent to {phone} via console: {template_name} ({tokens})")
            return True

        elif self.provider == 'kavenegar':
            try:
                import requests
                url = f"https://api.kavenegar.com/v1/{self.api_key}/verify/lookup.json"
                params = {
                    'receptor': phone,
                    'template': template_name,
                    'token': tokens.get('token', ''),
                    'token2': tokens.get('token2', ''),
                    'token3': tokens.get('token3', ''),
                }
                requests.get(url, params=params, timeout=5)
                return True
            except Exception as e:
                logger.error(f"Kavenegar SMS error: {e}")
                return False

        elif self.provider == 'melipayamak':
            try:
                import requests
                url = "https://console.melipayamak.com/api/send/shared/28038cbb"
                data = {'bodyId': int(template_name) if template_name.isdigit() else 100, 'to': phone, 'args': list(tokens.values())}
                requests.post(url, json=data, timeout=5)
                return True
            except Exception as e:
                logger.error(f"MeliPayamak SMS error: {e}")
                return False

        return False

    def send_otp(self, phone, code):
        """ارسال کد تایید ۶ رقمی OTP در لحظه ورود/ثبت‌نام."""
        return self.send_pattern(phone, 'NMH_OTP_VERIFY', {'token': code})

    def send_order_status_update(self, phone, order_number, status_text):
        """ارسال خودکار پیامک وضعیت سفارش (تایید، ساخت، ارسال)."""
        return self.send_pattern(phone, 'NMH_ORDER_STATUS', {'token': order_number, 'token2': status_text})

    def send_custom_order_received(self, phone, request_number):
        """ارسال پیامک دریافت درخواست ساخت سفارشی."""
        return self.send_pattern(phone, 'NMH_BESPOKE_REQ', {'token': request_number})

    def send_custom_order_quoted(self, phone, request_number, price_text):
        """ارسال پیامک اعلام برآورد قیمت به مشتری."""
        return self.send_pattern(phone, 'NMH_BESPOKE_QUOTE', {'token': request_number, 'token2': price_text})
