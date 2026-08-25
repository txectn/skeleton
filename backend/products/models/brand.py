from django.db import models

class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "product_brands"
        ordering = ["name"]

    def __str__(self):
        return self.name