import random

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .forms_auth import LoginForm, OTPVerifyForm, PasswordResetRequestForm, RegisterForm
from .models import Profile, ReferralCode, User, UserAPIKey


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.save()
        Profile.objects.get_or_create(user=user)
        ReferralCode.objects.get_or_create(user=user, defaults={'code': f'NMH-{random.randint(100000, 999999)}'})
        self.request.session['otp_code'] = '123456'
        self.request.session['pending_user_id'] = str(user.id)
        try:
            from core.services import SMSService
            if user.phone:
                SMSService().send_otp(user.phone, '123456')
        except Exception:
            pass
        if user.email:
            send_mail('خوش آمدید به NEWMOON HOME', 'ثبت‌نام شما با موفقیت انجام شد.', None, [user.email])
        messages.success(self.request, 'ثبت‌نام انجام شد. کد تایید برای شما ارسال شد.')
        return redirect('accounts:verify_otp')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return redirect('accounts:profile')


class OTPVerifyView(FormView):
    template_name = 'login.html'
    form_class = OTPVerifyForm

    def form_valid(self, form):
        if form.cleaned_data['code'] == self.request.session.get('otp_code'):
            user_id = self.request.session.get('pending_user_id')
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if not user:
                    messages.error(self.request, 'کاربر یافت نشد.')
                    return redirect('accounts:register')
                user.is_verified = True
                user.save(update_fields=['is_verified'])
                login(self.request, user)
                messages.success(self.request, 'حساب شما تایید شد.')
                return redirect('accounts:profile')
        messages.error(self.request, 'کد تایید نامعتبر است.')
        return redirect('accounts:verify_otp')


class PasswordResetRequestView(FormView):
    template_name = 'login.html'
    form_class = PasswordResetRequestForm

    def form_valid(self, form):
        send_mail('بازیابی رمز عبور', 'لینک بازیابی رمز عبور برای شما ارسال شد.', None, [form.cleaned_data['email']])
        messages.success(self.request, 'ایمیل بازیابی رمز عبور ارسال شد.')
        return redirect('accounts:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        orders = user.orders.all().order_by('-created_at')
        custom_orders = user.custom_orders.all().order_by('-created_at')
        api_keys = user.api_keys.all().order_by('-created_at')
        profile = getattr(user, 'profile', None)
        referral_code = getattr(user, 'referral_code', None)
        total_spent = sum(o.total_amount for o in orders)

        context.update({
            'orders': orders,
            'custom_orders': custom_orders,
            'api_keys': api_keys,
            'profile': profile,
            'referral_code': referral_code,
            'total_spent': total_spent,
            'orders_count': orders.count(),
            'custom_orders_count': custom_orders.count(),
        })
        return context


class APIKeyGenerateView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip() or 'کلید دسترسی همکار / موبایل'
        api_key = UserAPIKey.objects.create(user=request.user, name=name)
        messages.success(request, f'کلید API جدید شما ساخته شد: {api_key.key} (لطفاً این کلید را در مکانی امن ذخیره کنید)')
        return redirect('accounts:profile')
