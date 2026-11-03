from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import OauthAccount

@admin.register(OauthAccount)
class OauthAccountAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "provider",
        "provider_user_id",
        "email",
        "connected_at",
    )

    list_filter = (
        "provider",
        "connected_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "email",
        "provider_user_id",
    )

    ordering = ("-connected_at",)

    readonly_fields = (
        "connected_at",
        "updated_at",
        "extra_data",
    )

    autocomplete_fields = ("user",)

    list_per_page = 25
    date_hierarchy = "connected_at"
    list_select_related = ("user",)

    fieldsets = (
        (
            "User Information",
            {
                "classes": ("tab",),
                "fields": (
                    "user",
                    "provider",
                    "provider_user_id",
                ),
            },
        ),
        (
            "Profile Information",
            {
                "classes": ("tab",),
                "fields": (
                    "email",
                    "avatar_url",
                ),
            },
        ),
        (
            "Provider Data",
            {
                "classes": ("tab",),
                "fields": (
                    "extra_data",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("tab",),
                "fields": (
                    "connected_at",
                    "updated_at",
                ),
            },
        ),
    )