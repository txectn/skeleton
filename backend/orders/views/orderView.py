from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import OrderSerializer
from ..services import OrderService

from common.throttling import ThrottleService

class OrderView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        ThrottleService.check(
            request=request,
            scope="order_creation",
        )

        serializer = OrderSerializer(
            data=request.data,
            many=True,
        )
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user,
            items=serializer.validated_data,
        )

        return Response(
            {
                "id": order.id,
                "status": order.status,
                "subtotal": order.subtotal,
                "discount": order.discount,
                "shipping": order.shipping,
                "total": order.total,
            },
            status=status.HTTP_201_CREATED,
        )
