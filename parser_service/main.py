from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

from parser_service.core import DEFAULT_WORKERS, parse_urls_multiprocessing

app = FastAPI(title="Parser Service")


class ParseRequest(BaseModel):
    url: str | None = None
    urls: list[str] | None = None
    workers: int = Field(default=DEFAULT_WORKERS, ge=1, le=32)

    @model_validator(mode="after")
    def validate_input(self) -> "ParseRequest":
        if not self.url and not self.urls:
            raise ValueError("Provide either 'url' or 'urls'.")
        if self.url and self.urls:
            raise ValueError("Use either 'url' or 'urls', not both.")
        return self


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", tags=["parser"])
def parse(payload: ParseRequest) -> dict:
    urls = [payload.url] if payload.url else list(payload.urls or [])
    try:
        results = parse_urls_multiprocessing(urls=urls, workers=payload.workers)
    except Exception as error:  # noqa: BLE001 - expose service failure as HTTP 500
        raise HTTPException(status_code=500, detail=f"Parser service error: {error}") from error

    saved_count = sum(1 for item in results if item.get("saved"))
    return {
        "message": "Parsing completed",
        "approach": "multiprocessing",
        "total": len(results),
        "saved": saved_count,
        "results": results,
    }
