from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CheckoutSerializer, CheckoutItemSerializer
from ..services import CheckoutService

class CheckoutView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        checkout = CheckoutService.get_checkout(
            user=request.user,
        )

        # serializer = CheckoutSerializer(
        #     checkout,
        # )
        
        serializer = CheckoutItemSerializer(
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