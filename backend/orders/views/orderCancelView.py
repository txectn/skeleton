from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import OrderCancelSerializer
from ..services import OrderCancelService

class OrderCancelView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]

        resutl = OrderCancelService.cancel(
            user=request.user,
            order=order,
        )

        return Response(
            resutl,
            status=status.HTTP_200_OK,
        )