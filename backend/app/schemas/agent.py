from typing import Any

from pydantic import BaseModel


class MessageAgentResult(BaseModel):
    message_id: str | None = None
    intent: str | None = None
    confidence_score: float | None = None
    suggested_reply: str | None = None
    action_required: str | None = None
    follow_up_required: bool | None = None
    follow_up_id: str | None = None
    lead_id: str | None = None
    appointment_data: dict[str, Any] | None = None
    invoice_data: dict[str, Any] | None = None
    requires_human_review: bool | None = None
    sent_message_id: str | None = None
    ai_reasoning: str | None = None
    error_message: str | None = None
