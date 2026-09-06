"""Declarative validation helpers built on the validators.

Provides small classes that integrate with Pydantic v2 ``field_validator`` and
standalone checks, plus an ``ensure`` runner for pipelines.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .validators import (
    validate_email,
    validate_password,
    validate_url,
    validate_uuid,
)

ValidatorFn = Callable[[Any], Any]


class Validate:
    """Namespace of pre-built validators usable in Pydantic ``field_validator``.

    Example::

        from pydantic import BaseModel, field_validator
        from agentforge_shared.validation import Validate

        class Signup(BaseModel):
            email: str
            password: str

            _email = field_validator("email")(Validate(email=True))
    """

    @staticmethod
    def email(value: Any) -> str:
        """Validate an email address."""
        return validate_email(value)

    @staticmethod
    def url(value: Any) -> str:
        """Validate a URL."""
        return validate_url(value)

    @staticmethod
    def uuid(value: Any) -> object:
        """Validate a UUID (any version)."""
        return validate_uuid(value)

    @staticmethod
    def password(*, min_length: int = 8, require_upper: bool = True) -> ValidatorFn:
        """Construct a password validator with the given policy."""
        return lambda value: validate_password(
            value, min_length=min_length, require_upper=require_upper
        )


def ensure(*validators: ValidatorFn) -> ValidatorFn:
    """Compose validators into a single pipeline.

    Each validator runs in order; the first failure short-circuits.
    """

    def _runner(value: Any) -> Any:
        result = value
        for fn in validators:
            result = fn(result)
        return result

    return _runner


__all__ = ["Validate", "ensure", "ValidatorFn"]
