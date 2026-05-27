from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session, require_roles
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.summary import DailySummaryRead, GenerateSummaryRequest
from app.services.summary_service import SummaryService
from app.utils.responses import success_response

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post("/generate", response_model=APIResponse[DailySummaryRead])
async def generate_summary(
    payload: GenerateSummaryRequest,
    current_user: User = Depends(require_roles("owner", "admin")),
    db: Session = Depends(get_db_session),
) -> APIResponse[DailySummaryRead]:
    data = SummaryService(db).generate(current_user.business_id, payload.summary_date)
    return success_response(data=data, message="Daily summary generated.")


@router.get("", response_model=APIResponse[list[DailySummaryRead]])
async def list_summaries(
    limit: int = Query(default=30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[list[DailySummaryRead]]:
    data = SummaryService(db).list(current_user.business_id, limit)
    return success_response(data=data, message="Summaries loaded.")


@router.get("/{summary_date}", response_model=APIResponse[DailySummaryRead])
async def get_summary(
    summary_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[DailySummaryRead]:
    data = SummaryService(db).get_by_date(current_user.business_id, summary_date)
    return success_response(data=data, message="Summary loaded.")

