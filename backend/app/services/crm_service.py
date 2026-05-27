from math import ceil

from fastapi import status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.ai_log import AILog
from app.models.appointment import Appointment
from app.models.customer import Customer
from app.models.follow_up import FollowUp
from app.models.invoice import Invoice
from app.models.lead import Lead
from app.models.message import Message
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.schemas.lead import LeadCreate, LeadRead, LeadUpdate
from app.schemas.pagination import PaginatedResponse


class CRMService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.customers = CustomerRepository(db)
        self.leads = LeadRepository(db)

    def list_customers(
        self,
        business_id: str,
        search: str | None,
        tag: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[CustomerRead]:
        items, total = self.customers.list(business_id, search, tag, page, page_size)
        return PaginatedResponse(
            items=[CustomerRead.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=max(ceil(total / page_size), 1),
        )

    def get_customer(self, business_id: str, customer_id: str) -> CustomerRead:
        customer = self.customers.get(business_id, customer_id)
        if not customer:
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")
        return CustomerRead.model_validate(customer)

    def create_customer(self, business_id: str, payload: CustomerCreate) -> CustomerRead:
        customer = self.customers.create(Customer(business_id=business_id, **payload.model_dump()))
        self.db.commit()
        return CustomerRead.model_validate(customer)

    def update_customer(
        self,
        business_id: str,
        customer_id: str,
        payload: CustomerUpdate,
    ) -> CustomerRead:
        customer = self.customers.get(business_id, customer_id)
        if not customer:
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
        self.db.commit()
        self.db.refresh(customer)
        return CustomerRead.model_validate(customer)

    def delete_customer(self, business_id: str, customer_id: str) -> None:
        customer = self.customers.get(business_id, customer_id)
        if not customer:
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")
        for model in (Lead, Message, FollowUp, Invoice, Appointment, AILog):
            self.db.execute(
                update(model)
                .where(model.business_id == business_id, model.customer_id == customer_id)
                .values(customer_id=None)
            )
        self.customers.delete(customer)
        self.db.commit()

    def list_leads(
        self,
        business_id: str,
        search: str | None,
        lead_status: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[LeadRead]:
        items, total = self.leads.list(business_id, search, lead_status, page, page_size)
        return PaginatedResponse(
            items=[self._lead_read(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=max(ceil(total / page_size), 1),
        )

    def get_lead(self, business_id: str, lead_id: str) -> LeadRead:
        lead = self.leads.get(business_id, lead_id)
        if not lead:
            raise AppException("Lead not found.", status.HTTP_404_NOT_FOUND, "lead_not_found")
        return self._lead_read(lead)

    def create_lead(self, business_id: str, payload: LeadCreate) -> LeadRead:
        if payload.customer_id and not self.customers.get(business_id, payload.customer_id):
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")

        lead = self.leads.create(
            Lead(
                business_id=business_id,
                **payload.model_dump(mode="json"),
            )
        )
        self.db.commit()
        self.db.refresh(lead)
        return self.get_lead(business_id, lead.id)

    def update_lead(self, business_id: str, lead_id: str, payload: LeadUpdate) -> LeadRead:
        lead = self.leads.get(business_id, lead_id)
        if not lead:
            raise AppException("Lead not found.", status.HTTP_404_NOT_FOUND, "lead_not_found")

        values = payload.model_dump(exclude_unset=True, mode="json")
        if values.get("customer_id") and not self.customers.get(business_id, values["customer_id"]):
            raise AppException("Customer not found.", status.HTTP_404_NOT_FOUND, "customer_not_found")

        for key, value in values.items():
            setattr(lead, key, value)
        self.db.commit()
        return self.get_lead(business_id, lead.id)

    def delete_lead(self, business_id: str, lead_id: str) -> None:
        lead = self.leads.get(business_id, lead_id)
        if not lead:
            raise AppException("Lead not found.", status.HTTP_404_NOT_FOUND, "lead_not_found")
        for model in (FollowUp, AILog):
            self.db.execute(
                update(model)
                .where(model.business_id == business_id, model.lead_id == lead_id)
                .values(lead_id=None)
            )
        self.leads.delete(lead)
        self.db.commit()

    def _lead_read(self, lead: Lead) -> LeadRead:
        return LeadRead(
            id=lead.id,
            business_id=lead.business_id,
            customer_id=lead.customer_id,
            title=lead.title,
            status=lead.status,
            source=lead.source,
            value_cents=lead.value_cents,
            priority_score=lead.priority_score,
            notes=lead.notes,
            customer_name=lead.customer.full_name if lead.customer else None,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
        )
