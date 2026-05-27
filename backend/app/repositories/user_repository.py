from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.business))
            .where(User.email == email.lower())
        )
        return self.db.scalar(statement)

    def get_by_id(self, user_id: str) -> User | None:
        statement = select(User).options(selectinload(User.business)).where(User.id == user_id)
        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

