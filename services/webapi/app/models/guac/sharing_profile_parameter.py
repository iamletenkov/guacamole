"""Guacamole sharing profile parameters (guacamole_sharing_profile_parameter)."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String

from app.db.base import Base


class GuacamoleSharingProfileParameter(Base):
    __tablename__ = "guacamole_sharing_profile_parameter"

    sharing_profile_id = Column(
        Integer,
        ForeignKey(
            "guacamole_sharing_profile.sharing_profile_id",
            name="guacamole_sharing_profile_parameter_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    parameter_name = Column(String(128), nullable=False)
    parameter_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("sharing_profile_id", "parameter_name"),)
