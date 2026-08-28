from django.utils.timesince import timesince
from django.utils import timezone
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Presence

@admin.register(Presence)
class PresenceAdmin(ModelAdmin):
    list_display = (
        "presence_id",
        "user",
        "device_type",
        "browser",
        "operating_system",
        "ip_address",
        "status",
    )

    list_filter = (
        "user",
        "device_type",
        "browser",
        "operating_system",
        "first_seen_at",
        "last_seen_at",
    )

    search_fields = (
        "presence_id",
        "device_id",
        "fingerprint",
        "ip_address",
        "user__email",
        "user_agent",
    )

    readonly_fields = (
        "presence_id",
        "first_seen_at",
        "last_seen_at",
        "status",
    )

    ordering = (
        "-last_seen_at",
    )

    list_per_page = 50

    @admin.display(description="Status")
    def status(self, obj):
        elapsed = timezone.now() - obj.last_seen_at

        if elapsed.total_seconds() < 60:
            return "Online"

        if elapsed.total_seconds() < 600:
            return f"Last seen {timesince(obj.last_seen_at)} ago"

        return f"Last seen at {obj.last_seen_at.strftime('%I:%M %p').lstrip('0')}"