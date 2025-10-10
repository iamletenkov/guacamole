"""Guacamole sharing profile (guacamole_sharing_profile)."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base import Base


class GuacamoleSharingProfile(Base):
    __tablename__ = "guacamole_sharing_profile"

    sharing_profile_id = Column(Integer, primary_key=True)
    sharing_profile_name = Column(String(128), nullable=False)
    primary_connection_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection.connection_id",
            name="guacamole_sharing_profile_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

