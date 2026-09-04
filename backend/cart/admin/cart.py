from django.contrib import admin
from django import forms
from unfold.admin import (
    ModelAdmin, 
    TabularInline
)

from ..models import (
    Cart, 
    CartItem,
)

class CartItemInline(TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "cart_token",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "cart_token",
        "user__email",
    )

    readonly_fields = (
        "cart_token",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    list_per_page = 50

    inlines = (
        CartItemInline,    
    )