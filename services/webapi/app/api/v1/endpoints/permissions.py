"""Permissions endpoints: grant/revoke/query for Guacamole schema."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db.session import get_db

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
from app.repositories.permissions import PermissionRepository

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class ConnectionPermissionPayload(BaseModel):
    entity_id: int
    connection_id: int
    permission: Literal["READ", "UPDATE", "DELETE", "ADMINISTER"]


@router.post("/connections/grant")
def grant_connection(
    payload: ConnectionPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    repo.grant_connection(payload.entity_id, payload.connection_id, payload.permission)
    db.commit()
    return {"status": "ok"}


@router.post("/connections/revoke")
def revoke_connection(
    payload: ConnectionPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    removed = repo.revoke_connection(
        payload.entity_id, payload.connection_id, payload.permission
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
    return {"status": "ok"}


class ConnectionGroupPermissionPayload(BaseModel):
    entity_id: int
    connection_group_id: int
    permission: Literal["READ", "UPDATE", "DELETE", "ADMINISTER"]


@router.post("/connection-groups/grant")
def grant_connection_group(
    payload: ConnectionGroupPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    repo.grant_connection_group(
        payload.entity_id, payload.connection_group_id, payload.permission
    )
    db.commit()
    return {"status": "ok"}


@router.post("/connection-groups/revoke")
def revoke_connection_group(
    payload: ConnectionGroupPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    removed = repo.revoke_connection_group(
        payload.entity_id, payload.connection_group_id, payload.permission
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
    return {"status": "ok"}


class UserPermissionPayload(BaseModel):
    entity_id: int
    affected_user_id: int
    permission: Literal["READ", "UPDATE", "DELETE", "ADMINISTER"]


@router.post("/users/grant")
def grant_user(payload: UserPermissionPayload, db: Session = db_dependency) -> dict:
    repo = PermissionRepository(db)
    repo.grant_user(payload.entity_id, payload.affected_user_id, payload.permission)
    db.commit()
    return {"status": "ok"}


@router.post("/users/revoke")
def revoke_user(payload: UserPermissionPayload, db: Session = db_dependency) -> dict:
    repo = PermissionRepository(db)
    removed = repo.revoke_user(
        payload.entity_id, payload.affected_user_id, payload.permission
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
    return {"status": "ok"}


class UserGroupPermissionPayload(BaseModel):
    entity_id: int
    affected_user_group_id: int
    permission: Literal["READ", "UPDATE", "DELETE", "ADMINISTER"]


@router.post("/user-groups/grant")
def grant_user_group(
    payload: UserGroupPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    repo.grant_user_group(
        payload.entity_id, payload.affected_user_group_id, payload.permission
    )
    db.commit()
    return {"status": "ok"}


@router.post("/user-groups/revoke")
def revoke_user_group(
    payload: UserGroupPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    removed = repo.revoke_user_group(
        payload.entity_id, payload.affected_user_group_id, payload.permission
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
    return {"status": "ok"}


class SystemPermissionPayload(BaseModel):
    entity_id: int
    permission: Literal[
        "CREATE_CONNECTION",
        "CREATE_CONNECTION_GROUP",
        "CREATE_SHARING_PROFILE",
        "CREATE_USER",
        "CREATE_USER_GROUP",
        "ADMINISTER",
    ]


@router.post("/system/grant")
def grant_system(payload: SystemPermissionPayload, db: Session = db_dependency) -> dict:
    repo = PermissionRepository(db)
    repo.grant_system(payload.entity_id, payload.permission)
    db.commit()
    return {"status": "ok"}


@router.post("/system/revoke")
def revoke_system(
    payload: SystemPermissionPayload, db: Session = db_dependency
) -> dict:
    repo = PermissionRepository(db)
    removed = repo.revoke_system(payload.entity_id, payload.permission)
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
    return {"status": "ok"}
