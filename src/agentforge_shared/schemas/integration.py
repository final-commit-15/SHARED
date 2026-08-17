"""Integration-related Pydantic schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from ..enums.integration import IntegrationType
from ..utils.datetime_helpers import utc_now   # <-- new import


class Integration(BaseModel):
    """External integration configuration."""
    id: str = Field(..., description="Integration identifier")
    name: str = Field(..., min_length=1, max_length=50)
    type: IntegrationType
    config: Dict[str, Any] = Field(..., description="Integration-specific settings")
    is_enabled: bool = True
    created_at: datetime = Field(default_factory=utc_now)   # <-- changed
    updated_at: datetime = Field(default_factory=utc_now)   # <-- changed