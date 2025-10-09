"""Repositories for Guacamole connections and groups."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from app.models.guac.connection import GuacamoleConnection
from app.models.guac.connection_group import GuacamoleConnectionGroup
from app.models.guac.connection_parameter import GuacamoleConnectionParameter


class ConnectionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Connection groups
    def create_group(
        self,
        name: str,
        parent_id: int | None = None,
        group_type: str = "ORGANIZATIONAL",
        max_connections: int | None = None,
        max_connections_per_user: int | None = None,
        enable_session_affinity: bool | None = None,
    ) -> GuacamoleConnectionGroup:
        group = GuacamoleConnectionGroup(
            connection_group_name=name,
            parent_id=parent_id,
            type=group_type,
            max_connections=max_connections,
            max_connections_per_user=max_connections_per_user,
            enable_session_affinity=enable_session_affinity or False,
        )
        self.db.add(group)
        self.db.flush()
        return group

    def list_groups(
        self, parent_id: int | None = None
    ) -> list[GuacamoleConnectionGroup]:
        stmt = select(GuacamoleConnectionGroup)
        if parent_id is not None:
            stmt = stmt.where(GuacamoleConnectionGroup.parent_id == parent_id)
        return list(self.db.scalars(stmt))

    def delete_group(self, group_id: int) -> int:
        grp = self.db.get(GuacamoleConnectionGroup, group_id)
        if not grp:
            return 0
        self.db.delete(grp)
        return 1

    # Connections
    def create_connection(
        self,
        name: str,
        protocol: str,
        parent_group_id: int | None = None,
        max_connections: int | None = None,
        max_connections_per_user: int | None = None,
        proxy_port: int | None = None,
        proxy_hostname: str | None = None,
        proxy_encryption_method: str | None = None,
        parameters: dict[str, str] | None = None,
    ) -> GuacamoleConnection:
        conn = GuacamoleConnection(
            connection_name=name,
            protocol=protocol,
            parent_id=parent_group_id,
            max_connections=max_connections,
            max_connections_per_user=max_connections_per_user,
            proxy_port=proxy_port,
            proxy_hostname=proxy_hostname,
            proxy_encryption_method=proxy_encryption_method,
        )
        self.db.add(conn)
        self.db.flush()

        if parameters:
            for k, v in parameters.items():
                self.set_parameter(conn.connection_id, k, v)
        return conn

    def set_parameter(self, connection_id: int, name: str, value: str) -> None:
        param = self.db.get(
            GuacamoleConnectionParameter,
            {"connection_id": connection_id, "parameter_name": name},
        )
        if param is None:
            param = GuacamoleConnectionParameter(
                connection_id=connection_id, parameter_name=name, parameter_value=value
            )
            self.db.add(param)
        else:
            param.parameter_value = value

    def list_connections(
        self, parent_group_id: int | None = None
    ) -> list[GuacamoleConnection]:
        stmt = select(GuacamoleConnection)
        if parent_group_id is not None:
            stmt = stmt.where(GuacamoleConnection.parent_id == parent_group_id)
        return list(self.db.scalars(stmt))

    def delete_connection(self, connection_id: int) -> int:
        conn = self.db.get(GuacamoleConnection, connection_id)
        if not conn:
            return 0
        self.db.delete(conn)
        return 1
