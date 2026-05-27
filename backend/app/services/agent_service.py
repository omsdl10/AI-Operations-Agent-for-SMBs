from typing import Any

from sqlalchemy.orm import Session

from app.agents.message_agent.workflow import MessageAgentWorkflow


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def run_message_agent(self, message_id: str) -> dict[str, Any]:
        state = MessageAgentWorkflow(self.db).run(message_id)
        return {
            "message_id": state.get("message_id"),
            "intent": state.get("intent"),
            "confidence_score": state.get("confidence_score"),
            "suggested_reply": state.get("suggested_reply"),
            "action_required": state.get("action_required"),
            "follow_up_required": state.get("follow_up_required"),
            "follow_up_id": state.get("follow_up_id"),
            "lead_id": state.get("lead_id"),
            "appointment_data": state.get("appointment_data"),
            "invoice_data": state.get("invoice_data"),
            "requires_human_review": state.get("requires_human_review"),
            "sent_message_id": state.get("sent_message_id"),
            "ai_reasoning": state.get("ai_reasoning"),
            "error_message": state.get("error_message"),
        }
