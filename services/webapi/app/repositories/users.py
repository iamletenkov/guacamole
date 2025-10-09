"""Repositories for Guacamole users and entities."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from app.models.guac.entity import GuacamoleEntity
from app.models.guac.user import GuacamoleUser
from app.security.passwords import GuacPasswordService


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.passwords = GuacPasswordService()

    # Entities
    def get_entity_by_name(self, name: str) -> GuacamoleEntity | None:
        stmt = select(GuacamoleEntity).where(
            GuacamoleEntity.name == name, GuacamoleEntity.type == "USER"
        )
        return self.db.scalar(stmt)

    def create_entity_user(self, name: str) -> GuacamoleEntity:
        entity = GuacamoleEntity(name=name, type="USER")
        self.db.add(entity)
        self.db.flush()  # assign entity_id
        return entity

    # Users
    def get_user_by_entity_id(self, entity_id: int) -> GuacamoleUser | None:
        stmt = select(GuacamoleUser).where(GuacamoleUser.entity_id == entity_id)
        return self.db.scalar(stmt)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[GuacamoleUser]:
        stmt = select(GuacamoleUser).offset(offset).limit(limit)
        return list(self.db.scalars(stmt))

    def create_user(self, name: str, password: str) -> GuacamoleUser:
        # Ensure entity
        entity = self.get_entity_by_name(name)
        if entity is None:
            entity = self.create_entity_user(name)

        # Hash password
        salt, pwd_hash = self.passwords.hash_password(password)

        user = GuacamoleUser(
            entity_id=entity.entity_id,
            password_hash=pwd_hash,
            password_salt=salt,
            password_date=datetime.now(UTC),
            disabled=False,
            expired=False,
        )
        self.db.add(user)
        self.db.flush()
        return user

    def set_password(self, user: GuacamoleUser, new_password: str) -> None:
        salt, pwd_hash = self.passwords.hash_password(new_password)
        user.password_salt = salt
        user.password_hash = pwd_hash
        user.password_date = datetime.now(UTC)
        self.db.add(user)

    def delete_user(self, user: GuacamoleUser) -> None:
        self.db.delete(user)
