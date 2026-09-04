from django.urls import path

from .views import (
    CartView, 
    CartItemView,
    CartItemDecreaseQuantityView,
    CartItemUpdateQuantityView,
    CartItemRemoveView,
    CartClearView
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/item/", CartItemView.as_view(), name="cart-item"),
    path("cart/item/decrease/", CartItemDecreaseQuantityView.as_view(), name="cart-item-decrease"),
    path("cart/item/update/", CartItemUpdateQuantityView.as_view(), name="cart-item-update"),
    path("cart/item/remove/", CartItemRemoveView.as_view(), name="cart-item-remove"),
    path("cart/clear/", CartClearView.as_view(), name="cart-clear"),
]