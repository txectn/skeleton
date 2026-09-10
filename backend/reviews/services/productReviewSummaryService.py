from django.db.models import Avg, Count, Q

from ..models import ProductReviewSummary, Review

class ProductReviewSummaryService:

    @staticmethod
    def update(product_id):
        summary = Review.objects.filter(
            product_id=product_id,
        ).aggregate(
            review_count=Count("id"),
            average_rating=Avg("rating"),
            rating_1_count=Count(
                "id",
                filter=Q(rating=1),
            ),
            rating_2_count=Count(
                "id",
                filter=Q(rating=2),
            ),
            rating_3_count=Count(
                "id",
                filter=Q(rating=3),
            ),
            rating_4_count=Count(
                "id",
                filter=Q(rating=4),
            ),
            rating_5_count=Count(
                "id",
                filter=Q(rating=5),
            ),
        )

        ProductReviewSummary.objects.update_or_create(
            product_id=product_id,
            defaults={
                "review_count": summary["review_count"],
                "average_rating": summary["average_rating"] or 0,
                "rating_1_count": summary["rating_1_count"],
                "rating_2_count": summary["rating_2_count"],
                "rating_3_count": summary["rating_3_count"],
                "rating_4_count": summary["rating_4_count"],
                "rating_5_count": summary["rating_5_count"],
            },
        )