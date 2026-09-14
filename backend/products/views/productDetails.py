from rest_framework import generics
from rest_framework.response import Response
from ..serializers import (
    ProductDetailSerializer
)

from ..models import Product

from productMetrics.tasks import record_product_view

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = []
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        record_product_view.delay(instance.id)

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

