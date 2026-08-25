from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product

from .models import ProductMetrics

@receiver(post_save, sender=Product)
def create_product_metrics(
    sender,
    instance: Product,
    created: bool,
    **kwargs,
) -> None:
    """
    Create ProductMetrics automatically when a Product is created.

    A ProductMetrics record is a required one-to-one companion
    of every Product.
    """
    if not created:
        return

    ProductMetrics.objects.create(
        product=instance,
    )