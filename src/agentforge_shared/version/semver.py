"""SemVer parsing and comparison helpers."""

from __future__ import annotations

import re

from agentforge_shared.exceptions.base import ConfigurationException

_SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


class SemVer:
    """Semantic Version 2.0.0 value object.

    Example::

        v = SemVer.parse("1.4.2-beta.1+build7")
        assert v.major == 1 and v.prerelease == "beta.1"
        assert SemVer.parse("2.0.0") > v
    """

    __slots__ = ("major", "minor", "patch", "prerelease", "build")

    def __init__(
        self,
        major: int,
        minor: int = 0,
        patch: int = 0,
        prerelease: str | None = None,
        build: str | None = None,
    ) -> None:
        if major < 0 or minor < 0 or patch < 0:
            raise ValueError("version numbers must be non-negative")
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
        self.prerelease = prerelease
        self.build = build

    @classmethod
    def parse(cls, version: str) -> SemVer:
        """Parse a SemVer string, raising ``ValueError`` when invalid."""
        match = _SEMVER_RE.match((version or "").strip())
        if match is None:
            raise ValueError(f"invalid semantic version: {version!r}")
        return cls(
            major=int(match.group("major")),
            minor=int(match.group("minor")),
            patch=int(match.group("patch")),
            prerelease=match.group("prerelease"),
            build=match.group("build"),
        )

    def __str__(self) -> str:
        out = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            out += f"-{self.prerelease}"
        if self.build:
            out += f"+{self.build}"
        return out

    def __repr__(self) -> str:
        return f"SemVer({str(self)!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (
            (self.major, self.minor, self.patch, self._prerelease_key()) ==
            (other.major, other.minor, other.patch, other._prerelease_key())
        )

    def __lt__(self, other: SemVer) -> bool:
        left = (self.major, self.minor, self.patch, self._prerelease_key())
        right = (other.major, other.minor, other.patch, other._prerelease_key())
        return left < right

    def __le__(self, other: SemVer) -> bool:
        return self == other or self < other

    def __gt__(self, other: SemVer) -> bool:
        return not self <= other

    def __ge__(self, other: SemVer) -> bool:
        return not self < other

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch, self._prerelease_key()))

    def _prerelease_key(self) -> tuple[int, tuple] | tuple[int | str, ...]:
        """Precedence key per SemVer spec: releases > prereleases."""
        if self.prerelease is None:
            return (1,)
        identifiers = self.prerelease.split(".")
        key: list[object] = []
        for identifier in identifiers:
            if identifier.isdigit():
                key.append(0)
                key.append(int(identifier))
            else:
                key.append(1)
                key.append(identifier)
        return (0, tuple(key))

    def bump(self, level: str) -> SemVer:
        """Return a new version bumped at ``major``/``minor``/``patch``."""
        if level == "major":
            return SemVer(self.major + 1, 0, 0)
        if level == "minor":
            return SemVer(self.major, self.minor + 1, 0)
        if level == "patch":
            return SemVer(self.major, self.minor, self.patch + 1)
        raise ValueError(f"bump level must be major|minor|patch, got {level!r}")


def parse_version(version: str) -> SemVer:
    """Parse a version string, raising ``ConfigurationException`` on error."""
    try:
        return SemVer.parse(version)
    except ValueError as exc:
        raise ConfigurationException(message=str(exc)) from exc


def is_supported(version: SemVer | str, *, min_version: str | None = None, max_version: str | None = None) -> bool:
    """Check ``version`` against optional inclusive bounds."""
    current = SemVer.parse(str(version)) if isinstance(version, str) else version
    if min_version is not None and current < SemVer.parse(min_version):
        return False
    if max_version is not None and current > SemVer.parse(max_version):
        return False
    return True


def compatible_version(version: SemVer | str, *, major: int | None = None, minor: int | None = None) -> bool:
    """Return whether ``version`` shares the given ``major``/``minor``."""
    current = SemVer.parse(str(version)) if isinstance(version, str) else version
    if major is not None and current.major != major:
        return False
    if minor is not None and current.minor != minor:
        return False
    return True


def deprecated_version(version: SemVer | str, *, min_supported: str) -> bool:
    """Whether ``version`` is below ``min_supported`` (deprecated)."""
    current = SemVer.parse(str(version)) if isinstance(version, str) else version
    return current < SemVer.parse(min_supported)


__all__ = [
    "SemVer",
    "parse_version",
    "is_supported",
    "compatible_version",
    "deprecated_version",
]
