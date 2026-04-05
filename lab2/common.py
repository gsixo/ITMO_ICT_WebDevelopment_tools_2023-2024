from typing import Iterable, List, Sequence, Tuple


URLS: list[str] = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://httpbin.org/html",
    "https://www.wikipedia.org",
    "https://pypi.org",
    "https://github.com",
    "https://fastapi.tiangolo.com",
]


def split_into_ranges(start: int, end: int, parts: int) -> list[tuple[int, int]]:
    if parts <= 0:
        raise ValueError("parts must be positive")

    total = end - start + 1
    base = total // parts
    remainder = total % parts

    ranges: list[tuple[int, int]] = []
    current = start
    for index in range(parts):
        extra = 1 if index < remainder else 0
        chunk_size = base + extra
        chunk_end = current + chunk_size - 1
        ranges.append((current, chunk_end))
        current = chunk_end + 1
    return ranges


def split_evenly(items: Sequence[str], parts: int) -> list[list[str]]:
    if parts <= 0:
        raise ValueError("parts must be positive")

    base = len(items) // parts
    remainder = len(items) % parts
    result: list[list[str]] = []
    start = 0
    for index in range(parts):
        extra = 1 if index < remainder else 0
        stop = start + base + extra
        result.append(list(items[start:stop]))
        start = stop
    return [chunk for chunk in result if chunk]
