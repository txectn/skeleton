from celery import shared_task

from ..services import (
    GuestCartCleanupWorkerService,
)

@shared_task
def cleanup_guest_carts():
    return GuestCartCleanupWorkerService.cleanup()