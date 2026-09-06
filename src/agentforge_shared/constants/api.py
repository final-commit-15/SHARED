"""API-related constants: versioning, prefixes, and content types."""

API_VERSION = "v1"
API_MAJOR_VERSION = "v1"
API_PREFIX = "/api"
API_V1_PREFIX = "/api/v1"
API_V2_PREFIX = "/api/v2"
API_HEALTH_PATH = "/health"
API_LIVEZ_PATH = "/health/live"
API_READYZ_PATH = "/health/ready"
API_METRICS_PATH = "/metrics"
API_DOCS_PATH = "/docs"
API_REDOC_PATH = "/redoc"
API_OPENAPI_PATH = "/openapi.json"
API_DEFAULT_LANG = "en"

# Response envelope field names, kept stable across the platform.
API_FIELD_SUCCESS = "success"
API_FIELD_DATA = "data"
API_FIELD_ERROR = "error"
API_FIELD_CODE = "code"
API_FIELD_DETAILS = "details"
API_FIELD_MESSAGE = "message"
API_FIELD_PAGINATION = "pagination"
API_FIELD_METADATA = "metadata"
API_FIELD_TRACE_ID = "trace_id"
API_FIELD_REQUEST_ID = "request_id"
API_FIELD_CORRELATION_ID = "correlation_id"
API_FIELD_TIMESTAMP = "timestamp"
API_FIELD_VERSION = "version"

# Well-known error code prefix for the platform.
ERROR_CODE_PREFIX = "AF"
ERROR_CODE_SEPARATOR = "_"

# JSON content type / status helpers.
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_SSE = "text/event-stream"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"
CONTENT_TYPE_MULTIPART = "multipart/form-data"

# Pagination defaults exposed through API contracts.
API_DEFAULT_PAGE = 1
API_DEFAULT_PER_PAGE = 20

# Max accepted page size for query parameters.
API_MAX_PER_PAGE = 100

# Reserved status codes commonly returned for idempotency conflicts.
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE = 422

# Stream chunk terminators.
SSE_DATA_PREFIX = "data: "
SSE_EVENT_PREFIX = "event: "
SSE_DONE_EVENT = "done"
SSE_ERROR_EVENT = "error"
SSE_PING_EVENT = "ping"
SSE_KEEPALIVE_SECONDS = 15
