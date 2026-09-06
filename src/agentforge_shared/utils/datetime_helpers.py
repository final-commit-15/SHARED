"""Date/time utilities used across services."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Optional

import dateutil.parser


def utc_now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(UTC)


def iso_format(dt: datetime) -> str:
    """Format a datetime as an ISO 8601 string with a ``Z`` UTC suffix.

    Args:
        dt: Any timezone-aware (or naive, assumed UTC) datetime.

    Returns:
        E.g. ``"2026-09-06T12:34:56.789012Z"``.
    """
    value = ensure_utc(dt)
    return value.isoformat().replace("+00:00", "Z")


def parse_iso(value: str | datetime) -> datetime:
    """Parse an ISO 8601 string (or pass through a datetime) into UTC.

    Raises:
        ValueError: when the string cannot be parsed.
    """
    if isinstance(value, datetime):
        return ensure_utc(value)
    parsed = dateutil.parser.isoparse(value)
    return ensure_utc(parsed)


def ensure_utc(dt: datetime) -> datetime:
    """Attach UTC to naive datetimes, otherwise convert the tzinfo to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def to_timestamp(dt: datetime) -> float:
    """Return the POSIX epoch seconds for ``dt``."""
    return ensure_utc(dt).timestamp()


def from_timestamp(ts: float) -> datetime:
    """Return a UTC datetime from a POSIX epoch timestamp."""
    return datetime.fromtimestamp(ts, tz=UTC)


def seconds_since(dt: datetime, *, now: datetime | None = None) -> float:
    """Return the number of seconds elapsed since ``dt`` (non-negative)."""
    delta = (now or utc_now()) - ensure_utc(dt)
    return max(0.0, delta.total_seconds())


def is_within_past(dt: datetime, seconds: float, *, now: datetime | None = None) -> bool:
    """Return ``True`` when ``dt`` occurred within the last ``seconds``."""
    return seconds_since(dt, now=now) <= seconds


def add_seconds(dt: datetime, seconds: float) -> datetime:
    """Return ``dt`` shifted by ``seconds`` (keeps timezone)."""
    base = ensure_utc(dt)
    return base + timedelta(seconds=seconds)


def iso_timestamp_ms(dt: datetime | None = None) -> str:
    """Return a millisecond-precision ISO timestamp suitable for logs."""
    value = ensure_utc(dt or utc_now())
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def iso_timestamp_dt() -> str:
    """Return an ISO timestamp with date precision (yyyy-mm-dd)."""
    return utc_now().date().isoformat()


def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format ``dt`` with an arbitrary ``strftime`` format."""
    return ensure_utc(dt).strftime(fmt)


def to_date_string(dt: datetime) -> str:
    """Return ``dt`` as ``yyyy-mm-dd``."""
    return format_date(dt)


def to_datetime_string(dt: datetime) -> str:
    """Return ``dt`` as ``yyyy-mm-dd HH:MM:SS`` (UTC)."""
    return format_date(dt, "%Y-%m-%d %H:%M:%S")


# Optional import is intentionally lazy to avoid a hard dependency in docs builds.
try:
    from zoneinfo import ZoneInfo  # noqa: F401

    _HAS_ZONEINFO = True
except ImportError:  # pragma: no cover - py<3.9
    _HAS_ZONEINFO = False


def in_timezone(dt: datetime, tz_name: str = "UTC") -> datetime:
    """Convert ``dt`` into an IANA timezone, e.g. ``"Europe/London"``."""
    base = ensure_utc(dt)
    if tz_name in {"", "UTC"} or not _HAS_ZONEINFO:
        return base
    try:
        return base.astimezone(ZoneInfo(tz_name))
    except (ValueError, KeyError):
        return base


__all__ = [
    "utc_now",
    "iso_format",
    "parse_iso",
    "ensure_utc",
    "to_timestamp",
    "from_timestamp",
    "seconds_since",
    "is_within_past",
    "add_seconds",
    "iso_timestamp_ms",
    "iso_timestamp_dt",
    "format_date",
    "to_date_string",
    "to_datetime_string",
    "in_timezone",
    "Optional",
]
