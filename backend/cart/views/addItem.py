from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    CartItemCrudSerializer,
    CartItemSerializer
)

from ..services import CartService

class CartItemView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CartItemCrudSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        cart, cart_item, increase_limit_reached = CartService.add_item(
            request=request,
            **serializer.validated_data,
        )

        response_serializer = CartItemSerializer(
            cart_item,
            context={"request": request},
        )

        response_data = response_serializer.data

        response_data["cart_token"] = (
            str(cart.cart_token)
            if cart.cart_token
            else None
        )

        response_data["increase_limit_reached"] = (
            increase_limit_reached
        )

        return Response(
            response_data,
        )

'''
POST /api/cart/
        │
        ├── variant
        └── quantity
              ↓
        Is user authenticated?
              │
       ┌─────────┴─────────┐
       │                   │
      YES                 NO
       │                   │
       ▼                   ▼
Find user's Cart       Read cart_token
       │                    │
   ┌───┴───┐            ┌───┴────┐
   │       │            │        │
 exists  missing       exists  missing
   │       │            │        │
   │       ▼            │        ▼
   │  Create User Cart  │     Create Cart
   │       │            │     + Generate UUID
   │       │            │        │
   │       │            │        │
   └───────┘            └────────┘
       │                    │
       └─────────┬──────────┘
                 ↓
            Resolve Cart
                 ↓
          Find CartItem for
               Variant
                 │
          ┌──────┴──────┐
          │             │
        exists      doesn't exist
          │             │
          ▼             ▼
   Update quantity   Create CartItem
          │             │
          └──────┬──────┘
                 ↓
          Return updated cart
'''