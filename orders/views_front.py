from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from cart.models import Cart
from orders.services import OrderWorkflowService


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user, is_active=True).first()
        items = cart.items.all() if cart else []
        subtotal_amount = cart.total_amount if cart else Decimal('0')
        shipping_amount = Decimal('0')
        discount_amount = Decimal('0')
        total_amount = subtotal_amount + shipping_amount - discount_amount

        saved_addresses = []
        try:
            profile = getattr(user, 'profile', None)
            if profile and isinstance(profile.addresses, list):
                saved_addresses = profile.addresses
        except Exception:
            pass

        context.update({
            'cart': cart,
            'items': items,
            'subtotal_amount': subtotal_amount,
            'shipping_amount': shipping_amount,
            'discount_amount': discount_amount,
            'total_amount': total_amount,
            'saved_addresses': saved_addresses,
        })
        return context

    def post(self, request, *args, **kwargs):
        receiver_name = request.POST.get('receiver_name', '').strip()
        receiver_phone = request.POST.get('receiver_phone', '').strip()
        province = request.POST.get('province', '').strip()
        city = request.POST.get('city', '').strip()
        address = request.POST.get('address', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()

        if not all([receiver_name, receiver_phone, province, city, address]):
            messages.error(request, 'لطفاً تمامی فیلدهای ضروری آدرس (نام، تلفن، استان، شهر و نشانی کامل) را وارد کنید.')
            return redirect('orders:checkout')

        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart or not cart.items.exists():
            messages.error(request, 'سبد خرید شما خالی است و امکان ثبت سفارش وجود ندارد.')
            return redirect('orders:checkout')

        address_data = {
            'receiver_name': receiver_name,
            'receiver_phone': receiver_phone,
            'province': province,
            'city': city,
            'address': address,
            'postal_code': postal_code,
        }

        order = OrderWorkflowService.build_order_from_cart(request.user, address_data)
        if not order:
            messages.error(request, 'خطایی در ثبت سفارش رخ داد. لطفاً مجدداً تلاش کنید.')
            return redirect('orders:checkout')

        try:
            profile = getattr(request.user, 'profile', None)
            if profile and isinstance(profile.addresses, list):
                if not any(a.get('address') == address and a.get('city') == city for a in profile.addresses):
                    profile.addresses.append(address_data)
                    profile.save(update_fields=['addresses', 'updated_at'])
        except Exception:
            pass

        messages.success(
            request,
            f'سفارش شما با شماره {order.order_number} با موفقیت ثبت شد. (صفحه‌ی جزئیات سفارش هنوز در سیستم وجود ندارد)'
        )
        return redirect('core:home')
