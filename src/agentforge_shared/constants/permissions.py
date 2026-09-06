"""Permission identifiers for the entire platform.

Permissions follow the convention ``<resource>:<action>`` where ``action`` is
one of ``create``, ``read``, ``update``, ``delete``, ``execute``, ``manage``.
Wildcard ``*`` grants every action on the resource.
"""

# --- Users ---------------------------------------------------------------
PERM_USER_CREATE = "user:create"
PERM_USER_READ = "user:read"
PERM_USER_UPDATE = "user:update"
PERM_USER_DELETE = "user:delete"
PERM_USER_MANAGE = "user:manage"
PERM_USER_LIST = "user:list"
PERM_USER_IMPERSONATE = "user:impersonate"

# --- Agents ---------------------------------------------------------------
PERM_AGENT_CREATE = "agent:create"
PERM_AGENT_READ = "agent:read"
PERM_AGENT_UPDATE = "agent:update"
PERM_AGENT_DELETE = "agent:delete"
PERM_AGENT_EXECUTE = "agent:execute"
PERM_AGENT_MANAGE = "agent:manage"
PERM_AGENT_PUBLISH = "agent:publish"
PERM_AGENT_DEPLOY = "agent:deploy"
PERM_AGENT_LIST = "agent:list"

# --- Workflows ------------------------------------------------------------
PERM_WORKFLOW_CREATE = "workflow:create"
PERM_WORKFLOW_READ = "workflow:read"
PERM_WORKFLOW_UPDATE = "workflow:update"
PERM_WORKFLOW_DELETE = "workflow:delete"
PERM_WORKFLOW_EXECUTE = "workflow:execute"
PERM_WORKFLOW_MANAGE = "workflow:manage"
PERM_WORKFLOW_PUBLISH = "workflow:publish"

# --- Models / LLM ---------------------------------------------------------
PERM_MODEL_READ = "model:read"
PERM_MODEL_USE = "model:use"
PERM_MODEL_MANAGE = "model:manage"
PERM_EMBEDDING_USE = "embedding:use"

# --- Memory ---------------------------------------------------------------
PERM_MEMORY_READ = "memory:read"
PERM_MEMORY_WRITE = "memory:write"
PERM_MEMORY_DELETE = "memory:delete"
PERM_MEMORY_MANAGE = "memory:manage"

# --- Search / RAG ---------------------------------------------------------
PERM_SEARCH_USE = "search:use"
PERM_SEARCH_MANAGE = "search:manage"
PERM_DOCUMENT_UPLOAD = "document:upload"
PERM_DOCUMENT_READ = "document:read"
PERM_DOCUMENT_DELETE = "document:delete"
PERM_DOCUMENT_INDEX = "document:index"

# --- Integrations ---------------------------------------------------------
PERM_INTEGRATION_READ = "integration:read"
PERM_INTEGRATION_WRITE = "integration:write"
PERM_INTEGRATION_DELETE = "integration:delete"
PERM_INTEGRATION_MANAGE = "integration:manage"
PERM_WEBHOOK_SEND = "webhook:send"

# --- Executions -----------------------------------------------------------
PERM_EXECUTION_READ = "execution:read"
PERM_EXECUTION_LIST = "execution:list"
PERM_EXECUTION_CANCEL = "execution:cancel"
PERM_EXECUTION_RETRY = "execution:retry"

# --- Billing / usage ------------------------------------------------------
PERM_BILLING_READ = "billing:read"
PERM_USAGE_READ = "usage:read"
PERM_TOKEN_USAGE_READ = "token-usage:read"

# --- Platform administration ----------------------------------------------
PERM_SYSTEM_HEALTH = "system:health"
PERM_SYSTEM_METRICS = "system:metrics"
PERM_SYSTEM_CONFIG = "system:config"
PERM_SYSTEM_LOGS = "system:logs"
PERM_SYSTEM_MAINTENANCE = "system:maintenance"
PERM_AUDIT_READ = "audit:read"
PERM_RATE_LIMIT_MANAGE = "ratelimit:manage"
PERM_FEATURE_FLAG_MANAGE = "feature-flag:manage"

# --- Service accounts -----------------------------------------------------
PERM_SERVICE_TOKEN = "service:token"
PERM_SERVICE_REGISTER = "service:register"

# Wildcard
PERM_ALL = "*"

ALL_PERMISSIONS: frozenset[str] = frozenset(
    {value for name, value in list(globals().items()) if name.startswith("PERM_")}
)

# Default permissions granted to a fresh, fully-privileged role.
SUPER_ADMIN_PERMISSIONS: frozenset[str] = frozenset({PERM_ALL})

# Role -> permission mapping used by ``security.permissions.PermissionChecker``.
_READ_ONLY: frozenset[str] = frozenset(
    {
        PERM_USER_READ,
        PERM_USER_LIST,
        PERM_AGENT_READ,
        PERM_AGENT_LIST,
        PERM_WORKFLOW_READ,
        PERM_MODEL_READ,
        PERM_MEMORY_READ,
        PERM_SEARCH_USE,
        PERM_DOCUMENT_READ,
        PERM_INTEGRATION_READ,
        PERM_EXECUTION_READ,
        PERM_EXECUTION_LIST,
        PERM_BILLING_READ,
        PERM_USAGE_READ,
        PERM_TOKEN_USAGE_READ,
        PERM_SYSTEM_HEALTH,
        PERM_AUDIT_READ,
    }
)

_ANALYST: frozenset[str] = _READ_ONLY | frozenset(
    {
        PERM_AGENT_EXECUTE,
        PERM_WORKFLOW_EXECUTE,
        PERM_MODEL_USE,
        PERM_EMBEDDING_USE,
        PERM_MEMORY_WRITE,
        PERM_SEARCH_MANAGE,
        PERM_DOCUMENT_UPLOAD,
        PERM_DOCUMENT_INDEX,
        PERM_INTEGRATION_WRITE,
        PERM_EXECUTION_CANCEL,
        PERM_EXECUTION_RETRY,
        PERM_WEBHOOK_SEND,
    }
)

_OPERATOR: frozenset[str] = _ANALYST | frozenset(
    {
        PERM_USER_UPDATE,
        PERM_AGENT_CREATE,
        PERM_AGENT_UPDATE,
        PERM_AGENT_DELETE,
        PERM_AGENT_PUBLISH,
        PERM_AGENT_DEPLOY,
        PERM_WORKFLOW_CREATE,
        PERM_WORKFLOW_UPDATE,
        PERM_WORKFLOW_DELETE,
        PERM_WORKFLOW_PUBLISH,
        PERM_MEMORY_DELETE,
        PERM_DOCUMENT_DELETE,
        PERM_INTEGRATION_DELETE,
        PERM_SYSTEM_CONFIG,
        PERM_SYSTEM_LOGS,
        PERM_SERVICE_TOKEN,
    }
)

ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "super_admin": SUPER_ADMIN_PERMISSIONS,
    "admin": frozenset(ALL_PERMISSIONS - {PERM_USER_IMPERSONATE}),
    "operator": _OPERATOR,
    "analyst": _ANALYST,
    "auditor": _READ_ONLY,
    "user": _READ_ONLY - {PERM_AUDIT_READ},
}
