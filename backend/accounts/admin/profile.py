from django.contrib import admin

from ..models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone_number",
        "gender",
        "country",
        "region",
        "city",
        "created_at",
    )

    list_filter = (
        "gender",
        "country",
        "region",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "phone_number",
        "city",
        "region",
        "country",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
    )

    fieldsets = (
        ("User", {
            "fields": (
                "user",
            ),
        }),
        ("Personal Information", {
            "fields": (
                "avatar",
                "phone_number",
                "date_of_birth",
                "gender",
            ),
        }),
        ("Address", {
            "fields": (
                "address",
                "country",
                "region",
                "city",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )