from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CheckoutReviewSerializer, CheckoutReviewItemSerializer
from ..services import CheckoutReviewService

class CheckoutReviewView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        checkout = CheckoutReviewService.get_checkout(
            user=request.user,
        )

        # serializer = CheckoutReviewSerializer(
        #     checkout,
        # )
        
        serializer = CheckoutReviewItemSerializer(
            checkout,
            many=True,
        )

        return Response(
            serializer.data,
        )




'''
orders/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── urls.py
│
├── serializers/
│   ├── __init__.py
│   └── checkout.py
│
├── services/
│   ├── __init__.py
│   ├── checkout_service.py
│   └── shipping_service.py
│
└── views/
    ├── __init__.py
    └── checkout.py
'''