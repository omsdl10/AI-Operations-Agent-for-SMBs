from sqlalchemy.orm import Session

from app.models.business import Business


class BusinessRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, business: Business) -> Business:
        self.db.add(business)
        self.db.flush()
        self.db.refresh(business)
        return business

