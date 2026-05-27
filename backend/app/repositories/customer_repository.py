from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        business_id: str,
        search: str | None,
        tag: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Customer], int]:
        filters = [Customer.business_id == business_id]
        if search:
            pattern = f"%{search.lower()}%"
            filters.append(
                or_(
                    func.lower(Customer.full_name).like(pattern),
                    func.lower(Customer.email).like(pattern),
                    func.lower(Customer.phone).like(pattern),
                )
            )
        if tag:
            filters.append(cast(Customer.tags, String).ilike(f"%{tag}%"))

        total = self.db.scalar(select(func.count()).select_from(Customer).where(*filters)) or 0
        statement = (
            select(Customer)
            .where(*filters)
            .order_by(Customer.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self.db.scalars(statement).all()), total

    def get(self, business_id: str, customer_id: str) -> Customer | None:
        statement = select(Customer).where(
            Customer.business_id == business_id,
            Customer.id == customer_id,
        )
        return self.db.scalar(statement)

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.flush()
        self.db.refresh(customer)
        return customer

    def delete(self, customer: Customer) -> None:
        self.db.delete(customer)
