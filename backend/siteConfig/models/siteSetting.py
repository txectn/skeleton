from django.db import models

class SiteSetting(models.Model):

    site_name = models.CharField(
        max_length=100,
    )

    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    timezone = models.CharField(
        max_length=50,
        default="Asia/Dhaka",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )