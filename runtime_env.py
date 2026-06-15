import os
from pathlib import Path


def running_in_docker() -> bool:
    return Path("/.dockerenv").exists()


def adjust_database_url(url: str) -> str:
    if running_in_docker() or not url:
        return url

    host_port = os.getenv("DATABASE_HOST_PORT", "5433")
    return url.replace("@db:5432", f"@localhost:{host_port}")
