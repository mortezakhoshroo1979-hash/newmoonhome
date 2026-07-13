from django.views.generic import TemplateView

from core.mixins import SeoContextMixin
from products.models import Product


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
