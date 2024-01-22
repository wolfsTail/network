from django.contrib import admin

from .models import Message, Chat


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "chat", 
        "author",
        "text",
        "created_at",
        )
    
    search_fields = ("created_at", "text",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "user_1", 
        "user_2",
        )
    
    search_fields = ("user_1__username", "user_2__username",)
