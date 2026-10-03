from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    BkashVerifyPaymentSerializer,
)
from ..services import (
    BkashPaymentVerificationService,
)

class BkashVerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BkashVerifyPaymentSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        result = BkashPaymentVerificationService.verify_payment(
            user=request.user,
            data=serializer.validated_data,
        )

        return Response(result)