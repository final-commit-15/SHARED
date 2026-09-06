"""Version bumping utility for AgentForge release automation.

Bumps the version in ``pyproject.toml`` (and ``src/agentforge_shared/__init__.py``
when present) using SemVer logic.

Usage::

    python -m agentforge_shared.scripts.bump_version patch
    python -m agentforge_shared.scripts.bump_version minor --path pyproject.toml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from agentforge_shared.version.semver import SemVer

_VERSION_TAG = re.compile(r"^[ \t]*__version__\s*=\s*[\"'](?P<version>[^\"']+)[\"']", re.MULTILINE)


def read_version(pyproject_path: Path) -> str | None:
    """Extract the ``version`` string from ``[project]/[tool.poetry]``."""
    text = pyproject_path.read_text(encoding="utf-8")
    for section in re.findall(r"^\[(project|tool\.poetry)\]", text, flags=re.MULTILINE):
        pass
    match = re.search(r"^version\s*=\s*[\"'](?P<version>[^\"']+)[\"']", text, flags=re.MULTILINE)
    return match.group("version") if match else None


def write_version(pyproject_path: Path, new_version: str, current: str) -> None:
    """Replace the version assignment in ``pyproject.toml``."""
    text = pyproject_path.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf"^(version\s*=\s*)[\"']{re.escape(current)}[\"']",
        lambda m: f"{m.group(1)}{new_version!r}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count == 0:
        raise RuntimeError(f"could not locate current version {current!r} in {pyproject_path}")
    pyproject_path.write_text(updated, encoding="utf-8")


def bump_init_version(init_path: Path, new_version: str) -> None:
    """Update ``__version__`` in the package ``__init__.py``."""
    if not init_path.exists():
        return
    text = init_path.read_text(encoding="utf-8")
    updated = _VERSION_TAG.sub(lambda m: f'__version__ = "{new_version}"', text, count=1)
    init_path.write_text(updated, encoding="utf-8")


def bump_version(level: str, *, pyproject_path: Path | None = None, package_dir: Path | None = None) -> str:
    """Bump the current version and return the new version string."""
    root = package_dir or Path(__file__).resolve().parents[2]
    project_file = pyproject_path or root / "pyproject.toml"
    if not project_file.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {project_file}")
    current = read_version(project_file)
    if current is None:
        raise RuntimeError(f"no version found in {project_file}")
    new_version = str(SemVer.parse(current).bump(level))
    write_version(project_file, new_version, current)
    bump_init_version(root / "src" / "agentforge_shared" / "__init__.py", new_version)
    return new_version


def main(argv: list[str] | None = None) -> int:
    """CLI entry point (installed as ``agentforge-bump-version``)."""
    parser = argparse.ArgumentParser(prog="agentforge-bump-version", description=__doc__)
    parser.add_argument("level", choices=("major", "minor", "patch"), help="Version segment to bump.")
    parser.add_argument("--path", default=None, help="Explicit pyproject.toml path.")
    args = parser.parse_args(argv)
    try:
        new_version = bump_version(args.level, pyproject_path=Path(args.path) if args.path else None)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"bumped to {new_version}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
