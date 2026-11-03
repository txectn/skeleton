from django.urls import path

from .views import (
    ReturnRequestView,
    ReturnRequestCancelView,
    ReturnTokenActionView,
)

urlpatterns = [
    path("return-request/", ReturnRequestView.as_view(), name="return-request"),
    path("return-request/cancel/", ReturnRequestCancelView.as_view(), name="return-request-cancel"),
    path("action/<uuid:token>/", ReturnTokenActionView.as_view(), name="return-action-token"),
]
