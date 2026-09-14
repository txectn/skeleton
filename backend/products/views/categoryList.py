from rest_framework import generics
from ..serializers import (
    CategorySerializer
)

from ..models import Category

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []

