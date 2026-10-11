from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ...permissions import IsStaffOrSuperUser
from ...services import CustomersService
from common.pagination import Pagination

class CustomersView(GenericAPIView):
    permission_classes = [IsStaffOrSuperUser]

    pagination_class = Pagination

    def get(self, request):
        queryset = CustomersService.get_customers()

        page = self.paginate_queryset(queryset)

        data = CustomersService.serialize_customers(page)

        return self.get_paginated_response(data)