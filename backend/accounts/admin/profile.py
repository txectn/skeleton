from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Profile

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
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

    list_display_links = (
        "id",
        "user",
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
                ),
            },
        ),
        (
            "Personal Information",
            {
                "classes": ("tab",),
                "fields": (
                    "avatar",
                    "phone_number",
                    "date_of_birth",
                    "gender",
                ),
            },
        ),
        (
            "Address Information",
            {
                "classes": ("tab",),
                "fields": (
                    "address",
                    "country",
                    "region",
                    "city",
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