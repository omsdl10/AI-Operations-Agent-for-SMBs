from sqlalchemy.orm import Session

from .nodes import MessageAgentNodes
from .state import MessageAgentState


class MessageAgentWorkflow:
    def __init__(self, db: Session) -> None:
        self.nodes = MessageAgentNodes(db)
        self.graph = self._build_graph()

    def run(self, message_id: str) -> MessageAgentState:
        initial_state: MessageAgentState = {"message_id": message_id}
        if self.graph:
            return self.graph.invoke(initial_state)
        return self._run_sequential(initial_state)

    def _build_graph(self):
        try:
            from langgraph.graph import END, StateGraph
        except ImportError:
            return None

        workflow = StateGraph(MessageAgentState)
        workflow.add_node("receive_message_node", self.nodes.receive_message_node)
        workflow.add_node("classify_intent_node", self.nodes.classify_intent_node)
        workflow.add_node("customer_lookup_node", self.nodes.customer_lookup_node)
        workflow.add_node("ai_response_generation_node", self.nodes.ai_response_generation_node)
        workflow.add_node("action_decision_node", self.nodes.action_decision_node)
        workflow.add_node("follow_up_creation_node", self.nodes.follow_up_creation_node)
        workflow.add_node("payment_reminder_node", self.nodes.payment_reminder_node)
        workflow.add_node("appointment_scheduler_node", self.nodes.appointment_scheduler_node)
        workflow.add_node("human_review_node", self.nodes.human_review_node)
        workflow.add_node("send_reply_node", self.nodes.send_reply_node)
        workflow.add_node("log_activity_node", self.nodes.log_activity_node)

        workflow.set_entry_point("receive_message_node")
        workflow.add_edge("receive_message_node", "classify_intent_node")
        workflow.add_edge("classify_intent_node", "customer_lookup_node")
        workflow.add_edge("customer_lookup_node", "ai_response_generation_node")
        workflow.add_edge("ai_response_generation_node", "action_decision_node")
        workflow.add_edge("action_decision_node", "follow_up_creation_node")
        workflow.add_edge("follow_up_creation_node", "payment_reminder_node")
        workflow.add_edge("payment_reminder_node", "appointment_scheduler_node")
        workflow.add_edge("appointment_scheduler_node", "human_review_node")
        workflow.add_conditional_edges(
            "human_review_node",
            self._reply_route,
            {
                "send": "send_reply_node",
                "skip": "log_activity_node",
            },
        )
        workflow.add_edge("send_reply_node", "log_activity_node")
        workflow.add_edge("log_activity_node", END)
        return workflow.compile()

    def _reply_route(self, state: MessageAgentState) -> str:
        return "skip" if state.get("requires_human_review") else "send"

    def _run_sequential(self, state: MessageAgentState) -> MessageAgentState:
        for node in (
            self.nodes.receive_message_node,
            self.nodes.classify_intent_node,
            self.nodes.customer_lookup_node,
            self.nodes.ai_response_generation_node,
            self.nodes.action_decision_node,
            self.nodes.follow_up_creation_node,
            self.nodes.payment_reminder_node,
            self.nodes.appointment_scheduler_node,
            self.nodes.human_review_node,
        ):
            state = node(state)

        if not state.get("requires_human_review"):
            state = self.nodes.send_reply_node(state)
        return self.nodes.log_activity_node(state)

