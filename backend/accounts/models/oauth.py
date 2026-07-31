from django.conf import settings
from django.db import models

class OauthAccount(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="oauth_accounts",
    )

    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
    )

    provider_user_id = models.CharField(
        max_length=255,
        help_text="Unique user ID returned by the OAuth provider.",
    )

    email = models.EmailField(
        blank=True,
    )

    avatar_url = models.URLField(
        blank=True,
    )

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional user information returned by the OAuth provider.",
    )

    connected_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "accounts_oauth"
        verbose_name = "OAuth Account"
        verbose_name_plural = "OAuth Accounts"

        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_user_id"],
                name="unique_oauth_provider_account",
            )
        ]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["provider"]),
        ]

    def __str__(self):
        return f"{self.user.email} ({self.get_provider_display()})"