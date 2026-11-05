from django.contrib import admin
from django.utils import timezone

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
        (
            "Contact Information",
            {
                "classes": ("tab",),
                "fields": (
                    "name",
                    "email",
                    "phone",
                    "subject",
                    "message",
                ),
            },
        ),

        (
            "Management",
            {
                "classes": ("tab",),
                "fields": (
                    "status",
                    "admin_note",
                    "replied_at",
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

    def save_model(self, request, obj, form, change):

        if obj.status == ContactMessage.Status.REPLIED:

            if not obj.replied_at:
                obj.replied_at = timezone.now()

        else:
            obj.replied_at = None

        super().save_model(request, obj, form, change)