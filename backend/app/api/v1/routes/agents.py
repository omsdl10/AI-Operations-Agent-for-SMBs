from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.models.user import User
from app.repositories.message_repository import MessageRepository
from app.schemas.agent import MessageAgentResult
from app.schemas.base import APIResponse
from app.services.agent_service import AgentService
from app.utils.responses import success_response
from app.core.exceptions import AppException

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/messages/{message_id}/run", response_model=APIResponse[MessageAgentResult])
async def run_message_agent(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[MessageAgentResult]:
    message = MessageRepository(db).get_by_id(message_id)
    if not message or message.business_id != current_user.business_id:
        raise AppException("Message not found.", 404, "message_not_found")

    result = AgentService(db).run_message_agent(message_id)
    return success_response(
        data=MessageAgentResult(**result),
        message="Message agent workflow completed.",
    )

