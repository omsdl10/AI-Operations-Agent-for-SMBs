from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.customer import Customer
from app.models.message import Message


class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.flush()
        self.db.refresh(message)
        return message

    def get_by_id(self, message_id: str) -> Message | None:
        return self.db.scalar(select(Message).where(Message.id == message_id))

    def list_for_customer(self, business_id: str, customer_id: str, limit: int = 100) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.business_id == business_id, Message.customer_id == customer_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def list_recent_by_business(self, business_id: str, limit: int = 200) -> list[Message]:
        statement = (
            select(Message)
            .options(selectinload(Message.customer))
            .where(Message.business_id == business_id, Message.customer_id.is_not(None))
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def get_by_external_id(self, external_id: str) -> Message | None:
        return self.db.scalar(select(Message).where(Message.external_id == external_id))

    def get_customer_by_phone(self, business_id: str, phone: str) -> Customer | None:
        statement = select(Customer).where(Customer.business_id == business_id, Customer.phone == phone)
        return self.db.scalar(statement)

    def get_customer(self, business_id: str, customer_id: str) -> Customer | None:
        statement = select(Customer).where(Customer.business_id == business_id, Customer.id == customer_id)
        return self.db.scalar(statement)

    def get_default_business_id(self) -> str | None:
        from app.models.business import Business

        return self.db.scalar(select(Business.id).order_by(Business.created_at.asc()).limit(1))

    def count_unread_for_customer(self, business_id: str, customer_id: str) -> int:
        statement = (
            select(func.count())
            .select_from(Message)
            .where(
                Message.business_id == business_id,
                Message.customer_id == customer_id,
                Message.direction == "inbound",
                Message.status == "received",
            )
        )
        return self.db.scalar(statement) or 0
