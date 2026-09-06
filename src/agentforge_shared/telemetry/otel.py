"""OpenTelemetry tracing helpers (safe import; no-ops when disabled)."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager, nullcontext
from typing import Any

from agentforge_shared.config.telemetry import ObservabilitySettings

_ENABLED = False


def setup_otel(settings: ObservabilitySettings | None = None, *, enabled: bool = False) -> bool:
    """Initialise the OpenTelemetry tracer provider.

    Args:
        settings: Observability settings (defaults to env-driven values).
        enabled: Force enable/disable tracing.

    Returns:
        ``True`` when tracing is active.
    """
    global _ENABLED
    if not enabled:
        _ENABLED = False
        return False
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanExporter, ConsoleSpanExporter

        if settings is None:
            settings = ObservabilitySettings()
        attributes = {"service.name": settings.service_name or "agentforge"}
        if settings.environment:
            attributes["deployment.environment"] = settings.environment
        resource = Resource.create(attributes)
        provider = TracerProvider(resource=resource)
        if settings.exporter == "console":
            provider.add_span_processor(BatchSpanExporter(ConsoleSpanExporter()))
        elif settings.exporter == "otlp":
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

            endpoint = settings.endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
            if endpoint:
                provider.add_span_processor(BatchSpanExporter(OTLPSpanExporter(endpoint=endpoint)))
        trace.set_tracer_provider(provider)
        _ENABLED = True
        return True
    except ImportError:
        _ENABLED = False
        return False


def is_enabled() -> bool:
    """Whether tracing has been activated."""
    return _ENABLED


def get_tracer(name: str = "agentforge"):
    """Return the OpenTelemetry tracer for ``name`` (no-op when disabled)."""
    try:
        from opentelemetry import trace as _otel_trace

        return _otel_trace.get_tracer(name)
    except ImportError:  # pragma: no cover
        return None


def start_span(name: str, *, attributes: dict[str, Any] | None = None, **kwargs: Any):
    """Start a tracing span via a context manager (safe fallback)."""
    tracer = get_tracer()
    if tracer is None or not _ENABLED:
        return nullcontext()
    return tracer.start_as_current_span(name=name, attributes=attributes or {}, **kwargs)


def get_active_span_context() -> dict[str, str | None]:
    """Expose the current trace/span ids (empty when tracing is off)."""
    try:
        from opentelemetry import trace as _otel_trace

        span_context = _otel_trace.get_current_span().get_span_context()
        if not span_context.is_valid:
            return {"trace_id": None, "span_id": None}
        return {
            "trace_id": format(span_context.trace_id, "032x"),
            "span_id": format(span_context.span_id, "016x"),
        }
    except (ImportError, AttributeError):  # pragma: no cover
        return {"trace_id": None, "span_id": None}


@contextmanager
def span(name: str, *, attributes: dict[str, Any] | None = None, **kwargs: Any) -> Generator[Any, None, None]:
    """Context manager wrapping :func:`start_span` for use in services."""
    with start_span(name, attributes=attributes, **kwargs) as active:
        yield active


__all__ = ["setup_otel", "is_enabled", "get_tracer", "start_span", "get_active_span_context", "span"]
