"""Declarative base and model imports for Alembic discovery."""

from __future__ import annotations

import contextlib

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so Alembic can discover them via app.db.base import
# NOTE: Keep imports at the end to avoid circular imports during module init
with contextlib.suppress(
    Exception
):  # pragma: no cover - optional during early bootstrap
    from app.models.guac import (  # noqa: F401
        attributes,
        connection,
        connection_group,
        connection_parameter,
        entity,
        history,
        permissions,
        sharing_profile,
        sharing_profile_parameter,
        user,
        user_group,
        user_group_member,
    )
