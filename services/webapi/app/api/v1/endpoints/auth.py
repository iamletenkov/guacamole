"""Authentication endpoints (OAuth2 password + JWT)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.config import settings
from app.db.session import get_db
from app.repositories.users import UserRepository
from app.security.jwt import create_access_token, decode_access_token
from app.security.passwords import GuacPasswordService

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)) -> Token:
    repo = UserRepository(db)
    ent = repo.get_entity_by_name(form_data.username)
    if ent is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = repo.get_user_by_entity_id(ent.entity_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not GuacPasswordService().verify(form_data.password, user.password_salt, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": ent.name})
    return Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


@router.get("/me")
def me(token: str = Depends(lambda: None)) -> dict[str, Any]:
    # For Swagger Authorize, use OAuth2 scheme injected via global dependencies; here decode from Authorization header
    # This simple route expects Authorization to be set by Swagger Authorize (handled by OAuth2PasswordBearer in deps)
    # Since we don't have access to the token here directly, advise using protected endpoints to get user context.
    return {"message": "Use protected endpoints with Authorization header; /me kept minimal."}


@router.post("/refresh", response_model=Token)
def refresh(token_str: str = Depends(lambda: None)) -> Token:
    # For simplicity, refreshing requires client to just call /login again; keeping endpoint for compatibility
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Use /auth/login to obtain a new token")
