"""RFC 9562 (uuid7)-compliant time-ordered identifier generation.

UUIDv7 encodes a 48-bit millisecond UNIX timestamp followed by random bits and
a version/variant marker. Values sort lexicographically by creation time, which
makes them ideal for database primary keys and event ordering.

This implementation has no third-party dependencies.
"""

from __future__ import annotations

import os
import threading
import time
import uuid
from typing import ClassVar

_VERSION_SHIFT = 12
_VERSION = 7
_VARIANT = 0b10
_RANDOM_MASK = (1 << 62) - 1

_clock_lock = threading.Lock()
_last_millis: ClassVar[int] = 0
_random_counter: ClassVar[int] = 0


def _current_unix_ms() -> int:
    return int(time.time() * 1000)


def uuid7(millis: int | None = None, *, force_sequence: bool = False) -> uuid.UUID:
    """Generate a time-ordered UUIDv7.

    Args:
        millis: Optional explicit UNIX epoch milliseconds (used by tests to
            pin ordering). Defaults to ``time.time() * 1000``.
        force_sequence: When ``True`` (and no ``millis`` given), reuse the same
            millisecond with a bumped counter to guarantee strict ordering.

    Returns:
        A ``uuid.UUID`` whose integer value sorts by creation time.
    """
    global _last_millis, _random_counter

    timestamp = millis if millis is not None else _current_unix_ms()

    with _clock_lock:
        if millis is None:
            if timestamp > _last_millis:
                _last_millis = timestamp
                _random_counter = 0
            elif timestamp == _last_millis:
                _random_counter += 1
            else:  # pragma: no cover - clock moved backwards
                timestamp = _last_millis
                _random_counter += 1
        elif force_sequence:
            _random_counter += 1

        counter = _random_counter

    # 48-bit unix ms | 12-bit version | 62-bit random
    rand_a = (counter << 0) & 0x0FFF
    rand_b = os.urandom(8)
    rand_int = int.from_bytes(rand_b, "big") & _RANDOM_MASK

    high = (timestamp << 16) & 0xFFFFFFFFFFFF0000 | (_VERSION << _VERSION_SHIFT) | rand_a
    mid_low = rand_int & 0x3FFFFFFFFFFFFFFF
    low = mid_low | (_VARIANT << 62)

    value = (high << 64) | low
    return uuid.UUID(int=value)


def uuid7_str(millis: int | None = None) -> str:
    """Return a UUIDv7 as a canonical lowercase string."""
    return str(uuid7(millis))


def is_uuid7(value: str | uuid.UUID) -> bool:
    """Return ``True`` when ``value`` is a UUID with version 7 and RFC variant."""
    try:
        parsed = value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    return parsed.version == 7 and parsed.variant == uuid.RFC_4122


def uuid7_to_timestamp_ms(value: str | uuid.UUID) -> int:
    """Extract the embedded UNIX epoch milliseconds from a UUIDv7.

    Raises:
        ValueError: when ``value`` is not a UUIDv7.
    """
    parsed = value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
    if parsed.version != 7:
        raise ValueError(f"Expected a UUIDv7, got version {parsed.version}")
    return parsed.int >> 80


def generate_uuid7_id(prefix: str = "") -> str:
    """Generate a prefixed, time-ordered UUIDv7 identifier.

    Note: legacy ``generate_*_id`` helpers in :mod:`id_generator` return
    shorter uuid4-based strings and remain available for backward compatibility.
    """
    return f"{prefix}_{uuid7_str()}" if prefix else uuid7_str()


__all__ = [
    "uuid7",
    "uuid7_str",
    "is_uuid7",
    "uuid7_to_timestamp_ms",
    "generate_uuid7_id",
]
