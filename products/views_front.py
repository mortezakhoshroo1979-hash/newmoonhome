from django.db.models import Q
from django.views.generic import DetailView, ListView

from core.mixins import SeoContextMixin
from .models import Product


class ProductListView(SeoContextMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    seo_title = 'محصولات | NEWMOON HOME'
    seo_description = 'مشاهده لیست کامل محصولات لوکس NEWMOON HOME شامل مبلمان، سرویس خواب، میز و محصولات چوبی.'

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand').filter(is_active=True)
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        ordering = self.request.GET.get('ordering', '-created_at')

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(sku__icontains=q)
            )
        if category:
            queryset = queryset.filter(category__slug=category)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        allowed_ordering = ['-created_at', '-sales_count', 'base_price', '-base_price', '-views_count']
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class ProductDetailView(SeoContextMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_seo_title(self):
        return f'{self.object.name} | NEWMOON HOME'

    def get_seo_description(self):
        return (self.object.description or '')[:160]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['related_products'] = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
        context['recently_viewed'] = Product.objects.filter(is_active=True).exclude(pk=product.pk)[:4]
        return context
