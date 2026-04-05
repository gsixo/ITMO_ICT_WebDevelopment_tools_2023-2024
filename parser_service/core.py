from multiprocessing import Pool
from typing import Any

import requests
from bs4 import BeautifulSoup

from lab2.db import init_db_sync, save_parsed_page_sync

APPROACH = "multiprocessing"
DEFAULT_WORKERS = 4
REQUEST_TIMEOUT_SECONDS = 10


def _parse_url(url: str) -> dict[str, Any]:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = (soup.title.string or "").strip() if soup.title else "NO_TITLE"
        return {
            "url": url,
            "title": title,
            "saved": False,
            "error": None,
        }
    except Exception as error:  # noqa: BLE001 - return structured error for API response
        return {
            "url": url,
            "title": None,
            "saved": False,
            "error": str(error),
        }


def parse_urls_multiprocessing(urls: list[str], workers: int = DEFAULT_WORKERS) -> list[dict[str, Any]]:
    init_db_sync()
    if not urls:
        return []

    worker_count = max(1, min(workers, len(urls)))
    with Pool(processes=worker_count) as pool:
        parsed_results = pool.map(_parse_url, urls)

    # Save in parent process only: avoids DB connection issues in child processes.
    for result in parsed_results:
        if result["error"] is not None:
            continue
        try:
            save_parsed_page_sync(
                url=result["url"],
                title=(result["title"] or "NO_TITLE")[:1024],
                approach=APPROACH,
            )
            result["saved"] = True
        except Exception as error:  # noqa: BLE001 - preserve parsing result with DB error
            result["saved"] = False
            result["error"] = str(error)

    return parsed_results


def parse_urls_sequential(urls: list[str]) -> list[dict[str, Any]]:
    init_db_sync()
    parsed_results: list[dict[str, Any]] = []
    for url in urls:
        result = _parse_url(url)
        if result["error"] is None:
            try:
                save_parsed_page_sync(
                    url=result["url"],
                    title=(result["title"] or "NO_TITLE")[:1024],
                    approach=APPROACH,
                )
                result["saved"] = True
            except Exception as error:  # noqa: BLE001 - preserve parsing result with DB error
                result["saved"] = False
                result["error"] = str(error)
        parsed_results.append(result)
    return parsed_results
