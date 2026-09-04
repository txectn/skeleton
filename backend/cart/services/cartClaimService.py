class CartClaimService:

    @staticmethod
    def claim(cart, user):
        cart.user = user
        cart.cart_token = None
        cart.save(
            update_fields=[
                "user",
                "cart_token",
            ],
        )

        return cart