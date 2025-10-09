"""PostgreSQL ENUM types matching Guacamole names exactly."""

from __future__ import annotations

from sqlalchemy.dialects.postgresql import ENUM as PGEnum

# Define Python-level ENUM objects (creation handled in Alembic for exact control)

guacamole_connection_group_type = PGEnum(
    "ORGANIZATIONAL",
    "BALANCING",
    name="guacamole_connection_group_type",
)

guacamole_entity_type = PGEnum(
    "USER",
    "USER_GROUP",
    name="guacamole_entity_type",
)

guacamole_object_permission_type = PGEnum(
    "READ",
    "UPDATE",
    "DELETE",
    "ADMINISTER",
    name="guacamole_object_permission_type",
)

guacamole_system_permission_type = PGEnum(
    "CREATE_CONNECTION",
    "CREATE_CONNECTION_GROUP",
    "CREATE_SHARING_PROFILE",
    "CREATE_USER",
    "CREATE_USER_GROUP",
    "ADMINISTER",
    name="guacamole_system_permission_type",
)

guacamole_proxy_encryption_method = PGEnum(
    "NONE",
    "SSL",
    name="guacamole_proxy_encryption_method",
)
