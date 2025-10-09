<!-- 9bfd2ee6-ab48-4381-8f65-7dbc473ee41e 395a4e8f-a154-4af2-8bb1-3c90b8a52d56 -->
# Guacamole-compatible DB via SQLAlchemy/Alembic

## Scope

- Recreate the full Guacamole schema in Postgres using SQLAlchemy models and Alembic migrations, 1:1 with 01_create_guacamole_db.sql (same table/type/index/constraint names and semantics).
- Implement Guacamole-compatible password hashing and user management.
- Provide REST endpoints to manage users, user groups, connections, connection groups, sharing profiles, parameters, attributes, and permissions (grant/revoke).

## Key Design Decisions

- Names: Keep exact table, column, enum type, index, and constraint names as in SQL to ensure Guacamole works unmodified.
- Enums: Use PostgreSQL native enums with explicit names (e.g., `guacamole_entity_type`).
- FKs & ON DELETE: Mirror behaviors (CASCADE/SET NULL) exactly.
- Seeding: Optional creation of default `guacadmin` with the same salt+hash as in SQL (toggle via env `SEED_GUACADMIN=true`).
- Passwords: Port Guacamole’s algorithm precisely (bytea salt/hash) and add tests validating the given hex samples.

## Files to Add

- `services/webapi/app/db/session.py`: SQLAlchemy engine/session, Alembic config hook.
- `services/webapi/app/db/base.py`: Base metadata import aggregator.
- `services/webapi/alembic.ini` + `services/webapi/alembic/` (env.py, versions/…): Alembic setup.
- `services/webapi/app/models/guac/*.py`: SQLAlchemy models, exact names:
  - `entity.py` → `guacamole_entity`
  - `user.py` → `guacamole_user`
  - `user_group.py` → `guacamole_user_group`
  - `user_group_member.py` → `guacamole_user_group_member`
  - `connection_group.py` → `guacamole_connection_group`
  - `connection.py` → `guacamole_connection`
  - `connection_parameter.py` → `guacamole_connection_parameter`
  - `sharing_profile.py` → `guacamole_sharing_profile`
  - `sharing_profile_parameter.py` → `guacamole_sharing_profile_parameter`
  - `attributes.py` (user, user_group, connection, connection_group)
  - `permissions.py` (connection, connection_group, sharing_profile, user, user_group, system)
  - `history.py` (connection_history, user_history, user_password_history)
  - `enums.py` (Postgres enums with exact names)
- `services/webapi/app/security/passwords.py`: Guacamole hashing (salt gen, hash, verify) matching Java implementation.
- `services/webapi/app/repositories/*.py`: CRUD operations encapsulating DB logic.
- `services/webapi/app/api/v1/endpoints/` additions: CRUD + grant/revoke endpoints.
- `services/webapi/tests/` minimal tests to verify schema & hashing compatibility.

## Migrations (Alembic)

- Migration 1: Create Postgres enums in exact order/names.
- Migration 2: Create tables with exact names/columns/defaults and constraints.
- Migration 3: Create indexes with exact names.
- Migration 4 (optional seed): Insert `guacadmin` using provided hex salt/hash when `SEED_GUACADMIN=true`.

## Critical Implementation Notes

- Use `sqlalchemy.dialects.postgresql.ENUM(..., name='guacamole_entity_type', create_type=False)` and create via Alembic op.create_enum to control type names.
- Explicit constraint and index names via `UniqueConstraint(name=...)`, `ForeignKey(..., name=..., ondelete='CASCADE')`, `Index('guacamole_connection_parent_id', ...)`.
- Maintain invariants: create `guacamole_entity` first, then `guacamole_user`/`guacamole_user_group` with 1:1 mapping.
- Passwords: implement exact salt+hash and test equality against known values from SQL file.

## Example Snippets

- Enum (model-layer reference only):
```python
# services/webapi/app/models/guac/enums.py
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy import MetaData

guacamole_entity_type = pg.ENUM('USER', 'USER_GROUP', name='guacamole_entity_type')
```

- Model with exact names:
```python
# services/webapi/app/models/guac/entity.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
from .enums import guacamole_entity_type

Base = declarative_base()

class GuacamoleEntity(Base):
    __tablename__ = 'guacamole_entity'
    entity_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(guacamole_entity_type, nullable=False)
    __table_args__ = (
        UniqueConstraint('type', 'name', name='guacamole_entity_name_scope'),
    )
```

- Password hashing adapter (API signature):
```python
# services/webapi/app/security/passwords.py
class GuacPasswordService:
    def hash_password(self, password: str) -> tuple[bytes, bytes]: ...  # returns (salt, hash)
    def verify(self, password: str, salt: bytes, password_hash: bytes) -> bool: ...
```


## Endpoints (high level)

- Users: create/update/delete, set password, get by name, list.
- User groups: create/update/delete, add/remove members, list.
- Connections: CRUD, parameters CRUD.
- Connection groups: CRUD.
- Sharing profiles: CRUD, parameters CRUD.
- Attributes: CRUD per scope.
- Permissions: grant/revoke/query for entity vs resource.
- History: read-only list/filter.

## Testing

- Hashing unit test: matches provided hex for `guacadmin`.
- Migration test: metadata compare with expected names.
- Endpoint smoke tests for CRUD and permissions.

### To-dos

- [x] Initialize Alembic in services/webapi and configure Postgres URL from settings
- [x] Create Alembic migration to define Postgres enums with exact names
- [x] Add Alembic migration to create all tables with exact constraints and indexes
- [x] Add optional seed for guacadmin user guarded by env flag
- [x] Implement SQLAlchemy models with exact names matching Guacamole SQL
- [x] Implement Guacamole-compatible password hashing and verification
- [x] Add repository classes for entities, users, groups, connections, permissions
- [x] Implement users and user-groups endpoints including set-password and membership
- [x] Implement connections, groups, sharing profiles, parameters endpoints
- [x] Implement grant/revoke/query permissions endpoints
- [x] Implement attributes (CRUD) and history read endpoints
- [x] Add tests asserting hashing matches known Guacamole values
- [x] Add migrations smoke tests and basic CRUD tests


