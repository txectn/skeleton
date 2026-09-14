from celery import shared_task

from ..services.loginHistoryService import LoginHistoryService

@shared_task
def create_login_history(
    user_id,
    provider,
    provider_user,
    device,
    ip_address,
    success,
):
    LoginHistoryService.create(
        user_id=user_id,
        provider=provider,
        provider_user=provider_user,
        device=device,
        ip_address=ip_address,
        success=success,
    )