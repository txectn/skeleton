from django.contrib import admin

from ..models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
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

    fieldsets = (
        ("User", {
            "fields": (
                "user",
                "refresh_token_hash",
            )
        }),
        ("Device Information", {
            "fields": (
                "device",
                "browser",
                "operating_system",
                "ip_address",
            )
        }),
        ("Session", {
            "fields": (
                "is_active",
                "expires_at",
                "last_activity",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )