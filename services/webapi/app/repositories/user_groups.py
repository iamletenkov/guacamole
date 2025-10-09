"""Repositories for Guacamole user groups and memberships."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from app.models.guac.entity import GuacamoleEntity
from app.models.guac.user_group import GuacamoleUserGroup
from app.models.guac.user_group_member import GuacamoleUserGroupMember


class UserGroupRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Entities
    def get_group_entity_by_name(self, name: str) -> GuacamoleEntity | None:
        stmt = select(GuacamoleEntity).where(
            GuacamoleEntity.name == name, GuacamoleEntity.type == "USER_GROUP"
        )
        return self.db.scalar(stmt)

    def create_group_entity(self, name: str) -> GuacamoleEntity:
        entity = GuacamoleEntity(name=name, type="USER_GROUP")
        self.db.add(entity)
        self.db.flush()
        return entity

    # Groups
    def create_group(
        self, name: str, disabled: bool | None = None
    ) -> GuacamoleUserGroup:
        entity = self.get_group_entity_by_name(name)
        if entity is None:
            entity = self.create_group_entity(name)
        group = GuacamoleUserGroup(
            entity_id=entity.entity_id, disabled=disabled or False
        )
        self.db.add(group)
        self.db.flush()
        return group

    def get_group_by_name(self, name: str) -> GuacamoleUserGroup | None:
        ent = self.get_group_entity_by_name(name)
        if not ent:
            return None
        stmt = select(GuacamoleUserGroup).where(
            GuacamoleUserGroup.entity_id == ent.entity_id
        )
        return self.db.scalar(stmt)

    def delete_group(self, name: str) -> bool:
        group = self.get_group_by_name(name)
        if not group:
            return False
        self.db.delete(group)
        self.db.flush()
        return True

    # Memberships
    def add_member(self, group_id: int, member_entity_id: int) -> None:
        rel = GuacamoleUserGroupMember(
            user_group_id=group_id, member_entity_id=member_entity_id
        )
        self.db.add(rel)

    def remove_member(self, group_id: int, member_entity_id: int) -> int:
        stmt = select(GuacamoleUserGroupMember).where(
            GuacamoleUserGroupMember.user_group_id == group_id,
            GuacamoleUserGroupMember.member_entity_id == member_entity_id,
        )
        rel = self.db.scalar(stmt)
        if rel is None:
            return 0
        self.db.delete(rel)
        return 1
