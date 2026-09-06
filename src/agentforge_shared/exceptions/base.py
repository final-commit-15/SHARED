"""Exception hierarchy for the AgentForge platform.

Every exception carries:

- a human-readable ``message``,
- a stable machine-readable ``error_code`` (see :mod:`agentforge_shared.constants.errors`),
- an HTTP ``status_code`` used when the exception is mapped to a response,
- optional ``details`` (structured payload exposed to clients).

DecimalScheme
``BaseAgentForgeException`` subclasses are used directly by services; the
middleware package converts them into :class:`FastAPI` responses.
"""

from __future__ import annotations

import uuid
from typing import Any, Literal

from agentforge_shared.constants.errors import (
    ERR_AI_SERVICE,
    ERR_ALREADY_EXISTS,
    ERR_AUTHENTICATION,
    ERR_AUTHENTICATION_EXPIRED,
    ERR_AUTHORIZATION,
    ERR_CACHE,
    ERR_CIRCUIT_OPEN,
    ERR_CONFIGURATION,
    ERR_CONFLICT,
    ERR_EXECUTION,
    ERR_EXECUTION_TIMEOUT,
    ERR_INSUFFICIENT_PERMISSION,
    ERR_INSUFFICIENT_SCOPE,
    ERR_INTERNAL,
    ERR_INVALID_TOKEN,
    ERR_NOT_FOUND,
    ERR_NOT_IMPLEMENTED,
    ERR_PROVIDER,
    ERR_PROVIDER_TIMEOUT,
    ERR_RATE_LIMITED,
    ERR_RETRY_EXHAUSTED,
    ERR_SERVICE_UNAVAILABLE,
    ERR_STORAGE,
    ERR_TIMEOUT,
    ERR_TOKEN_EXPIRED,
    ERR_VALIDATION,
    ERR_WORKFLOW,
    ERR_WORKFLOW_CYCLE,
    ERR_WORKFLOW_INVALID,
)

# HTTP status codes.
HTTP_400 = 400
HTTP_401 = 401
HTTP_403 = 403
HTTP_404 = 404
HTTP_409 = 409
HTTP_422 = 422
HTTP_429 = 429
HTTP_500 = 500
HTTP_502 = 502
HTTP_503 = 503
HTTP_504 = 504


class BaseAgentForgeException(Exception):
    """Base class for every AgentForge error."""

    status_code: int = HTTP_500
    error_code: str = ERR_INTERNAL

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        *,
        error_code: str | None = None,
        status_code: int | None = None,
        details: Any = None,
        cause: BaseException | None = None,
    ) -> None:
        """Initialise the exception.

        Args:
            message: Human-readable error description.
            error_code: Stable machine-readable code. Defaults to the class code.
            status_code: HTTP status code to map this exception to.
            details: Arbitrary structured payload included in error responses.
            cause: The underlying exception, if any.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.error_code
        self.status_code = status_code or self.__class__.status_code
        self.details = details
        self.cause = cause
        self.request_id: str | None = None

    def with_request_id(self, request_id: str | None) -> BaseAgentForgeException:
        """Attach the request that produced this error and return ``self``."""
        self.request_id = request_id
        return self

    def to_dict(self) -> dict[str, Any]:
        """Return a plain, JSON-serialisable description of the error."""
        return {
            "success": False,
            "error": self.message,
            "code": self.error_code,
            "details": self.details,
            "request_id": self.request_id,
        }

    def __repr__(self) -> str:
        extra = str(self.error_code)
        if self.details is not None:
            extra += f" details={self.details!r}"
        return f"{self.__class__.__name__}({self.message!r}, {extra})"


# ---------------------------------------------------------------------------
# Legacy alias used by the initial release of the library.
# ---------------------------------------------------------------------------
AgentForgeError = BaseAgentForgeException


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
class ValidationException(BaseAgentForgeException):
    """Raised when input fails validation."""

    status_code = HTTP_422
    error_code = ERR_VALIDATION

    def __init__(
        self,
        message: str = "Validation failed.",
        *,
        error_code: str | None = None,
        details: Any = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message, error_code=error_code, details=details, cause=cause)


# ---------------------------------------------------------------------------
# Authentication / authorization
# ---------------------------------------------------------------------------
class AuthenticationException(BaseAgentForgeException):
    """Raised when a caller cannot be authenticated."""

    status_code = HTTP_401
    error_code = ERR_AUTHENTICATION


class InvalidTokenException(AuthenticationException):
    """Raised when a token is malformed or fails signature verification."""

    status_code = HTTP_401
    error_code = ERR_INVALID_TOKEN


class TokenExpiredException(AuthenticationException):
    """Raised when a token is structurally valid but expired."""

    status_code = HTTP_401
    error_code = ERR_TOKEN_EXPIRED


class RefreshTokenExpiredException(AuthenticationException):
    """Raised when a refresh token rotation fails."""

    status_code = HTTP_401
    error_code = ERR_AUTHENTICATION_EXPIRED


class AuthorizationException(BaseAgentForgeException):
    """Raised when a caller lacks permission to perform an action."""

    status_code = HTTP_403
    error_code = ERR_AUTHORIZATION


class InsufficientScopeException(AuthorizationException):
    """Raised when a token's scopes are narrower than required."""

    status_code = HTTP_403
    error_code = ERR_INSUFFICIENT_SCOPE


