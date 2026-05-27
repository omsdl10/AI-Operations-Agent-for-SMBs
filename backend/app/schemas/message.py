from datetime import datetime

from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: str
    business_id: str
    customer_id: str | None
    direction: str
    channel: str
    status: str
    body: str
    external_id: str | None
    sent_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationRead(BaseModel):
    customer_id: str
    customer_name: str
    phone: str | None
    last_message: str
    last_message_at: datetime
    unread_count: int
    status: str


class SendMessageRequest(BaseModel):
    customer_id: str
    body: str = Field(..., min_length=1, max_length=1600)


class TwilioWebhookResponse(BaseModel):
    stored: bool
    message_id: str | None = None

