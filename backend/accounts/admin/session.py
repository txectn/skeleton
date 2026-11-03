from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "device",
        "browser",
        "operating_system",
        "ip_address",
        "is_active",
        "expires_at",
        "last_activity",
        "created_at",
    )

    list_filter = (
        "is_active",
        "browser",
        "operating_system",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "device",
        "browser",
        "operating_system",
        "ip_address",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_activity",
    )

    autocomplete_fields = ("user",)

    list_per_page = 25
    date_hierarchy = "created_at"
    list_select_related = ("user",)

    fieldsets = (
        (
            "User Information",
            {
                "classes": ("tab",),
                "fields": (
                    "user",
                    "refresh_token_hash",
                ),
            },
        ),
        (
            "Device Information",
            {
                "classes": ("tab",),
                "fields": (
                    "device",
                    "browser",
                    "operating_system",
                    "ip_address",
                ),
            },
        ),
        (
            "Session Information",
            {
                "classes": ("tab",),
                "fields": (
                    "is_active",
                    "expires_at",
                    "last_activity",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("tab",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )