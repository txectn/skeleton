from django.urls import path

from ...views import (
    UserSummaryView,
    CustomersView,
) 

urlpatterns = [
    # User Summary
    path("account-summary/", UserSummaryView.as_view(), name="user-summary"),

    # Customers
    path("account-customers/", CustomersView.as_view(), name="customers"),
]