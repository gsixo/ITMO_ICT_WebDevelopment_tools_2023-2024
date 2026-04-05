import asyncio
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup

from benchmark import append_result, measure_seconds
from common import URLS, split_evenly
from db import init_db_async, save_parsed_page_async

APPROACH = "async"
WORKERS = 4


async def parse_and_save(url: str, session: aiohttp.ClientSession) -> None:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
        response.raise_for_status()
        html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else "NO_TITLE"
    await save_parsed_page_async(url=url, title=title[:1024], approach=APPROACH)
    print(f"[{APPROACH}] {url} -> {title}")


async def worker(url_chunk: list[str], session: aiohttp.ClientSession) -> None:
    for url in url_chunk:
        try:
            await parse_and_save(url, session)
        except Exception as error:
            print(f"[{APPROACH}] error for {url}: {error}")


async def run_async() -> None:
    await init_db_async()
    chunks = split_evenly(URLS, WORKERS)
    async with aiohttp.ClientSession() as session:
        tasks = [worker(chunk, session) for chunk in chunks]
        await asyncio.gather(*tasks)


def run() -> None:
    asyncio.run(run_async())


if __name__ == "__main__":
    _, elapsed = measure_seconds(run)
    print(f"[{APPROACH}] parsed={len(URLS)}, elapsed={elapsed:.6f}s")
    append_result(
        Path("task2_times.csv"),
        APPROACH,
        elapsed,
        f"workers={WORKERS}, urls={len(URLS)}",
    )
