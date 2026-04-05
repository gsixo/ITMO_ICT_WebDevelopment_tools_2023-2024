import httpx
from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from pydantic import BaseModel, Field, model_validator

from app.celery_app import celery_app
from app.config import settings
from app.tasks.parser_tasks import parse_urls_task

router = APIRouter()


class ParserProxyRequest(BaseModel):
    url: str | None = None
    urls: list[str] | None = None
    workers: int = Field(default=4, ge=1, le=32)

    @model_validator(mode="after")
    def validate_input(self) -> "ParserProxyRequest":
        if not self.url and not self.urls:
            raise ValueError("Provide either 'url' or 'urls'.")
        if self.url and self.urls:
            raise ValueError("Use either 'url' or 'urls', not both.")
        return self


class ParserAsyncRequest(BaseModel):
    url: str | None = None
    urls: list[str] | None = None

    @model_validator(mode="after")
    def validate_input(self) -> "ParserAsyncRequest":
        if not self.url and not self.urls:
            raise ValueError("Provide either 'url' or 'urls'.")
        if self.url and self.urls:
            raise ValueError("Use either 'url' or 'urls', not both.")
        return self


def _normalize_urls(payload: ParserProxyRequest) -> list[str]:
    urls = [payload.url] if payload.url else list(payload.urls or [])
    return [url.strip() for url in urls if isinstance(url, str) and url.strip()]


def _normalize_urls_async(payload: ParserAsyncRequest) -> list[str]:
    urls = [payload.url] if payload.url else list(payload.urls or [])
    return [url.strip() for url in urls if isinstance(url, str) and url.strip()]


@router.post("/parse")
async def parse_with_parser_service(payload: ParserProxyRequest) -> dict:
    parser_url = f"{settings.parser_service_url.rstrip('/')}/parse"
    try:
        async with httpx.AsyncClient(timeout=settings.parser_service_timeout_seconds) as client:
            response = await client.post(parser_url, json=payload.model_dump(exclude_none=True))
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Cannot reach parser service: {error}",
        ) from error

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Parser service error: {response.text}",
        )

    return response.json()


@router.post("/parse-async")
async def parse_async(payload: ParserAsyncRequest) -> dict:
    urls = _normalize_urls_async(payload)
    if not urls:
        raise HTTPException(status_code=422, detail="At least one non-empty URL is required.")

    try:
        task = parse_urls_task.delay(urls=urls)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Cannot queue parsing task. Check Redis and Celery worker: "
                f"{error}"
            ),
        ) from error

    return {
        "message": "Parsing task queued",
        "task_id": task.id,
        "status": "QUEUED",
        "total_urls": len(urls),
    }


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    state = result.state

    if state == "PENDING":
        return {"task_id": task_id, "status": state}
    if state == "STARTED":
        return {"task_id": task_id, "status": state}
    if state == "FAILURE":
        return {"task_id": task_id, "status": state, "error": str(result.result)}
    if state == "SUCCESS":
        payload = result.result if isinstance(result.result, dict) else {"result": result.result}
        return {"task_id": task_id, "status": state, **payload}

    return {"task_id": task_id, "status": state, "result": str(result.result)}
