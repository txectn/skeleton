from rest_framework.exceptions import ValidationError

from datetime import timedelta
from django.utils import timezone

from ..models import ReturnRequest, ReturnPolicy

class ReturnRequestService:

    @staticmethod
    def create(user, data):

        # Get order
        order = data["order"]

        # Check if order belongs to user
        if order.user_id != user.id:
            raise ValidationError(
                {
                    "message": "This order does not belong to you.",
                }
            )

        # Check if order has been delivered
        if order.status != order.Status.DELIVERED:
            raise ValidationError(
                {
                    "message": "This order has not been delivered yet.",
                    "order_id": order.id,
                    "order_status": order.status,
                }
            )

        # Get active return policy
        policy = ReturnPolicy.objects.filter(
            is_active=True,
        ).first()

        if not policy:
            raise ValidationError(
                {
                    "message": "No active return policy is configured.",
                }
            )

        # Check return window
        deadline = order.updated_at + timedelta(
            days=policy.return_window_days,
        )

        if timezone.now() > deadline:
            raise ValidationError(
                {
                    "message": "The return window has expired.",
                    "order_id": order.id,
                    "order_status": order.status,
                    "deadline": deadline,
                }
            )

        # Check if an active return request already exists
        existing_request = ReturnRequest.objects.filter(
            order=order,
        ).exclude(
            status=ReturnRequest.Status.CANCELLED,
        ).first()

        if existing_request:
            raise ValidationError(
                {
                    "message": "A return request already exists for this order.",
                    "return_request_id": existing_request.id,
                    "return_status": existing_request.status,
                    "return_decision": existing_request.decision,
                    "order_total": existing_request.order.total,
                    "refund_amount": existing_request.refund_amount,
                    "return_charge": existing_request.return_charge,
                }
            )

        # Get return reason
        reason = data["reason"]

        # Check return reasons

        if reason == ReturnRequest.Reason.CHANGED_MIND:
            if not policy.allow_changed_mind:
                raise ValidationError(
                    {
                        "message": "Returns for changed mind are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_customer_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
                policy=policy,
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.ORDERED_BY_MISTAKE:
            if not policy.allow_ordered_by_mistake:
                raise ValidationError(
                    {
                        "message": "Returns for orders placed by mistake are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_customer_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
                policy=policy,
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.WRONG_PRODUCT:
            if not policy.allow_wrong_product:
                raise ValidationError(
                    {
                        "message": "Returns for wrong products are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.DAMAGED:
            if not policy.allow_damaged:
                raise ValidationError(
                    {
                        "message": "Returns for damaged products are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.FAKE:
            if not policy.allow_fake:
                raise ValidationError(
                    {
                        "message": "Returns for fake or unauthentic products are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.NOT_AS_DESCRIBED:
            if not policy.allow_not_as_described:
                raise ValidationError(
                    {
                        "message": "Returns for products not as described are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.MISSING_ITEM:
            if not policy.allow_missing_item:
                raise ValidationError(
                    {
                        "message": "Returns for missing items are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

        if reason == ReturnRequest.Reason.OTHER:
            if not policy.allow_other:
                raise ValidationError(
                    {
                        "message": "Other return reasons are not allowed.",
                    }
                )

            return_request = ReturnRequestService._create_business_fault_return(
                order=order,
                reason=reason,
                customer_note=data.get("customer_note", ""),
            )

            return ReturnRequestService._success_response(return_request)

    @staticmethod
    def _create_customer_return(
        order,
        reason,
        customer_note,
        policy,
    ):
        return ReturnRequest.objects.create(
            order=order,
            status=ReturnRequest.Status.PENDING,
            reason=reason,
            customer_note=customer_note,
            decision=ReturnRequest.Decision.CUSTOMER_RETURN,
            return_charge=policy.customer_return_charge,
            refund_amount=order.total - policy.customer_return_charge,
        )

    @staticmethod
    def _create_business_fault_return(
        order,
        reason,
        customer_note,
    ):
        return ReturnRequest.objects.create(
            order=order,
            status=ReturnRequest.Status.PENDING,
            reason=reason,
            customer_note=customer_note,
            decision=ReturnRequest.Decision.PENDING,
            return_charge=0,
            refund_amount=order.total,
        )

    @staticmethod
    def _success_response(return_request):
        return {
            "message": "Return request created successfully.",
            "return_request_id": return_request.id,
            "return_status": return_request.status,
            "return_decision": return_request.decision,
            "order_total": return_request.order.total,
            "refund_amount": return_request.refund_amount,
            "return_charge": return_request.return_charge,
        }