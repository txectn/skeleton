from django.db import models

class ReturnPolicy(models.Model):

    name = models.CharField(
        max_length=100,
    )

    return_window_days = models.PositiveIntegerField(
        default=1,
    )

    customer_return_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    allow_changed_mind = models.BooleanField(
        default=True,
    )

    allow_ordered_by_mistake = models.BooleanField(
        default=True,
    )

    allow_wrong_product = models.BooleanField(
        default=True,
    )

    allow_damaged = models.BooleanField(
        default=True,
    )

    allow_fake = models.BooleanField(
        default=True,
    )

    allow_not_as_described = models.BooleanField(
        default=True,
    )

    allow_missing_item = models.BooleanField(
        default=True,
    )

    allow_other = models.BooleanField(
        default=False,
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

    def __str__(self):
        return self.name