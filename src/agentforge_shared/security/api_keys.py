"""API key generation and verification.

API keys follow a ``prefix_<base64url-24-random-bytes>`` shape. Only a
SHA-256 digest of a key is ever stored; the raw key is shown once.
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets as _secrets

from agentforge_shared.validation.validators import validate_identifier


def generate_api_key(*, prefix: str = "agf", entropy_bytes: int = 32) -> str:
    """Generate a high-entropy API key string.

    Args:
        prefix: Short key prefix (validated as an identifier).
        entropy_bytes: Random bytes (>= 32 recommended).

    Returns:
        An opaque, URL-safe key to hand to the caller once.
    """
    validate_identifier(prefix, max_length=16)
    raw = base64.urlsafe_b64encode(os.urandom(max(entropy_bytes, 16))).rstrip(b"=").decode("ascii")
    return f"{prefix}_{raw}"


def hash_api_key(api_key: str) -> str:
    """Return the SHA-256 hex digest of ``api_key`` (safe to store)."""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(api_key: str, stored_digest: str) -> bool:
    """Compare ``api_key`` against a stored digest in constant time."""
    if not api_key or not stored_digest:
        return False
    return _secrets.compare_digest(hash_api_key(api_key), stored_digest.lower())


def key_fingerprint(api_key: str, length: int = 4) -> str:
    """Return a masked fingerprint ``prefix_****abcd`` for logs/UIs."""
    if "_" in api_key:
        prefix, raw = api_key.split("_", 1)
    else:
        prefix, raw = "key", api_key
    tail = raw[-length:]
    return f"{prefix}_****{tail}"


__all__ = ["generate_api_key", "hash_api_key", "verify_api_key", "key_fingerprint"]
