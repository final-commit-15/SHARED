"""String manipulation utilities."""

from __future__ import annotations

import re
import secrets
import string as _string
import unicodedata


def snake_case(value: str) -> str:
    """Convert arbitrary text to ``snake_case``."""
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(c for c in normalized if not unicodedata.combining(c))
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", ascii_text)
    s = re.sub(r"[^\w]", " ", s)
    s = re.sub(r"\s+", "_", s.strip()).lower()
    return s


def kebab_case(value: str) -> str:
    """Convert arbitrary text to ``kebab-case``."""
    return snake_case(value).replace("_", "-")


def camel_case(value: str) -> str:
    """Convert arbitrary text to ``camelCase``."""
    words = [w for w in re.split(r"[_\-\s]+", snake_case(value)) if w]
    return words[0] + "".join(w.capitalize() for w in words[1:])


def pascal_case(value: str) -> str:
    """Convert arbitrary text to ``PascalCase``."""
    words = [w for w in re.split(r"[_\-\s]+", snake_case(value)) if w]
    return "".join(w.capitalize() for w in words) if words else ""


def title_case(value: str) -> str:
    """Convert arbitrary text to ``Title Case``."""
    return " ".join(w.capitalize() for w in value.replace("_", " ").replace("-", " ").split())


def truncate(value: str, length: int = 200, suffix: str = "...") -> str:
    """Truncate ``value`` to ``length`` characters, appending ``suffix``."""
    if length < 0:
        raise ValueError("length must be >= 0")
    if len(value) <= length:
        return value
    return value[:length] + suffix


def first_non_empty(values: list[str | None]) -> str | None:
    """Return the first non-empty (after stripping) value, else ``None``."""
    for value in values:
        if value and value.strip():
            return value.strip()
    return None


def normalize_whitespace(value: str) -> str:
    """Collapse consecutive whitespace into single spaces and trim."""
    return re.sub(r"\s+", " ", value).strip()


def is_blank(value: str | None) -> bool:
    """Return ``True`` for ``None`` / empty / whitespace-only strings."""
    return not (value and value.strip())


def has_text(value: str | None) -> bool:
    """Inverse of :func:`is_blank`."""
    return not is_blank(value)


def slugify(value: str) -> str:
    """Produce a URL-safe slug from arbitrary text."""
    s = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def random_string(length: int = 16, *, alphabet: str | None = None) -> str:
    """Return a cryptographically random string of ``length`` chars."""
    chars = alphabet or (_string.ascii_letters + _string.digits)
    if length < 1:
        raise ValueError("length must be >= 1")
    return "".join(secrets.choice(chars) for _ in range(length))


def mask(value: str | None, *, visible: int = 4, mask_char: str = "*") -> str:
    """Mask ``value`` keeping the last ``visible`` characters visible."""
    if not value:
        return ""
    if len(value) <= visible:
        return mask_char * len(value)
    return mask_char * (len(value) - visible) + value[-visible:]


def mask_email(value: str) -> str:
    """Partially mask an email address: ``jo**@example.com``."""
    if "@" not in value:
        return mask(value)
    local, _, domain = value.partition("@")
    if len(local) <= 2:
        return f"{'*' * len(local)}@{domain}"
    return f"{local[:2]}{'*' * (len(local) - 2)}@{domain}"


def mask_token(value: str, *, visible: int = 6) -> str:
    """Mask a token showing only the last ``visible`` characters."""
    return mask(value, visible=visible)


def ellipsize_middle(value: str, *, max_length: int = 40) -> str:
    """Shorten long strings by replacing the middle with ``...``."""
    if len(value) <= max_length:
        return value
    half = (max_length - 3) // 2
    return f"{value[:half]}...{value[-half:]}"


def remove_prefix(value: str, prefix: str) -> str:
    """Strip ``prefix`` from ``value`` when present."""
    return value[len(prefix) :] if value.startswith(prefix) else value


def remove_suffix(value: str, suffix: str) -> str:
    """Strip ``suffix`` from ``value`` when present."""
    return value[: -len(suffix)] if value.endswith(suffix) else value


def ascii_only(value: str) -> str:
    """Return ``value`` with non-ASCII characters removed."""
    return value.encode("ascii", "ignore").decode("ascii")


def has_uppercase(value: str) -> bool:
    """Return ``True`` when ``value`` contains at least one uppercase letter."""
    return any(c.isupper() for c in value)


def has_lowercase(value: str) -> bool:
    """Return ``True`` when ``value`` contains at least one lowercase letter."""
    return any(c.islower() for c in value)


def has_digit(value: str) -> bool:
    """Return ``True`` when ``value`` contains at least one digit."""
    return any(c.isdigit() for c in value)


def has_symbol(value: str) -> bool:
    """Return ``True`` when ``value`` contains at least one non-alphanumeric char."""
    return any(not c.isalnum() for c in value)


def has_min_length(value: str, length: int) -> bool:
    """Return ``True`` when ``len(value) >= length``."""
    return len(value) >= length


def strip_all(values: list[str]) -> list[str]:
    """Strip whitespace from every element and drop empties."""
    return [v.strip() for v in values if v and v.strip()]


def join_non_empty(parts: list[str | None], separator: str = ",") -> str:
    """Join only the non-empty parts with ``separator``."""
    return separator.join(p for p in parts if p and p.strip())


def dedupe_keywords(value: str, *keywords: str) -> bool:
    """Return ``True`` when any keyword appears in ``value`` (word boundary)."""
    for keyword in keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", value, flags=re.IGNORECASE):
            return True
    return False


__all__ = [
    "snake_case",
    "kebab_case",
    "camel_case",
    "pascal_case",
    "title_case",
    "truncate",
    "first_non_empty",
    "normalize_whitespace",
    "is_blank",
    "has_text",
    "slugify",
    "random_string",
    "mask",
    "mask_email",
    "mask_token",
    "ellipsize_middle",
    "remove_prefix",
    "remove_suffix",
    "ascii_only",
    "has_uppercase",
    "has_lowercase",
    "has_digit",
    "has_symbol",
    "has_min_length",
    "strip_all",
    "join_non_empty",
    "dedupe_keywords",
]
