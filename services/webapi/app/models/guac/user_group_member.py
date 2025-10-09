"""Guacamole user group membership (guacamole_user_group_member)."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from app.db.base import Base


class GuacamoleUserGroupMember(Base):
    __tablename__ = "guacamole_user_group_member"

    user_group_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user_group.user_group_id",
            name="guacamole_user_group_member_parent",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    member_entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_user_group_member_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    __table_args__ = (PrimaryKeyConstraint("user_group_id", "member_entity_id"),)
