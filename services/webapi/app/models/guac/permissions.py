"""Guacamole permissions tables models."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from app.db.base import Base

from .enums import guacamole_object_permission_type, guacamole_system_permission_type


class GuacamoleConnectionPermission(Base):
    __tablename__ = "guacamole_connection_permission"

    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_connection_permission_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    connection_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection.connection_id",
            name="guacamole_connection_permission_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    permission = Column(guacamole_object_permission_type, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("entity_id", "connection_id", "permission"),)


class GuacamoleConnectionGroupPermission(Base):
    __tablename__ = "guacamole_connection_group_permission"

    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_connection_group_permission_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    connection_group_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection_group.connection_group_id",
            name="guacamole_connection_group_permission_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    permission = Column(guacamole_object_permission_type, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("entity_id", "connection_group_id", "permission"),
    )


class GuacamoleUserPermission(Base):
    __tablename__ = "guacamole_user_permission"

    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_user_permission_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    affected_user_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user.user_id",
            name="guacamole_user_permission_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    permission = Column(guacamole_object_permission_type, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("entity_id", "affected_user_id", "permission"),
    )


class GuacamoleUserGroupPermission(Base):
    __tablename__ = "guacamole_user_group_permission"

    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_user_group_permission_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    affected_user_group_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user_group.user_group_id",
            name="guacamole_user_group_permission_affected_user_group",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    permission = Column(guacamole_object_permission_type, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("entity_id", "affected_user_group_id", "permission"),
    )


class GuacamoleSystemPermission(Base):
    __tablename__ = "guacamole_system_permission"

    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_system_permission_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    permission = Column(guacamole_system_permission_type, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("entity_id", "permission"),)
