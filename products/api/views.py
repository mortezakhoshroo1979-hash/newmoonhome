from rest_framework import generics
from products.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
    serializer_class = ProductSerializer
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['created_at', 'sales_count', 'base_price', 'views_count']
    filterset_fields = ['category__slug', 'brand__slug', 'is_featured']


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
