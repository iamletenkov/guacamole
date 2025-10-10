"""Sharing profiles endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.session import get_db
from app.models.guac.sharing_profile import GuacamoleSharingProfile  # noqa: TCH001
from app.repositories.sharing_profiles import SharingProfileRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter()

# Dependency injection
db_dependency = Depends(get_db)


class SharingProfileCreate(BaseModel):
    name: str
    primary_connection_id: int
    parameters: dict[str, str] | None = None


class SharingProfileOut(BaseModel):
    sharing_profile_id: int
    name: str
    primary_connection_id: int

    @staticmethod
    def from_model(m: GuacamoleSharingProfile) -> SharingProfileOut:
        return SharingProfileOut(
            sharing_profile_id=m.sharing_profile_id,
            name=m.sharing_profile_name,
            primary_connection_id=m.primary_connection_id,
        )


@router.post("/", response_model=SharingProfileOut, status_code=status.HTTP_201_CREATED)
def create_sharing_profile(
    payload: SharingProfileCreate, db: Session = db_dependency
) -> SharingProfileOut:
    repo = SharingProfileRepository(db)
    profile = repo.create_profile(
        name=payload.name,
        primary_connection_id=payload.primary_connection_id,
        parameters=payload.parameters,
    )
    db.commit()
    return SharingProfileOut.from_model(profile)


@router.get("/", response_model=List[SharingProfileOut])
def list_sharing_profiles(db: Session = db_dependency) -> List[SharingProfileOut]:
    repo = SharingProfileRepository(db)
    return [SharingProfileOut.from_model(x) for x in repo.list_profiles()]


@router.delete("/{sharing_profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sharing_profile(
    sharing_profile_id: int, db: Session = db_dependency
) -> None:
    repo = SharingProfileRepository(db)
    deleted = repo.delete_profile(sharing_profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sharing profile not found")
    db.commit()
