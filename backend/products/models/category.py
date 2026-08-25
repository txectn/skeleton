from django.db import models

class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "product_categories"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "name"],
                name="unique_category_name_per_parent",
            ),
            models.UniqueConstraint(
                fields=["parent", "slug"],
                name="unique_category_slug_per_parent",
            ),
        ]
        indexes = [
            models.Index(
                fields=["parent", "name"],
                name="category_parent_name_idx",
            ),
            models.Index(
                fields=["parent", "slug"],
                name="category_parent_slug_idx",
            ),
        ]

    def __str__(self):
        return self.name