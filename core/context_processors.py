from core.models import SiteSetting
from cart.models import Cart


def site_settings(request):
    return {
        'site_settings': SiteSetting.objects.order_by('-created_at').first()
    }


def cart_summary(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key, is_active=True).first()

    items_count = cart.items.count() if cart else 0
    total_amount = cart.total_amount if cart else 0
    return {
        'header_cart_count': items_count,
        'header_cart_total': total_amount,
    }
