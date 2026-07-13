from django.contrib import admin
from .models import Category, Product, ProductImage, SiteSetting, ProductVariant, CustomOrder, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_fa', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name_fa',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_fa', 'price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name_fa',)}

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'status']

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['brand_name_fa']

admin.site.register(Order)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)