from django.core.exceptions import ValidationError
from django.db import models

class Variant(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    compare_at_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    options = models.ManyToManyField(
        "products.Option",
        related_name="variants",
        blank=True,
    )

    currency = models.ForeignKey(
        "products.Currency",
        on_delete=models.PROTECT,
        related_name="variants",
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("position", "id")
        constraints = (
            models.UniqueConstraint(
                fields=("product", "position"),
                name="unique_variant_position_per_product",
            ),
        )
        indexes = (
            models.Index(fields=("product", "position")),
            models.Index(fields=("product", "is_active")),
        )

    def clean(self):
        super().clean()

        if (
            self.compare_at_price is not None
            and self.compare_at_price < self.price
        ):
            raise ValidationError(
                {
                    "compare_at_price": (
                        "Compare-at price must be greater than or equal to price."
                    )
                }
            )

        if (
            self.cost_price is not None
            and self.cost_price < 0
        ):
            raise ValidationError(
                {
                    "cost_price": "Cost price cannot be negative."
                }
            )

    def __str__(self):
        return self.sku