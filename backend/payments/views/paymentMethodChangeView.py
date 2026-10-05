from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PaymentMethodChangeSerializer
from ..services import PaymentMethodChangeService

class PaymentMethodChangeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentMethodChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = PaymentMethodChangeService.change_payment_method(
            user=request.user,
            order=serializer.validated_data["order"],
            payment_method=serializer.validated_data["payment_method"],
            provider=serializer.validated_data.get("provider"),
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )