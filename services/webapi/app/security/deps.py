from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.config import settings
from app.db.session import get_db
from app.repositories.users import UserRepository
from app.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials = token
    try:
        payload = decode_access_token(credentials)
        username: str | None = payload.get("sub")
        if not username:
            raise ValueError("missing sub")
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    repo = UserRepository(db)
    ent = repo.get_entity_by_name(username)
    if ent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return ent
