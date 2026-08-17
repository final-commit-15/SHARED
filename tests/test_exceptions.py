"""Exception hierarchy tests."""

import pytest
from agentforge_shared.exceptions import (
    AgentForgeError,
    ValidationError,
    AuthenticationError,
    NotFoundError,
)


def test_exception_inheritance():
    assert issubclass(ValidationError, AgentForgeError)
    assert issubclass(AuthenticationError, AgentForgeError)
    assert issubclass(NotFoundError, AgentForgeError)


def test_exception_raise():
    with pytest.raises(ValidationError):
        raise ValidationError("Invalid input")