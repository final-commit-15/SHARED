"""Hashing and digest utilities (non-password cryptography helpers)."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from collections.abc import Iterable


def sha256_hex(value: str | bytes, *, encoding: str = "utf-8") -> str:
    """Return the lowercase SHA-256 hex digest of ``value``."""
    data = value.encode(encoding) if isinstance(value, str) else value
    return hashlib.sha256(data).hexdigest()


def sha256_digest(value: str | bytes, *, encoding: str = "utf-8") -> bytes:
    """Return the raw SHA-256 digest of ``value``."""
    data = value.encode(encoding) if isinstance(value, str) else value
    return hashlib.sha256(data).digest()


def sha1_hex(value: str | bytes, *, encoding: str = "utf-8") -> str:
    """Return the lowercase SHA-1 hex digest of ``value``."""
    data = value.encode(encoding) if isinstance(value, str) else value
    return hashlib.sha1(data).hexdigest()


def md5_hex(value: str | bytes, *, encoding: str = "utf-8") -> str:
    """Return the lowercase MD5 hex digest of ``value`` (checksums only)."""
    data = value.encode(encoding) if isinstance(value, str) else value
    return hashlib.md5(data).hexdigest()


def hmac_sha256_hex(secret: str | bytes, message: str | bytes) -> str:
    """Return an HMAC-SHA-256 hex digest of ``message`` keyed by ``secret``."""
    key = secret if isinstance(secret, bytes) else secret.encode("utf-8")
    msg = message if isinstance(message, bytes) else message.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def hmac_sha256_digest(secret: str | bytes, message: str | bytes) -> bytes:
    """Return a raw HMAC-SHA-256 digest of ``message`` keyed by ``secret``."""
    key = secret if isinstance(secret, bytes) else secret.encode("utf-8")
    msg = message if isinstance(message, bytes) else message.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).digest()


def constant_time_compare(a: str | bytes, b: str | bytes) -> bool:
    """Constant-time comparison of two byte strings (safe for secrets)."""
    return hmac.compare_digest(a, b)


def short_hash(value: str, length: int = 8) -> str:
    """Return a stable, short hex digest of ``value`` for cache keys etc."""
    if length < 1:
        raise ValueError("length must be >= 1")
    return sha256_hex(value)[:length]


def stable_map_key(*parts: str, length: int | None = None) -> str:
    """Build a stable key from parts joined with ``:`` and optionally hashed."""
    joined = ":".join(parts)
    if length is None:
        return joined
    return short_hash(joined, length)


def secure_bytes(count: int = 32) -> bytes:
    """Return ``count`` cryptographically random bytes."""
    return secrets.token_bytes(count)


def secure_hex(count: int = 32) -> str:
    """Return a cryptographically random hex string (``2*count`` chars)."""
    return secrets.token_hex(count)


def digest_bytes(value: bytes) -> str:
    """Return the sha256 hex of bytes input (convenience wrapper)."""
    return sha256_hex(value)


def sha256_iter(values: Iterable[str]) -> str:
    """Hash every value in ``values`` and combine them into one digest.

    Useful for fingerprinting composite keys or payloads.
    """
    hasher = hashlib.sha256()
    for value in values:
        hasher.update(value.encode("utf-8"))
        hasher.update(b"\x00")
    return hasher.hexdigest()


__all__ = [
    "sha256_hex",
    "sha256_digest",
    "sha1_hex",
    "md5_hex",
    "hmac_sha256_hex",
    "hmac_sha256_digest",
    "constant_time_compare",
    "short_hash",
    "stable_map_key",
    "secure_bytes",
    "secure_hex",
    "digest_bytes",
    "sha256_iter",
]
