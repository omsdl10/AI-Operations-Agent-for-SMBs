from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.models.user import User
from app.schemas.base import APIResponse
from app.schemas.message import ConversationRead, MessageRead, SendMessageRequest
from app.services.twilio_service import TwilioService
from app.utils.responses import success_response

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/conversations", response_model=APIResponse[list[ConversationRead]])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[list[ConversationRead]]:
    data = TwilioService(db).list_conversations(current_user.business_id)
    return success_response(data=data, message="Conversations loaded.")


@router.get("/conversations/{customer_id}", response_model=APIResponse[list[MessageRead]])
async def list_conversation_messages(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[list[MessageRead]]:
    data = TwilioService(db).list_conversation_messages(current_user.business_id, customer_id)
    return success_response(data=data, message="Conversation messages loaded.")


@router.post("/send", response_model=APIResponse[MessageRead])
async def send_message(
    payload: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> APIResponse[MessageRead]:
    data = TwilioService(db).send_whatsapp_message(
        business_id=current_user.business_id,
        customer_id=payload.customer_id,
        body=payload.body,
    )
    return success_response(data=data, message="Message sent.")

