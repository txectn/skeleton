from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import CartItem

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = (
        "id",
        "cart",
        "variant",
        "quantity",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "cart__user__email",
        "cart__cart_token",
        "variant__sku",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_per_page = 50