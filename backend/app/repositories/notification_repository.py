from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        self.db.flush()
        self.db.refresh(notification)
        return notification

    def list_for_business(self, business_id: str, limit: int = 50) -> list[Notification]:
        statement = (
            select(Notification)
            .where(Notification.business_id == business_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def exists_for_reference(self, business_id: str, reference_key: str, reference_id: str) -> bool:
        statement = select(Notification).where(
            Notification.business_id == business_id,
            Notification.metadata_json[reference_key].as_string() == reference_id,
        )
        return self.db.scalar(statement) is not None

    def due_pending(self, now: datetime) -> list[Notification]:
        statement = select(Notification).where(
            Notification.status == "pending",
            Notification.scheduled_for.is_not(None),
            Notification.scheduled_for <= now,
        )
        return list(self.db.scalars(statement).all())

