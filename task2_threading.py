import threading
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from benchmark import append_result, measure_seconds
from common import URLS, split_evenly
from db import init_db_sync, save_parsed_page_sync

APPROACH = "threading"
WORKERS = 4


def parse_and_save(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else "NO_TITLE"
    save_parsed_page_sync(url=url, title=title[:1024], approach=APPROACH)
    print(f"[{APPROACH}] {url} -> {title}")


def run() -> None:
    init_db_sync()
    chunks = split_evenly(URLS, WORKERS)

    def worker(url_chunk: list[str]) -> None:
        for url in url_chunk:
            try:
                parse_and_save(url)
            except Exception as error:
                print(f"[{APPROACH}] error for {url}: {error}")

    threads: list[threading.Thread] = []
    for chunk in chunks:
        thread = threading.Thread(target=worker, args=(chunk,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    _, elapsed = measure_seconds(run)
    print(f"[{APPROACH}] parsed={len(URLS)}, elapsed={elapsed:.6f}s")
    append_result(
        Path("task2_times.csv"),
        APPROACH,
        elapsed,
        f"workers={WORKERS}, urls={len(URLS)}",
    )
