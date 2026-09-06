"""Common MIME type constants (RFC 6838-friendly)."""

from __future__ import annotations

from typing import Final

MIME_JSON: Final[str] = "application/json"
MIME_JSON_LINES: Final[str] = "application/jsonl"
MIME_XML: Final[str] = "application/xml"
MIME_YAML: Final[str] = "application/yaml"
MIME_TEXT: Final[str] = "text/plain"
MIME_HTML: Final[str] = "text/html"
MIME_CSV: Final[str] = "text/csv"
MIME_SSE: Final[str] = "text/event-stream"
MIME_MARKDOWN: Final[str] = "text/markdown"
MIME_PDF: Final[str] = "application/pdf"
MIME_OCTET: Final[str] = "application/octet-stream"
MIME_FORM_URLENCODED: Final[str] = "application/x-www-form-urlencoded"
MIME_MULTIPART: Final[str] = "multipart/form-data"

MIME_PNG: Final[str] = "image/png"
MIME_JPEG: Final[str] = "image/jpeg"
MIME_GIF: Final[str] = "image/gif"
MIME_WEBP: Final[str] = "image/webp"
MIME_SVG: Final[str] = "image/svg+xml"
MIME_TIFF: Final[str] = "image/tiff"
MIME_ICO: Final[str] = "image/x-icon"
MIME_BMP: Final[str] = "image/bmp"
MIME_HEIC: Final[str] = "image/heic"

MIME_MP4: Final[str] = "video/mp4"
MIME_WEBM: Final[str] = "video/webm"
MIME_OGG: Final[str] = "video/ogg"
MIME_AVI: Final[str] = "video/x-msvideo"
MIME_MOV: Final[str] = "video/quicktime"
MIME_MPEG: Final[str] = "video/mpeg"

MIME_MP3: Final[str] = "audio/mpeg"
MIME_WAV: Final[str] = "audio/wav"
MIME_OGG_AUDIO: Final[str] = "audio/ogg"
MIME_FLAC: Final[str] = "audio/flac"
MIME_AAC: Final[str] = "audio/aac"
MIME_OPUS: Final[str] = "audio/opus"
MIME_M4A: Final[str] = "audio/mp4"

MIME_ZIP: Final[str] = "application/zip"
MIME_TAR: Final[str] = "application/x-tar"
MIME_GZIP: Final[str] = "application/gzip"
MIME_7Z: Final[str] = "application/x-7z-compressed"
MIME_RAR: Final[str] = "application/vnd.rar"

# Document formats
MIME_DOC: Final[str] = "application/msword"
MIME_DOCX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
MIME_XLS: Final[str] = "application/vnd.ms-excel"
MIME_XLSX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
MIME_PPT: Final[str] = "application/vnd.ms-powerpoint"
MIME_PPTX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)
MIME_ODT: Final[str] = "application/vnd.oasis.opendocument.text"

# Code files used by document ingestion
MIME_PY: Final[str] = "text/x-python"
MIME_JS: Final[str] = "application/javascript"
MIME_TS: Final[str] = "text/typescript"
MIME_GO: Final[str] = "text/x-go"
MIME_RUST: Final[str] = "text/x-rust"
MIME_JSONL_CODE: Final[str] = "application/jsonl"

# Static assets
MIME_WASM: Final[str] = "application/wasm"
MIME_FONT_WOFF2: Final[str] = "font/woff2"
MIME_FONT_TTF: Final[str] = "font/ttf"

# Extension → MIME lookup (lowercase, no leading dot).
EXTENSION_TO_MIME: Final[dict[str, str]] = {
    "json": MIME_JSON,
    "jsonl": MIME_JSON_LINES,
    "xml": MIME_XML,
    "yaml": MIME_YAML,
    "yml": MIME_YAML,
    "txt": MIME_TEXT,
    "md": MIME_MARKDOWN,
    "markdown": MIME_MARKDOWN,
    "html": MIME_HTML,
    "htm": MIME_HTML,
    "csv": MIME_CSV,
    "pdf": MIME_PDF,
    "png": MIME_PNG,
    "jpg": MIME_JPEG,
    "jpeg": MIME_JPEG,
    "gif": MIME_GIF,
    "webp": MIME_WEBP,
    "svg": MIME_SVG,
    "tiff": MIME_TIFF,
    "ico": MIME_ICO,
    "bmp": MIME_BMP,
    "heic": MIME_HEIC,
    "mp4": MIME_MP4,
    "webm": MIME_WEBM,
    "mov": MIME_MOV,
    "mp3": MIME_MP3,
    "wav": MIME_WAV,
    "flac": MIME_FLAC,
    "zip": MIME_ZIP,
    "tar": MIME_TAR,
    "gz": MIME_GZIP,
    "doc": MIME_DOC,
    "docx": MIME_DOCX,
    "xls": MIME_XLS,
    "xlsx": MIME_XLSX,
    "ppt": MIME_PPT,
    "pptx": MIME_PPTX,
    "odt": MIME_ODT,
    "py": MIME_PY,
    "js": MIME_JS,
    "mjs": MIME_JS,
    "ts": MIME_TS,
    "tsx": MIME_TS,
    "go": MIME_GO,
    "rs": MIME_RUST,
}

MIME_TO_EXTENSION: Final[dict[str, str]] = {v: k for k, v in EXTENSION_TO_MIME.items()}


def mime_from_filename(filename: str) -> str:
    """Return the MIME type for ``filename`` based on its extension.

    Falls back to ``application/octet-stream`` for unknown extensions.
    """
    dot = filename.rfind(".")
    if dot == -1 or dot == len(filename) - 1:
        return MIME_OCTET
    ext = filename[dot + 1 :].lower()
    return EXTENSION_TO_MIME.get(ext, MIME_OCTET)
