"""Common API response schemas."""

from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel):
    """Pagination metadata."""
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    total: int = Field(0, ge=0)
    pages: Optional[int] = None


class APIResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""
    success: bool = True
    data: T
    message: Optional[str] = None
    pagination: Optional[Pagination] = None


class ErrorResponse(BaseModel):
    """Standard API error response."""
    success: bool = False
    error: str = Field(..., description="Error message")
    code: Optional[str] = None
    details: Optional[Any] = None