from django.urls import path

from .views import (
    PaymentView,
    PaymentWebhookView
)

urlpatterns = [
    path("checkout/payment/", PaymentView.as_view(), name="checkout-payment"),
    path("payment/webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),
]
