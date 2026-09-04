from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CartClearSerializer
from ..services import CartService

class CartClearView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CartClearSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        cart, cleared = CartService.clear_cart(
            request=request,
            **serializer.validated_data,
        )

        response_data = {
            "cart_token": (
                str(cart.cart_token)
                if cart and cart.cart_token
                else None
            ),
            "cleared": cleared,
        }

        return Response(
            response_data,
        )