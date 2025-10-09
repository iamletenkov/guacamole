"""Guacamole connection parameters (guacamole_connection_parameter)."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String

from app.db.base import Base


class GuacamoleConnectionParameter(Base):
    __tablename__ = "guacamole_connection_parameter"

    connection_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection.connection_id",
            name="guacamole_connection_parameter_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    parameter_name = Column(String(128), nullable=False)
    parameter_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("connection_id", "parameter_name"),)
