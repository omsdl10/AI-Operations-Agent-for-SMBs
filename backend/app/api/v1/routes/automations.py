from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session, require_roles
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas.base import APIResponse
from app.schemas.notification import AutomationRunResult, NotificationRead
from app.services.automation_service import AutomationService
from app.utils.responses import success_response

router = APIRouter(prefix="/automations", tags=["automations"])


@router.post("/run-due", response_model=APIResponse[AutomationRunResult])
async def run_due_automations(
    current_user: User = Depends(require_roles("owner", "admin")),
    db: Session = Depends(get_db_session),
) -> APIResponse[AutomationRunResult]:
    data = AutomationService(db).run_due_automations()
    return success_response(data=data, message="Automation cycle completed.")


@router.get("/notifications", response_model=APIResponse[list[NotificationRead]])
async def list_notifications(
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[list[NotificationRead]]:
    notifications = NotificationRepository(db).list_for_business(current_user.business_id, limit=limit)
    data = [NotificationRead.model_validate(notification) for notification in notifications]
    return success_response(data=data, message="Notifications loaded.")

