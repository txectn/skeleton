from django.core.exceptions import ValidationError
from django.db import models

from .brand import Brand
from .model import Model
from .category import Category
from .collection import Collection
from .tag import Tag
from .shippingClass import ShippingClass

class Product(models.Model):
    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    model = models.ForeignKey(
        Model,
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    collections = models.ManyToManyField(
        Collection,
        related_name="products",
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True,
    )

    shipping_class = models.ForeignKey(
        ShippingClass,
        on_delete=models.PROTECT,
        related_name="products",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "product_products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["brand"],
                name="product_brand_idx",
            ),
            models.Index(
                fields=["model"],
                name="product_model_idx",
            ),
            models.Index(
                fields=["category"],
                name="product_category_idx",
            ),
            models.Index(
                fields=["created_at"],
                name="product_created_at_idx",
            ),
        ]

    def clean(self):
        super().clean()

        if self.model_id and self.brand_id:
            if self.model.brand_id != self.brand_id:
                raise ValidationError(
                    {
                        "model": (
                            "The selected model does not belong "
                            "to the selected brand."
                        )
                    }
                )

    def __str__(self):
        return self.name

'''
Model references can be written in two ways:

Direct import:
from .currency import Currency
models.ForeignKey(Currency, ...)

String reference:
models.ForeignKey("products.Currency", ...)

Both approaches are valid. Use direct imports when there is no
circular import issue; use string references when needed to avoid one.
'''