from django.contrib import admin

from .models import Payment, PaymentAttempt

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "method",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "method",
        "status",
    )

    search_fields = (
        "order__id",
        "order__user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "payment",
        "provider",
        "status",
        "transaction_id",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "provider",
        "status",
    )

    search_fields = (
        "transaction_id",
        "payment__order__id",
        "payment__order__user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )