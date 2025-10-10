"""Optional seed of default guacadmin user (controlled by SEED_GUACADMIN=true)

Revision ID: 0002_seed_guacadmin
Revises: 0001_init_guacamole_schema
Create Date: 2025-10-09
"""

from __future__ import annotations

import os

from alembic import op

revision = "0002_seed_guacadmin"
down_revision = "0001_init_guacamole_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if os.getenv("SEED_GUACADMIN", "").lower() not in ("1", "true", "yes"):  # skip
        return

    # Insert entity 'guacadmin' (USER)
    op.execute(
        """
        INSERT INTO guacamole_entity (name, type)
        VALUES ('guacadmin', 'USER')
        ON CONFLICT DO NOTHING;
    """
    )

    # Insert into guacamole_user with known salt/hash from official schema
    # password: 'guacadmin'
    op.execute(
        """
        INSERT INTO guacamole_user (
            entity_id, password_hash, password_salt, password_date,
            disabled, expired
        )
        SELECT
            e.entity_id,
            decode('CA458A7D494E3BE824F5E1E175A1556C0F8EEF2C2D7DF3633BEC4A29C4411960', 'hex'),
            decode('FE24ADC5E11E2B25288D1704ABE67A79E342ECC26064CE69C5B3177795A82264', 'hex'),
            CURRENT_TIMESTAMP,
            false,
            false
        FROM guacamole_entity e
        WHERE e.name = 'guacadmin' AND e.type = 'USER'
        ON CONFLICT (entity_id) DO NOTHING;
    """
    )

    # Grant system permissions to guacadmin
    op.execute(
        """
        INSERT INTO guacamole_system_permission (entity_id, permission)
        SELECT e.entity_id, p.permission::guacamole_system_permission_type
        FROM (
            VALUES
                ('CREATE_CONNECTION'),
                ('CREATE_CONNECTION_GROUP'),
                ('CREATE_SHARING_PROFILE'),
                ('CREATE_USER'),
                ('CREATE_USER_GROUP'),
                ('ADMINISTER')
        ) p(permission)
        JOIN guacamole_entity e ON e.name = 'guacadmin' AND e.type = 'USER'
        ON CONFLICT DO NOTHING;
    """
    )

    # Grant self permissions to guacadmin
    op.execute(
        """
        INSERT INTO guacamole_user_permission (entity_id, affected_user_id, permission)
        SELECT e.entity_id, u.user_id, p.permission::guacamole_object_permission_type
        FROM (
            VALUES ('READ'), ('UPDATE'), ('ADMINISTER')
        ) p(permission)
        JOIN guacamole_entity e ON e.name = 'guacadmin' AND e.type = 'USER'
        JOIN guacamole_user u ON u.entity_id = e.entity_id
        ON CONFLICT DO NOTHING;
    """
    )


def downgrade() -> None:
    # Remove permissions and user if seeded
    op.execute(
        """
        DELETE FROM guacamole_user_permission
        WHERE entity_id IN (SELECT entity_id FROM guacamole_entity WHERE name='guacadmin' AND type='USER');
    """
    )
    op.execute(
        """
        DELETE FROM guacamole_system_permission
        WHERE entity_id IN (SELECT entity_id FROM guacamole_entity WHERE name='guacadmin' AND type='USER');
    """
    )
    op.execute(
        """
        DELETE FROM guacamole_user
        WHERE entity_id IN (SELECT entity_id FROM guacamole_entity WHERE name='guacadmin' AND type='USER');
    """
    )
    op.execute(
        """
        DELETE FROM guacamole_entity WHERE name='guacadmin' AND type='USER';
    """
    )

