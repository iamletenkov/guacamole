"""Authentication endpoints."""

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr

router = APIRouter()
security = HTTPBearer()

# Dependency injection
security_dependency = Depends(security)


class LoginRequest(BaseModel):
    """Login request model."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Constants
TOKEN_TYPE_BEARER = "bearer"  # HTTP Bearer token type  # noqa: S105


class TokenData(BaseModel):
    """Token data model."""

    user_id: str
    email: str


# Mock users for authentication
# Token parts: mock_token_{user_id}_{uuid}
MIN_TOKEN_PARTS = 3

# TODO: Move to environment variables in production
ADMIN_PASSWORD = "admin123"  # Default admin password for development  # noqa: S105
USER_PASSWORD = "user123"  # Default user password for development  # noqa: S105

MOCK_AUTH_USERS = {
    "admin@spacer.local": {
        "id": str(uuid4()),
        "email": "admin@spacer.local",
        "password": ADMIN_PASSWORD,  # In real app, this would be hashed
        "full_name": "Administrator",
        "is_active": True,
    },
    "user@spacer.local": {
        "id": str(uuid4()),
        "email": "user@spacer.local",
        "password": USER_PASSWORD,  # In real app, this would be hashed
        "full_name": "Regular User",
        "is_active": True,
    },
}


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest) -> Token:
    """Authenticate user and return access token."""
    user = MOCK_AUTH_USERS.get(login_data.email)

    if not user or user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create mock token (in real app, use proper JWT)
    access_token = f"mock_token_{user['id']}_{uuid4()}"

    return Token(
        access_token=access_token,
        token_type=TOKEN_TYPE_BEARER,
        expires_in=1800,  # 30 minutes
    )


@router.post("/logout")
async def logout(token: str = security_dependency) -> dict[str, str]:
    """Logout user (invalidate token)."""
    # In real app, add token to blacklist
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user(token: str = security_dependency) -> dict[str, Any]:
    """Get current user information."""
    # In real app, decode and validate JWT token
    if not token.credentials.startswith("mock_token_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # Extract user ID from mock token
    token_parts = token.credentials.split("_")
    if len(token_parts) < MIN_TOKEN_PARTS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        )

    user_id = token_parts[2]

    # Find user by ID
    for user in MOCK_AUTH_USERS.values():
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "is_active": user["is_active"],
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Depends(security)) -> Token:
    """Refresh access token."""
    # In real app, validate refresh token and issue new access token
    if not token.credentials.startswith("mock_token_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # Create new mock token
    new_access_token = f"mock_token_refreshed_{uuid4()}"

    return Token(
        access_token=new_access_token,
        token_type=TOKEN_TYPE_BEARER,
        expires_in=1800,  # 30 minutes
    )
