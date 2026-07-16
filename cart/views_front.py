from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from cart.models import Cart, CartItem
from products.models import Product


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


class CartAddView(View):
    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key, is_active=True)

        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            return JsonResponse({
                'status': 'ok',
                'cart_items_count': cart.items.count(),
                'total_amount': str(cart.total_amount),
                'product_name': product.name,
                'message': f'«{product.name}» به سبد خرید اضافه شد.'
            })
        return redirect('cart:detail')