class InsufficientPermissionException(AuthorizationException):
    """Raised when a caller lacks a specific permission."""

    status_code = HTTP_403
    error_code = ERR_INSUFFICIENT_PERMISSION


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------
class NotFoundException(BaseAgentForgeException):
    """Raised when a requested resource does not exist."""

    status_code = HTTP_404
    error_code = ERR_NOT_FOUND

    def __init__(
        self,
        message: str | None = None,
        *,
        resource: str | None = None,
        identifier: str | uuid.UUID | None = None,
        error_code: str | None = None,
    ) -> None:
        if message is None:
            message = f"{resource or 'Resource'} not found"
            if identifier is not None:
                message += f": {identifier}"
        self.resource = resource
        self.identifier = identifier
        super().__init__(message, error_code=error_code)


class ConflictException(BaseAgentForgeException):
    """Raised when the request conflicts with the current resource state."""

    status_code = HTTP_409
    error_code = ERR_CONFLICT


class AlreadyExistsException(ConflictException):
    """Raised when a unique resource already exists."""

    error_code = ERR_ALREADY_EXISTS


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
class RateLimitException(BaseAgentForgeException):
    """Raised when a caller exceeds a rate limit."""

    status_code = HTTP_429
    error_code = ERR_RATE_LIMITED

    def __init__(
        self,
        message: str = "Rate limit exceeded.",
        *,
        limit: int | None = None,
        remaining: int = 0,
        reset_at: float | None = None,
        retry_after_seconds: int = 1,
        details: Any = None,
    ) -> None:
        self.limit = limit
        self.remaining = remaining
        self.reset_at = reset_at
        self.retry_after_seconds = retry_after_seconds
        super().__init__(message, details=details)

    def response_headers(self) -> dict[str, str]:
        """Rate-limit headers matching the constants in :mod:`constants.headers`."""
        headers: dict[str, str] = {
            "retry-after": str(self.retry_after_seconds),
        }
        if self.limit is not None:
            headers["x-ratelimit-limit"] = str(self.limit)
        headers["x-ratelimit-remaining"] = str(self.remaining)
        if self.reset_at is not None:
            headers["x-ratelimit-reset"] = str(int(self.reset_at))
        return headers


# ---------------------------------------------------------------------------
# Providers / AI
# ---------------------------------------------------------------------------
class ProviderException(BaseAgentForgeException):
    """Raised when an upstream provider (LLM, vector store, ...) fails."""

    status_code = HTTP_502
    error_code = ERR_PROVIDER


class ProviderTimeoutException(ProviderException):
    """Raised when an upstream provider does not respond in time."""

    status_code = HTTP_504
    error_code = ERR_PROVIDER_TIMEOUT


class AIServiceException(BaseAgentForgeException):
    """Raised when an AI pipeline stage (embedding, RAG, generation) fails."""

    status_code = HTTP_502
    error_code = ERR_AI_SERVICE


# ---------------------------------------------------------------------------
# Workflows / executions
# ---------------------------------------------------------------------------
class WorkflowException(BaseAgentForgeException):
    """Raised when a workflow definition is invalid or cannot run."""

    status_code = HTTP_422
    error_code = ERR_WORKFLOW


