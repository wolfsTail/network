from rangefilter.filters import DateRangeFilter
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from django.contrib import admin

from .models import Post, Comment, Reaction
from .filters import CustomAuthorFilter, CustomPostFilter


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "author", 
        "title",
        "get_content",
        "get_comment_count",
        "created_at",
        )
    readonly_fields = ("created_at", "get_comment_count")
    search_fields = ("title",)
    list_filter = (
        CustomAuthorFilter, 
        ("created_at", DateRangeFilter),
        )
    
    @admin.display(description="Краткое содержание")
    def get_content(self, obj):
        max_length = 64
        if len(obj.content) > max_length:
            return obj.content[:max_length-3] + "..."
        else:
            return obj.content
    
    @admin.display(description="Количество комментариев")
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author", 
        "content",
        "post",
        "created_at",
        )
    list_display_links = ("author", "content",)
    list_filter = (CustomAuthorFilter, CustomPostFilter)
    raw_id_fields = ("author",)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        "author", 
        "post",
        "value",
        )
    list_filter = (
        CustomAuthorFilter, 
        CustomPostFilter, 
        ("value", ChoiceDropdownFilter),
        )
    autocomplete_fields = (
        "author",
        "post",
        )
