from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Review

class ProductReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user,
        )