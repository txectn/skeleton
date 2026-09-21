from decimal import Decimal

from rest_framework.exceptions import ValidationError

class OrderShippingService:
    @staticmethod
    def get_shipping_information(user):

        profile = user.profile

        if any(
            not value
            for value in (
                profile.country,
                profile.region,
                profile.city,
                profile.address,
                profile.phone_number,
            )
        ):
            raise ValidationError(
                {
                    "shipping": (
                        "Profile is not complete. "
                        "Please update your profile."
                    )
                }
            )

        return {
            "shipping_address": profile.address,
            "shipping_city": profile.city,
            "shipping_region": profile.region,
            "shipping_country": profile.country,
            "phone_number": profile.phone_number,
        }

    @staticmethod
    def calculate(order):

        shipping_country = order.shipping_country
        shipping_region = order.shipping_region
        shipping_city = order.shipping_city
        shipping_address = order.shipping_address
        phone_number = order.phone_number

        # ---------------------------------------------------------
        # Validate shipping information
        # ---------------------------------------------------------

        if any(
            not value
            for value in (
                shipping_country,
                shipping_region,
                shipping_city,
                shipping_address,
                phone_number,
            )
        ):
            raise ValidationError(
                {
                    "shipping": (
                        "Shipping information is incomplete. "
                        "Please update your shipping information."
                    )
                }
            )

        # ---------------------------------------------------------
        # Calculate shipping for each OrderItem
        # ---------------------------------------------------------

        shipping_rates = []

        for order_item in order.items.select_related(
            "variant__product",
        ):
            shipping_class_rate = (
                order_item.variant.product.shipping_class_rates
            )

            if shipping_class_rate is None:
                rate = Decimal("0.00")

            else:
                shipping_zone = (
                    shipping_class_rate.shipping_zone
                )

                # No shipping zone means use the flat rate.
                if shipping_zone is None:
                    rate = (
                        shipping_class_rate.flat_rate
                        or Decimal("0.00")
                    )

                else:
                    country_matches = (
                        shipping_country.strip().lower()
                        == shipping_zone.country.strip().lower()
                    )

                    if not country_matches:
                        raise ValidationError(
                            {
                                "shipping": (
                                    "Shipping is not available "
                                    "to your country."
                                )
                            }
                        )

                    region_matches = (
                        bool(shipping_region)
                        and bool(shipping_zone.region)
                        and shipping_region.strip().lower()
                        == shipping_zone.region.strip().lower()
                    )

                    if country_matches and region_matches:
                        rate = (
                            shipping_class_rate.inner_zone_rate
                        )
                    else:
                        rate = (
                            shipping_class_rate.outer_zone_rate
                        )

                    rate = rate or Decimal("0.00")

            shipping_rates.append(rate)

        # ---------------------------------------------------------
        # Final Order Shipping
        # ---------------------------------------------------------

        if not shipping_rates:
            return Decimal("0.00")

        return max(shipping_rates)

