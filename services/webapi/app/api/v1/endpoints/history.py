"""History endpoints (read-only)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.db.session import get_db

if TYPE_CHECKING:
    from datetime import datetime

    from sqlalchemy.orm import Session

from app.models.guac.history import GuacamoleConnectionHistory, GuacamoleUserHistory

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class ConnectionHistoryOut(BaseModel):
    history_id: int
    user_id: int | None
    username: str
    remote_host: str | None
    connection_id: int | None
    connection_name: str
    sharing_profile_id: int | None
    sharing_profile_name: str | None
    start_date: datetime
    end_date: datetime | None

    @staticmethod
    def from_model(m: GuacamoleConnectionHistory) -> ConnectionHistoryOut:
        return ConnectionHistoryOut(
            history_id=m.history_id,
            user_id=m.user_id,
            username=m.username,
            remote_host=m.remote_host,
            connection_id=m.connection_id,
            connection_name=m.connection_name,
            sharing_profile_id=m.sharing_profile_id,
            sharing_profile_name=m.sharing_profile_name,
            start_date=m.start_date,
            end_date=m.end_date,
        )


class UserHistoryOut(BaseModel):
    history_id: int
    user_id: int | None
    username: str
    remote_host: str | None
    start_date: datetime
    end_date: datetime | None

    @staticmethod
    def from_model(m: GuacamoleUserHistory) -> UserHistoryOut:
        return UserHistoryOut(
            history_id=m.history_id,
            user_id=m.user_id,
            username=m.username,
            remote_host=m.remote_host,
            start_date=m.start_date,
            end_date=m.end_date,
        )


@router.get("/connections", response_model=list[ConnectionHistoryOut])
def get_connection_history(
    user_id: int | None = Query(None),
    connection_id: int | None = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = db_dependency,
) -> list[ConnectionHistoryOut]:
    stmt = db.query(GuacamoleConnectionHistory)
    if user_id is not None:
        stmt = stmt.filter(GuacamoleConnectionHistory.user_id == user_id)
    if connection_id is not None:
        stmt = stmt.filter(GuacamoleConnectionHistory.connection_id == connection_id)
    stmt = (
        stmt.offset(offset)
        .limit(limit)
        .order_by(GuacamoleConnectionHistory.start_date.desc())
    )
    return [ConnectionHistoryOut.from_model(h) for h in stmt.all()]


@router.get("/users", response_model=list[UserHistoryOut])
def get_user_history(
    user_id: int | None = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = db_dependency,
) -> list[UserHistoryOut]:
    stmt = db.query(GuacamoleUserHistory)
    if user_id is not None:
        stmt = stmt.filter(GuacamoleUserHistory.user_id == user_id)
    stmt = (
        stmt.offset(offset)
        .limit(limit)
        .order_by(GuacamoleUserHistory.start_date.desc())
    )
    return [UserHistoryOut.from_model(h) for h in stmt.all()]
