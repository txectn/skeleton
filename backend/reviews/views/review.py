from django.db import IntegrityError, transaction
from django.db.models import BooleanField, Count, Exists, OuterRef, Value

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..models import Review, ReviewLike
from ..serializers import ReviewSerializer, ReviewCreateSerializer

from ..services import ProductReviewSummaryService

from common.pagination import Pagination

class ProductReviewListCreateView(generics.ListCreateAPIView):
    pagination_class = Pagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]

        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        queryset = (
            Review.objects
            .filter(product_id=product_id)
            .select_related("user", "product")
            .annotate(
                like_count=Count("likes", distinct=True),
            )
        )

        user = self.request.user

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_liked=Exists(
                    ReviewLike.objects.filter(
                        review=OuterRef("pk"),
                        user=user,
                    )
                )
            )
        else:
            queryset = queryset.annotate(
                is_liked=Value(
                    False,
                    output_field=BooleanField(),
                )
            )

        return queryset

    def create(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                review = serializer.save(
                    user=request.user,
                    product_id=product_id,
                )

                ProductReviewSummaryService.update(product_id)

        except IntegrityError:
            return Response(
                {
                    "detail": "You have already reviewed this product.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        review.like_count = 0
        review.is_liked = False

        response_serializer = ReviewSerializer(
            review,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )