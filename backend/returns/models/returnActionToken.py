import uuid

from django.db import models
from django.utils import timezone

from datetime import timedelta

def default_token_expiry():
    return timezone.now() + timedelta(hours=24)

class ReturnActionToken(models.Model):
    return_request = models.ForeignKey(
        "returns.ReturnRequest",
        on_delete=models.CASCADE,
        related_name="action_tokens",
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    expires_at = models.DateTimeField(
        default=default_token_expiry,
    )
    
    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_valid(self):
        return (
            self.used_at is None
            and self.expires_at > timezone.now()
        )