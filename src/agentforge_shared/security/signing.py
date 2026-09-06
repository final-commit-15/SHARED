"""HMAC request signing and verification."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from agentforge_shared.utils.json_utils import dumps_bytes


def _normalize_body(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, (dict, list, tuple)):
        return dumps_bytes(payload, sort_keys=True)
    return str(payload).encode("utf-8")


def sign_payload(
    payload: Any,
    *,
    secret: str,
    timestamp: int | None = None,
    method: str = "POST",
    path: str = "",
    algo: str = "sha256",
) -> str:
    """Sign ``payload`` with HMAC (returns hex digest).

    The digest covers ``method\\npath\\ntimestamp\\n<sha256(body)>`` so body,
    route and time are bound to the signature.
    """
    ts = timestamp if timestamp is not None else int(time.time())
    body_hash = hashlib.sha256(_normalize_body(payload)).hexdigest()
    message = f"{method.upper()}\n{path}\n{ts}\n{body_hash}".encode()
    return hmac.new(secret.encode("utf-8"), message, getattr(hashlib, algo)).hexdigest()


def verify_signature(
    payload: Any,
    *,
    signature: str,
    secret: str,
    timestamp: int | None = None,
    method: str = "POST",
    path: str = "",
    max_age_seconds: int = 300,
    algo: str = "sha256",
) -> bool:
    """Verify an HMAC signature, rejecting old timestamps.

    Args:
        payload: The signed request body (same bytes as when signed).
        signature: Hex digest expected to match.
        secret: Shared signing secret.
        timestamp: Signature timestamp (replay window applied).
        max_age_seconds: Accepted clock skew for ``timestamp``.

    Returns:
        ``True`` if the signature is valid and fresh.
    """
    expected = sign_payload(
        payload,
        secret=secret,
        timestamp=timestamp,
        method=method,
        path=path,
        algo=algo,
    )
    valid = hmac.compare_digest(expected, signature)
    if not valid or timestamp is None:
        return valid
    age = abs(int(time.time()) - timestamp)
    return age <= max_age_seconds


def signed_headers(
    payload: Any,
    *,
    secret: str,
    method: str = "POST",
    path: str = "",
    timestamp: int | None = None,
) -> dict[str, str]:
    """Build the HTTP headers carrying an HMAC signature."""
    ts = timestamp if timestamp is not None else int(time.time())
    return {
        "Content-Type": "application/json",
        "X-AgentForge-Signature": sign_payload(
            payload, secret=secret, timestamp=ts, method=method, path=path
        ),
        "X-AgentForge-Timestamp": str(ts),
    }


__all__ = ["sign_payload", "verify_signature", "signed_headers"]
