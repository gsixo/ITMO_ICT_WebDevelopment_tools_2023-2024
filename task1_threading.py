import threading
from pathlib import Path

from benchmark import append_result, measure_seconds
from common import split_into_ranges

START = 1
END = 1_000_000
WORKERS = 4
EXPECTED_SUM = END * (END + 1) // 2


def calculate_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


def run() -> int:
    ranges = split_into_ranges(START, END, WORKERS)
    results = [0] * len(ranges)

    def worker(index: int, sub_range: tuple[int, int]) -> None:
        range_start, range_end = sub_range
        results[index] = calculate_sum(range_start, range_end)

    threads: list[threading.Thread] = []
    for index, sub_range in enumerate(ranges):
        thread = threading.Thread(target=worker, args=(index, sub_range))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return sum(results)


if __name__ == "__main__":
    total, elapsed = measure_seconds(run)
    print(f"[threading] sum={total}, expected={EXPECTED_SUM}, elapsed={elapsed:.6f}s")
    append_result(Path("task1_times.csv"), "threading", elapsed, f"workers={WORKERS}, total={total}")
