from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "phone_number", "is_verified", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_verified")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("phone_number", "is_verified")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)

admin.site.register(User, CustomUserAdmin)
