import uuid

from django.conf import settings
from django.db import models

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart",
    )

    cart_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.email}"

        return f"Guest Cart - {self.cart_token}"