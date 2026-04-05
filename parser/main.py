from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
import httpx

app = FastAPI(title="Parser Service")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
def parse(url: str = Query(...)) -> dict[str, str]:
    try:
        response = httpx.get(url, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    return {
        "message": "Parsing completed",
        "url": url,
        "title": title,
    }
