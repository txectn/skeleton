from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    CartItemCrudSerializer,
    CartItemSerializer,
)

from ..services import CartService

class CartItemUpdateQuantityView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CartItemCrudSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        cart, cart_item, quantity_limit_reached = CartService.update_quantity(
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

        response_data["quantity_limit_reached"] = quantity_limit_reached

        return Response(
            response_data,
        )


'''
POST /api/cart/item/update/
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
   │  Find guest Cart  │      RETURN
   │  using cart_token │    Cart Not Found
   │       │            │
   │   ┌───┴───┐        │
   │   │       │        │
   │ found   missing    │
   │   │       │        │
   │   ▼       ▼        │
   │ CLAIM   RETURN     │
   │   │   Cart Not     │
   │   │    Found       │
   │   │                │
   └───┴────────────────┘
              │
              ▼
         Resolved Cart
              │
              ▼
      Find CartItem for
           Variant
              │
       ┌──────┴──────┐
       │             │
     exists       doesn't exist
       │             │
       │             ▼
       │          RETURN
       │       Item Not Found
       │
       ▼
 Get available inventory
       │
       ▼
 Is requested quantity
 > available quantity?
       │
   ┌───┴──────┐
   │          │
  YES         NO
   │          │
   ▼          ▼
Set          Set
quantity     quantity
to           to requested
available   quantity
inventory    │
   │         │
   ▼         ▼
quantity_limit_reached
       = True
              │
              │
       quantity_limit_reached
              = False
              │
              └──────┬──────┘
                     ▼
             Update CartItem
             with new quantity
                     │
                     ▼
               Save CartItem
                     │
                     ▼
          Return updated CartItem
                     │
                     ▼
             Return cart_token
             + quantity_limit_reached
'''


