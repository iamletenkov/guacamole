"""Recording management endpoints."""

from datetime import datetime
from uuid import UUID, uuid4

from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

router = APIRouter()

# Query defaults
SESSION_ID_QUERY = Query(None)
IS_PROCESSED_QUERY = Query(None)


class RecordingBase(BaseModel):
    """Base recording model."""

    session_id: UUID
    filename: str
    duration: int  # in seconds
    file_size: int  # in bytes


class RecordingCreate(RecordingBase):
    """Recording creation model."""


class RecordingUpdate(BaseModel):
    """Recording update model."""

    filename: str | None = None
    duration: int | None = None
    file_size: int | None = None
    is_processed: bool | None = None


class Recording(RecordingBase):
    """Recording response model."""

    id: UUID
    is_processed: bool
    created_at: str
    updated_at: str
    download_url: str | None = None

    class Config:
        from_attributes = True


class RecordingMetadata(BaseModel):
    """Recording metadata model."""

    recording_id: UUID
    session_info: dict
    technical_details: dict
    quality_metrics: dict


# Mock data
MOCK_RECORDINGS = [
    Recording(
        id=uuid4(),
        session_id=uuid4(),
        filename="session_20240101_120000.rec",
        duration=3600,  # 1 hour
        file_size=104857600,  # 100 MB
        is_processed=True,
        created_at="2024-01-01T12:00:00Z",
        updated_at="2024-01-01T13:00:00Z",
        download_url="/api/v1/recordings/download/session_20240101_120000.rec",
    ),
    Recording(
        id=uuid4(),
        session_id=uuid4(),
        filename="session_20240101_140000.rec",
        duration=1800,  # 30 minutes
        file_size=52428800,  # 50 MB
        is_processed=False,
        created_at="2024-01-01T14:00:00Z",
        updated_at="2024-01-01T14:00:00Z",
        download_url=None,
    ),
]


@router.get("/", response_model=List[Recording])
async def get_recordings(
    skip: int = 0,
    limit: int = 100,
    session_id: UUID | None = SESSION_ID_QUERY,
    is_processed: bool | None = IS_PROCESSED_QUERY,
) -> List[Recording]:
    """Get list of recordings."""
    recordings = MOCK_RECORDINGS

    if session_id:
        recordings = [r for r in recordings if r.session_id == session_id]

    if is_processed is not None:
        recordings = [r for r in recordings if r.is_processed == is_processed]

    return recordings[skip : skip + limit]


@router.get("/{recording_id}", response_model=Recording)
async def get_recording(recording_id: UUID) -> Recording:
    """Get recording by ID."""
    for recording in MOCK_RECORDINGS:
        if recording.id == recording_id:
            return recording
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found"
    )


@router.post("/", response_model=Recording, status_code=status.HTTP_201_CREATED)
async def create_recording(recording: RecordingCreate) -> Recording:
    """Create new recording entry."""
    new_recording = Recording(
        id=uuid4(),
        session_id=recording.session_id,
        filename=recording.filename,
        duration=recording.duration,
        file_size=recording.file_size,
        is_processed=False,
        created_at=datetime.utcnow().isoformat() + "Z",
        updated_at=datetime.utcnow().isoformat() + "Z",
    )
    MOCK_RECORDINGS.append(new_recording)
    return new_recording


@router.put("/{recording_id}", response_model=Recording)
async def update_recording(
    recording_id: UUID, recording_update: RecordingUpdate
) -> Recording:
    """Update recording."""
    for i, recording in enumerate(MOCK_RECORDINGS):
        if recording.id == recording_id:
            update_data = recording_update.dict(exclude_unset=True)
            updated_recording = recording.copy(update=update_data)
            MOCK_RECORDINGS[i] = updated_recording
            return updated_recording
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found"
    )


@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recording(recording_id: UUID) -> None:
    """Delete recording."""
    for i, recording in enumerate(MOCK_RECORDINGS):
        if recording.id == recording_id:
            del MOCK_RECORDINGS[i]
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found"
    )


@router.get("/{recording_id}/metadata", response_model=RecordingMetadata)
async def get_recording_metadata(recording_id: UUID) -> RecordingMetadata:
    """Get recording metadata."""
    recording = None
    for r in MOCK_RECORDINGS:
        if r.id == recording_id:
            recording = r
            break

    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found"
        )

    # Mock metadata
    return RecordingMetadata(
        recording_id=recording_id,
        session_info={
            "session_id": str(recording.session_id),
            "connection_name": "Production Server",
            "protocol": "SSH",
            "host": "192.168.1.100",
        },
        technical_details={
            "codec": "H.264",
            "resolution": "1920x1080",
            "fps": 30,
            "bitrate": "2000kbps",
        },
        quality_metrics={
            "video_quality": "high",
            "audio_quality": "high",
            "compression_ratio": 0.8,
        },
    )


@router.post("/{recording_id}/process")
async def process_recording(recording_id: UUID) -> dict[str, str]:
    """Start processing recording."""
    recording = None
    for r in MOCK_RECORDINGS:
        if r.id == recording_id:
            recording = r
            break

    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found"
        )

    if recording.is_processed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recording is already processed",
        )

    # Mock processing start
    return {"message": "Recording processing started", "status": "processing"}


@router.get("/download/{filename}")
async def download_recording(filename: str) -> dict[str, str]:
    """Download recording file."""
    # In real app, this would serve the actual file
    return {
        "message": f"Download link for {filename}",
        "download_url": f"/recordings/{filename}",
        "expires_at": "2024-01-02T00:00:00Z",
    }
