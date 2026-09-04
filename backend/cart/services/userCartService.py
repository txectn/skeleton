from ..models import Cart

class UserCartService:

    @staticmethod
    def get(user):
        return Cart.objects.filter(
            user=user,
        ).first()

    @staticmethod
    def create(user):
        return Cart.objects.create(
            user=user,
        )