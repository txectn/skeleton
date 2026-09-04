from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CartItemRemoveSerializer
from ..services import CartService

class CartItemRemoveView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CartItemRemoveSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        cart, variant_id = CartService.remove_item(
            request=request,
            **serializer.validated_data,
        )

        response_data = {
            "variant": variant_id,
            "removed": True,
        }

        return Response(response_data)
    

'''
POST /api/cart/remove/
        │
        ├── variant
        └── cart_token
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
   ┌───┴────┐          ┌────┴─────┐
   │        │          │          │
 exists   missing    exists     missing
   │        │          │          │
   │        ▼          │          ▼
   │   Read guest      │     Cart Not Found
   │   cart_token      │
   │        │          │
   │        ▼          │
   │   Find guest      │
   │      Cart         │
   │        │          │
   │    ┌───┴───┐      │
   │    │       │      │
   │  found   missing  │
   │    │       │      │
   │    ▼       ▼      │
   │  Claim   Cart     │
   │  guest   Not      │
   │  cart    Found    │
   │    │              │
   └────┴──────────────┘
              │
              ▼
         Resolve Cart
              │
              ▼
      Find CartItem for
           Variant
              │
        ┌─────┴─────┐
        │           │
      exists     doesn't exist
        │           │
        ▼           ▼
   Store variant   Item Not Found
       ID
        │
        ▼
   Delete CartItem
        │
        ▼
   Return variant ID
        │
        ▼
{
    "variant": 12,
    "removed": true
}
'''