from datetime import date
from typing import Any, TypedDict


class SummaryAgentState(TypedDict, total=False):
    business_id: str
    summary_date: date
    metrics: dict[str, Any]
    sales_summary: str
    customer_summary: str
    payment_summary: str
    appointment_summary: str
    recommendations: list[str]
    final_summary: str
    summary_id: str | None
    error_message: str | None

