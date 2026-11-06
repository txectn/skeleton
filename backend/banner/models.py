from datetime import timedelta

from django.utils import timezone

from django.db import models

from products.models import Product, Collection
from promotions.models import Promotion

# =====================================
# Banner
# =====================================

def default_end():
    return timezone.now() + timedelta(days=7)


class Banner(models.Model):

    class DestinationType(models.TextChoices):
        COLLECTION = "collection", "Collection"
        ALL_COLLECTIONS = "all_collections", "All Collections"
        PROMOTION = "promotion", "Promotion"
        PRODUCT = "product", "Product"
        CUSTOM_URL = "custom_url", "Custom URL"
        NORMAL = "normal", "Normal"
        
    # =====================================
    # Banner Information
    # =====================================

    title = models.CharField(
        max_length=255,
    )

    heading = models.CharField(
        max_length=255,
        blank=True,
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.ImageField(
        upload_to="banners/",
    )

    mobile_image = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True,
    )

    # =====================================
    # Destination
    # =====================================

    destination_type = models.CharField(
        max_length=30,
        choices=DestinationType.choices,
        default=DestinationType.NORMAL,
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="banners",
    )

    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="banners",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="banners",
    )

    custom_url = models.URLField(
        max_length=500,
        blank=True,
    )

    # =====================================
    # Call To Action
    # =====================================

    cta_label = models.CharField(
        max_length=100,
        blank=True,
    )

    # =====================================
    # Display Settings
    # =====================================

    position = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    starts_at = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
    )

    ends_at = models.DateTimeField(
        default=default_end,
        blank=True,
        null=True,
    )

    # =====================================
    # Timestamps
    # =====================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # =====================================
    # Methods
    # =====================================

    def save(self, *args, **kwargs):

        if self._state.adding and self.position == 0:
            last_position = Banner.objects.aggregate(
                max_position=models.Max("position")
            )["max_position"] or 0

            self.position = last_position + 1

        super().save(*args, **kwargs)

    # =====================================
    # Meta
    # =====================================

    class Meta:
        db_table = "banner_banners"
        ordering = [
            "position",
            "-created_at",
        ]

    def __str__(self):
        return self.title