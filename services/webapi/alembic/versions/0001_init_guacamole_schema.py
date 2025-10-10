"""Initialize Guacamole-compatible schema (enums, tables, indexes)

Revision ID: 0001_init_guacamole_schema
Revises:
Create Date: 2025-10-09
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

# from sqlalchemy.dialects import postgresql as pg  # noqa: F401


# revision identifiers, used by Alembic.
revision = "0001_init_guacamole_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enums (create safely if not exists)
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE guacamole_connection_group_type AS ENUM ('ORGANIZATIONAL', 'BALANCING');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END$$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE guacamole_entity_type AS ENUM ('USER', 'USER_GROUP');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END$$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE guacamole_object_permission_type AS ENUM ('READ','UPDATE','DELETE','ADMINISTER');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END$$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE guacamole_system_permission_type AS ENUM ('CREATE_CONNECTION','CREATE_CONNECTION_GROUP','CREATE_SHARING_PROFILE','CREATE_USER','CREATE_USER_GROUP','ADMINISTER');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END$$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE guacamole_proxy_encryption_method AS ENUM ('NONE','SSL');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END$$;
        """
    )

    # Tables
    op.create_table(
        "guacamole_connection_group",
        sa.Column(
            "connection_group_id", sa.Integer(), primary_key=True, nullable=False
        ),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("connection_group_name", sa.String(128), nullable=False),
        sa.Column(
            "type",
            PGEnum(
                "ORGANIZATIONAL",
                "BALANCING",
                name="guacamole_connection_group_type",
                create_type=False,
            ),
            nullable=False,
            server_default="ORGANIZATIONAL",
        ),
        sa.Column("max_connections", sa.Integer(), nullable=True),
        sa.Column("max_connections_per_user", sa.Integer(), nullable=True),
        sa.Column(
            "enable_session_affinity",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.create_table(
        "guacamole_connection",
        sa.Column("connection_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("connection_name", sa.String(128), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("protocol", sa.String(32), nullable=False),
        sa.Column("max_connections", sa.Integer(), nullable=True),
        sa.Column("max_connections_per_user", sa.Integer(), nullable=True),
        sa.Column("connection_weight", sa.Integer(), nullable=True),
        sa.Column(
            "failover_only",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("proxy_port", sa.Integer(), nullable=True),
        sa.Column("proxy_hostname", sa.String(512), nullable=True),
        sa.Column(
            "proxy_encryption_method",
            PGEnum(
                "NONE",
                "SSL",
                name="guacamole_proxy_encryption_method",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    # FK for connection_group parent, and connection.parent -> connection_group
    op.create_foreign_key(
        "guacamole_connection_group_ibfk_1",
        source_table="guacamole_connection_group",
        referent_table="guacamole_connection_group",
        local_cols=["parent_id"],
        remote_cols=["connection_group_id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "guacamole_connection_ibfk_1",
        source_table="guacamole_connection",
        referent_table="guacamole_connection_group",
        local_cols=["parent_id"],
        remote_cols=["connection_group_id"],
        ondelete="CASCADE",
    )

    # Uniques
    op.create_unique_constraint(
        "connection_group_name_parent",
        "guacamole_connection_group",
        ["connection_group_name", "parent_id"],
    )
    op.create_unique_constraint(
        "connection_name_parent",
        "guacamole_connection",
        ["connection_name", "parent_id"],
    )

    # Indexes
    op.create_index(
        "guacamole_connection_group_parent_id",
        "guacamole_connection_group",
        ["parent_id"],
    )
    op.create_index(
        "guacamole_connection_parent_id",
        "guacamole_connection",
        ["parent_id"],
    )

    # Entities and users/groups
    op.create_table(
        "guacamole_entity",
        sa.Column("entity_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column(
            "type",
            PGEnum(
                "USER",
                "USER_GROUP",
                name="guacamole_entity_type",
                create_type=False,
            ),
            nullable=False,
        ),
    )
    op.create_unique_constraint(
        "guacamole_entity_name_scope", "guacamole_entity", ["type", "name"]
    )

    op.create_table(
        "guacamole_user",
        sa.Column("user_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("password_hash", sa.LargeBinary(), nullable=False),
        sa.Column("password_salt", sa.LargeBinary(), nullable=True),
        sa.Column("password_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "disabled", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column(
            "expired", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("access_window_start", sa.Time(), nullable=True),
        sa.Column("access_window_end", sa.Time(), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column("timezone", sa.String(64), nullable=True),
        sa.Column("full_name", sa.String(256), nullable=True),
        sa.Column("email_address", sa.String(256), nullable=True),
        sa.Column("organization", sa.String(256), nullable=True),
        sa.Column("organizational_role", sa.String(256), nullable=True),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(256), nullable=True),
        sa.Column("last_name", sa.String(256), nullable=True),
    )
    op.create_foreign_key(
        "guacamole_user_entity",
        "guacamole_user",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )

    op.create_table(
        "guacamole_user_group",
        sa.Column("user_group_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False, unique=True),
        sa.Column(
            "disabled", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.create_foreign_key(
        "guacamole_user_group_entity",
        "guacamole_user_group",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )

    op.create_table(
        "guacamole_user_group_member",
        sa.Column("user_group_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("member_entity_id", sa.Integer(), primary_key=True, nullable=False),
    )
    op.create_foreign_key(
        "guacamole_user_group_member_parent",
        "guacamole_user_group_member",
        "guacamole_user_group",
        ["user_group_id"],
        ["user_group_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_user_group_member_entity",
        "guacamole_user_group_member",
        "guacamole_entity",
        ["member_entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )

    # Connection parameters
    op.create_table(
        "guacamole_connection_parameter",
        sa.Column("connection_id", sa.Integer(), nullable=False),
        sa.Column("parameter_name", sa.String(128), nullable=False),
        sa.Column("parameter_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("connection_id", "parameter_name"),
    )
    op.create_foreign_key(
        "guacamole_connection_parameter_ibfk_1",
        "guacamole_connection_parameter",
        "guacamole_connection",
        ["connection_id"],
        ["connection_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_connection_parameter_connection_id",
        "guacamole_connection_parameter",
        ["connection_id"],
    )

    # Sharing profiles and parameters
    op.create_table(
        "guacamole_sharing_profile",
        sa.Column("sharing_profile_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("sharing_profile_name", sa.String(128), nullable=False),
        sa.Column("primary_connection_id", sa.Integer(), nullable=False),
    )
    op.create_unique_constraint(
        "sharing_profile_name_primary",
        "guacamole_sharing_profile",
        ["sharing_profile_name", "primary_connection_id"],
    )
    op.create_foreign_key(
        "guacamole_sharing_profile_ibfk_1",
        "guacamole_sharing_profile",
        "guacamole_connection",
        ["primary_connection_id"],
        ["connection_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_sharing_profile_primary_connection_id",
        "guacamole_sharing_profile",
        ["primary_connection_id"],
    )

    op.create_table(
        "guacamole_sharing_profile_parameter",
        sa.Column("sharing_profile_id", sa.Integer(), nullable=False),
        sa.Column("parameter_name", sa.String(128), nullable=False),
        sa.Column("parameter_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("sharing_profile_id", "parameter_name"),
    )
    op.create_foreign_key(
        "guacamole_sharing_profile_parameter_ibfk_1",
        "guacamole_sharing_profile_parameter",
        "guacamole_sharing_profile",
        ["sharing_profile_id"],
        ["sharing_profile_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_sharing_profile_parameter_sharing_profile_id",
        "guacamole_sharing_profile_parameter",
        ["sharing_profile_id"],
    )

    # Attributes
    op.create_table(
        "guacamole_user_attribute",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("attribute_name", sa.String(128), nullable=False),
        sa.Column("attribute_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "attribute_name"),
    )
    op.create_foreign_key(
        "guacamole_user_attribute_ibfk_1",
        "guacamole_user_attribute",
        "guacamole_user",
        ["user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_user_attribute_user_id",
        "guacamole_user_attribute",
        ["user_id"],
    )

    op.create_table(
        "guacamole_user_group_attribute",
        sa.Column("user_group_id", sa.Integer(), nullable=False),
        sa.Column("attribute_name", sa.String(128), nullable=False),
        sa.Column("attribute_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("user_group_id", "attribute_name"),
    )
    op.create_foreign_key(
        "guacamole_user_group_attribute_ibfk_1",
        "guacamole_user_group_attribute",
        "guacamole_user_group",
        ["user_group_id"],
        ["user_group_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_user_group_attribute_user_group_id",
        "guacamole_user_group_attribute",
        ["user_group_id"],
    )

    op.create_table(
        "guacamole_connection_attribute",
        sa.Column("connection_id", sa.Integer(), nullable=False),
        sa.Column("attribute_name", sa.String(128), nullable=False),
        sa.Column("attribute_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("connection_id", "attribute_name"),
    )
    op.create_foreign_key(
        "guacamole_connection_attribute_ibfk_1",
        "guacamole_connection_attribute",
        "guacamole_connection",
        ["connection_id"],
        ["connection_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_connection_attribute_connection_id",
        "guacamole_connection_attribute",
        ["connection_id"],
    )

    op.create_table(
        "guacamole_connection_group_attribute",
        sa.Column("connection_group_id", sa.Integer(), nullable=False),
        sa.Column("attribute_name", sa.String(128), nullable=False),
        sa.Column("attribute_value", sa.String(4096), nullable=False),
        sa.PrimaryKeyConstraint("connection_group_id", "attribute_name"),
    )
    op.create_foreign_key(
        "guacamole_connection_group_attribute_ibfk_1",
        "guacamole_connection_group_attribute",
        "guacamole_connection_group",
        ["connection_group_id"],
        ["connection_group_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_connection_group_attribute_connection_group_id",
        "guacamole_connection_group_attribute",
        ["connection_group_id"],
    )

    # Permissions
    op.create_table(
        "guacamole_connection_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("connection_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "READ",
                "UPDATE",
                "DELETE",
                "ADMINISTER",
                name="guacamole_object_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "connection_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_connection_permission_ibfk_1",
        "guacamole_connection_permission",
        "guacamole_connection",
        ["connection_id"],
        ["connection_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_connection_permission_entity",
        "guacamole_connection_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_connection_permission_connection_id",
        "guacamole_connection_permission",
        ["connection_id"],
    )
    op.create_index(
        "guacamole_connection_permission_entity_id",
        "guacamole_connection_permission",
        ["entity_id"],
    )

    op.create_table(
        "guacamole_connection_group_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("connection_group_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "READ",
                "UPDATE",
                "DELETE",
                "ADMINISTER",
                name="guacamole_object_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "connection_group_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_connection_group_permission_ibfk_1",
        "guacamole_connection_group_permission",
        "guacamole_connection_group",
        ["connection_group_id"],
        ["connection_group_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_connection_group_permission_entity",
        "guacamole_connection_group_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_connection_group_permission_connection_group_id",
        "guacamole_connection_group_permission",
        ["connection_group_id"],
    )
    op.create_index(
        "guacamole_connection_group_permission_entity_id",
        "guacamole_connection_group_permission",
        ["entity_id"],
    )

    op.create_table(
        "guacamole_sharing_profile_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("sharing_profile_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "READ",
                "UPDATE",
                "DELETE",
                "ADMINISTER",
                name="guacamole_object_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "sharing_profile_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_sharing_profile_permission_ibfk_1",
        "guacamole_sharing_profile_permission",
        "guacamole_sharing_profile",
        ["sharing_profile_id"],
        ["sharing_profile_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_sharing_profile_permission_entity",
        "guacamole_sharing_profile_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_sharing_profile_permission_sharing_profile_id",
        "guacamole_sharing_profile_permission",
        ["sharing_profile_id"],
    )
    op.create_index(
        "guacamole_sharing_profile_permission_entity_id",
        "guacamole_sharing_profile_permission",
        ["entity_id"],
    )

    op.create_table(
        "guacamole_user_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("affected_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "READ",
                "UPDATE",
                "DELETE",
                "ADMINISTER",
                name="guacamole_object_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "affected_user_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_user_permission_ibfk_1",
        "guacamole_user_permission",
        "guacamole_user",
        ["affected_user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_user_permission_entity",
        "guacamole_user_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_user_permission_affected_user_id",
        "guacamole_user_permission",
        ["affected_user_id"],
    )
    op.create_index(
        "guacamole_user_permission_entity_id",
        "guacamole_user_permission",
        ["entity_id"],
    )

    op.create_table(
        "guacamole_user_group_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("affected_user_group_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "READ",
                "UPDATE",
                "DELETE",
                "ADMINISTER",
                name="guacamole_object_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "affected_user_group_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_user_group_permission_affected_user_group",
        "guacamole_user_group_permission",
        "guacamole_user_group",
        ["affected_user_group_id"],
        ["user_group_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "guacamole_user_group_permission_entity",
        "guacamole_user_group_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_user_group_permission_affected_user_group_id",
        "guacamole_user_group_permission",
        ["affected_user_group_id"],
    )
    op.create_index(
        "guacamole_user_group_permission_entity_id",
        "guacamole_user_group_permission",
        ["entity_id"],
    )

    op.create_table(
        "guacamole_system_permission",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column(
            "permission",
            PGEnum(
                "CREATE_CONNECTION",
                "CREATE_CONNECTION_GROUP",
                "CREATE_SHARING_PROFILE",
                "CREATE_USER",
                "CREATE_USER_GROUP",
                "ADMINISTER",
                name="guacamole_system_permission_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id", "permission"),
    )
    op.create_foreign_key(
        "guacamole_system_permission_entity",
        "guacamole_system_permission",
        "guacamole_entity",
        ["entity_id"],
        ["entity_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_system_permission_entity_id",
        "guacamole_system_permission",
        ["entity_id"],
    )

    # History tables
    op.create_table(
        "guacamole_connection_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(128), nullable=False),
        sa.Column("remote_host", sa.String(256), nullable=True),
        sa.Column("connection_id", sa.Integer(), nullable=True),
        sa.Column("connection_name", sa.String(128), nullable=False),
        sa.Column("sharing_profile_id", sa.Integer(), nullable=True),
        sa.Column("sharing_profile_name", sa.String(128), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "guacamole_connection_history_ibfk_1",
        "guacamole_connection_history",
        "guacamole_user",
        ["user_id"],
        ["user_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "guacamole_connection_history_ibfk_2",
        "guacamole_connection_history",
        "guacamole_connection",
        ["connection_id"],
        ["connection_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "guacamole_connection_history_ibfk_3",
        "guacamole_connection_history",
        "guacamole_sharing_profile",
        ["sharing_profile_id"],
        ["sharing_profile_id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "guacamole_connection_history_user_id",
        "guacamole_connection_history",
        ["user_id"],
    )
    op.create_index(
        "guacamole_connection_history_connection_id",
        "guacamole_connection_history",
        ["connection_id"],
    )
    op.create_index(
        "guacamole_connection_history_sharing_profile_id",
        "guacamole_connection_history",
        ["sharing_profile_id"],
    )
    op.create_index(
        "guacamole_connection_history_start_date",
        "guacamole_connection_history",
        ["start_date"],
    )
    op.create_index(
        "guacamole_connection_history_end_date",
        "guacamole_connection_history",
        ["end_date"],
    )
    op.create_index(
        "guacamole_connection_history_connection_id_start_date",
        "guacamole_connection_history",
        ["connection_id", "start_date"],
    )

    op.create_table(
        "guacamole_user_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(128), nullable=False),
        sa.Column("remote_host", sa.String(256), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "guacamole_user_history_ibfk_1",
        "guacamole_user_history",
        "guacamole_user",
        ["user_id"],
        ["user_id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "guacamole_user_history_user_id",
        "guacamole_user_history",
        ["user_id"],
    )
    op.create_index(
        "guacamole_user_history_start_date",
        "guacamole_user_history",
        ["start_date"],
    )
    op.create_index(
        "guacamole_user_history_end_date",
        "guacamole_user_history",
        ["end_date"],
    )
    op.create_index(
        "guacamole_user_history_user_id_start_date",
        "guacamole_user_history",
        ["user_id", "start_date"],
    )

    op.create_table(
        "guacamole_user_password_history",
        sa.Column(
            "password_history_id", sa.Integer(), primary_key=True, nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("password_hash", sa.LargeBinary(), nullable=False),
        sa.Column("password_salt", sa.LargeBinary(), nullable=True),
        sa.Column("password_date", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_foreign_key(
        "guacamole_user_password_history_ibfk_1",
        "guacamole_user_password_history",
        "guacamole_user",
        ["user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "guacamole_user_password_history_user_id",
        "guacamole_user_password_history",
        ["user_id"],
    )


def downgrade() -> None:
    # Drop in reverse dependency order
    op.drop_table("guacamole_user_password_history")
    op.drop_table("guacamole_user_history")
    op.drop_table("guacamole_connection_history")

    op.drop_table("guacamole_system_permission")
    op.drop_table("guacamole_user_group_permission")
    op.drop_table("guacamole_user_permission")
    op.drop_table("guacamole_sharing_profile_permission")
    op.drop_table("guacamole_connection_group_permission")
    op.drop_table("guacamole_connection_permission")

    op.drop_table("guacamole_connection_group_attribute")
    op.drop_table("guacamole_connection_attribute")
    op.drop_table("guacamole_user_group_attribute")
    op.drop_table("guacamole_user_attribute")

    op.drop_table("guacamole_sharing_profile_parameter")
    op.drop_table("guacamole_sharing_profile")
    op.drop_table("guacamole_connection_parameter")

    op.drop_table("guacamole_user_group_member")
    op.drop_table("guacamole_user_group")
    op.drop_table("guacamole_user")
    op.drop_table("guacamole_entity")

    op.drop_constraint(
        "guacamole_connection_ibfk_1", "guacamole_connection", type_="foreignkey"
    )
    op.drop_table("guacamole_connection")
    op.drop_constraint(
        "guacamole_connection_group_ibfk_1",
        "guacamole_connection_group",
        type_="foreignkey",
    )
    op.drop_table("guacamole_connection_group")

    # Enums
    for t in (
        "guacamole_proxy_encryption_method",
        "guacamole_system_permission_type",
        "guacamole_object_permission_type",
        "guacamole_entity_type",
        "guacamole_connection_group_type",
    ):
        op.execute(f"DROP TYPE IF EXISTS {t}")
