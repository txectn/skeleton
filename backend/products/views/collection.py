from rest_framework import generics
from ..serializers import (
    CollectionSerializer
)

from ..models import Collection

class CollectionListView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = []

