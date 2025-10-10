"""User management endpoints backed by Guacamole-compatible schema."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from app.db.session import get_db
from app.models.guac.entity import GuacamoleEntity
from app.models.guac.user import GuacamoleUser  # noqa: TCH001
from app.repositories.users import UserRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class UserCreate(BaseModel):
    name: str
    password: str
    full_name: str | None = None
    email_address: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    name: str
    full_name: str | None = None
    email_address: str | None = None
    disabled: bool

    @staticmethod
    def from_models(user: GuacamoleUser, entity: GuacamoleEntity) -> UserOut:
        return UserOut(
            user_id=user.user_id,
            name=entity.name,
            full_name=user.full_name,
            email_address=user.email_address,
            disabled=user.disabled,
        )


@router.get("/", response_model=List[UserOut])
def list_users(
    limit: int = 100, offset: int = 0, db: Session = db_dependency
) -> List[UserOut]:
    repo = UserRepository(db)
    users = repo.list_users(limit=limit, offset=offset)
    # Load entities for names
    result: list[UserOut] = []
    for u in users:
        ent = db.get(GuacamoleEntity, u.entity_id)
        if ent is None:
            # Invariant violation should not happen
            continue
        result.append(UserOut.from_models(u, ent))
    return result


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = db_dependency) -> UserOut:
    repo = UserRepository(db)
    if repo.get_entity_by_name(payload.name):
        raise HTTPException(status_code=409, detail="User already exists")

    user = repo.create_user(payload.name, payload.password)
    # Optional profile fields
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.email_address is not None:
        user.email_address = payload.email_address
    db.commit()

    ent = db.get(GuacamoleEntity, user.entity_id)
    assert ent is not None
    return UserOut.from_models(user, ent)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(name: str, db: Session = db_dependency) -> None:
    repo = UserRepository(db)
    ent = repo.get_entity_by_name(name)
    if ent is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = repo.get_user_by_entity_id(ent.entity_id)
    if user is None:
        # Entity exists but user row missing; still remove entity
        db.delete(ent)
        db.commit()
        return
    repo.delete_user(user)
    # CASCADE will remove entity via FK? In schema, user -> entity CASCADE.
    db.commit()
    return


class SetPasswordPayload(BaseModel):
    password: str


@router.post("/{name}/set-password")
def set_password(
    name: str, payload: SetPasswordPayload, db: Session = db_dependency
) -> dict:
    repo = UserRepository(db)
    ent = repo.get_entity_by_name(name)
    if ent is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = repo.get_user_by_entity_id(ent.entity_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User row not found")
    repo.set_password(user, payload.password)
    db.commit()
    return {"status": "ok"}
