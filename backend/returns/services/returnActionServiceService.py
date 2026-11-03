from django.db import transaction

from django.utils import timezone

from rest_framework.exceptions import ValidationError

from ..models import ReturnRequest, ReturnPolicy, ReturnActionToken

from siteConfig.models import SiteSetting

from metrics.tasks import update_analytical_metrics

class ReturnActionService:
    @staticmethod
    def get_Return_Data(token):
        # Validate token And Get Action Model Instance
        try:
            action_token = ReturnActionToken.objects.select_related(
                "return_request"
            ).get(token=token)

        except ReturnActionToken.DoesNotExist:
            raise ValidationError({
                "message": "Token does not exist.",
            })

        if not action_token.is_valid:
            raise ValidationError({
                "message": "Invalid token.",
            })

        # Get Return Request Decision Options
        decision_options = [
            {
                "value": value,
                "label": label,
            }
            for value, label in ReturnRequest.Decision.choices
        ]

        site_setting = SiteSetting.objects.first()

        currency = {
            "symbol": site_setting.default_currency.symbol,
            "code": site_setting.default_currency.code,
            "name": site_setting.default_currency.name,
        }

        return {
            "order_id": action_token.return_request.order_id,
            "order_total": action_token.return_request.order.total,
            "currency": currency,
            "return_request_id": action_token.return_request_id,
            "status_options": [
                {
                    "value": "inspecting",
                    "label": "Inspecting",
                },
                {
                    "value": "returning",
                    "label": "Returning",
                },
                {
                    "value": "completed",
                    "label": "Completed",
                },
                {
                    "value": "failed",
                    "label": "Failed",
                }
            ],
            "decision_options": [
                {
                    "value": "business_fault",
                    "label": "Business Fault"
                },
                {
                    "value": "customer_return",
                    "label": "Customer Return"
                },
                {
                    "value": "invalid_return",
                    "label": "Invalid Return"
                },
                {
                    "value": "customer_cancelled",
                    "label": "Customer Cancelled"
                }
            ],
            # "decision_options": decision_options,
            "reason": action_token.return_request.reason,
            "status": action_token.return_request.status,
            "decision": action_token.return_request.decision,
            "customer_note": action_token.return_request.customer_note,
            "inspector_note": action_token.return_request.inspector_note,
            "return_charge": action_token.return_request.return_charge or 0,
            "refund_amount": action_token.return_request.refund_amount or 0,
        }
    
    @staticmethod
    @transaction.atomic
    def update_Return_Request(token, data):
        # 1. Get and lock the token
        try:
            action_token = (
                ReturnActionToken.objects
                .select_for_update()
                .select_related("return_request__order")
                .get(token=token)
            )
        except ReturnActionToken.DoesNotExist:
            raise ValidationError({
                "message": "Token does not exist.",
            })

        # 2. Validate token
        if not action_token.is_valid:
            raise ValidationError({
                "message": "Invalid token.",
            })

        return_request = action_token.return_request
        update_fields = []

        # 3. Update status only if provided
        if "status" in data:
            status = data["status"]

            allowed_statuses = [
                "inspecting",
                "returning",
                "completed",
                "failed",
            ]

            if status not in allowed_statuses:
                raise ValidationError({
                    "status": "Invalid status.",
                })

            return_request.status = status
            update_fields.append("status")

        # 4. Update decision only if provided
        if "decision" in data:
            decision = data["decision"]

            if decision not in ReturnRequest.Decision.values:
                raise ValidationError({
                    "decision": "Invalid decision.",
                })

            if decision == ReturnRequest.Decision.PENDING:
                raise ValidationError({
                    "decision": "Please select a valid decision.",
                })

            return_request.decision = decision
            update_fields.append("decision")

        # 5. Update inspector note only if provided
        if "inspector_note" in data:
            return_request.inspector_note = data["inspector_note"]
            update_fields.append("inspector_note")

        # 6. Calculate return charge and refund amount
        if return_request.status == "completed":

            # Decision is required before completing
            if return_request.decision == ReturnRequest.Decision.PENDING:
                raise ValidationError({
                    "decision": "Please select a valid decision before completing the return.",
                })

            order_total = return_request.order.total

            return_charge = 0
            refund_amount = 0

            if return_request.decision == ReturnRequest.Decision.BUSINESS_FAULT:
                refund_amount = order_total

            elif return_request.decision == ReturnRequest.Decision.CUSTOMER_RETURN:
                policy = ReturnPolicy.objects.filter(
                    is_active=True
                ).first()

                if not policy:
                    raise ValidationError({
                        "message": "No active return policy found.",
                    })

                return_charge = policy.customer_return_charge
                refund_amount = max(order_total - return_charge, 0)

            elif return_request.decision in [
                ReturnRequest.Decision.INVALID_RETURN,
                ReturnRequest.Decision.CUSTOMER_CANCELLED,
            ]:
                return_charge = 0
                refund_amount = 0

            return_request.return_charge = return_charge
            return_request.refund_amount = refund_amount

            update_fields.extend([
                "return_charge",
                "refund_amount",
            ])

        # 7. Save only if at least one field was provided
        if update_fields:
            update_fields.append("updated_at")

            return_request.save(
                update_fields=list(set(update_fields))
            )

            # 8. Consume token when workflow is finished
            if return_request.status in ["completed", "failed"]:
                action_token.used_at = timezone.now()
                action_token.save(update_fields=["used_at"])

        site_setting = SiteSetting.objects.first()

        currency = {
            "symbol": site_setting.default_currency.symbol,
            "code": site_setting.default_currency.code,
            "name": site_setting.default_currency.name,
        }

        update_analytical_metrics.delay(return_request.order.id)

        # 9. Return updated data
        return {
            "message": "Return request updated successfully.",
            "currency": currency,
            "return_request_id": return_request.id,
            "status": return_request.status,
            "decision": return_request.decision,
            "inspector_note": return_request.inspector_note,
            "order_total": return_request.order.total,
            "refund_amount": return_request.refund_amount,
            "return_charge": return_request.return_charge,
        }




