from django.urls import path

from .views import (
    PaymentView,
    PaymentWebhookView,
    BkashVerifyPaymentView,
    PaymentMethodChangeView
)

urlpatterns = [
    path("checkout/payment/", PaymentView.as_view(), name="checkout-payment"),
    path("payment/webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),
    path("bkash/verify-payment/", BkashVerifyPaymentView.as_view(), name="bkash-verify-payment"),
    path("change-payment-method/", PaymentMethodChangeView.as_view(), name="change-payment-method"),
]
