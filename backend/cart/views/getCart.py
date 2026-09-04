from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..pagination import CartPagination

from ..serializers import CartSerializer

from ..services import CartService

class CartView(GenericAPIView):
    permission_classes = []
    pagination_class = CartPagination

    def get(self, request):
        cart = CartService.get_cart(
            request=request,
        )

        if cart is None:
            return Response({
                "cart": None,
                "items": [],
            })

        items = self.paginate_queryset(
            cart.items.all(),
        )

        serializer = CartSerializer(
            cart,
            context={
                "request": request,
                "items": items,
            },
        )

        return Response({
            "next": self.paginator.get_next_link(),
            "previous": self.paginator.get_previous_link(),
            **serializer.data,
        })





'''
GET /api/cart/
   ↓
request.user.is_authenticated?
   │
   ├── Yes
   │    ↓
   │  Check whether request.user has a Cart
   │    ↓
   │  If no Cart → use the guest cart UUID to find it
   │    ↓
   │  Attach that Cart to the user then clear uuid
   │    ↓
   │  Return Cart
   │
   └── No
        ↓
      Use cart UUID
        ↓
      Find guest Cart
        ↓
      Return Cart
'''