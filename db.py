import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base, ParsedPage

load_dotenv()


def _derive_sync_url(async_url: str) -> str:
    return async_url.replace("+asyncpg", "")


def _running_in_docker() -> bool:
    return Path("/.dockerenv").exists()


def _adjust_url_for_runtime(url: str) -> str:
    if _running_in_docker():
        return url

    host_port = os.getenv("DATABASE_HOST_PORT", "5433")
    return url.replace("@db:5432", f"@localhost:{host_port}")


def _require_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Put it in .env")
    return _adjust_url_for_runtime(database_url)


ASYNC_DATABASE_URL = _require_database_url()
SYNC_DATABASE_URL = _adjust_url_for_runtime(
    os.getenv("DATABASE_URL_SYNC", _derive_sync_url(os.getenv("DATABASE_URL", "")))
)

sync_engine: Engine = create_engine(SYNC_DATABASE_URL, future=True)
async_engine: AsyncEngine = create_async_engine(ASYNC_DATABASE_URL, future=True)

SyncSessionLocal = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db_sync() -> None:
    Base.metadata.create_all(bind=sync_engine)


async def init_db_async() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def _upsert_page(session: Session, url: str, title: str, approach: str) -> None:
    existing = session.execute(
        select(ParsedPage).where(ParsedPage.url == url, ParsedPage.approach == approach)
    ).scalar_one_or_none()

    if existing is None:
        session.add(
            ParsedPage(
                url=url,
                title=title,
                approach=approach,
                fetched_at=datetime.now(timezone.utc),
            )
        )
        return

    existing.title = title
    existing.fetched_at = datetime.now(timezone.utc)


def save_parsed_page_sync(url: str, title: str, approach: str) -> None:
    with SyncSessionLocal() as session:
        _upsert_page(session, url=url, title=title, approach=approach)
        session.commit()


async def save_parsed_page_async(url: str, title: str, approach: str) -> None:
    async with AsyncSessionLocal() as session:
        await _upsert_page_async(session, url=url, title=title, approach=approach)
        await session.commit()


async def _upsert_page_async(session: AsyncSession, url: str, title: str, approach: str) -> None:
    existing = (
        await session.execute(select(ParsedPage).where(ParsedPage.url == url, ParsedPage.approach == approach))
    ).scalar_one_or_none()

    if existing is None:
        session.add(
            ParsedPage(
                url=url,
                title=title,
                approach=approach,
                fetched_at=datetime.now(timezone.utc),
            )
        )
        return

    existing.title = title
    existing.fetched_at = datetime.now(timezone.utc)
