from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.models.lead import LeadStatus
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.lead import LeadCreate, LeadRead, LeadUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.crm_service import CRMService
from app.utils.responses import success_response

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=APIResponse[PaginatedResponse[LeadRead]])
async def list_leads(
    search: str | None = None,
    status_filter: LeadStatus | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[PaginatedResponse[LeadRead]]:
    data = CRMService(db).list_leads(
        business_id=current_user.business_id,
        search=search,
        lead_status=status_filter.value if status_filter else None,
        page=page,
        page_size=page_size,
    )
    return success_response(data=data, message="Leads loaded.")


@router.post("", response_model=APIResponse[LeadRead], status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[LeadRead]:
    data = CRMService(db).create_lead(current_user.business_id, payload)
    return success_response(data=data, message="Lead created.")


@router.get("/{lead_id}", response_model=APIResponse[LeadRead])
async def get_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[LeadRead]:
    data = CRMService(db).get_lead(current_user.business_id, lead_id)
    return success_response(data=data, message="Lead loaded.")


@router.put("/{lead_id}", response_model=APIResponse[LeadRead])
async def update_lead(
    lead_id: str,
    payload: LeadUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[LeadRead]:
    data = CRMService(db).update_lead(current_user.business_id, lead_id, payload)
    return success_response(data=data, message="Lead updated.")


@router.delete("/{lead_id}", response_model=APIResponse[None])
async def delete_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[None]:
    CRMService(db).delete_lead(current_user.business_id, lead_id)
    return success_response(data=None, message="Lead deleted.")

