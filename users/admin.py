from rangefilter.filters import DateRangeFilter

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username", 
        "first_name", 
        "last_name", 
        "email",
        "is_staff",
        "is_active",
        "date_joined")
    

    readonly_fields = ("date_joined",)
    
    fieldsets = (
        ("Check boxes", {
            "classes": ("collapse",),
            "fields": (
                "is_staff",
                "is_active",
                "is_superuser",
            )
        }),
        ("Личные данные", {
            "fields": (                
                "first_name",
                "last_name",
            )
        }),
        ("Данные учетной записи", {
            "fields": (
                "username",
                "email",
                "password",
            )
            
        }),
        (None, {
            "fields": ("friends", "date_joined")
        }),
    )

    search_fields = ("username", "email")
    list_filter = (
        "is_staff", 
        "is_active", 
        ("date_joined", DateRangeFilter),
        )


admin.site.unregister(Group)
