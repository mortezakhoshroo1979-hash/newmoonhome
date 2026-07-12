from django.contrib import admin, messages
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import Brand, Category, Product, ProductImage, ProductThreeD, ProductVideo


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


class ProductThreeDInline(admin.TabularInline):
    model = ProductThreeD
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "sku",
        "category",
        "brand",
        "base_price",
        "special_price",
        "stock",
        "is_active",
        "is_featured",
    )
    list_editable = ("base_price", "special_price", "stock", "is_active")
    list_filter = ("category", "brand", "is_active", "is_featured")
    search_fields = ("name", "sku", "description")
    prepopulated_fields = {"slug": ("name",)}
    actions = [
        "make_active",
        "make_inactive",
        "clear_special_price",
    ]
    inlines = [ProductImageInline, ProductVideoInline, ProductThreeDInline]

    def thumbnail(self, obj):
        image = obj.images.filter(is_feature=True).first() or obj.images.first()
        if image and image.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;" />', image.image.url)
        return "-"

    thumbnail.short_description = "تصویر"

    @admin.action(description="فعال کردن محصولات انتخاب‌شده")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} محصول فعال شد.", messages.SUCCESS)

    @admin.action(description="غیرفعال کردن محصولات انتخاب‌شده")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} محصول غیرفعال شد.", messages.WARNING)

    @admin.action(description="حذف قیمت ویژه")
    def clear_special_price(self, request, queryset):
        updated = queryset.update(special_price=None)
        self.message_user(request, f"{updated} قیمت ویژه پاک شد.", messages.INFO)
