"""Main API router."""

from fastapi import APIRouter, Depends

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
from app.security.deps import get_current_user

api_router = APIRouter()

# Public auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])  # no guard

# Protected routers
_guard = [Depends(get_current_user)]
api_router.include_router(users.router, prefix="/users", tags=["users"], dependencies=_guard)
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"], dependencies=_guard)
api_router.include_router(recordings.router, prefix="/recordings", tags=["recordings"], dependencies=_guard)
api_router.include_router(groups.router, prefix="/groups", tags=["groups"], dependencies=_guard)
api_router.include_router(connections.router, prefix="/connections", tags=["connections"], dependencies=_guard)
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"], dependencies=_guard)
api_router.include_router(sharing_profiles.router, prefix="/sharing-profiles", tags=["sharing-profiles"], dependencies=_guard)
api_router.include_router(attributes.router, prefix="/attributes", tags=["attributes"], dependencies=_guard)
api_router.include_router(history.router, prefix="/history", tags=["history"], dependencies=_guard)
