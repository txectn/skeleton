from django.urls import path

from .views import (
    CheckoutReviewView,
    OrderView
) 

urlpatterns = [
    path("checkout/review/", CheckoutReviewView.as_view(), name="checkout"),
    path("order/", OrderView.as_view(), name="order"),
]