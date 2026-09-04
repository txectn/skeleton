import logging

from uuid import UUID

# Get cart services
from .cartClaimService import CartClaimService
from .guestCartService import GuestCartService
from .userCartService import UserCartService

from .cartItemService import CartItemService
from .cartItemDecreaseService import CartItemDecreaseService
from .cartItemUpdateQuantityService import CartItemUpdateQuantityService
from .cartItemRemoveService import CartItemRemoveService
from .cartItemClearService import CartItemClearService

from common.throttling import ThrottleService

logger = logging.getLogger(__name__)

class CartService:

    @staticmethod
    def get_cart(request):
        """
        Retrieve the cart for the current request.

        Authenticated user:
            1. Find the user's cart.
            2. If no cart exists, check for a guest cart token.
            3. If a guest cart exists, claim it for the user.
            4. Return the cart or None.

        Guest user:
            1. Check for a guest cart token.
            2. If no token exists, return None.
            3. Find and return the guest cart or None.
        """

        try:
            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # Guest cart
                # -----------------------------------------------------

                if cart is None:

                    try:
                        cart_token = UUID(
                            request.query_params.get(
                                "cart_token",
                            ),
                        )

                    except (ValueError, TypeError, AttributeError):
                        cart_token = None

                    if cart_token:
                        cart = GuestCartService.get(
                            cart_token=cart_token,
                        )

                        # -------------------------------------------------
                        # Claim guest cart
                        # -------------------------------------------------

                        if cart is not None:
                            cart = CartClaimService.claim(
                                cart=cart,
                                user=request.user,
                            )

                return cart

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            try:
                cart_token = UUID(
                    request.query_params.get(
                        "cart_token",
                    ),
                )
                
            except (ValueError, TypeError, AttributeError):
                cart_token = None

            if not cart_token:
                return None

            return GuestCartService.get(
                cart_token=cart_token,
            )

        except Exception:
            logger.exception(
                "Failed to retrieve cart.",
            )

            raise

    @staticmethod
    def add_item(
        request,
        *,
        variant,
        quantity,
        cart_token=None,
    ):
        """
        Add a variant to the current user's or guest's cart.

        Authenticated user:
            1. Find the user's cart.
            2. If no cart exists, check for a guest cart.
            3. Claim the guest cart if found.
            4. If no cart exists, create a user cart.

        Guest user:
            1. Check for a guest cart token.
            2. If found, use the existing guest cart.
            3. If not found, create a new guest cart.
            4. The caller is responsible for setting the new
               cart token in the response cookie.

        Then:
            1. Validate inventory.
            2. Create or update the CartItem.
            3. Return the Cart.
        """

        try:
            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # No user cart → try guest cart
                # -----------------------------------------------------

                if cart is None:
                    if cart_token:
                        cart = GuestCartService.get(
                            cart_token=cart_token,
                        )

                        if cart is not None:
                            cart = CartClaimService.claim(
                                cart=cart,
                                user=request.user,
                            )

                # -----------------------------------------------------
                # No cart at all → create user cart
                # -----------------------------------------------------

                if cart is None:
                    cart = UserCartService.create(
                        request.user,
                    )

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            else:
                cart = None

                if cart_token:
                    cart = GuestCartService.get(
                        cart_token=cart_token,
                    )

                # -----------------------------------------------------
                # No guest cart → create one
                # -----------------------------------------------------

                if cart is None:
                    ThrottleService.check(
                        request=request,
                        scope="guest_cart_creation",
                    )

                    cart = GuestCartService.create()

            # ---------------------------------------------------------
            # Add/update CartItem
            # ---------------------------------------------------------

            cart_item, increase_limit_reached = CartItemService.add_item(
                cart=cart,
                variant=variant,
                quantity=quantity,
            )

            return cart, cart_item, increase_limit_reached

        except Exception:
            logger.exception(
                "Failed to add item to cart.",
                extra={
                    "variant_id": getattr(variant, "id", None),
                    "quantity": quantity,
                    "user_id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                },
            )

            raise

    @staticmethod
    def decrease_quantity(
        request,
        *,
        variant,
        quantity,
        cart_token=None,
    ):
        """
        Decrease the quantity of a variant in the current user's
        or guest's cart.

        Authenticated user:
            1. Find the user's cart.
            2. If no user cart exists, check for a guest cart.
            3. Claim the guest cart if found.
            4. If no cart exists, return Cart Not Found.

        Guest user:
            1. Check for a guest cart token.
            2. If no token exists, return Cart Not Found.
            3. Find the guest cart.
            4. If the cart does not exist, return Cart Not Found.

        Then:
            1. Find the CartItem for the variant.
            2. If the CartItem does not exist, return Item Not Found.
            3. If quantity is already 1, do not decrease it.
            4. Otherwise decrease the quantity.
            5. Return the cart and CartItem.
        """

        try:
            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # No user cart → try guest cart
                # -----------------------------------------------------

                if cart is None:

                    if cart_token:
                        cart = GuestCartService.get(
                            cart_token=cart_token,
                        )

                        # -------------------------------------------------
                        # Claim guest cart
                        # -------------------------------------------------

                        if cart is not None:
                            cart = CartClaimService.claim(
                                cart=cart,
                                user=request.user,
                            )

                # -----------------------------------------------------
                # No cart found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            else:

                if not cart_token:
                    return None, None

                cart = GuestCartService.get(
                    cart_token=cart_token,
                )

                # -----------------------------------------------------
                # Guest cart not found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            cart_item, decrease_limit_reached = CartItemDecreaseService.decrease_quantity(
                cart=cart,
                variant=variant,
                quantity=quantity,
            )

            return cart, cart_item, decrease_limit_reached

        except Exception:
            logger.exception(
                "Failed to decrease cart item quantity.",
                extra={
                    "variant_id": getattr(variant, "id", None),
                    "quantity": quantity,
                    "user_id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                },
            )

            raise

    @staticmethod
    def update_quantity(
        request,
        *,
        variant,
        quantity,
        cart_token=None,
    ):
        """
        Update the total quantity of a variant in the current
        user's or guest's cart.

        The supplied quantity represents the new total quantity.
        It is not an increase or decrease amount.

        Authenticated user:
            1. Find the user's cart.
            2. If no user cart exists, check for a guest cart.
            3. Claim the guest cart if found.
            4. If no cart exists, return Cart Not Found.

        Guest user:
            1. Check for a guest cart token.
            2. If no token exists, return Cart Not Found.
            3. Find the guest cart.
            4. If the cart does not exist, return Cart Not Found.

        Then:
            1. Find the CartItem for the variant.
            2. If the CartItem does not exist, return Item Not Found.
            3. Set the CartItem quantity to the requested total.
            4. If the requested quantity exceeds available inventory,
               clamp it to the available quantity.
            5. Return the cart, CartItem, and limit status.
        """

        try:
            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # No user cart → try guest cart
                # -----------------------------------------------------

                if cart is None:

                    if cart_token:

                        cart = GuestCartService.get(
                            cart_token=cart_token,
                        )

                        # -------------------------------------------------
                        # Claim guest cart
                        # -------------------------------------------------

                        if cart is not None:

                            cart = CartClaimService.claim(
                                cart=cart,
                                user=request.user,
                            )

                # -----------------------------------------------------
                # No cart found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            else:

                if not cart_token:
                    return None, None

                cart = GuestCartService.get(
                    cart_token=cart_token,
                )

                # -----------------------------------------------------
                # Guest cart not found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            # ---------------------------------------------------------
            # Update CartItem quantity
            # ---------------------------------------------------------

            cart_item, quantity_limit_reached = (
                CartItemUpdateQuantityService.update_quantity(
                    cart=cart,
                    variant=variant,
                    quantity=quantity,
                )
            )

            return (
                cart,
                cart_item,
                quantity_limit_reached,
            )

        except Exception:

            logger.exception(
                "Failed to update cart item quantity.",
                extra={
                    "variant_id": getattr(
                        variant,
                        "id",
                        None,
                    ),
                    "quantity": quantity,
                    "user_id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                },
            )

            raise

    @staticmethod
    def remove_item(
        request,
        *,
        variant,
        cart_token=None,
    ):
        """
        Remove a variant from the current user's or guest's cart.

        Authenticated user:
            1. Find the user's cart.
            2. If no user cart exists, check for a guest cart.
            3. Claim the guest cart if found.
            4. If no cart exists, return Cart Not Found.

        Guest user:
            1. Check for a guest cart token.
            2. If no token exists, return Cart Not Found.
            3. Find the guest cart.
            4. If the cart does not exist, return Cart Not Found.

        Then:
            1. Find the CartItem for the variant.
            2. If the CartItem does not exist, return Item Not Found.
            3. Remove the CartItem.
            4. Return the cart and removed variant ID.
        """

        try:
            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # No user cart → try guest cart
                # -----------------------------------------------------

                if cart is None:

                    if cart_token:

                        cart = GuestCartService.get(
                            cart_token=cart_token,
                        )

                        # -------------------------------------------------
                        # Claim guest cart
                        # -------------------------------------------------

                        if cart is not None:

                            cart = CartClaimService.claim(
                                cart=cart,
                                user=request.user,
                            )

                # -----------------------------------------------------
                # No cart found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            else:

                if not cart_token:
                    return None, None

                cart = GuestCartService.get(
                    cart_token=cart_token,
                )

                # -----------------------------------------------------
                # Guest cart not found
                # -----------------------------------------------------

                if cart is None:
                    return None, None

            # ---------------------------------------------------------
            # Remove CartItem
            # ---------------------------------------------------------

            variant_id = CartItemRemoveService.remove_item(
                cart=cart,
                variant=variant,
            )

            return cart, variant_id

        except Exception:

            logger.exception(
                "Failed to remove cart item.",
                extra={
                    "variant_id": getattr(
                        variant,
                        "id",
                        None,
                    ),
                    "user_id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                },
            )

            raise

    @staticmethod
    def clear_cart(
        request,
        *,
        cart_token,
    ):
        """
        Clear all items from the current user's or guest's cart.

        Authenticated user:
            1. Find the user's cart.
            2. If no user cart exists, check the provided cart_token.
            3. If a guest cart is found, claim it.
            4. If no cart exists, return no cart.

        Guest user:
            1. Require cart_token.
            2. Find the guest cart.
            3. If no cart exists, return no cart.

        Then:
            1. Remove all CartItems from the resolved cart.
            2. Keep the Cart itself.
            3. Return the cart and clear status.

        This service does not:
            - Modify inventory.
            - Reserve inventory.
            - Delete the Cart.
            - Create a Cart.
        """

        try:

            # ---------------------------------------------------------
            # Authenticated user
            # ---------------------------------------------------------

            if request.user.is_authenticated:

                cart = UserCartService.get(
                    request.user,
                )

                # -----------------------------------------------------
                # No user cart → try guest cart using token
                # -----------------------------------------------------

                if cart is None and cart_token:

                    cart = GuestCartService.get(
                        cart_token=cart_token,
                    )

                    # -------------------------------------------------
                    # Claim guest cart
                    # -------------------------------------------------

                    if cart is not None:

                        cart = CartClaimService.claim(
                            cart=cart,
                            user=request.user,
                        )

            # ---------------------------------------------------------
            # Guest user
            # ---------------------------------------------------------

            else:

                if not cart_token:
                    return None, False

                cart = GuestCartService.get(
                    cart_token=cart_token,
                )

            # ---------------------------------------------------------
            # No cart found
            # ---------------------------------------------------------

            if cart is None:
                return None, False

            # ---------------------------------------------------------
            # Clear all CartItems
            # ---------------------------------------------------------

            CartItemClearService.clear_items(
                cart=cart,
            )

            return cart, True

        except Exception:

            logger.exception(
                "Failed to clear cart.",
                extra={
                    "user_id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                },
            )

            raise