from datetime import datetime

from pydantic import BaseModel, Field

from app.models.lead import LeadStatus


class LeadBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    customer_id: str | None = None
    status: LeadStatus = LeadStatus.new
    source: str | None = Field(default=None, max_length=120)
    value_cents: int = Field(default=0, ge=0)
    priority_score: int = Field(default=0, ge=0, le=100)
    notes: str | None = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    customer_id: str | None = None
    status: LeadStatus | None = None
    source: str | None = Field(default=None, max_length=120)
    value_cents: int | None = Field(default=None, ge=0)
    priority_score: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = None


class LeadRead(BaseModel):
    id: str
    business_id: str
    customer_id: str | None
    title: str
    status: str
    source: str | None
    value_cents: int
    priority_score: int
    notes: str | None
    customer_name: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

