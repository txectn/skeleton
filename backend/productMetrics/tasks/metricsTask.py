from celery import shared_task
from django.db.models import F

from ..models import ProductMetrics, ProductMetricsSnapshot

# Record the view count for a product
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

# Record the wishlist count for a product
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_wishlist(product_id: int) -> None:
    """
    Atomically increment the wishlist count for a product.

    ProductMetrics is expected to exist because it is automatically
    created when the Product is created.
    """
    ProductMetrics.objects.filter(
        product_id=product_id,
    ).update(
        wishlist_count=F("wishlist_count") + 1,
    )

# Record the sold count for a product
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_sold(product_id: int) -> None:
    """
    Atomically increment the sold count for a product.

    ProductMetrics is expected to exist because it is automatically
    created when the Product is created.
    """
    ProductMetrics.objects.filter(
        product_id=product_id,
    ).update(
        sold_count=F("sold_count") + 1,
    )

# Record the cart add count for a product
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_cart_add(product_id: int) -> None:
    """
    Atomically increment the cart add count for a product.

    ProductMetrics is expected to exist because it is automatically
    created when the Product is created.
    """
    ProductMetrics.objects.filter(
        product_id=product_id,
    ).update(
        cart_add_count=F("cart_add_count") + 1,
    )


# Record the ProductMetricsSnapshot
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_metrics_snapshot() -> None:
    """
    Record the current product metrics for all products.

    Each ProductMetrics row is copied into a ProductMetricsSnapshot
    so historical metric values can be compared later.
    """
    metrics = ProductMetrics.objects.all()

    ProductMetricsSnapshot.objects.bulk_create(
        [
            ProductMetricsSnapshot(
                product=metric.product,
                view_count=metric.view_count,
                cart_add_count=metric.cart_add_count,
                wishlist_count=metric.wishlist_count,
                sold_count=metric.sold_count,
            )
            for metric in metrics
        ]
    )


# Record the trending score for a product
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_trending() -> None:
    """
    Calculate the recent trending score for all products.

    The score is based on the metric increase between the
    latest and previous snapshots.
    """

    VIEW_SCORE = 1
    CART_ADD_SCORE = 5
    WISHLIST_SCORE = 3
    SOLD_SCORE = 10

    for metrics in ProductMetrics.objects.all():

        snapshots = list(
            ProductMetricsSnapshot.objects
            .filter(product=metrics.product)
            .order_by("-recorded_at")[:2]
        )

        # Not enough history to calculate a change.
        if len(snapshots) < 2:
            continue

        current = snapshots[0]
        previous = snapshots[1]

        view_delta = max(
            current.view_count - previous.view_count,
            0,
        )

        cart_add_delta = max(
            current.cart_add_count - previous.cart_add_count,
            0,
        )

        wishlist_delta = max(
            current.wishlist_count - previous.wishlist_count,
            0,
        )

        sold_delta = max(
            current.sold_count - previous.sold_count,
            0,
        )

        trending_score = (
            view_delta * VIEW_SCORE
            + cart_add_delta * CART_ADD_SCORE
            + wishlist_delta * WISHLIST_SCORE
            + sold_delta * SOLD_SCORE
        )

        metrics.trending_score = trending_score
        metrics.save(update_fields=["trending_score"])

        
# Record the popularity score for a product
@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def record_product_popularity(product_id: int) -> None:
    """
    Calculate the popularity score for a product
    using its accumulated metrics.
    """

    VIEW_SCORE = 1
    CART_ADD_SCORE = 5
    WISHLIST_SCORE = 3
    SOLD_SCORE = 10

    metrics = ProductMetrics.objects.filter(
        product_id=product_id,
    ).first()

    if not metrics:
        return

    popularity_score = (
        metrics.view_count * VIEW_SCORE
        + metrics.cart_add_count * CART_ADD_SCORE
        + metrics.wishlist_count * WISHLIST_SCORE
        + metrics.sold_count * SOLD_SCORE
    )

    ProductMetrics.objects.filter(
        product_id=product_id,
    ).update(
        popularity_score=popularity_score,
    )

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def update_all_product_popularity() -> None:
    """
    Queue popularity calculation for all products.
    """

    product_ids = ProductMetrics.objects.values_list(
        "product_id",
        flat=True,
    )

    for product_id in product_ids:
        record_product_popularity.delay(product_id)