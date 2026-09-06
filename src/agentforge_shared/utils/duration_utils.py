"""Human-readable formatting helpers (durations, sizes, counts)."""

from __future__ import annotations

from datetime import UTC


def human_duration(seconds: float, *, verbose: bool = False) -> str:
    """Format ``seconds`` as a human-readable string like ``"2m 5s"``.

    Args:
        seconds: Duration in seconds.
        verbose: Use full unit names (``"2 minutes 5 seconds"``) when ``True``.
    """
    seconds = max(0.0, float(seconds))
    if seconds < 1.0:
        return f"{seconds * 1000:.0f} ms" if verbose else f"{seconds * 1000:.0f}ms"
    total = int(round(seconds))
    days, rem = divmod(total, 86_400)
    hours, rem = divmod(rem, 3_600)
    minutes, secs = divmod(rem, 60)

    parts: list[str] = []
    if days:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if secs or not parts:
        parts.append(f"{secs} second{'s' if secs > 1 else ''}")

    if verbose:
        return " ".join(parts)
    return " ".join(f"{n}{_short_unit(unit)}" for n, unit in _parse_parts(days, hours, minutes, secs))


def _short_unit(unit: str) -> str:
    return {"day": "d", "hour": "h", "minute": "m", "second": "s"}[unit]


def _parse_parts(days: int, hours: int, minutes: int, secs: int) -> list[tuple[int, str]]:
    parts: list[tuple[int, str]] = []
    if days:
        parts.append((days, "day"))
    if hours:
        parts.append((hours, "hour"))
    if minutes:
        parts.append((minutes, "minute"))
    if secs or not parts:
        parts.append((secs, "second"))
    return parts


def human_timestamp(epoch_seconds: float) -> str:
    """Format a POSIX timestamp as a compact ISO-8601 UTC string."""
    from datetime import datetime

    return datetime.fromtimestamp(epoch_seconds, tz=UTC).isoformat().replace("+00:00", "Z")


def human_count(number: float) -> str:
    """Format a count with thousands separators, e.g. ``"1,234,567"``."""
    return f"{int(number):,}"


def human_percentage(part: float, whole: float, *, places: int = 1) -> str:
    """Return ``part/whole`` as a percentage string, or ``"0%"`` on zero whole."""
    if whole <= 0:
        return "0%"
    return f"{(part / whole) * 100:.{places}f}%"


def pluralize(count: float, singular: str, plural: str | None = None) -> str:
    """Return ``singular`` or ``plural`` (default: singular + ``s``) for ``count``."""
    return plural if plural is not None else singular + "s" if abs(count) != 1 else singular


def format_float(value: float, *, places: int = 2) -> str:
    """Format a float to ``places`` decimals, trimming trailing zeros."""
    return f"{value:.{places}f}".rstrip("0").rstrip(".") if "." in f"{value:.{places}f}" else f"{value:.{places}f}"


def format_money(value: float, *, currency: str = "$", places: int = 2) -> str:
    """Format a monetary value with a currency symbol."""
    return f"{currency}{value:,.{places}f}"


__all__ = [
    "human_duration",
    "human_timestamp",
    "human_count",
    "human_percentage",
    "pluralize",
    "format_float",
    "format_money",
]
