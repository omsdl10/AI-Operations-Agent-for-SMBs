from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.config import settings
from app.schemas.base import APIResponse
from app.schemas.message import MessageRead, TwilioWebhookResponse
from app.services.agent_service import AgentService
from app.services.twilio_service import TwilioService
from app.utils.responses import success_response

router = APIRouter(prefix="/twilio", tags=["twilio"])


@router.post("/webhook", response_model=APIResponse[TwilioWebhookResponse])
async def whatsapp_webhook(
    From: str = Form(default=""),
    Body: str = Form(default=""),
    MessageSid: str = Form(default=""),
    db: Session = Depends(get_db_session),
) -> APIResponse[TwilioWebhookResponse]:
    message = TwilioService(db).store_inbound_message(
        from_number=From,
        body=Body,
        external_id=MessageSid,
    )
    if settings.ai_auto_reply_enabled:
        AgentService(db).run_message_agent(message.id)
    return success_response(
        data=TwilioWebhookResponse(stored=True, message_id=message.id),
        message="Inbound WhatsApp message stored.",
    )


@router.post("/status", response_model=APIResponse[TwilioWebhookResponse])
async def whatsapp_status_callback(
    MessageSid: str = Form(default=""),
    MessageStatus: str = Form(default=""),
    db: Session = Depends(get_db_session),
) -> APIResponse[TwilioWebhookResponse]:
    updated = TwilioService(db).update_message_status(MessageSid, MessageStatus)
    return success_response(
        data=TwilioWebhookResponse(stored=updated, message_id=None),
        message="Message status processed.",
    )


@router.post("/mock-inbound", response_model=APIResponse[MessageRead])
async def mock_inbound_message(
    from_number: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db_session),
) -> APIResponse[MessageRead]:
    data = TwilioService(db).store_inbound_message(
        from_number=from_number,
        body=body,
        external_id=None,
    )
    if settings.ai_auto_reply_enabled:
        AgentService(db).run_message_agent(data.id)
    return success_response(data=data, message="Mock inbound message stored.")
