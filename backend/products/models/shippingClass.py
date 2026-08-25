from django.db import models

class ShippingClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.name} - {self.delivery_charge}"