from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_log import AILog, AILogStatus
from app.models.appointment import Appointment, AppointmentStatus
from app.models.follow_up import FollowUp, FollowUpStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.lead import Lead, LeadStatus
from app.models.message import Message
from app.services.twilio_service import TwilioService

from .state import MessageAgentState, SupportedIntent


class MessageAgentNodes:
    def __init__(self, db: Session) -> None:
        self.db = db

    def receive_message_node(self, state: MessageAgentState) -> MessageAgentState:
        message = self.db.scalar(select(Message).where(Message.id == state["message_id"]))
        if not message:
            return {**state, "error_message": "Message not found.", "requires_human_review": True}
        return {
            **state,
            "message_text": message.body,
            "customer_id": message.customer_id,
            "business_id": message.business_id,
            "ai_reasoning": "Inbound message loaded for workflow processing.",
        }

    def classify_intent_node(self, state: MessageAgentState) -> MessageAgentState:
        text = state.get("message_text", "").lower()
        intent: SupportedIntent = "unknown"
        confidence = 0.45

        keyword_map: list[tuple[SupportedIntent, list[str], float]] = [
            ("complaint", ["angry", "bad", "complaint", "unhappy", "refund"], 0.9),
            ("payment_issue", ["invoice", "paid", "payment", "overdue", "receipt"], 0.86),
            ("appointment_booking", ["appointment", "book", "schedule", "slot", "available"], 0.84),
            ("pricing_inquiry", ["price", "cost", "rate", "quote", "how much"], 0.82),
            ("sales_lead", ["interested", "buy", "package", "plan", "service"], 0.78),
            ("support_request", ["help", "issue", "problem", "support", "broken"], 0.76),
            ("follow_up_response", ["following up", "checking", "yes", "no", "later"], 0.68),
            ("general_question", ["what", "when", "where", "how"], 0.66),
        ]
        for candidate, keywords, score in keyword_map:
            if any(keyword in text for keyword in keywords):
                intent = candidate
                confidence = score
                break

        return {
            **state,
            "intent": intent,
            "confidence_score": confidence,
            "ai_reasoning": f"Intent classified as {intent} with confidence {confidence:.2f}.",
        }

    def customer_lookup_node(self, state: MessageAgentState) -> MessageAgentState:
        if state.get("customer_id"):
            return {**state, "ai_reasoning": state.get("ai_reasoning", "") + " Customer linked."}
        return {
            **state,
            "requires_human_review": True,
            "ai_reasoning": state.get("ai_reasoning", "") + " Customer missing; human review required.",
        }

    def ai_response_generation_node(self, state: MessageAgentState) -> MessageAgentState:
        intent = state.get("intent", "unknown")
        reply = self._openai_reply(intent, state.get("message_text", "")) or self._fallback_reply(
            intent,
            state.get("message_text", ""),
        )
        return {
            **state,
            "suggested_reply": reply,
            "ai_reasoning": state.get("ai_reasoning", "") + " Reply generated.",
        }

    def action_decision_node(self, state: MessageAgentState) -> MessageAgentState:
        intent = state.get("intent", "unknown")
        confidence = state.get("confidence_score", 0)
        requires_review = confidence < settings.ai_low_confidence_threshold or intent in {
            "complaint",
            "unknown",
        }
        action_map = {
            "payment_issue": "lookup_invoice",
            "appointment_booking": "schedule_appointment",
            "sales_lead": "update_crm",
            "pricing_inquiry": "create_follow_up",
            "complaint": "priority_escalation",
        }
        return {
            **state,
            "action_required": action_map.get(intent),
            "follow_up_required": intent in {"pricing_inquiry", "sales_lead", "support_request", "complaint"},
            "requires_human_review": requires_review,
            "ai_reasoning": state.get("ai_reasoning", "") + " Action decision completed.",
        }

    def follow_up_creation_node(self, state: MessageAgentState) -> MessageAgentState:
        lead_id = state.get("lead_id")
        if state.get("intent") in {"sales_lead", "pricing_inquiry"} and state.get("customer_id"):
            lead = Lead(
                business_id=state["business_id"],
                customer_id=state["customer_id"],
                title=f"WhatsApp {state.get('intent', 'lead').replace('_', ' ')}",
                status=LeadStatus.interested.value,
                source="whatsapp",
                priority_score=int((state.get("confidence_score") or 0) * 100),
                notes=state.get("message_text"),
            )
            self.db.add(lead)
            self.db.flush()
            lead_id = lead.id

        if not state.get("follow_up_required") or not state.get("customer_id"):
            return {**state, "lead_id": lead_id}

        follow_up = FollowUp(
            business_id=state["business_id"],
            customer_id=state["customer_id"],
            lead_id=lead_id,
            status=FollowUpStatus.scheduled.value,
            title=f"Review {state.get('intent', 'customer')} conversation",
            notes=state.get("suggested_reply"),
            due_at=datetime.utcnow() + timedelta(days=1),
        )
        self.db.add(follow_up)
        self.db.flush()
        return {**state, "follow_up_id": follow_up.id, "lead_id": lead_id}

    def payment_reminder_node(self, state: MessageAgentState) -> MessageAgentState:
        if state.get("intent") != "payment_issue" or not state.get("customer_id"):
            return state

        invoice = self.db.scalar(
            select(Invoice)
            .where(
                Invoice.business_id == state["business_id"],
                Invoice.customer_id == state["customer_id"],
                Invoice.status.in_([InvoiceStatus.sent.value, InvoiceStatus.overdue.value]),
            )
            .order_by(Invoice.due_at.asc())
        )
        invoice_data = None
        if invoice:
            invoice_data = {
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "status": invoice.status,
                "amount_cents": invoice.amount_cents,
            }
        return {**state, "invoice_data": invoice_data}

    def appointment_scheduler_node(self, state: MessageAgentState) -> MessageAgentState:
        if state.get("intent") != "appointment_booking" or not state.get("customer_id"):
            return state

        appointment = Appointment(
            business_id=state["business_id"],
            customer_id=state["customer_id"],
            title="Appointment request from WhatsApp",
            status=AppointmentStatus.scheduled.value,
            starts_at=datetime.utcnow() + timedelta(days=1),
            ends_at=datetime.utcnow() + timedelta(days=1, hours=1),
            notes="Auto-created placeholder from customer request. Confirm exact time with customer.",
        )
        self.db.add(appointment)
        self.db.flush()
        return {
            **state,
            "appointment_data": {
                "appointment_id": appointment.id,
                "status": appointment.status,
                "starts_at": appointment.starts_at.isoformat(),
            },
        }

    def human_review_node(self, state: MessageAgentState) -> MessageAgentState:
        if state.get("requires_human_review"):
            return {
                **state,
                "suggested_reply": state.get("suggested_reply")
                or "Thanks for your message. Our team will review this and follow up shortly.",
            }
        return state

    def send_reply_node(self, state: MessageAgentState) -> MessageAgentState:
        if state.get("requires_human_review") or not settings.ai_auto_reply_enabled:
            return state
        if not state.get("customer_id") or not state.get("suggested_reply"):
            return state

        sent = TwilioService(self.db).send_whatsapp_message(
            business_id=state["business_id"],
            customer_id=state["customer_id"],
            body=state["suggested_reply"],
        )
        return {**state, "sent_message_id": sent.id}

    def log_activity_node(self, state: MessageAgentState) -> MessageAgentState:
        status = AILogStatus.human_review.value if state.get("requires_human_review") else AILogStatus.success.value
        if state.get("error_message"):
            status = AILogStatus.failed.value

        self.db.add(
            AILog(
                business_id=state["business_id"],
                customer_id=state.get("customer_id"),
                lead_id=state.get("lead_id"),
                message_id=state.get("message_id"),
                workflow_name="customer_message_agent",
                node_name="log_activity_node",
                status=status,
                input_payload={"message_text": state.get("message_text")},
                output_payload=self._serializable_state(state),
                reasoning=state.get("ai_reasoning"),
                error_message=state.get("error_message"),
            )
        )
        self.db.commit()
        return state

    def _fallback_reply(self, intent: str, message_text: str) -> str:
        replies = {
            "pricing_inquiry": "Thanks for reaching out. I can help with pricing. Could you share which service or package you are interested in?",
            "sales_lead": "Thanks for your interest. I can help you choose the right option. What outcome are you looking for?",
            "support_request": "Thanks for the details. Our team can help with this. Could you share any extra context or photos if relevant?",
            "appointment_booking": "Yes, we can help schedule an appointment. What day and time works best for you?",
            "payment_issue": "Thanks for checking in. I will review the invoice/payment details and follow up with the next step.",
            "follow_up_response": "Thanks for the update. I have noted your response and we will follow up if anything else is needed.",
            "complaint": "I am sorry about that experience. I am escalating this for review so the team can follow up carefully.",
            "general_question": "Thanks for your message. I can help with that. Could you share one more detail so we can respond accurately?",
            "unknown": "Thanks for your message. Our team will review this and follow up shortly.",
        }
        return replies.get(intent, replies["unknown"])[:1500]

    def _openai_reply(self, intent: str, message_text: str) -> str | None:
        if not settings.openai_api_key:
            return None
        for _attempt in range(2):
            try:
                from langchain_openai import ChatOpenAI

                model = ChatOpenAI(
                    model=settings.openai_model,
                    api_key=settings.openai_api_key,
                    temperature=0.2,
                )
                response = model.invoke(
                    [
                        (
                            "system",
                            "You draft concise WhatsApp replies for small businesses. Return only the reply text.",
                        ),
                        ("human", f"Intent: {intent}\nCustomer message: {message_text}"),
                    ]
                )
                content = response.content if isinstance(response.content, str) else str(response.content)
                return content.strip()[:1500] or None
            except Exception:
                continue
        return None

    def _serializable_state(self, state: MessageAgentState) -> dict[str, Any]:
        return {key: value for key, value in state.items() if isinstance(value, (str, int, float, bool, list, dict, type(None)))}
