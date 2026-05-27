from typing import Any, Literal, TypedDict

SupportedIntent = Literal[
    "pricing_inquiry",
    "sales_lead",
    "support_request",
    "appointment_booking",
    "payment_issue",
    "follow_up_response",
    "complaint",
    "general_question",
    "unknown",
]


class MessageAgentState(TypedDict, total=False):
    message_id: str
    message_text: str
    customer_id: str | None
    business_id: str
    intent: SupportedIntent
    confidence_score: float
    suggested_reply: str
    action_required: str | None
    follow_up_required: bool
    follow_up_id: str | None
    lead_id: str | None
    appointment_data: dict[str, Any] | None
    invoice_data: dict[str, Any] | None
    requires_human_review: bool
    ai_reasoning: str
    sent_message_id: str | None
    error_message: str | None
