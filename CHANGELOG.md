# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial production-ready release of `agentforge-shared`.
- Configuration system (`config/`) backed by `pydantic-settings` with `.env`,
  environment variables, secrets directory, nested settings, and per-environment presets.
- Centralised constants (`constants/`) covering API, headers, limits, timeouts,
  paths, roles, permissions, error codes, MIME types, and model metadata.
- Enumerations (`enums/`) for the entire platform: users, execution, providers,
  workflows, events, notifications, audit, health, permissions, and capabilities.
- Shared Pydantic v2 schemas (`schemas/`): generic `APIResponse[T]`,
  `PaginatedResponse[T]`, `ErrorResponse`, health models, and reusable mixins.
- DTO layer (`dto/`) for chat, embeddings, RAG, execution, agents, workflows,
  memory, search, token usage, cost estimation, and streaming.
- Event contracts (`events/`) with trace/correlation propagation.
- Security package (`security/`): JWT (HS256, refresh tokens), bcrypt password
  hashing, API keys, request signing, scope parsing, and permission checks.
- Middleware (`middleware/`): request ID, correlation ID, logging, timing,
  exception mapping, security headers, CORS, trusted hosts, compression, and
  rate limiting.
- Exception hierarchy (`exceptions/`) mapped to HTTP status codes.
- Structured JSON logging (`logging/`) via structlog with context variables and
  sensitive value masking.
- Telemetry (`telemetry/`): OpenTelemetry tracing and Prometheus metrics.
- Retry utilities (`retry/`): tenacity wrappers, backoff policies, circuit
  breaker, and timeout helpers.
- Cache abstractions (`cache/`): async Redis cache with namespaces, TTL
  handling, and JSON serialization.
- Utilities (`utils/`): datetime, UUIDv7, hashing, JSON, files, strings,
  collections, environment, async, batching, chunking, and safe parsing.
- Pagination (`pagination/`): offset and cursor pagination with sort/filter/search.
- Validation (`validation/`): email, password, URL, UUID, file, JSON, cron, env.
- Typing helpers (`typing/`): `Result[T]`, `Maybe[T]`, `JSONType`, protocols.
- Versioning (`version/`): semantic version parsing, compatibility checks,
  deprecation helpers.
- Metadata (`metadata/`): build, version, git, environment, and runtime info.
- API helpers (`api/`): response, error, pagination, streaming, and SSE builders.
- Test suite with 100+ tests across every module.
- Examples, scripts, Docker support, and full developer tooling.