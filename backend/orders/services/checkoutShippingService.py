from decimal import Decimal

class CheckoutShippingService:

    @staticmethod
    def calculate_rates(
        *,
        items,
        profile,
    ):
        for item in items:
            cart_item = item["cart_item"]

            item["shipping"] = (
                CheckoutShippingService.calculate_rate(
                    variant=cart_item.variant,
                    profile=profile,
                )
            )

        return items

    @staticmethod
    def calculate_rate(
        *,
        variant,
        profile,
    ):
        shipping_class_rate = (
            variant.product.shipping_class_rates
        )

        if shipping_class_rate is None:
            return {
                "shipping_class": None,
                "rate": Decimal("0.00"),
            }

        shipping_class = (
            shipping_class_rate.shipping_class
        )

        shipping_zone = (
            shipping_class_rate.shipping_zone
        )

        # No shipping zone means use the flat rate.
        if shipping_zone is None:
            return {
                "shipping_class": shipping_class,
                "rate": (
                    shipping_class_rate.flat_rate
                    or Decimal("0.00")
                ),
            }

        inCountry = CheckoutShippingService.country_matches(
            profile=profile,
            shipping_zone=shipping_zone,
        )

        inRegion = CheckoutShippingService.region_matches(
            profile=profile,
            shipping_zone=shipping_zone,
        )
        
        if inCountry and inRegion:
            rate = shipping_class_rate.inner_zone_rate
            
        else:
            rate = shipping_class_rate.outer_zone_rate

        return {
            "shipping_class": shipping_class,
            "rate": rate or Decimal("0.00"),
        }

    @staticmethod
    def country_matches(
        *,
        profile,
        shipping_zone,
    ):
        return (
            profile.country.strip().lower()
            == shipping_zone.country.strip().lower()
        )

    @staticmethod
    def region_matches(
        *,
        profile,
        shipping_zone,
    ):
        return (
            bool(profile.region)
            and bool(shipping_zone.region)
            and profile.region.strip().lower()
            == shipping_zone.region.strip().lower()
        )

