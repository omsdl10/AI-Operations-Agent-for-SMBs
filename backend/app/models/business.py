from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Business(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(120), nullable=True)

    users = relationship("User", back_populates="business")
    customers = relationship("Customer", back_populates="business", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="business", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="business", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="business", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="business", cascade="all, delete-orphan")
    appointments = relationship(
        "Appointment",
        back_populates="business",
        cascade="all, delete-orphan",
    )
    daily_summaries = relationship(
        "DailySummary",
        back_populates="business",
        cascade="all, delete-orphan",
    )
    ai_logs = relationship("AILog", back_populates="business", cascade="all, delete-orphan")
    notifications = relationship(
        "Notification",
        back_populates="business",
        cascade="all, delete-orphan",
    )
