"""HTTP/correlation header names used across AgentForge services."""

# Correlation / tracing
HEADER_REQUEST_ID = "x-request-id"
HEADER_CORRELATION_ID = "x-correlation-id"
HEADER_TRACE_ID = "x-trace-id"
HEADER_SPAN_ID = "x-span-id"
HEADER_BAGGAGE = "baggage"

# Convenient aliases used by middleware.
REQUEST_ID_HEADER = HEADER_REQUEST_ID
CORRELATION_ID_HEADER = HEADER_CORRELATION_ID
TRACE_ID_HEADER = HEADER_TRACE_ID

# W3C Trace Context
TRACEPARENT = "traceparent"
TRACESTATE = "tracestate"

# Authentication
HEADER_AUTHORIZATION = "authorization"
HEADER_API_KEY = "x-api-key"
HEADER_JWT = "x-jwt"
HEADER_REFRESH_TOKEN = "x-refresh-token"
HEADER_SERVICE_TOKEN = "x-service-token"

# Client identity / provenance
HEADER_USER_AGENT = "user-agent"
HEADER_FORWARDED_FOR = "x-forwarded-for"
HEADER_REAL_IP = "x-real-ip"
HEADER_ORIGIN = "origin"
HEADER_REFERER = "referer"
HEADER_HOST = "host"

# Pagination / rate limit
HEADER_TOTAL_COUNT = "x-total-count"
HEADER_PAGE = "x-page"
HEADER_PER_PAGE = "x-per-page"
HEADER_TOTAL_PAGES = "x-total-pages"
HEADER_RATE_LIMIT = "x-ratelimit-limit"
HEADER_RATE_REMAINING = "x-ratelimit-remaining"
HEADER_RATE_RESET = "x-ratelimit-reset"
HEADER_RETRY_AFTER = "retry-after"

# Caching
HEADER_CACHE_CONTROL = "cache-control"
HEADER_ETAG = "etag"
HEADER_IF_NONE_MATCH = "if-none-match"
HEADER_LAST_MODIFIED = "last-modified"
HEADER_EXPIRES = "expires"

# Security headers (response)
HEADER_SERVER = "server"
HEADER_X_FRAME_OPTIONS = "x-frame-options"
HEADER_X_CONTENT_TYPE_OPTIONS = "x-content-type-options"
HEADER_REFERRER_POLICY = "referrer-policy"
HEADER_STRICT_TRANSPORT = "strict-transport-security"
HEADER_CONTENT_SECURITY_POLICY = "content-security-policy"
HEADER_PERMISSIONS_POLICY = "permissions-policy"
HEADER_CROSS_ORIGIN_OPENER_POLICY = "cross-origin-opener-policy"

# CORS
HEADER_ACCESS_CONTROL_ALLOW_ORIGIN = "access-control-allow-origin"
HEADER_ACCESS_CONTROL_ALLOW_METHODS = "access-control-allow-methods"
HEADER_ACCESS_CONTROL_ALLOW_HEADERS = "access-control-allow-headers"
HEADER_ACCESS_CONTROL_EXPOSE_HEADERS = "access-control-expose-headers"
HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS = "access-control-allow-credentials"
HEADER_ACCESS_CONTROL_MAX_AGE = "access-control-max-age"
HEADER_ACCESS_CONTROL_REQUEST_METHOD = "access-control-request-method"
HEADER_ACCESS_CONTROL_REQUEST_HEADERS = "access-control-request-headers"
HEADER_VARY = "vary"

# Content negotiation
HEADER_CONTENT_TYPE = "content-type"
HEADER_ACCEPT = "accept"
HEADER_ACCEPT_ENCODING = "accept-encoding"
HEADER_CONTENT_ENCODING = "content-encoding"
HEADER_CONTENT_LENGTH = "content-length"
HEADER_CONTENT_DISPOSITION = "content-disposition"

# Misc
HEADER_X_POWERED_BY = "x-powered-by"
HEADER_IDEMPOTENCY_KEY = "idempotency-key"
HEADER_LOCATION = "location"

# Standard exposure for the API.
API_EXPOSE_HEADERS = ",".join(
    [
        HEADER_TOTAL_COUNT,
        HEADER_PAGE,
        HEADER_PER_PAGE,
        HEADER_TOTAL_PAGES,
        HEADER_RATE_LIMIT,
        HEADER_RATE_REMAINING,
        HEADER_RATE_RESET,
    ]
)
