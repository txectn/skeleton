from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):

    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "subject",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_per_page = 20

    ordering = (
        "-created_at",
    )

    fieldsets = (
        ("Contact Information", {
            "fields": (
                "name",
                "email",
                "phone",
                "subject",
            ),
        }),

        ("Message", {
            "fields": (
                "message",
            ),
        }),

        ("Management", {
            "fields": (
                "status",
                "admin_note",
                "replied_at",
            ),
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )