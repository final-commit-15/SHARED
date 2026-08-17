"""Date/time utilities."""

from datetime import datetime, timezone
from typing import Optional


def utc_now() -> datetime:
    """Return current UTC datetime (timezone‑aware)."""
    return datetime.now(timezone.utc)


def iso_format(dt: datetime) -> str:
    """Format datetime as ISO 8601 string (UTC)."""
    return dt.isoformat().replace("+00:00", "Z")


def parse_iso(s: str) -> datetime:
    """Parse ISO 8601 string into UTC datetime."""
    # Pydantic handles parsing, but we keep this for manual use.
    return datetime.fromisoformat(s.replace("Z", "+00:00"))