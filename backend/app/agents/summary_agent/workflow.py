from datetime import date

from sqlalchemy.orm import Session

from .nodes import SummaryAgentNodes
from .state import SummaryAgentState


class SummaryAgentWorkflow:
    def __init__(self, db: Session) -> None:
        self.nodes = SummaryAgentNodes(db)
        self.graph = self._build_graph()

    def run(self, business_id: str, summary_date: date) -> SummaryAgentState:
        initial_state: SummaryAgentState = {"business_id": business_id, "summary_date": summary_date}
        if self.graph:
            return self.graph.invoke(initial_state)
        return self._run_sequential(initial_state)

    def _build_graph(self):
        try:
            from langgraph.graph import END, StateGraph
        except ImportError:
            return None

        workflow = StateGraph(SummaryAgentState)
        workflow.add_node("collect_daily_data_node", self.nodes.collect_daily_data_node)
        workflow.add_node("summarize_sales_node", self.nodes.summarize_sales_node)
        workflow.add_node("summarize_customers_node", self.nodes.summarize_customers_node)
        workflow.add_node("summarize_payments_node", self.nodes.summarize_payments_node)
        workflow.add_node("summarize_appointments_node", self.nodes.summarize_appointments_node)
        workflow.add_node("recommendation_engine_node", self.nodes.recommendation_engine_node)
        workflow.add_node("generate_final_summary_node", self.nodes.generate_final_summary_node)

        workflow.set_entry_point("collect_daily_data_node")
        workflow.add_edge("collect_daily_data_node", "summarize_sales_node")
        workflow.add_edge("summarize_sales_node", "summarize_customers_node")
        workflow.add_edge("summarize_customers_node", "summarize_payments_node")
        workflow.add_edge("summarize_payments_node", "summarize_appointments_node")
        workflow.add_edge("summarize_appointments_node", "recommendation_engine_node")
        workflow.add_edge("recommendation_engine_node", "generate_final_summary_node")
        workflow.add_edge("generate_final_summary_node", END)
        return workflow.compile()

    def _run_sequential(self, state: SummaryAgentState) -> SummaryAgentState:
        for node in (
            self.nodes.collect_daily_data_node,
            self.nodes.summarize_sales_node,
            self.nodes.summarize_customers_node,
            self.nodes.summarize_payments_node,
            self.nodes.summarize_appointments_node,
            self.nodes.recommendation_engine_node,
            self.nodes.generate_final_summary_node,
        ):
            state = node(state)
        return state

