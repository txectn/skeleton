from rest_framework.exceptions import ValidationError

from ..models import ReturnRequest

class ReturnRequestCancelService:

    @staticmethod
    def cancel(user, data):

        return_request = data["return_request"]

        # Check ownership
        if return_request.order.user_id != user.id:
            raise ValidationError(
                {
                    "message": "This return request does not belong to you.",
                }
            )

        # Check if cancellation is allowed
        if return_request.status not in [
            ReturnRequest.Status.PENDING,
            ReturnRequest.Status.PREPARING,
        ]:
            raise ValidationError(
                {
                    "message": "This return request cannot be cancelled.",
                    "return_request_id": return_request.id,
                    "return_status": return_request.status,
                }
            )

        # Cancel return request
        return_request.status = ReturnRequest.Status.CANCELLED
        return_request.decision = ReturnRequest.Decision.CUSTOMER_CANCELLED
        return_request.money_refund_status = (
            ReturnRequest.MoneyRefundStatus.REFUND_CANCELLED
        )

        return_request.save(
            update_fields=[
                "status",
                "decision",
                "money_refund_status",
                "updated_at",
            ],
        )

        return {
            "message": "Return request cancelled successfully.",
            "return_request_id": return_request.id,
            "return_status": return_request.status,
            "return_decision": return_request.decision,
        }