"""Server-sent event (SSE) helpers."""

from __future__ import annotations

import json as _std_json
from collections.abc import AsyncIterable
from typing import Any

from fastapi.responses import StreamingResponse


def encode_sse_event(
    *,
    event: str,
    data: Any,
    event_id: str | None = None,
    retry: int | None = None,
) -> str:
    """Encode a single SSE frame.

    The ``data`` payload is JSON-serialized; multiline-safe so a Pydantic
    model can be passed directly.
    """
    lines: list[str] = []
    if event_id is not None:
        lines.append(f"id: {event_id}")
    if event is not None:
        lines.append(f"event: {event}")
    if retry is not None:
        lines.append(f"retry: {retry}")
    body = data if isinstance(data, str) else _std_json.dumps(data, default=str)
    for piece in body.splitlines():
        lines.append(f"data: {piece}")
    return "\n".join(lines) + "\n\n"


async def sse_event_generator(
    events: AsyncIterable[Any],
    *,
    event_name: str = "message",
) -> AsyncIterable[str]:
    """Wrap an async iterable of payloads into SSE frames."""
    async for item in events:
        yield encode_sse_event(event=event_name, data=item)


def sse_response(
    events: AsyncIterable[Any],
    *,
    event_name: str = "message",
    media_type: str = "text/event-stream",
    headers: dict[str, str] | None = None,
) -> StreamingResponse:
    """Build a ``StreamingResponse`` that emits SSE frames."""
    default_headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }
    if headers:
        default_headers.update(headers)
    return StreamingResponse(
        sse_event_generator(events, event_name=event_name),
        media_type=media_type,
        headers=default_headers,
    )


def ping_frame(event_id: str | None = None) -> str:
    """Emit an SSE heartbeat/keep-alive frame."""
    return encode_sse_event(event="ping", data={}, event_id=event_id, retry=15000)


__all__ = ["encode_sse_event", "sse_event_generator", "sse_response", "ping_frame"]
