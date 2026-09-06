"""Context variable binding for structured logs and tracing."""

from __future__ import annotations

import contextvars
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

#: Well-known keys attached to every log line via structlog contextvars.
_CONTEXT_KEY = "request_id"
_CONTEXT_KEYS: tuple[str, ...] = (
    "request_id",
    "correlation_id",
    "trace_id",
    "span_id",
    "user_id",
    "tenant_id",
    "organization_id",
    "agent_id",
    "execution_id",
    "workflow_id",
    "service",
    "version",
    "environment",
)

_context: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar("agentforge_log_ctx", default={})


def context_dict() -> dict[str, Any]:
    """Snapshot of the current bound context (values only)."""
    return dict(_context.get())


def bind_context(**kwargs: Any) -> None:
    """Bind key/value pairs into the current context."""
    filtered = {k: v for k, v in kwargs.items() if v is not None and k in _CONTEXT_KEYS}
    if not filtered:
        return
    data = dict(_context.get())
    data.update(filtered)
    _context.set(data)
    try:
        import structlog.contextvars

        structlog.contextvars.bind_contextvars(**filtered)
    except Exception:  # pragma: no cover  # fmt is optional at runtime
        pass


def unbind_context(*keys: str) -> None:
    """Remove specific keys from the context."""
    data = dict(_context.get())
    for key in keys:
        data.pop(key, None)
    _context.set(data)
    try:
        import structlog.contextvars

        structlog.contextvars.unbind_contextvars(*keys)
    except Exception:  # pragma: no cover
        pass


def clear_context() -> None:
    """Clear all bound context keys (start/end of a request)."""
    _context.set({})
    try:
        import structlog.contextvars

        structlog.contextvars.clear_contextvars()
    except Exception:  # pragma: no cover
        pass


def reset_context() -> None:
    """Alias of :func:`clear_context`."""
    clear_context()


class BoundContext:
    """Context-manager binding of log context for a block.

    Example::

        with BoundContext(request_id="req-1", user_id="u1"):
            ...
    """

    __slots__ = ("_saved",)

    def __init__(self, **kwargs: Any) -> None:
        self._saved = dict(_context.get())
        if kwargs:
            bind_context(**kwargs)

    def __enter__(self) -> BoundContext:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        _context.set(self._saved)
        try:
            import structlog.contextvars

            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(**self._saved)
        except Exception:  # pragma: no cover
            pass
        return False


def with_context(**kwargs: Any) -> Callable[[T], T]:
    """Decorator that binds ``kwargs`` around a callable's execution."""

    def _decorator(fn: T) -> T:
        def _wrapped(*args: Any, **call_kwargs: Any) -> Any:
            with BoundContext(**kwargs):
                return fn(*args, **call_kwargs)

        return _wrapped  # type: ignore[return-value]

    return _decorator


def get_request_id() -> str | None:
    """Return the bound request id, if any."""
    return _context.get().get("request_id")


__all__ = [
    "context_dict",
    "bind_context",
    "unbind_context",
    "clear_context",
    "reset_context",
    "BoundContext",
    "with_context",
    "get_request_id",
    "_CONTEXT_KEY",
    "_CONTEXT_KEYS",
]
