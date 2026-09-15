from django.urls import path

from .views import (
    QuantityValidatorView
)

urlpatterns = [
    path("validate-quantity/", QuantityValidatorView.as_view(), name="validate-quantity"),
]
