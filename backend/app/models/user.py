from enum import StrEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserRole(StrEnum):
    owner = "owner"
    admin = "admin"
    staff = "staff"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default=UserRole.owner.value, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    business = relationship("Business", back_populates="users")
    assigned_follow_ups = relationship("FollowUp", back_populates="assigned_user")
    ai_logs = relationship("AILog", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

