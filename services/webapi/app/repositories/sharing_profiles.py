"""Repositories for Guacamole sharing profiles and parameters."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from app.models.guac.sharing_profile import GuacamoleSharingProfile
from app.models.guac.sharing_profile_parameter import GuacamoleSharingProfileParameter


class SharingProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_profile(
        self,
        name: str,
        primary_connection_id: int,
        parameters: dict[str, str] | None = None,
    ) -> GuacamoleSharingProfile:
        profile = GuacamoleSharingProfile(
            sharing_profile_name=name,
            primary_connection_id=primary_connection_id,
        )
        self.db.add(profile)
        self.db.flush()

        if parameters:
            for k, v in parameters.items():
                self.set_parameter(profile.sharing_profile_id, k, v)
        return profile

    def set_parameter(self, sharing_profile_id: int, name: str, value: str) -> None:
        param = self.db.get(
            GuacamoleSharingProfileParameter,
            {"sharing_profile_id": sharing_profile_id, "parameter_name": name},
        )
        if param is None:
            param = GuacamoleSharingProfileParameter(
                sharing_profile_id=sharing_profile_id,
                parameter_name=name,
                parameter_value=value,
            )
            self.db.add(param)
        else:
            param.parameter_value = value

    def list_profiles(self) -> list[GuacamoleSharingProfile]:
        stmt = select(GuacamoleSharingProfile)
        return list(self.db.scalars(stmt))

    def delete_profile(self, sharing_profile_id: int) -> int:
        profile = self.db.get(GuacamoleSharingProfile, sharing_profile_id)
        if not profile:
            return 0
        self.db.delete(profile)
        return 1
