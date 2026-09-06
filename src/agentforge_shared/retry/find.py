"""Helpers to find failed records/sequences for reprocessing."""

from __future__ import annotations

from collections.abc import Iterable


def find_failed_sequences(
    records: Iterable[dict],
    *,
    id_key: str = "id",
    status_key: str = "status",
    failed_statuses: Iterable[str] = ("failed", "error"),
) -> list[object]:
    """Return identifiers of records with a failed status.

    Args:
        records: Iterable of record dictionaries.
        id_key: Field holding the identifier.
        status_key: Field holding the status string.
        failed_statuses: Statuses considered failures.
    """
    statuses = {s.lower() for s in failed_statuses}
    out: list[object] = []
    for record in records:
        if str(record.get(status_key, "")).lower() in statuses:
            ident = record.get(id_key)
            if ident is not None:
                out.append(ident)
    return out


def find_errored_ids(results: Iterable[tuple[object, BaseException | None]]) -> list[object]:
    """Extract identifiers whose corresponding result carried an exception.

    ``results`` entries are ``(identifier, error_or_none)`` pairs.
    """
    return [ident for ident, exc in results if exc is not None]


def retryable_backlog(
    records: Iterable[dict],
    *,
    outage_window_seconds: int = 300,
    status_key: str = "status",
    updated_key: str = "updated_at",
    id_key: str = "id",
) -> list[object]:
    """Return ids of failed records updated within the outage window.

    ``updated_key`` values are parsed as epoch seconds (int/float/str).
    """
    import time

    cutoff = time.time() - abs(outage_window_seconds)
    out: list[object] = []
    failed = set(find_failed_sequences(records, id_key=id_key, status_key=status_key))
    for record in records:
        ident = record.get(id_key)
        if ident not in failed:
            continue
        raw = record.get(updated_key)
        try:
            ts = float(raw)
        except (TypeError, ValueError):
            continue
        if ts >= cutoff:
            out.append(ident)
    return out


__all__ = ["find_failed_sequences", "find_errored_ids", "retryable_backlog"]
