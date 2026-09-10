from django.db import IntegrityError, transaction

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ReviewLike

class ReviewLikeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        review_id = kwargs["review_id"]

        try:
            with transaction.atomic():
                like = ReviewLike.objects.create(
                    user=request.user,
                    review_id=review_id,
                )

        except IntegrityError:
            return Response(
                {
                    "detail": "You have already liked this review.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": like.id,
                "review": like.review_id,
            },
            status=status.HTTP_201_CREATED,
        )

class ReviewLikeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReviewLike.objects.filter(
            user=self.request.user,
        )