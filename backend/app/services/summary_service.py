from datetime import date

from fastapi import status
from sqlalchemy.orm import Session

from app.agents.summary_agent.workflow import SummaryAgentWorkflow
from app.core.exceptions import AppException
from app.repositories.summary_repository import SummaryRepository
from app.schemas.summary import DailySummaryRead


class SummaryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.summaries = SummaryRepository(db)

    def generate(self, business_id: str, summary_date: date | None = None) -> DailySummaryRead:
        target_date = summary_date or date.today()
        state = SummaryAgentWorkflow(self.db).run(business_id, target_date)
        summary = self.summaries.get_by_date(business_id, target_date)
        if not summary:
            raise AppException("Summary generation failed.", status.HTTP_500_INTERNAL_SERVER_ERROR, "summary_failed")
        return DailySummaryRead.model_validate(summary)

    def list(self, business_id: str, limit: int = 30) -> list[DailySummaryRead]:
        return [DailySummaryRead.model_validate(summary) for summary in self.summaries.list(business_id, limit)]

    def get_by_date(self, business_id: str, summary_date: date) -> DailySummaryRead:
        summary = self.summaries.get_by_date(business_id, summary_date)
        if not summary:
            raise AppException("Summary not found.", status.HTTP_404_NOT_FOUND, "summary_not_found")
        return DailySummaryRead.model_validate(summary)

