from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ExportMixin

from .models import CustomerRank, Profile, ReferralCode, ReferralTransaction, User


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(ExportMixin, BaseUserAdmin):
    list_display = ("username", "email", "phone", "is_verified", "is_staff", "date_joined")
    list_filter = ("is_verified", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "phone", "national_code")
    inlines = [ProfileInline]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("اطلاعات تکمیلی", {"fields": ("phone", "birth_date", "national_code", "is_verified", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(CustomerRank)
class CustomerRankAdmin(admin.ModelAdmin):
    list_display = ("name", "minimum_score", "discount_percent", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "usage_count", "total_reward_amount", "is_active")
    search_fields = ("code", "user__username", "user__phone")


@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(admin.ModelAdmin):
    list_display = ("referral_code", "referrer", "referred_user", "reward_amount", "created_at")
    search_fields = ("referral_code__code", "referrer__username", "referred_user__username")
