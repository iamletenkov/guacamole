"""Guacamole attributes tables ORM models."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String

from app.db.base import Base


class GuacamoleUserAttribute(Base):
    __tablename__ = "guacamole_user_attribute"

    user_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user.user_id",
            name="guacamole_user_attribute_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    attribute_name = Column(String(128), nullable=False)
    attribute_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "attribute_name"),)


class GuacamoleUserGroupAttribute(Base):
    __tablename__ = "guacamole_user_group_attribute"

    user_group_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user_group.user_group_id",
            name="guacamole_user_group_attribute_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    attribute_name = Column(String(128), nullable=False)
    attribute_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_group_id", "attribute_name"),)


class GuacamoleConnectionAttribute(Base):
    __tablename__ = "guacamole_connection_attribute"

    connection_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection.connection_id",
            name="guacamole_connection_attribute_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    attribute_name = Column(String(128), nullable=False)
    attribute_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("connection_id", "attribute_name"),)


class GuacamoleConnectionGroupAttribute(Base):
    __tablename__ = "guacamole_connection_group_attribute"

    connection_group_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection_group.connection_group_id",
            name="guacamole_connection_group_attribute_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    attribute_name = Column(String(128), nullable=False)
    attribute_value = Column(String(4096), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("connection_group_id", "attribute_name"),)

