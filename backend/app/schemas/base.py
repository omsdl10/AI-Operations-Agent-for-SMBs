from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class APIResponse(BaseModel, Generic[DataT]):
    success: bool = True
    message: str = "OK"
    data: DataT | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail = Field(..., description="Machine-readable error details.")

