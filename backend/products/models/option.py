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
            models.UniqueConstraint(
                fields=("product", "option_variable", "value"),
                name="unique_product_option_variable_value",
            ),
            models.UniqueConstraint(
                fields=("product","position"),
                name="unique_product_option_position",
            )
        )
        indexes = (
            models.Index(fields=("product", "option_variable")),
            models.Index(fields=("product", "position")),
        )

    def __str__(self):
        return f"{self.option_variable.name}: {self.value}"