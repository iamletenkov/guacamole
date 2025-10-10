"""JWT utilities for issuing and verifying access tokens."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(
    data: Dict[str, Any], expires_minutes: int | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:  # let caller decide how to handle
        raise exc


