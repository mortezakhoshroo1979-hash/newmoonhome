from django.contrib import admin

from .forms import BannerForm, SiteSettingForm, SliderForm
from .models import Banner, ContactMessage, Newsletter, SiteSetting, Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    form = SliderForm
    list_display = ("title", "sort_order", "is_active", "created_at")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    form = BannerForm
    list_display = ("title", "position", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("position", "is_active")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    search_fields = ("email",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email", "phone", "subject", "message")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    form = SiteSettingForm
    list_display = ("site_name", "contact_phone", "contact_email", "created_at")
