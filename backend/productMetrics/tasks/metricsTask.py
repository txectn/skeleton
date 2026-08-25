from celery import shared_task
from django.db.models import F

from ..models import ProductMetrics

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_view(product_id: int) -> None:
    """
    Atomically increment the view count for a product.

    ProductMetrics is expected to exist because it is automatically
    created when the Product is created.
    """
    ProductMetrics.objects.filter(
        product_id=product_id,
    ).update(
        view_count=F("view_count") + 1,
    )