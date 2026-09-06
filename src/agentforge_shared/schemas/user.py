"""User-related Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field

from agentforge_shared.enums.platform import PermissionScope, UserRole
from agentforge_shared.utils.datetime_helpers import utc_now


class UserPreferences(BaseModel):
    """Per-user preference bag."""

    locale: str = Field(default="en", max_length=10)
    timezone: str = Field(default="UTC", max_length=64)
    notifications_enabled: bool = True
    extra: dict[str, Any] = Field(default_factory=dict)


class User(BaseModel):
    """User account information."""

    id: str = Field(..., description="User identifier.")
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=100)
    role: UserRole = UserRole.USER
    scopes: list[PermissionScope] = Field(default_factory=list)
    is_active: bool = True
    is_verified: bool = False
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


__all__ = ["User", "UserPreferences"]
