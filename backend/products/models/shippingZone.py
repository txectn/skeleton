from django.db import models

class ShippingZone(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    country = models.CharField(
        max_length=100,
    )

    region = models.CharField(
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.name