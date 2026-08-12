from django.contrib import admin

from ..models import LoginHistory

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
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

    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "user",
                    "email",
                    "provider",
                )
            },
        ),
        (
            "Device Information",
            {
                "fields": (
                    "ip_address",
                    "device",
                    "browser",
                    "operating_system",
                )
            },
        ),
        (
            "Login Information",
            {
                "fields": (
                    "success",
                    "logged_in_at",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False