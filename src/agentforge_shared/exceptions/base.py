"""Custom exception hierarchy for AgentForge."""


class AgentForgeError(Exception):
    """Base exception for all AgentForge errors."""
    pass


class ValidationError(AgentForgeError):
    """Raised when input validation fails."""
    pass


class AuthenticationError(AgentForgeError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(AgentForgeError):
    """Raised when the user lacks permission."""
    pass


class NotFoundError(AgentForgeError):
    """Raised when a requested resource is not found."""
    pass


class ConfigurationError(AgentForgeError):
    """Raised for configuration-related errors."""
    pass


class ExecutionError(AgentForgeError):
    """Raised when an agent execution fails."""
    pass