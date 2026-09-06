"""Document and indexing lifecycle events."""

from __future__ import annotations

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType

from .base import BaseEvent


class DocumentUploadedEvent(BaseEvent):
    """Published when a document is uploaded."""

    event_type: EventType = EventType.DOCUMENT_UPLOADED
    source: EventSource = EventSource.BACKEND

    document_id: str
    filename: str
    size_bytes: int = Field(default=0, ge=0)
    mime_type: str | None = None
    workspace_id: str | None = None
    uploaded_by: str | None = None


class DocumentIndexedEvent(BaseEvent):
    """Published when a document has been indexed for retrieval."""

    event_type: EventType = EventType.DOCUMENT_INDEXED
    source: EventSource = EventSource.AI_SERVICES

    document_id: str
    collection: str
    chunk_count: int = Field(default=0, ge=0)
    tokens_used: int = Field(default=0, ge=0)
    embedding_model: str | None = None


class DocumentDeletedEvent(BaseEvent):
    """Published when a document is deleted."""

    event_type: EventType = EventType.DOCUMENT_DELETED
    source: EventSource = EventSource.BACKEND

    document_id: str
    collection: str | None = None
    deleted_by: str | None = None


class DocumentIndexFailedEvent(BaseEvent):
    """Published when indexing a document fails."""

    event_type: EventType = EventType.DOCUMENT_INDEX_FAILED
    source: EventSource = EventSource.AI_SERVICES

    document_id: str
    error_code: str | None = None
    error_message: str | None = None
    retryable: bool = True


__all__ = [
    "DocumentUploadedEvent",
    "DocumentIndexedEvent",
    "DocumentDeletedEvent",
    "DocumentIndexFailedEvent",
]
