from .models import SiteSetting
from .cart import Cart

def site_settings(request):
    try:
        # لود کردن امن تنظیمات
        site = SiteSetting.load()
    except Exception:
        site = None
        
    return {
        "site": site,
        "cart": Cart(request)
    }