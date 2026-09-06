"""Integration-related Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from agentforge_shared.enums.integration import (
    IntegrationAuthType,
    IntegrationStatus,
    IntegrationType,
)
from agentforge_shared.utils.datetime_helpers import utc_now


class Integration(BaseModel):
    """External integration configuration."""

    id: str = Field(..., description="Integration identifier.")
    name: str = Field(..., min_length=1, max_length=50)
    type: IntegrationType
    status: IntegrationStatus = IntegrationStatus.UNVERIFIED
    auth_type: IntegrationAuthType = IntegrationAuthType.NONE
    config: dict[str, Any] = Field(default_factory=dict, description="Integration-specific settings.")
    is_enabled: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


__all__ = ["Integration"]
