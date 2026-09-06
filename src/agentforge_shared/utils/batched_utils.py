"""Batching and chunking utilities for large workloads."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

from agentforge_shared.constants.limits import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_CHUNK_SIZE,
    MAX_BATCH_SIZE,
)
from agentforge_shared.utils.collection_utils import batched as iter_batched, chunked, chunked_iter

_T = TypeVar("_T")
_R = TypeVar("_R")

DEFAULT_CHUNK_OVERLAP = 50


def batched_size(n: int) -> int:
    """Clamp a requested batch size to the platform limits."""
    return max(1, min(n, MAX_BATCH_SIZE)) if n else DEFAULT_BATCH_SIZE


def process_in_batches(
    items: list[_T],
    *,
    size: int = DEFAULT_BATCH_SIZE,
    fn: Callable[[list[_T]], _R],
    results: list[_R] | None = None,
) -> list[_R]:
    """Apply ``fn`` to each batch sequentially and collect the outputs.

    Args:
        items: The full list to process.
        size: Item count per batch (clamped to ``MAX_BATCH_SIZE``).
        fn: Callable applied to each batch slice.
        results: Optional accumulator list to extend.

    Returns:
        The collected results in batch order.
    """
    accumulator = results if results is not None else []
    actual = batched_size(size)
    for batch in chunked(items, actual):
        accumulator.append(fn(batch))
    return accumulator


def map_batches(
    items: list[_T],
    *,
    size: int = DEFAULT_BATCH_SIZE,
    fn: Callable[[_T], _R],
) -> list[_R]:
    """Map ``fn`` over every item but flush to ``size`` chunks for logging.

    Behaves like ``list(map(fn, items))`` while grouping progress.
    """
    outputs: list[_R] = []
    for batch in chunked(items, batched_size(size)):
        for item in batch:
            outputs.append(fn(item))
    return outputs


async def amap_batches(
    items: list[_T],
    *,
    size: int = DEFAULT_BATCH_SIZE,
    concurrency: int = 16,
    fn: Callable[[list[_T]], Any],
) -> list[Any]:
    """Run ``fn`` over each batch concurrently with a semaphore limit."""
    actual = batched_size(size)
    sem = asyncio.Semaphore(concurrency)

    async def _run(batch: list[_T]) -> Any:
        async with sem:
            return fn(batch)

    return await asyncio.gather(*(_run(batch) for batch in chunked(items, actual)))


def chunk_text(
    text: str,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """Split ``text`` into overlapping character chunks.

    Args:
        text: The text to chunk.
        chunk_size: Maximum characters per chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        A list of non-empty text chunks.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be in [0, chunk_size)")
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    result: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        result.append(text[start:end])
        if end == len(text):
            break
        start = max(start + chunk_size - overlap, start + 1)
    return result


def chunk_sentences(
    text: str,
    *,
    max_chars: int = 800,
) -> list[str]:
    """Split text on sentence boundaries, grouping until ``max_chars``."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for sentence in sentences:
        if not sentence:
            continue
        if current_len + len(sentence) > max_chars and current:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
        current.append(sentence)
        current_len += len(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def chunk_words(
    words: Iterable[str],
    *,
    size: int = DEFAULT_CHUNK_SIZE,
) -> Iterator[list[str]]:
    """Yield word-list chunks of at most ``size`` words from an iterable."""
    return iter_batched(words, size)


def chunk_bytes(data: bytes, *, size: int = 1024 * 1024) -> Iterator[bytes]:
    """Yield ``data`` as byte chunks of at most ``size`` bytes."""
    if size < 1:
        raise ValueError("size must be >= 1")
    for i in range(0, len(data), size):
        yield data[i : i + size]


async def aprocess_in_batches(
    items: list[_T],
    *,
    size: int = DEFAULT_BATCH_SIZE,
    fn: Callable[[list[_T]], Any],
    concurrency: int = 1,
) -> list[Any]:
    """Process batches with a concurrency cap (helper wrapping ``amap_batches``)."""
    batch_size = batched_size(size)
    results: list[Any] = []
    for i in range(0, len(items), batch_size * concurrency):
        slice_items = items[i : i + batch_size * concurrency]
        batches = chunked(slice_items, batch_size)
        results.extend(await asyncio.gather(*(fn(b) for b in batches)))
    return results


def estimate_chunk_count(total_items: int, *, per_batch: int) -> int:
    """Return the number of batches required to cover ``total_items``."""
    if per_batch < 1:
        raise ValueError("per_batch must be >= 1")
    return (total_items + per_batch - 1) // per_batch


# Re-export the low-level helpers so callers can import them here too.
__all__ = [
    "DEFAULT_CHUNK_OVERLAP",
    "batched_size",
    "process_in_batches",
    "map_batches",
    "amap_batches",
    "aprocess_in_batches",
    "chunk_text",
    "chunk_sentences",
    "chunk_words",
    "chunk_bytes",
    "estimate_chunk_count",
    "chunked",
    "chunked_iter",
    "iter_batched",
]
