from rest_framework.generics import ListAPIView

from .pagination import BannerPagination

from .models import Banner
from .serializers import BannerSerializer

class BannerListView(ListAPIView):

    permission_classes = []

    pagination_class = BannerPagination

    serializer_class = BannerSerializer

    queryset = Banner.objects.filter(
        is_active=True,
    )