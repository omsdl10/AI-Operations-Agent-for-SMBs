from datetime import datetime
from typing import Any

from pydantic import BaseModel


class NotificationRead(BaseModel):
    id: str
    business_id: str
    user_id: str | None
    title: str
    body: str
    channel: str
    status: str
    scheduled_for: datetime | None
    sent_at: datetime | None
    metadata_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AutomationRunResult(BaseModel):
    follow_up_notifications: int
    payment_reminders: int
    appointment_reminders: int
    overdue_invoices: int
    total_notifications: int

