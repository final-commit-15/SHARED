"""FastAPI-facing helpers: envelopes, errors, pagination, streaming, dependencies."""

from .dependencies import (
    Principal,
    apply_pagination_dependencies,
    current_principal,
    get_pagination_dependencies,
    require_permission,
    require_role,
    verify_token,
)
from .errors import (
    agentforge_exception_handler,
    exception_to_response,
    register_exception_handlers,
    validation_exception_handler,
)
from .pagination import cursor_data, paginated_data, paginated_response
from .response import created, fail, no_content, ok, success
from .streaming import (
    encode_sse_event,
    ping_frame,
    sse_event_generator,
    sse_response,
)

__all__ = [
    # response builders
    "ok",
    "created",
    "no_content",
    "success",
    "fail",
    # pagination builders
    "paginated_response",
    "paginated_data",
    "cursor_data",
    # error handling
    "exception_to_response",
    "agentforge_exception_handler",
    "validation_exception_handler",
    "register_exception_handlers",
    # streaming / SSE
    "encode_sse_event",
    "sse_event_generator",
    "sse_response",
    "ping_frame",
    # dependencies
    "Principal",
    "current_principal",
    "verify_token",
    "require_role",
    "require_permission",
    "apply_pagination_dependencies",
    "get_pagination_dependencies",
]
