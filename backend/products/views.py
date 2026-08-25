from rest_framework import generics
from rest_framework.response import Response
from .serializers import (
    ProductDetailSerializer,
    ProductListSerializer
)

from .models import Product

from .services import (
    ProductSearchService,
    ProductFilterService,
    ProductSortService
)

from productMetrics.tasks import record_product_view

from .pagination import ProductPagination

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    permission_classes = []

    def get_queryset(self):
        queryset = Product.objects.all()

        queryset = ProductSearchService().search(
            queryset=queryset,
            query=self.request.query_params.get("search"),
        )

        queryset = ProductFilterService().filter(
            queryset=queryset,
            params=self.request.query_params,
        )

        queryset = ProductSortService().sort(
            queryset=queryset,
            params=self.request.query_params,
        )

        return queryset
    

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

