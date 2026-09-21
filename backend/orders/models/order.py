from django.conf import settings
from django.db import models

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    shipping = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Snapshot of customer's delivery information
    shipping_country = models.CharField(
        max_length=100,
    )

    shipping_region = models.CharField(
        max_length=100,
        blank=True,
    )

    shipping_city = models.CharField(
        max_length=100,
    )

    shipping_address = models.TextField()

    phone_number = models.CharField(
        max_length=30,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )



'''
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    shipping = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Snapshot of customer's delivery information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_region = models.CharField(
        max_length=100,
        blank=True,
    )
    shipping_country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)











class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        "products.Variant",
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    product_name = models.CharField(
        max_length=255,
    )

    variant_name = models.CharField(
        max_length=255,
        blank=True,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )









    




OrderService.create_order()
        │
        ├── 1. Get checkout items
        │
        ├── 2. Validate items / quantities
        │
        ├── 3. Validate profile / shipping information
        │
        ├── 4. Create Order object
        │
        ├── 5. For each item
        │      │
        │      ├── OrderPromotionService
        │      │       └── PromotionService
        │      │
        │      └── OrderItemService
        │              └── create OrderItem snapshot
        │
        ├── 6. OrderShippingService
        │      └── calculate shipping
        │
        ├── 7. OrderPriceService
        │      └── calculate subtotal / discount / total
        │
        ├── 8. Save final Order totals
        │
        └── 9. Return Order
'''