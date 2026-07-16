from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from cart.models import Cart
from orders.models import CustomOrderRequest
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


class CustomOrderRequestView(TemplateView):
    template_name = 'custom_order_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wood_choices'] = CustomOrderRequest.WOOD_CHOICES
        context['finish_choices'] = CustomOrderRequest.FINISH_CHOICES
        context['fabric_choices'] = CustomOrderRequest.FABRIC_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        receiver_name = request.POST.get('receiver_name', '').strip()
        receiver_phone = request.POST.get('receiver_phone', '').strip()
        length_cm = request.POST.get('length_cm', '').strip()
        width_cm = request.POST.get('width_cm', '').strip()
        height_cm = request.POST.get('height_cm', '').strip()
        wood_type = request.POST.get('wood_type', 'raash').strip()
        finish_type = request.POST.get('finish_type', 'polyurethane').strip()
        fabric_type = request.POST.get('fabric_type', 'velvet').strip()
        fabric_color_code = request.POST.get('fabric_color_code', '').strip()
        customer_notes = request.POST.get('customer_notes', '').strip()
        inspiration_image = request.FILES.get('inspiration_image')

        if not receiver_name or not receiver_phone:
            messages.error(request, 'لطفاً نام سفارش‌دهنده و شماره تماس را وارد فرمایید.')
            return redirect('orders:custom_request')

        user = request.user if request.user.is_authenticated else None
        custom_order = CustomOrderRequest.objects.create(
            user=user,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            length_cm=int(length_cm) if length_cm.isdigit() else None,
            width_cm=int(width_cm) if width_cm.isdigit() else None,
            height_cm=int(height_cm) if height_cm.isdigit() else None,
            wood_type=wood_type,
            finish_type=finish_type,
            fabric_type=fabric_type,
            fabric_color_code=fabric_color_code,
            customer_notes=customer_notes,
            inspiration_image=inspiration_image,
            status=CustomOrderRequest.STATUS_PENDING_REVIEW,
        )

        try:
            from core.services import SMSService
            SMS_client = SMSService()
            SMS_client.send_custom_order_received(receiver_phone, custom_order.request_number)
        except Exception:
            pass

        messages.success(
            request,
            f'درخواست ساخت سفارشی شما با شماره {custom_order.request_number} با موفقیت ثبت شد و جهت برآورد قیمت توسط تیم مهندسی بررسی خواهد شد.'
        )
        if user:
            return redirect('accounts:profile')
        return redirect('orders:custom_request')
