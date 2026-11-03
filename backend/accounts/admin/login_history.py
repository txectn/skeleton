from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import LoginHistory

@admin.register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "email",
        "success",
        "provider",
        "ip_address",
        "device",
        "browser",
        "operating_system",
        "logged_in_at",
    )

    list_filter = (
        "success",
        "provider",
        "browser",
        "operating_system",
        "logged_in_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "email",
        "provider",
        "ip_address",
        "device",
        "browser",
        "operating_system",
    )

    ordering = ("-logged_in_at",)

    readonly_fields = (
        "user",
        "email",
        "success",
        "provider",
        "ip_address",
        "device",
        "browser",
        "operating_system",
        "logged_in_at",
    )

    autocomplete_fields = ("user",)

    list_per_page = 25
    date_hierarchy = "logged_in_at"
    list_select_related = ("user",)

    fieldsets = (
        (
            "User Information",
            {
                "classes": ("tab",),
                "fields": (
                    "user",
                    "email",
                    "provider",
                ),
            },
        ),
        (
            "Device Information",
            {
                "classes": ("tab",),
                "fields": (
                    "ip_address",
                    "device",
                    "browser",
                    "operating_system",
                ),
            },
        ),
        (
            "Login Information",
            {
                "classes": ("tab",),
                "fields": (
                    "success",
                    "logged_in_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False