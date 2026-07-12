from decimal import Decimal
from django.views.generic import TemplateView
from cart.models import Cart


class CartDetailView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user, is_active=True).prefetch_related('items__product').first()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart = Cart.objects.filter(session_key=session_key, is_active=True).prefetch_related('items__product').first()
        
        items = cart.items.all() if cart else []
        subtotal = cart.total_amount if cart else Decimal('0')
        context.update({
            'cart': cart,
            'items': items,
            'subtotal_amount': subtotal,
            'total_amount': subtotal,
        })
        return context
