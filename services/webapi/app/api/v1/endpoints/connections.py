"""Connections and connection groups endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.session import get_db
from app.repositories.connections import ConnectionRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from app.models.guac.connection import GuacamoleConnection
    from app.models.guac.connection_group import GuacamoleConnectionGroup

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class ConnectionGroupCreate(BaseModel):
    name: str
    parent_id: int | None = None
    type: str = "ORGANIZATIONAL"
    max_connections: int | None = None
    max_connections_per_user: int | None = None
    enable_session_affinity: bool = False


class ConnectionGroupOut(BaseModel):
    connection_group_id: int
    name: str
    parent_id: int | None = None
    type: str

    @staticmethod
    def from_model(m: GuacamoleConnectionGroup) -> ConnectionGroupOut:
        return ConnectionGroupOut(
            connection_group_id=m.connection_group_id,
            name=m.connection_group_name,
            parent_id=m.parent_id,
            type=m.type,
        )


@router.post(
    "/groups", response_model=ConnectionGroupOut, status_code=status.HTTP_201_CREATED
)
def create_group(
    payload: ConnectionGroupCreate, db: Session = db_dependency
) -> ConnectionGroupOut:
    repo = ConnectionRepository(db)
    grp = repo.create_group(
        name=payload.name,
        parent_id=payload.parent_id,
        group_type=payload.type,
        max_connections=payload.max_connections,
        max_connections_per_user=payload.max_connections_per_user,
        enable_session_affinity=payload.enable_session_affinity,
    )
    db.commit()
    return ConnectionGroupOut.from_model(grp)


@router.get("/groups", response_model=List[ConnectionGroupOut])
def list_groups(
    parent_id: int | None = None, db: Session = db_dependency
) -> List[ConnectionGroupOut]:
    repo = ConnectionRepository(db)
    return [ConnectionGroupOut.from_model(x) for x in repo.list_groups(parent_id)]


class ConnectionCreate(BaseModel):
    name: str
    protocol: str
    parent_group_id: int | None = None
    parameters: dict[str, str] | None = None


class ConnectionOut(BaseModel):
    connection_id: int
    name: str
    protocol: str
    parent_group_id: int | None = None

    @staticmethod
    def from_model(m: GuacamoleConnection) -> ConnectionOut:
        return ConnectionOut(
            connection_id=m.connection_id,
            name=m.connection_name,
            protocol=m.protocol,
            parent_group_id=m.parent_id,
        )


@router.post("/", response_model=ConnectionOut, status_code=status.HTTP_201_CREATED)
def create_connection(
    payload: ConnectionCreate, db: Session = db_dependency
) -> ConnectionOut:
    repo = ConnectionRepository(db)
    conn = repo.create_connection(
        name=payload.name,
        protocol=payload.protocol,
        parent_group_id=payload.parent_group_id,
        parameters=payload.parameters,
    )
    db.commit()
    return ConnectionOut.from_model(conn)


@router.get("/", response_model=List[ConnectionOut])
def list_connections(
    parent_group_id: int | None = None, db: Session = db_dependency
) -> List[ConnectionOut]:
    repo = ConnectionRepository(db)
    return [ConnectionOut.from_model(x) for x in repo.list_connections(parent_group_id)]


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(connection_id: int, db: Session = db_dependency) -> None:
    repo = ConnectionRepository(db)
    deleted = repo.delete_connection(connection_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.commit()
