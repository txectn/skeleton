from django.conf import settings
from django.db import models

class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    refresh_token_hash = models.CharField(
        max_length=255,
    )

    device = models.CharField(
        max_length=255,
        blank=True,
    )

    browser = models.CharField(
        max_length=255,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=255,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    expires_at = models.DateTimeField()

    last_activity = models.DateTimeField()

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "accounts_user_session"
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.device or 'Unknown Device'}"