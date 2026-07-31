from django.conf import settings
from django.db import models


class LoginHistory(models.Model):
    class Provider(models.TextChoices):
        EMAIL = "email", "Email"
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="login_history",
    )

    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
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

    logged_in_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "accounts_login_history"
        verbose_name = "Login History"
        verbose_name_plural = "Login History"

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["provider"]),
            models.Index(fields=["logged_in_at"]),
        ]

    def __str__(self):
        identifier = self.email or self.user or "Unknown User"
        return f"{identifier} - {self.get_provider_display()} ({self.logged_in_at:%Y-%m-%d %H:%M:%S})"