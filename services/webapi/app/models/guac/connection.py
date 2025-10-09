"""Guacamole connection (guacamole_connection)."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db.base import Base

from .enums import guacamole_proxy_encryption_method


class GuacamoleConnection(Base):
    __tablename__ = "guacamole_connection"

    connection_id = Column(Integer, primary_key=True)
    connection_name = Column(String(128), nullable=False)
    parent_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection_group.connection_group_id",
            name="guacamole_connection_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    protocol = Column(String(32), nullable=False)

    max_connections = Column(Integer)
    max_connections_per_user = Column(Integer)
    connection_weight = Column(Integer)
    failover_only = Column(Boolean, nullable=False, default=False)

    proxy_port = Column(Integer)
    proxy_hostname = Column(String(512))
    proxy_encryption_method = Column(guacamole_proxy_encryption_method)
