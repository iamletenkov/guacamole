"""SQLAlchemy engine and session setup."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.orm import Session


def _build_engine_url() -> str:
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    # Fallback assembled in settings.assemble_db_connection
    return settings.DATABASE_URL  # type: ignore[return-value]


ENGINE = create_engine(_build_engine_url(), pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
