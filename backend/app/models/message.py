from enum import StrEnum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class MessageDirection(StrEnum):
    inbound = "inbound"
    outbound = "outbound"


class MessageChannel(StrEnum):
    whatsapp = "whatsapp"
    sms = "sms"
    email = "email"
    web = "web"


class MessageStatus(StrEnum):
    received = "received"
    queued = "queued"
    sent = "sent"
    delivered = "delivered"
    failed = "failed"
    read = "read"


class Message(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_business_customer_created", "business_id", "customer_id", "created_at"),
        Index("ix_messages_business_status", "business_id", "status"),
    )

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id"), nullable=True, index=True)
    direction: Mapped[str] = mapped_column(String(20), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), default=MessageChannel.whatsapp.value, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=MessageStatus.received.value, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    business = relationship("Business", back_populates="messages")
    customer = relationship("Customer", back_populates="messages")
    ai_logs = relationship("AILog", back_populates="message")
