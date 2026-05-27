from datetime import date

from sqlalchemy import Date, ForeignKey, Index, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class DailySummary(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "daily_summaries"
    __table_args__ = (
        Index("ix_daily_summaries_business_date", "business_id", "summary_date", unique=True),
    )

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    summary_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    recommendations: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    business = relationship("Business", back_populates="daily_summaries")

