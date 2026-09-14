from rest_framework import generics
from ..serializers import (
    BrandSerializer
)

from ..models import Brand

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = []

