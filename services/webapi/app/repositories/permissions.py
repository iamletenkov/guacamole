"""Repositories for Guacamole permissions grant/revoke/query."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from app.models.guac.permissions import (
    GuacamoleConnectionGroupPermission,
    GuacamoleConnectionPermission,
    GuacamoleSystemPermission,
    GuacamoleUserGroupPermission,
    GuacamoleUserPermission,
)


class PermissionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Connection permissions
    def grant_connection(
        self, entity_id: int, connection_id: int, permission: str
    ) -> None:
        row = GuacamoleConnectionPermission(
            entity_id=entity_id, connection_id=connection_id, permission=permission
        )
        self.db.merge(row)

    def revoke_connection(
        self, entity_id: int, connection_id: int, permission: str
    ) -> int:
        stmt = (
            delete(GuacamoleConnectionPermission)
            .where(GuacamoleConnectionPermission.entity_id == entity_id)
            .where(GuacamoleConnectionPermission.connection_id == connection_id)
            .where(GuacamoleConnectionPermission.permission == permission)
        )
        res = self.db.execute(stmt)
        return res.rowcount or 0

    # Connection group permissions
    def grant_connection_group(
        self, entity_id: int, connection_group_id: int, permission: str
    ) -> None:
        row = GuacamoleConnectionGroupPermission(
            entity_id=entity_id,
            connection_group_id=connection_group_id,
            permission=permission,
        )
        self.db.merge(row)

    def revoke_connection_group(
        self, entity_id: int, connection_group_id: int, permission: str
    ) -> int:
        stmt = (
            delete(GuacamoleConnectionGroupPermission)
            .where(GuacamoleConnectionGroupPermission.entity_id == entity_id)
            .where(
                GuacamoleConnectionGroupPermission.connection_group_id
                == connection_group_id
            )
            .where(GuacamoleConnectionGroupPermission.permission == permission)
        )
        res = self.db.execute(stmt)
        return res.rowcount or 0

    # User permissions
    def grant_user(
        self, entity_id: int, affected_user_id: int, permission: str
    ) -> None:
        row = GuacamoleUserPermission(
            entity_id=entity_id,
            affected_user_id=affected_user_id,
            permission=permission,
        )
        self.db.merge(row)

    def revoke_user(
        self, entity_id: int, affected_user_id: int, permission: str
    ) -> int:
        stmt = (
            delete(GuacamoleUserPermission)
            .where(GuacamoleUserPermission.entity_id == entity_id)
            .where(GuacamoleUserPermission.affected_user_id == affected_user_id)
            .where(GuacamoleUserPermission.permission == permission)
        )
        res = self.db.execute(stmt)
        return res.rowcount or 0

    # User group permissions
    def grant_user_group(
        self, entity_id: int, affected_user_group_id: int, permission: str
    ) -> None:
        row = GuacamoleUserGroupPermission(
            entity_id=entity_id,
            affected_user_group_id=affected_user_group_id,
            permission=permission,
        )
        self.db.merge(row)

    def revoke_user_group(
        self, entity_id: int, affected_user_group_id: int, permission: str
    ) -> int:
        stmt = (
            delete(GuacamoleUserGroupPermission)
            .where(GuacamoleUserGroupPermission.entity_id == entity_id)
            .where(
                GuacamoleUserGroupPermission.affected_user_group_id
                == affected_user_group_id
            )
            .where(GuacamoleUserGroupPermission.permission == permission)
        )
        res = self.db.execute(stmt)
        return res.rowcount or 0

    # System permissions
    def grant_system(self, entity_id: int, permission: str) -> None:
        row = GuacamoleSystemPermission(entity_id=entity_id, permission=permission)
        self.db.merge(row)

    def revoke_system(self, entity_id: int, permission: str) -> int:
        stmt = (
            delete(GuacamoleSystemPermission)
            .where(GuacamoleSystemPermission.entity_id == entity_id)
            .where(GuacamoleSystemPermission.permission == permission)
        )
        res = self.db.execute(stmt)
        return res.rowcount or 0
