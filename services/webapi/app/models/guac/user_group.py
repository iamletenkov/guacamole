"""Guacamole user group model (guacamole_user_group)."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer

from app.db.base import Base


class GuacamoleUserGroup(Base):
    __tablename__ = "guacamole_user_group"

    user_group_id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_user_group_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )
    disabled = Column(Boolean, nullable=False, default=False)

