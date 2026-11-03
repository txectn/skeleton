from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models.user import User

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "provider_user_id",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )    
    
    list_display_links = (
        "id",
        "username",
        "email",
    )

    list_filter = (
        "is_verified",
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "provider_user_id",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    list_per_page = 25
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "User Information",
            {
                "classes": ("tab",),
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "classes": ("tab",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
        (
            "Authentication",
            {
                "classes": ("tab",),
                "fields": (
                    "provider_user_id",
                    "is_verified",
                    "token_version",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("tab",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "classes": ("tab",),
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_verified",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

        