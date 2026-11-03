from django.db import models

class InventoryStockLevel(models.Model):
    name = models.CharField(
        max_length=100,
        default="Default",
    )

    levels = models.JSONField(
        default=list,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "inventory_stock_levels"
        verbose_name = "Inventory Stock Level"
        verbose_name_plural = "Inventory Stock Levels"

    def __str__(self):
        return f"Inventory Stock Level #{self.pk}"