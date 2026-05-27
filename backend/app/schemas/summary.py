from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class DailySummaryRead(BaseModel):
    id: str
    business_id: str
    summary_date: date
    content: str
    metrics: dict[str, Any]
    recommendations: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class GenerateSummaryRequest(BaseModel):
    summary_date: date | None = None

