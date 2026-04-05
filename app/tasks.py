import httpx

from app.celery_app import celery_app
from app.config import settings


@celery_app.task(bind=True)
def parse_url_task(self, url: str) -> dict:
    with httpx.Client(timeout=settings.parser_service_timeout_seconds) as client:
        response = client.post(
            f"{settings.parser_service_url}/parse",
            params={"url": url},
        )
        response.raise_for_status()
        return response.json()
