from django.core.cache import cache
from django.http import HttpResponse


class HttpResponseTooManyRequests(HttpResponse):
    status_code = 429


class SimpleRateLimitMiddleware:
    """محدودکننده ساده درخواست برای مسیرهای حساس."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        sensitive_prefixes = ['/accounts/login/', '/accounts/register/', '/payments/']
        if any(request.path.startswith(prefix) for prefix in sensitive_prefixes):
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            key = f'rate-limit:{ip}:{request.path}'
            count = cache.get(key, 0)
            if count >= 40:
                return HttpResponseTooManyRequests('تعداد درخواست بیش از حد مجاز است.')
            cache.set(key, count + 1, 60)
        return self.get_response(request)
