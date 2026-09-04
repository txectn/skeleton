import uuid

from django.conf import settings
from django.db import models

def generate_presence_id():
    return uuid.uuid4().hex

class Presence(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="presences",
    )

    presence_id = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        default=generate_presence_id,
    )

    device_id = models.CharField(
        max_length=128,
        db_index=True,
    )

    fingerprint = models.CharField(
        max_length=128,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)

    browser = models.CharField(
        max_length=100,
        blank=True,
    )

    browser_version = models.CharField(
        max_length=50,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
    )

    os_version = models.CharField(
        max_length=50,
        blank=True,
    )

    device_type = models.CharField(
        max_length=30,
        blank=True,
    )

    first_seen_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_seen_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["device_id"]),
            models.Index(fields=["fingerprint"]),
            models.Index(fields=["last_seen_at"]),
        ]

    def __str__(self):
        return self.presence_id