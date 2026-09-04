from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    CartItemCrudSerializer,
    CartItemSerializer,
)

from ..services import CartService

class CartItemDecreaseQuantityView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CartItemCrudSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        cart, cart_item, decrease_limit_reached = CartService.decrease_quantity(
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

        response_data["decrease_limit_reached"] = decrease_limit_reached

        return Response(
            response_data,
        )



'''
                    Decrease Quantity
                           │
                           ▼
                 Is user authenticated?
                      /          \
                    YES           NO
                     │             │
                     ▼             ▼
              Find user's Cart   Find guest Cart
                     │            using cart_token
               ┌─────┴─────┐          │
               │           │      ┌───┴────┐
             found       missing  │        │
               │           │     found   missing
               │           ▼       │        │
               │      Find guest   │        ▼
               │      Cart using   │     RETURN
               │      cart_token   │     Cart Not Found
               │           │       │
               │      ┌────┴────┐  │
               │      │         │  │
               │    found     missing
               │      │         │
               │      ▼         ▼
               │    CLAIM     RETURN
               │      │       Cart Not Found
               │      │
               └──────┴───────────┐
                                  ▼
                           Resolved Cart
                                  │
                                  ▼
                           Find CartItem
                                  │
                       ┌──────────┴──────────┐
                       │                     │
                     found                missing
                       │                     │
                       ▼                     ▼
                Check current           RETURN
                  quantity              Item Not Found
                       │
                ┌──────┴──────┐
                │             │
          quantity > 1    quantity == 1
                │             │
                ▼             ▼
       Calculate new       Keep quantity
          quantity             at 1
                │             │
                ▼             │
 current - requested           │
                │             │
                ▼             │
        Is result < 1?         │
           /       \           │
         YES        NO         │
          │          │         │
          ▼          ▼         │
       Set to 1   Use result   │
          │          │         │
          └────┬─────┘         │
               ▼               │
          Save CartItem ◄──────┘
               │
               ▼
       RETURN updated CartItem
'''