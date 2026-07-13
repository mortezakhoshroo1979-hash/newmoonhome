from django.contrib import admin

from .models import Comment, Post, PostCategory, Tag


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "views_count", "published_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "excerpt", "content")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "is_approved", "created_at")
    list_filter = ("is_approved",)
    actions = ["approve_comments", "reject_comments"]

    @admin.action(description="تایید نظرات انتخاب‌شده")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="رد نظرات انتخاب‌شده")
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
