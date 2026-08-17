"""User-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from ..utils.datetime_helpers import utc_now   # <-- new import


class User(BaseModel):
    """User account information."""
    id: str = Field(..., description="User identifier")
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)   # <-- changed
    updated_at: datetime = Field(default_factory=utc_now)   # <-- changed