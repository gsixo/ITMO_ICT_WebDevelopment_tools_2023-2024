from typing import Any

from app.celery_app import celery_app
from parser_service.core import parse_urls_sequential


@celery_app.task(name="app.tasks.parse_urls", bind=True)
def parse_urls_task(self, urls: list[str]) -> dict[str, Any]:
    sanitized_urls = [url.strip() for url in urls if isinstance(url, str) and url.strip()]
    if not sanitized_urls:
        return {
            "task_id": self.request.id,
            "status": "SUCCESS",
            "approach": "multiprocessing",
            "total": 0,
            "saved": 0,
            "results": [],
        }

    # Celery worker processes are daemonic, so avoid nested multiprocessing here.
    results = parse_urls_sequential(sanitized_urls)
    saved_count = sum(1 for item in results if item.get("saved"))
    error_count = sum(1 for item in results if item.get("error"))

    return {
        "task_id": self.request.id,
        "status": "SUCCESS",
        "approach": "multiprocessing",
        "total": len(results),
        "saved": saved_count,
        "errors": error_count,
        "results": results,
    }
