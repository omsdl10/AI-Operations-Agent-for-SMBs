from sqlalchemy import ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Customer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "customers"
    __table_args__ = (
        Index("ix_customers_business_name", "business_id", "full_name"),
        Index("ix_customers_business_phone", "business_id", "phone"),
    )

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    business = relationship("Business", back_populates="customers")
    leads = relationship("Lead", back_populates="customer")
    messages = relationship("Message", back_populates="customer")
    follow_ups = relationship("FollowUp", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")
    appointments = relationship("Appointment", back_populates="customer")

