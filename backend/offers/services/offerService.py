from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone

from ..models import Offer

class OfferService:
    """
    Handles offer eligibility and discount calculation for variants.
    """

    MONEY_QUANT = Decimal("0.01")

    @classmethod
    def get_active_offers_for_variant(cls, variant):
        """
        Return all currently applicable offers for a variant,
        ordered by highest priority.
        """
        now = timezone.now()

        return (
            Offer.objects
            .filter(
                offer_variants__variant=variant,
                is_active=True,
                starts_at__lte=now,
                ends_at__gt=now,
            )
            .order_by("-priority", "-created_at")
            .distinct()
        )

    @classmethod
    def get_variant_offer(cls, variant):
        """
        Return the highest-priority active offer for a variant.

        Returns:
            Offer instance or None.
        """
        return cls.get_active_offers_for_variant(variant).first()

    @classmethod
    def calculate_discount(cls, *, price, offer):
        """
        Calculate the discount amount for a given price and offer.

        The discount can never exceed the original price.
        """
        price = Decimal(price)

        if price < 0:
            raise ValueError("Price cannot be negative.")

        discount_value = Decimal(offer.discount_value)

        if discount_value < 0:
            raise ValueError("Discount value cannot be negative.")

        if offer.discount_type == Offer.DiscountType.PERCENTAGE:
            if discount_value > Decimal("100"):
                raise ValueError(
                    "Percentage discount cannot exceed 100%."
                )

            discount = price * (
                discount_value / Decimal("100")
            )

        elif offer.discount_type == Offer.DiscountType.FIXED:
            discount = discount_value

        else:
            raise ValueError(
                f"Unsupported discount type: {offer.discount_type}"
            )

        # Never discount below zero.
        discount = min(discount, price)

        return discount.quantize(
            cls.MONEY_QUANT,
            rounding=ROUND_HALF_UP,
        )

    @classmethod
    def get_variant_pricing(cls, variant):
        """
        Return complete pricing information for a variant.

        The final offer price will never be lower than the
        variant's cost price.
        """
        original_price = Decimal(variant.price)

        if original_price < 0:
            raise ValueError("Variant price cannot be negative.")

        offer = cls.get_variant_offer(variant)

        if offer is None:
            return {
                "original_price": original_price,
                "discount_amount": Decimal("0.00"),
                "final_price": original_price,
                "offer": None,
            }

        discount_amount = cls.calculate_discount(
            price=original_price,
            offer=offer,
        )

        final_price = original_price - discount_amount

        # Safety check: never sell below cost price.
        if variant.cost_price is not None:
            cost_price = Decimal(variant.cost_price)

            if final_price < cost_price:
                return {
                    "original_price": original_price,
                    "discount_amount": Decimal("0.00"),
                    "final_price": original_price,
                    "offer": None,
                }

        final_price = final_price.quantize(
            cls.MONEY_QUANT,
            rounding=ROUND_HALF_UP,
        )

        return {
            "original_price": original_price,
            "discount_amount": discount_amount,
            "final_price": final_price,
            "offer": offer,
        }