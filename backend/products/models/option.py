from django.db import models

class Option(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="options",
    )

    option_variable = models.ForeignKey(
        "products.OptionVariable",
        on_delete=models.PROTECT,
        related_name="options",
    )

    value = models.CharField(
        max_length=255,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("position", "id")
        constraints = (
            # Ensures the same value can't be added twice for the same variable on a product
            models.UniqueConstraint(
                fields=("product", "option_variable", "value"),
                name="unique_product_option_variable_value",
            ),
            # Ensures position numbers can't repeat within the SAME option variable for this product
            models.UniqueConstraint(
                fields=("product", "option_variable", "position"),
                name="unique_product_variable_position",
            ),
        )
        indexes = (
            models.Index(fields=("product", "option_variable")),
            models.Index(fields=("product", "option_variable", "position")),
        )

    def __str__(self):
        return f"{self.option_variable.name}: {self.value}"