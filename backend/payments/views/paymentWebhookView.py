from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import PaymentVerificationService

class PaymentWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        PaymentVerificationService.process_webhook(
            data=request.data,
        )

        return Response(
            {
                "status": "received",
            },
            status=200
        )