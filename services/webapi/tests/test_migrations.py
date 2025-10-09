"""Smoke tests for Alembic migrations and basic CRUD operations."""

from collections.abc import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.guac.entity import GuacamoleEntity
from app.models.guac.user import GuacamoleUser
from app.repositories.users import UserRepository
from app.security.passwords import GuacPasswordService

pytestmark = pytest.mark.integration


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Test database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_schema_tables_exist(db_session: Session) -> None:
    """Test that all expected tables exist with correct names."""
    # Check that key tables exist
    result = db_session.execute(
        text(
            """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name LIKE 'guacamole_%'
        ORDER BY table_name
    """
        )
    )
    tables = [row[0] for row in result.fetchall()]

    expected_tables = [
        "guacamole_connection",
        "guacamole_connection_attribute",
        "guacamole_connection_group",
        "guacamole_connection_group_attribute",
        "guacamole_connection_group_permission",
        "guacamole_connection_history",
        "guacamole_connection_parameter",
        "guacamole_connection_permission",
        "guacamole_entity",
        "guacamole_sharing_profile",
        "guacamole_sharing_profile_attribute",
        "guacamole_sharing_profile_parameter",
        "guacamole_sharing_profile_permission",
        "guacamole_system_permission",
        "guacamole_user",
        "guacamole_user_attribute",
        "guacamole_user_group",
        "guacamole_user_group_attribute",
        "guacamole_user_group_member",
        "guacamole_user_group_permission",
        "guacamole_user_history",
        "guacamole_user_password_history",
        "guacamole_user_permission",
    ]

    for table in expected_tables:
        assert table in tables, f"Table {table} not found"


def test_enums_exist(db_session: Session) -> None:
    """Test that all expected ENUMs exist."""
    result = db_session.execute(
        text(
            """
        SELECT typname
        FROM pg_type
        WHERE typtype = 'e'
        AND typname LIKE 'guacamole_%'
        ORDER BY typname
    """
        )
    )
    enums = [row[0] for row in result.fetchall()]

    expected_enums = [
        "guacamole_connection_group_type",
        "guacamole_entity_type",
        "guacamole_object_permission_type",
        "guacamole_proxy_encryption_method",
        "guacamole_system_permission_type",
    ]

    for enum_name in expected_enums:
        assert enum_name in enums, f"ENUM {enum_name} not found"


def test_user_crud_operations(db_session: Session) -> None:
    """Test basic user CRUD operations."""
    repo = UserRepository(db_session)

    # Create user
    user = repo.create_user("testuser", "testpass123")
    assert user.user_id is not None
    assert user.entity_id is not None

    # Verify entity was created
    entity = db_session.get(GuacamoleEntity, user.entity_id)
    assert entity is not None
    assert entity.name == "testuser"
    assert entity.type == "USER"

    # Test password verification
    passwords = GuacPasswordService()
    assert passwords.verify("testpass123", user.password_salt, user.password_hash)
    assert not passwords.verify("wrongpass", user.password_salt, user.password_hash)

    # Update password
    repo.set_password(user, "newpass456")
    db_session.commit()

    # Verify new password
    updated_user = db_session.get(GuacamoleUser, user.user_id)
    assert passwords.verify(
        "newpass456", updated_user.password_salt, updated_user.password_hash
    )

    # Delete user
    repo.delete_user(user)
    db_session.commit()

    # Verify deletion
    deleted_user = db_session.get(GuacamoleUser, user.user_id)
    assert deleted_user is None


def test_entity_constraints(db_session: Session) -> None:
    """Test that entity constraints work correctly."""
    # Create entity
    entity1 = GuacamoleEntity(name="testuser", type="USER")
    db_session.add(entity1)
    db_session.flush()

    # Try to create duplicate (should fail)
    entity2 = GuacamoleEntity(name="testuser", type="USER")
    db_session.add(entity2)

    with pytest.raises(Exception, match="integrity"):  # Should raise integrity error
        db_session.flush()

    db_session.rollback()


def test_foreign_key_constraints(db_session: Session) -> None:
    """Test that foreign key constraints work."""
    repo = UserRepository(db_session)

    # Create user (creates entity + user)
    user = repo.create_user("fk_test_user", "password123")
    db_session.commit()

    # Verify cascade delete works
    entity = db_session.get(GuacamoleEntity, user.entity_id)
    db_session.delete(entity)  # Should cascade to user
    db_session.commit()

    # User should be deleted
    deleted_user = db_session.get(GuacamoleUser, user.user_id)
    assert deleted_user is None
