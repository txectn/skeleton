from django.contrib import admin

from ..models import OauthAccount

@admin.register(OauthAccount)
class OauthAccountAdmin(admin.ModelAdmin):
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

    fieldsets = (
        ("User", {
            "fields": (
                "user",
                "provider",
                "provider_user_id",
            )
        }),
        ("Profile", {
            "fields": (
                "email",
                "avatar_url",
            )
        }),
        ("Provider Data", {
            "fields": (
                "extra_data",
            )
        }),
        ("Timestamps", {
            "fields": (
                "connected_at",
                "updated_at",
            )
        }),
    )