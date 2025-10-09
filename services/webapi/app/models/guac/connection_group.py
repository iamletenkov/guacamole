"""Guacamole connection group (guacamole_connection_group)."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db.base import Base

from .enums import guacamole_connection_group_type


class GuacamoleConnectionGroup(Base):
    __tablename__ = "guacamole_connection_group"

    connection_group_id = Column(Integer, primary_key=True)
    parent_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection_group.connection_group_id",
            name="guacamole_connection_group_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    connection_group_name = Column(String(128), nullable=False)
    type = Column(guacamole_connection_group_type, nullable=False)

    max_connections = Column(Integer)
    max_connections_per_user = Column(Integer)
    enable_session_affinity = Column(Boolean, nullable=False, default=False)
