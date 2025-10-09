"""Main API router."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    attributes,
    auth,
    connections,
    groups,
    history,
    permissions,
    recordings,
    sessions,
    sharing_profiles,
    users,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(recordings.router, prefix="/recordings", tags=["recordings"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(
    connections.router, prefix="/connections", tags=["connections"]
)
api_router.include_router(
    permissions.router, prefix="/permissions", tags=["permissions"]
)
api_router.include_router(
    sharing_profiles.router, prefix="/sharing-profiles", tags=["sharing-profiles"]
)
api_router.include_router(attributes.router, prefix="/attributes", tags=["attributes"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
