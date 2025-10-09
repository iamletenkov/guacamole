"""Guacamole user model (guacamole_user)."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Time,
)

from app.db.base import Base


class GuacamoleUser(Base):
    __tablename__ = "guacamole_user"

    user_id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer,
        ForeignKey(
            "guacamole_entity.entity_id",
            name="guacamole_user_entity",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    password_hash = Column(LargeBinary, nullable=False)
    password_salt = Column(LargeBinary)
    password_date = Column(DateTime(timezone=True), nullable=False)

    disabled = Column(Boolean, nullable=False, default=False)
    expired = Column(Boolean, nullable=False, default=False)

    access_window_start = Column(Time)
    access_window_end = Column(Time)
    valid_from = Column(Date)
    valid_until = Column(Date)

    timezone = Column(String(64))

    full_name = Column(String(256))
    email_address = Column(String(256))
    organization = Column(String(256))
    organizational_role = Column(String(256))

    telegram_id = Column(Integer)
    first_name = Column(String(256))
    last_name = Column(String(256))
