from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_summary import DailySummary


class SummaryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, business_id: str, limit: int = 30) -> list[DailySummary]:
        return list(
            self.db.scalars(
                select(DailySummary)
                .where(DailySummary.business_id == business_id)
                .order_by(DailySummary.summary_date.desc())
                .limit(limit)
            ).all()
        )

    def get_by_date(self, business_id: str, summary_date: date) -> DailySummary | None:
        return self.db.scalar(
            select(DailySummary).where(
                DailySummary.business_id == business_id,
                DailySummary.summary_date == summary_date,
            )
        )

