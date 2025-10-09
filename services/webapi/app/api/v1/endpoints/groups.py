"""User group management endpoints backed by Guacamole schema."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.session import get_db
from app.models.guac.entity import GuacamoleEntity
from app.repositories.user_groups import UserGroupRepository
from app.repositories.users import UserRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from app.models.guac.user_group import GuacamoleUserGroup

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class GroupCreate(BaseModel):
    name: str
    disabled: bool = False


class GroupOut(BaseModel):
    user_group_id: int
    name: str
    disabled: bool

    @staticmethod
    def from_models(group: GuacamoleUserGroup, entity: GuacamoleEntity) -> GroupOut:
        return GroupOut(
            user_group_id=group.user_group_id, name=entity.name, disabled=group.disabled
        )


@router.post("/", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
def create_group(payload: GroupCreate, db: Session = db_dependency) -> GroupOut:
    repo = UserGroupRepository(db)
    if repo.get_group_by_name(payload.name):
        raise HTTPException(status_code=409, detail="Group already exists")
    group = repo.create_group(payload.name, disabled=payload.disabled)
    db.commit()
    ent = db.get(GuacamoleEntity, group.entity_id)
    assert ent is not None
    return GroupOut.from_models(group, ent)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(name: str, db: Session = db_dependency) -> None:
    repo = UserGroupRepository(db)
    if not repo.delete_group(name):
        raise HTTPException(status_code=404, detail="Group not found")
    db.commit()


class GroupMemberChange(BaseModel):
    group_name: str
    member_name: str  # user or group entity name


@router.post("/members/add")
def add_member(payload: GroupMemberChange, db: Session = db_dependency) -> dict:
    grepo = UserGroupRepository(db)
    urepo = UserRepository(db)
    group = grepo.get_group_by_name(payload.group_name)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    # member entity may be user or group
    ment = urepo.get_entity_by_name(
        payload.member_name
    ) or grepo.get_group_entity_by_name(payload.member_name)
    if not ment:
        raise HTTPException(status_code=404, detail="Member entity not found")
    grepo.add_member(group.user_group_id, ment.entity_id)
    db.commit()
    return {"status": "ok"}


@router.post("/members/remove")
def remove_member(payload: GroupMemberChange, db: Session = db_dependency) -> dict:
    grepo = UserGroupRepository(db)
    urepo = UserRepository(db)
    group = grepo.get_group_by_name(payload.group_name)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    ment = urepo.get_entity_by_name(
        payload.member_name
    ) or grepo.get_group_entity_by_name(payload.member_name)
    if not ment:
        raise HTTPException(status_code=404, detail="Member entity not found")
    removed = grepo.remove_member(group.user_group_id, ment.entity_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.commit()
    return {"status": "ok"}
