from enum import StrEnum

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LeadStatus(StrEnum):
    new = "new"
    contacted = "contacted"
    interested = "interested"
    converted = "converted"
    lost = "lost"


class Lead(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_business_status", "business_id", "status"),
        Index("ix_leads_business_source", "business_id", "source"),
    )

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=LeadStatus.new.value, nullable=False)
    source: Mapped[str | None] = mapped_column(String(120), nullable=True)
    value_cents: Mapped[int] = mapped_column(default=0, nullable=False)
    priority_score: Mapped[int] = mapped_column(default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    business = relationship("Business", back_populates="leads")
    customer = relationship("Customer", back_populates="leads")
    follow_ups = relationship("FollowUp", back_populates="lead")
    ai_logs = relationship("AILog", back_populates="lead")

