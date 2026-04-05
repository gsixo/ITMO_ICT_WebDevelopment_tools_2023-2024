import asyncio
from pathlib import Path

from benchmark import append_result, measure_seconds
from common import split_into_ranges

START = 1
END = 1_000_000
WORKERS = 4
EXPECTED_SUM = END * (END + 1) // 2


def calculate_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


async def calculate_sum_async(start: int, end: int) -> int:
    await asyncio.sleep(0)  # enqueue
    return calculate_sum(start, end)


async def run_async() -> int:
    ranges = split_into_ranges(START, END, WORKERS)
    tasks = [
        calculate_sum_async(range_start, range_end) for range_start, range_end in ranges
    ]
    partial_sums = await asyncio.gather(*tasks)
    return sum(partial_sums)


def run() -> int:
    return asyncio.run(run_async())


if __name__ == "__main__":
    total, elapsed = measure_seconds(run)
    print(f"[async] sum={total}, expected={EXPECTED_SUM}, elapsed={elapsed:.6f}s")
    append_result(
        Path("task1_times.csv"), "async", elapsed, f"workers={WORKERS}, total={total}"
    )
