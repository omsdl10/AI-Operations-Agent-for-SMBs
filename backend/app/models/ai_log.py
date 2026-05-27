from enum import StrEnum

from sqlalchemy import ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AILogStatus(StrEnum):
    success = "success"
    failed = "failed"
    human_review = "human_review"


class AILog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ai_logs"
    __table_args__ = (
        Index("ix_ai_logs_business_workflow_status", "business_id", "workflow_name", "status"),
    )

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id"), nullable=True, index=True)
    lead_id: Mapped[str | None] = mapped_column(ForeignKey("leads.id"), nullable=True, index=True)
    message_id: Mapped[str | None] = mapped_column(ForeignKey("messages.id"), nullable=True, index=True)
    invoice_id: Mapped[str | None] = mapped_column(ForeignKey("invoices.id"), nullable=True, index=True)
    appointment_id: Mapped[str | None] = mapped_column(
        ForeignKey("appointments.id"),
        nullable=True,
        index=True,
    )
    workflow_name: Mapped[str] = mapped_column(String(120), nullable=False)
    node_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default=AILogStatus.success.value, nullable=False)
    input_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    business = relationship("Business", back_populates="ai_logs")
    user = relationship("User", back_populates="ai_logs")
    lead = relationship("Lead", back_populates="ai_logs")
    message = relationship("Message", back_populates="ai_logs")
    invoice = relationship("Invoice", back_populates="ai_logs")
    appointment = relationship("Appointment", back_populates="ai_logs")

