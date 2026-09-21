from rest_framework import generics
from ..serializers import (
    TagSerializer
)

from ..models import Tag

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []

