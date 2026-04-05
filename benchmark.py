import csv
from pathlib import Path
from time import perf_counter
from typing import Callable, TypeVar

T = TypeVar("T")


RESULTS_DIR = Path("results")


def measure_seconds(func: Callable[[], T]) -> tuple[T, float]:
    start = perf_counter()
    result = func()
    elapsed = perf_counter() - start
    return result, elapsed


def append_result(csv_path: Path, approach: str, elapsed_seconds: float, details: str) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    absolute_path = RESULTS_DIR / csv_path
    file_exists = absolute_path.exists()

    with absolute_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["approach", "elapsed_seconds", "details"])
        writer.writerow([approach, f"{elapsed_seconds:.6f}", details])
