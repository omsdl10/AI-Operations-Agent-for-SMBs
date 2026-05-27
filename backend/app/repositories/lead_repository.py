from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.lead import Lead


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        business_id: str,
        search: str | None,
        status: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Lead], int]:
        filters = [Lead.business_id == business_id]
        if search:
            pattern = f"%{search.lower()}%"
            filters.append(
                or_(
                    func.lower(Lead.title).like(pattern),
                    func.lower(Lead.source).like(pattern),
                    func.lower(Lead.notes).like(pattern),
                )
            )
        if status:
            filters.append(Lead.status == status)

        total = self.db.scalar(select(func.count()).select_from(Lead).where(*filters)) or 0
        statement = (
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(*filters)
            .order_by(Lead.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self.db.scalars(statement).all()), total

    def get(self, business_id: str, lead_id: str) -> Lead | None:
        statement = (
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(Lead.business_id == business_id, Lead.id == lead_id)
        )
        return self.db.scalar(statement)

    def create(self, lead: Lead) -> Lead:
        self.db.add(lead)
        self.db.flush()
        self.db.refresh(lead)
        return lead

    def delete(self, lead: Lead) -> None:
        self.db.delete(lead)

