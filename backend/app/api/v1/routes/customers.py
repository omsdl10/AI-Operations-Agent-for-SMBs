from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.crm_service import CRMService
from app.utils.responses import success_response

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=APIResponse[PaginatedResponse[CustomerRead]])
async def list_customers(
    search: str | None = None,
    tag: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[PaginatedResponse[CustomerRead]]:
    data = CRMService(db).list_customers(
        business_id=current_user.business_id,
        search=search,
        tag=tag,
        page=page,
        page_size=page_size,
    )
    return success_response(data=data, message="Customers loaded.")


@router.post("", response_model=APIResponse[CustomerRead], status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[CustomerRead]:
    data = CRMService(db).create_customer(current_user.business_id, payload)
    return success_response(data=data, message="Customer created.")


@router.get("/{customer_id}", response_model=APIResponse[CustomerRead])
async def get_customer(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[CustomerRead]:
    data = CRMService(db).get_customer(current_user.business_id, customer_id)
    return success_response(data=data, message="Customer loaded.")


@router.put("/{customer_id}", response_model=APIResponse[CustomerRead])
async def update_customer(
    customer_id: str,
    payload: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[CustomerRead]:
    data = CRMService(db).update_customer(current_user.business_id, customer_id, payload)
    return success_response(data=data, message="Customer updated.")


@router.delete("/{customer_id}", response_model=APIResponse[None])
async def delete_customer(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[None]:
    CRMService(db).delete_customer(current_user.business_id, customer_id)
    return success_response(data=None, message="Customer deleted.")

