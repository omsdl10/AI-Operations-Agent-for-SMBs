from datetime import datetime

from pydantic import BaseModel, EmailStr


class BusinessRead(BaseModel):
    id: str
    name: str

    model_config = {"from_attributes": True}


class UserRead(BaseModel):
    id: str
    business_id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    business: BusinessRead | None = None

    model_config = {"from_attributes": True}

