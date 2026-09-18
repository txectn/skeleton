from django.urls import path

from .views import CheckoutReviewView

urlpatterns = [
    path("checkout/review/", CheckoutReviewView.as_view(), name="checkout"),
]