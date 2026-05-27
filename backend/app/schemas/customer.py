from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    email: EmailStr | None = None
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    email: EmailStr | None = None
    notes: str | None = None
    tags: list[str] | None = None


class CustomerRead(CustomerBase):
    id: str
    business_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

