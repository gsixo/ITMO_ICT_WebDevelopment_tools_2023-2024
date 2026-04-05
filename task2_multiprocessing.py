from multiprocessing import Process
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from benchmark import append_result, measure_seconds
from common import URLS, split_evenly
from db import init_db_sync, save_parsed_page_sync

APPROACH = "multiprocessing"
WORKERS = 4


def parse_and_save(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else "NO_TITLE"
    save_parsed_page_sync(url=url, title=title[:1024], approach=APPROACH)
    print(f"[{APPROACH}] {url} -> {title}")


def worker(url_chunk: list[str]) -> None:
    for url in url_chunk:
        try:
            parse_and_save(url)
        except Exception as error:
            print(f"[{APPROACH}] error for {url}: {error}")


def run() -> None:
    init_db_sync()
    chunks = split_evenly(URLS, WORKERS)
    processes: list[Process] = []

    for chunk in chunks:
        process = Process(target=worker, args=(chunk,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == "__main__":
    _, elapsed = measure_seconds(run)
    print(f"[{APPROACH}] parsed={len(URLS)}, elapsed={elapsed:.6f}s")
    append_result(
        Path("task2_times.csv"),
        APPROACH,
        elapsed,
        f"workers={WORKERS}, urls={len(URLS)}",
    )
