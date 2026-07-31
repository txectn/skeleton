from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    token_version = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return self.email or self.username