class WorkflowCycleException(WorkflowException):
    """Raised when a workflow contains a cycle."""

    status_code = HTTP_422
    error_code = ERR_WORKFLOW_CYCLE


class WorkflowInvalidException(WorkflowException):
    """Raised when a workflow is structurally invalid."""

    error_code = ERR_WORKFLOW_INVALID


class ExecutionException(BaseAgentForgeException):
    """Raised when an execution fails at runtime."""

    status_code = HTTP_500
    error_code = ERR_EXECUTION


class ExecutionTimeoutException(ExecutionException):
    """Raised when an execution exceeds its deadline."""

    status_code = HTTP_504
    error_code = ERR_EXECUTION_TIMEOUT


# ---------------------------------------------------------------------------
# Transient infrastructure
# ---------------------------------------------------------------------------
class TimeoutException(BaseAgentForgeException):
    """Raised when any operation exceeds its configured timeout."""

    status_code = HTTP_504
    error_code = ERR_TIMEOUT


class StorageException(BaseAgentForgeException):
    """Raised when file/object storage operations fail."""

    status_code = HTTP_500
    error_code = ERR_STORAGE


class CacheException(BaseAgentForgeException):
    """Raised when cache operations fail."""

    status_code = HTTP_500
    error_code = ERR_CACHE


class RetryExhaustedException(BaseAgentForgeException):
    """Raised when retry policies give up."""

    status_code = HTTP_503
    error_code = ERR_RETRY_EXHAUSTED


class CircuitOpenException(BaseAgentForgeException):
    """Raised when a circuit breaker is open and refuses calls."""

    status_code = HTTP_503
    error_code = ERR_CIRCUIT_OPEN


class ServiceUnavailableException(BaseAgentForgeException):
    """Raised when a required dependency is unavailable."""

    status_code = HTTP_503
    error_code = ERR_SERVICE_UNAVAILABLE


class ConfigurationException(BaseAgentForgeException):
    """Raised when application configuration is invalid or missing."""

    status_code = HTTP_500
    error_code = ERR_CONFIGURATION


class NotImplementedException(BaseAgentForgeException):
    """Raised for intentionally unimplemented functionality."""

    status_code = HTTP_500
    error_code = ERR_NOT_IMPLEMENTED


# ---------------------------------------------------------------------------
# Legacy aliases (kept for source compatibility with the first release).
# ---------------------------------------------------------------------------
ValidationError = ValidationException
AuthenticationError = AuthenticationException
AuthorizationError = AuthorizationException
NotFoundError = NotFoundException
ConfigurationError = ConfigurationException
ExecutionError = ExecutionException


def exception_to_dict(exc: BaseException) -> dict[str, Any]:
    """Best-effort conversion of any exception into the standard error envelope.

    Unknown exceptions are normalised to :class:`BaseAgentForgeException` with
    the internal error code so callers always receive the stable shape.
    """
    if isinstance(exc, BaseAgentForgeException):
        return exc.to_dict()
    return BaseAgentForgeException(str(exc)).to_dict()


# Convenience re-export of the result type for callers mapping exceptions.
ExceptionKind = Literal["validation", "auth", "authorization", "not_found", "internal"]

__all__ = [
    "BaseAgentForgeException",
    "AgentForgeError",
    "ValidationException",
    "AuthenticationException",
    "InvalidTokenException",
    "TokenExpiredException",
    "RefreshTokenExpiredException",
    "AuthorizationException",
    "InsufficientScopeException",
    "InsufficientPermissionException",
    "NotFoundException",
    "ConflictException",
    "AlreadyExistsException",
    "RateLimitException",
    "ProviderException",
    "ProviderTimeoutException",
    "AIServiceException",
    "WorkflowException",
    "WorkflowCycleException",
    "WorkflowInvalidException",
    "ExecutionException",
    "ExecutionTimeoutException",
    "TimeoutException",
    "StorageException",
    "CacheException",
    "RetryExhaustedException",
    "CircuitOpenException",
    "ServiceUnavailableException",
    "ConfigurationException",
    "NotImplementedException",
    # Legacy aliases
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConfigurationError",
    "ExecutionError",
    "exception_to_dict",
]
