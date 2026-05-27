from fastapi import APIRouter

from app.core.config import settings
from app.schemas.base import APIResponse
from app.schemas.health import HealthData
from app.utils.responses import success_response

router = APIRouter()


@router.get("/health", response_model=APIResponse[HealthData])
async def health_check() -> APIResponse[HealthData]:
    return success_response(
        data=HealthData(status="ok", service="backend", environment=settings.app_env),
        message="Service is healthy.",
    )
