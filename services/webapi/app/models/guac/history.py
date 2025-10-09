"""Guacamole history tables ORM representations."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.base import Base


class GuacamoleConnectionHistory(Base):
    __tablename__ = "guacamole_connection_history"

    history_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user.user_id",
            name="guacamole_connection_history_ibfk_1",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    username = Column(String(128), nullable=False)
    remote_host = Column(String(256))
    connection_id = Column(
        Integer,
        ForeignKey(
            "guacamole_connection.connection_id",
            name="guacamole_connection_history_ibfk_2",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    connection_name = Column(String(128), nullable=False)
    sharing_profile_id = Column(
        Integer,
        ForeignKey(
            "guacamole_sharing_profile.sharing_profile_id",
            name="guacamole_connection_history_ibfk_3",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    sharing_profile_name = Column(String(128))
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))


class GuacamoleUserHistory(Base):
    __tablename__ = "guacamole_user_history"

    history_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user.user_id",
            name="guacamole_user_history_ibfk_1",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    username = Column(String(128), nullable=False)
    remote_host = Column(String(256))
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))


class GuacamoleUserPasswordHistory(Base):
    __tablename__ = "guacamole_user_password_history"

    password_history_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(
            "guacamole_user.user_id",
            name="guacamole_user_password_history_ibfk_1",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    password_hash = Column(
        "password_hash", String
    )  # left as String for brevity; stored as bytea via migration
    password_salt = Column("password_salt", String)
    password_date = Column(DateTime(timezone=True), nullable=False)
