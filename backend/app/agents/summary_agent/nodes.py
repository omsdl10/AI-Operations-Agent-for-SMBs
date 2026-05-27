from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_log import AILog, AILogStatus
from app.models.appointment import Appointment, AppointmentStatus
from app.models.daily_summary import DailySummary
from app.models.follow_up import FollowUp, FollowUpStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.lead import Lead
from app.models.message import Message

from .state import SummaryAgentState


class SummaryAgentNodes:
    def __init__(self, db: Session) -> None:
        self.db = db

    def collect_daily_data_node(self, state: SummaryAgentState) -> SummaryAgentState:
        summary_date = state["summary_date"]
        start_at = datetime.combine(summary_date, time.min)
        end_at = start_at + timedelta(days=1)
        business_id = state["business_id"]

        metrics: dict[str, Any] = {
            "new_leads": self._count(Lead, business_id, start_at, end_at),
            "conversations_handled": self._count(Message, business_id, start_at, end_at),
            "invoices_paid": self._count(
                Invoice,
                business_id,
                start_at,
                end_at,
                Invoice.status == InvoiceStatus.paid.value,
            ),
            "overdue_invoices": self._count_current(
                Invoice,
                business_id,
                Invoice.status == InvoiceStatus.overdue.value,
            ),
            "pending_follow_ups": self._count_current(
                FollowUp,
                business_id,
                FollowUp.status.in_([FollowUpStatus.pending.value, FollowUpStatus.scheduled.value]),
            ),
            "appointments_completed": self._count(
                Appointment,
                business_id,
                start_at,
                end_at,
                Appointment.status == AppointmentStatus.completed.value,
            ),
            "appointments_today": self._count_between(
                Appointment,
                business_id,
                start_at,
                end_at,
                Appointment.starts_at,
            ),
        }
        metrics["revenue_cents"] = self.db.scalar(
            select(func.coalesce(func.sum(Invoice.amount_cents), 0)).where(
                Invoice.business_id == business_id,
                Invoice.status == InvoiceStatus.paid.value,
                Invoice.paid_at >= start_at,
                Invoice.paid_at < end_at,
            )
        ) or 0

        return {**state, "metrics": metrics}

    def summarize_sales_node(self, state: SummaryAgentState) -> SummaryAgentState:
        metrics = state["metrics"]
        revenue = metrics["revenue_cents"] / 100
        text = f"{metrics['new_leads']} new leads were captured. Paid revenue recorded today was ${revenue:,.2f}."
        return {**state, "sales_summary": text}

    def summarize_customers_node(self, state: SummaryAgentState) -> SummaryAgentState:
        metrics = state["metrics"]
        text = f"{metrics['conversations_handled']} customer messages were handled today."
        return {**state, "customer_summary": text}

    def summarize_payments_node(self, state: SummaryAgentState) -> SummaryAgentState:
        metrics = state["metrics"]
        text = (
            f"{metrics['invoices_paid']} invoices were paid. "
            f"{metrics['overdue_invoices']} invoices are currently overdue."
        )
        return {**state, "payment_summary": text}

    def summarize_appointments_node(self, state: SummaryAgentState) -> SummaryAgentState:
        metrics = state["metrics"]
        text = (
            f"{metrics['appointments_today']} appointments were scheduled for the day. "
            f"{metrics['appointments_completed']} were marked completed."
        )
        return {**state, "appointment_summary": text}

    def recommendation_engine_node(self, state: SummaryAgentState) -> SummaryAgentState:
        metrics = state["metrics"]
        recommendations: list[str] = []
        if metrics["pending_follow_ups"]:
            recommendations.append("Review pending follow-ups before the next business day.")
        if metrics["overdue_invoices"]:
            recommendations.append("Send payment reminders for overdue invoices.")
        if metrics["new_leads"]:
            recommendations.append("Prioritize new leads while customer intent is fresh.")
        if metrics["appointments_today"] and not metrics["appointments_completed"]:
            recommendations.append("Update appointment statuses so daily reporting stays accurate.")
        if not recommendations:
            recommendations.append("No urgent action detected. Keep monitoring conversations and follow-ups.")

        ai_recommendations = self._openai_recommendations(state)
        if ai_recommendations:
            recommendations = ai_recommendations
        return {**state, "recommendations": recommendations[:5]}

    def generate_final_summary_node(self, state: SummaryAgentState) -> SummaryAgentState:
        final_summary = "\n".join(
            [
                state["sales_summary"],
                state["customer_summary"],
                state["payment_summary"],
                state["appointment_summary"],
            ]
        )
        existing = self.db.scalar(
            select(DailySummary).where(
                DailySummary.business_id == state["business_id"],
                DailySummary.summary_date == state["summary_date"],
            )
        )
        if existing:
            existing.content = final_summary
            existing.metrics = state["metrics"]
            existing.recommendations = state["recommendations"]
            summary = existing
        else:
            summary = DailySummary(
                business_id=state["business_id"],
                summary_date=state["summary_date"],
                content=final_summary,
                metrics=state["metrics"],
                recommendations=state["recommendations"],
            )
            self.db.add(summary)
            self.db.flush()

        self.db.add(
            AILog(
                business_id=state["business_id"],
                workflow_name="daily_summary_agent",
                node_name="generate_final_summary_node",
                status=AILogStatus.success.value,
                input_payload={"summary_date": state["summary_date"].isoformat()},
                output_payload={"metrics": state["metrics"], "recommendations": state["recommendations"]},
                reasoning="Daily business summary generated.",
            )
        )
        self.db.commit()
        return {**state, "final_summary": final_summary, "summary_id": summary.id}

    def _count(self, model, business_id: str, start_at: datetime, end_at: datetime, *extra_filters) -> int:
        return self.db.scalar(
            select(func.count()).select_from(model).where(
                model.business_id == business_id,
                model.created_at >= start_at,
                model.created_at < end_at,
                *extra_filters,
            )
        ) or 0

    def _count_current(self, model, business_id: str, *extra_filters) -> int:
        return self.db.scalar(
            select(func.count()).select_from(model).where(model.business_id == business_id, *extra_filters)
        ) or 0

    def _count_between(self, model, business_id: str, start_at: datetime, end_at: datetime, column) -> int:
        return self.db.scalar(
            select(func.count()).select_from(model).where(
                model.business_id == business_id,
                column >= start_at,
                column < end_at,
            )
        ) or 0

    def _openai_recommendations(self, state: SummaryAgentState) -> list[str] | None:
        if not settings.openai_api_key:
            return None
        try:
            from langchain_openai import ChatOpenAI

            model = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.2)
            response = model.invoke(
                [
                    ("system", "Return 3 concise daily recommendations for a small business, one per line."),
                    ("human", f"Metrics: {state['metrics']}"),
                ]
            )
            content = response.content if isinstance(response.content, str) else str(response.content)
            items = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
            return items[:5] or None
        except Exception:
            return None

