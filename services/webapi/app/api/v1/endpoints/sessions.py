"""Session management endpoints."""

from datetime import datetime
from uuid import UUID, uuid4

from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

router = APIRouter()

# Query defaults
USER_ID_QUERY = Query(None)
IS_ACTIVE_QUERY = Query(None)


class SessionBase(BaseModel):
    """Base session model."""

    user_id: UUID
    connection_name: str
    protocol: str
    host: str
    port: int
    username: str


class SessionCreate(SessionBase):
    """Session creation model."""

    password: str


class SessionUpdate(BaseModel):
    """Session update model."""

    connection_name: str | None = None
    protocol: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    is_active: bool | None = None


class Session(SessionBase):
    """Session response model."""

    id: UUID
    is_active: bool
    created_at: str
    updated_at: str
    last_connected: str | None = None

    class Config:
        from_attributes = True


class SessionConnection(BaseModel):
    """Session connection model."""

    session_id: UUID
    status: str
    connected_at: str
    duration: int | None = None


# Mock data
MOCK_SESSIONS = [
    Session(
        id=uuid4(),
        user_id=uuid4(),
        connection_name="Production Server",
        protocol="SSH",
        host="192.168.1.100",
        port=22,
        username="admin",
        is_active=True,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_connected="2024-01-01T12:00:00Z",
    ),
    Session(
        id=uuid4(),
        user_id=uuid4(),
        connection_name="Development Server",
        protocol="RDP",
        host="192.168.1.101",
        port=3389,
        username="developer",
        is_active=True,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_connected=None,
    ),
]


@router.get("/", response_model=List[Session])
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    user_id: UUID | None = USER_ID_QUERY,
    is_active: bool | None = IS_ACTIVE_QUERY,
) -> List[Session]:
    """Get list of sessions."""
    sessions = MOCK_SESSIONS

    if user_id:
        sessions = [s for s in sessions if s.user_id == user_id]

    if is_active is not None:
        sessions = [s for s in sessions if s.is_active == is_active]

    return sessions[skip : skip + limit]


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: UUID) -> Session:
    """Get session by ID."""
    for session in MOCK_SESSIONS:
        if session.id == session_id:
            return session
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
    )


@router.post("/", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate) -> Session:
    """Create new session."""
    new_session = Session(
        id=uuid4(),
        user_id=session.user_id,
        connection_name=session.connection_name,
        protocol=session.protocol,
        host=session.host,
        port=session.port,
        username=session.username,
        is_active=True,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )
    MOCK_SESSIONS.append(new_session)
    return new_session


@router.put("/{session_id}", response_model=Session)
async def update_session(session_id: UUID, session_update: SessionUpdate) -> Session:
    """Update session."""
    for i, session in enumerate(MOCK_SESSIONS):
        if session.id == session_id:
            update_data = session_update.dict(exclude_unset=True)
            updated_session = session.copy(update=update_data)
            MOCK_SESSIONS[i] = updated_session
            return updated_session
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: UUID) -> None:
    """Delete session."""
    for i, session in enumerate(MOCK_SESSIONS):
        if session.id == session_id:
            del MOCK_SESSIONS[i]
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
    )


@router.post("/{session_id}/connect", response_model=SessionConnection)
async def connect_session(session_id: UUID) -> SessionConnection:
    """Connect to session."""
    session = None
    for s in MOCK_SESSIONS:
        if s.id == session_id:
            session = s
            break

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    if not session.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Session is not active"
        )

    # Mock connection
    return SessionConnection(
        session_id=session_id,
        status="connected",
        connected_at=datetime.utcnow().isoformat() + "Z",
        duration=0,
    )


@router.post("/{session_id}/disconnect")
async def disconnect_session(session_id: UUID) -> dict[str, str]:
    """Disconnect from session."""
    session = None
    for s in MOCK_SESSIONS:
        if s.id == session_id:
            session = s
            break

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    return {"message": "Session disconnected successfully"}
