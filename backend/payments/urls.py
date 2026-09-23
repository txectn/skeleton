from django.urls import path

from .views import (
    PaymentView,
    PaymentWebhookView
)

urlpatterns = [
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),
]
