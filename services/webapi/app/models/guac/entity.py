"""Guacamole entity model (guacamole_entity)."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.db.base import Base

from .enums import guacamole_entity_type


class GuacamoleEntity(Base):
    __tablename__ = "guacamole_entity"

    entity_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(guacamole_entity_type, nullable=False)

    __table_args__ = (
        UniqueConstraint("type", "name", name="guacamole_entity_name_scope"),
    )

