"""Filesystem utilities used by ingestion, storage, and deployment tooling."""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterable
from pathlib import Path

from agentforge_shared.constants.mime_types import mime_from_filename


def ensure_directory(path: str | Path) -> Path:
    """Create ``path`` (and parents) and return it as a ``Path``."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_filename(filename: str, *, fallback: str = "file") -> str:
    """Sanitize a filename to safe path segments (no separators/control chars)."""
    import re

    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", filename).strip("._")
    return cleaned or fallback


def read_text(path: str | Path, *, encoding: str = "utf-8") -> str:
    """Read a small text file, raising ``FileNotFoundError`` when missing."""
    return Path(path).read_text(encoding=encoding)


def write_text(path: str | Path, content: str, *, encoding: str = "utf-8") -> Path:
    """Write ``content`` atomically to ``path`` (parent dirs created)."""
    p = Path(path)
    ensure_directory(p.parent)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(content, encoding=encoding)
    tmp.replace(p)
    return p


def read_bytes(path: str | Path) -> bytes:
    """Read binary file contents."""
    return Path(path).read_bytes()


def write_bytes(path: str | Path, content: bytes) -> Path:
    """Write binary ``content`` atomically to ``path``."""
    p = Path(path)
    ensure_directory(p.parent)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_bytes(content)
    tmp.replace(p)
    return p


def list_files(directory: str | Path, pattern: str = "*") -> list[Path]:
    """Return all files under ``directory`` matching ``pattern`` (sorted)."""
    return sorted(Path(directory).glob(pattern))


def list_files_recursive(directory: str | Path, pattern: str = "**/*") -> list[Path]:
    """Return all files (no dirs) recursively, sorted."""
    return sorted(p for p in Path(directory).glob(pattern) if p.is_file())


def file_size(path: str | Path) -> int:
    """Return the byte size of ``path``."""
    return Path(path).stat().st_size


def human_size(num_bytes: float, *, binary: bool = False) -> str:
    """Format a byte count as a human-readable string.

    Args:
        num_bytes: Byte count.
        binary: Use 1024-based units (KiB/MiB) vs 1000-based (KB/MB).
    """
    base = 1024.0 if binary else 1000.0
    units = ["B", "KiB", "MiB", "GiB", "TiB"] if binary else ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        if value < base or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= base
    return f"{num_bytes} B"


def get_extension(filename: str) -> str:
    """Return the lowercase extension without the dot (``"pdf"``)."""
    dot = filename.rfind(".")
    if dot == -1 or dot == len(filename) - 1:
        return ""
    return filename[dot + 1 :].lower()


def detect_mime_type(filename: str) -> str:
    """Return the MIME type for ``filename`` (default octet-stream)."""
    return mime_from_filename(filename)


def is_binary(path: str | Path, *, sample_size: int = 1024) -> bool:
    """Heuristically detect whether a file is probably binary."""
    with open(path, "rb") as handle:
        chunk = handle.read(sample_size)
        if b"\x00" in chunk:
            return True
        if not chunk:
            return False
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x7F)) | {0x80})
        return bool(chunk.translate(None, text_chars))


def atomic_write(path: str | Path, content: str | bytes, *, encoding: str = "utf-8") -> Path:
    """Atomically write text or bytes to ``path``."""
    if isinstance(content, bytes):
        return write_bytes(path, content)
    return write_text(path, content, encoding=encoding)


def temp_file(prefix: str = "agentforge-", suffix: str = ".tmp") -> Path:
    """Create a temporary file and return its path (caller must remove)."""
    f = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False)
    f.close()
    return Path(f.name)


def remove_file(path: str | Path) -> bool:
    """Remove ``path`` if it exists; return ``True`` when removed."""
    try:
        Path(path).unlink()
        return True
    except FileNotFoundError:
        return False


def remove_tree(path: str | Path) -> bool:
    """Recursively remove ``path``; return ``True`` when removed."""
    try:
        shutil.rmtree(Path(path))
        return True
    except FileNotFoundError:
        return False


def copy_tree(source: str | Path, destination: str | Path) -> None:
    """Copy ``source`` into ``destination`` recursively."""
    shutil.copytree(Path(source), Path(destination), dirs_exist_ok=True)


def disk_usage(path: str | Path) -> int:
    """Return available disk bytes on the filesystem holding ``path``."""
    usage = shutil.disk_usage(Path(path).resolve())
    return usage.free


def filter_existing(paths: Iterable[str | Path]) -> list[Path]:
    """Return only the paths that exist on disk."""
    return [p for p in (Path(x) for x in paths) if p.exists()]


def is_within_directory(child: str | Path, parent: str | Path) -> bool:
    """Return ``True`` when ``child`` resolves inside ``parent`` (path-traversal guard)."""
    child_resolved = Path(child).resolve()
    parent_resolved = Path(parent).resolve()
    try:
        child_resolved.relative_to(parent_resolved)
        return True
    except ValueError:
        return False


__all__ = [
    "ensure_directory",
    "safe_filename",
    "read_text",
    "write_text",
    "read_bytes",
    "write_bytes",
    "atomic_write",
    "list_files",
    "list_files_recursive",
    "file_size",
    "human_size",
    "get_extension",
    "detect_mime_type",
    "is_binary",
    "temp_file",
    "remove_file",
    "remove_tree",
    "copy_tree",
    "disk_usage",
    "filter_existing",
    "is_within_directory",
]
