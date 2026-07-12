from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from blog.models import Comment, Post
from core.mixins import SeoContextMixin
from core.models import Banner, ContactMessage, Slider
from orders.models import Order
from products.models import Product


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class HomeView(SeoContextMixin, TemplateView):
    template_name = 'home.html'
    seo_title = 'NEWMOON HOME | فروشگاه لوکس مبلمان و محصولات چوبی'
    seo_description = 'فروشگاه آنلاین مبلمان، سرویس خواب، میز و محصولات چوبی با طراحی لوکس و امکان شخصی‌سازی.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:8]
        context['latest_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
        context['best_sellers'] = Product.objects.filter(is_active=True).order_by('-sales_count')[:6]
        return context


class AboutView(SeoContextMixin, TemplateView):
    template_name = 'about.html'
    seo_title = 'درباره ما | NEWMOON HOME'
    seo_description = 'آشنایی با برند NEWMOON HOME، فلسفه طراحی، کیفیت متریال و داستان شکل‌گیری مجموعه.'


class ContactView(SeoContextMixin, TemplateView):
    template_name = 'contact.html'
    seo_title = 'تماس با ما | NEWMOON HOME'
    seo_description = 'راه‌های ارتباطی با NEWMOON HOME برای مشاوره خرید، سفارش ویژه و همکاری.'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip() or 'پیام از فرم تماس با ما'
        message = request.POST.get('message', '').strip()

        if not name or not message or (not email and not phone):
            messages.error(request, 'لطفاً نام، متن پیام و حداقل یکی از موارد ایمیل یا شماره تماس را وارد کنید.')
            return self.get(request, *args, **kwargs)

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )
        messages.success(request, 'پیام شما با موفقیت ارسال شد و در اسرع وقت بررسی خواهد شد.')
        return redirect('core:contact')


class AdminHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = Product.objects.count()
        context['orders_count'] = Order.objects.count()
        context['posts_count'] = Post.objects.count()
        context['messages_count'] = ContactMessage.objects.count()
        context['recent_orders'] = Order.objects.order_by('-created_at')[:10]
        return context


class ContentDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'admin/content/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all().order_by('sort_order')
        context['banners'] = Banner.objects.all().order_by('sort_order')
        context['comments'] = Comment.objects.order_by('-created_at')[:10]
        return context
