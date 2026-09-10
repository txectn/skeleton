from django.urls import path

from .views import (
    ProductReviewListCreateView,
    ProductReviewDeleteView,
    ReviewLikeCreateView,
    ReviewLikeDeleteView,
)

urlpatterns = [
    # List + create reviews
    path(
        "products/<int:product_id>/reviews/",
        ProductReviewListCreateView.as_view(),
        name="product-review-list-create",
    ),

    # Delete own review
    path(
        "reviews/<int:pk>/",
        ProductReviewDeleteView.as_view(),
        name="product-review-delete",
    ),

    # Like review
    path(
        "reviews/<int:review_id>/like/",
        ReviewLikeCreateView.as_view(),
        name="review-like",
    ),

    # Unlike own like
    path(
        "review-likes/<int:pk>/",
        ReviewLikeDeleteView.as_view(),
        name="review-like-delete",
    ),
]