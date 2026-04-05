from multiprocessing import Pool
from pathlib import Path

from benchmark import append_result, measure_seconds
from common import split_into_ranges

START = 1
END = 1_000_000
WORKERS = 4
EXPECTED_SUM = END * (END + 1) // 2


def calculate_sum(sub_range: tuple[int, int]) -> int:
    start, end = sub_range
    return sum(range(start, end + 1))


def run() -> int:
    ranges = split_into_ranges(START, END, WORKERS)
    with Pool(processes=WORKERS) as pool:
        partial_sums = pool.map(calculate_sum, ranges)
    return sum(partial_sums)


if __name__ == "__main__":
    total, elapsed = measure_seconds(run)
    print(f"[multiprocessing] sum={total}, expected={EXPECTED_SUM}, elapsed={elapsed:.6f}s")
    append_result(
        Path("task1_times.csv"),
        "multiprocessing",
        elapsed,
        f"workers={WORKERS}, total={total}",
    )
