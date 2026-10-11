from django.urls import path

from .views import (
    ReturnRequestView,
    ReturnRequestCancelView,
)

urlpatterns = [
    path("return-request/", ReturnRequestView.as_view(), name="return-request"),
    path("return-request/cancel/", ReturnRequestCancelView.as_view(), name="return-request-cancel"),
]
