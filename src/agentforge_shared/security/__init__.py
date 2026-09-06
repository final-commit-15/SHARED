"""Security toolkit: JWT, passwords, API keys, HMAC signing, scopes, permissions."""

from .api_keys import generate_api_key, hash_api_key, key_fingerprint, verify_api_key
from .jwt import JWTManager
from .password import hash_password, require_password, verify_password
from .permissions import PermissionChecker, has_scopes_for_resource, require_permission
from .scopes import (
    has_all_scopes,
    has_any_scope,
    has_scope,
    parse_scopes,
    scope_matches,
    scopes_diff,
)
from .signing import sign_payload, signed_headers, verify_signature

__all__ = [
    # JWT
    "JWTManager",
    # passwords
    "hash_password",
    "verify_password",
    "require_password",
    # API keys
    "generate_api_key",
    "hash_api_key",
    "verify_api_key",
    "key_fingerprint",
    # signing
    "sign_payload",
    "signed_headers",
    "verify_signature",
    # scopes
    "parse_scopes",
    "scope_matches",
    "has_scope",
    "has_all_scopes",
    "has_any_scope",
    "scopes_diff",
    # permissions
    "PermissionChecker",
    "require_permission",
    "has_scopes_for_resource",
]
