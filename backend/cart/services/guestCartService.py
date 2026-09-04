from ..models import Cart

class GuestCartService:

    @staticmethod
    def get(cart_token):
        return Cart.objects.filter(
            cart_token=cart_token,
            user__isnull=True,
        ).first()

    @staticmethod
    def create():
        return Cart.objects.create()