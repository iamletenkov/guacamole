# Spacer Web API

Modern FastAPI-based web service for the Spacer project with Guacamole-compatible database schema.

## Features

- **FastAPI** with automatic OpenAPI documentation
- **Guacamole-compatible** PostgreSQL schema (1:1 with Apache Guacamole)
- **Poetry** for dependency management
- **SQLAlchemy** with Alembic migrations
- **Comprehensive testing** suite
- **Pre-commit hooks** for code quality
- **Docker** support with multi-stage builds
- **Type hints** throughout the codebase
- **Modern Python** (3.14) features

## Development Setup

### Prerequisites

- **Python 3.14+**
- **Poetry** (for dependency management)
- **Docker & Docker Compose** (for containerized development)
- **PostgreSQL** (for database)

### Quick Start

1. **Setup development environment:**
   ```bash
   cd services/webapi
   ./setup.sh
   ```

2. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Start development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **View API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Available Commands

#### Development Workflow
- `make install` - Install dependencies
- `make dev-install` - Install development dependencies
- `make lint` - Run linting tools (ruff, flake8)
- `make format` - Format code (black, isort, ruff)
- `make check` - Run type checking (mypy)
- `make test` - Run tests
- `make ci` - Run full CI pipeline

#### Docker Commands
- `make build` - Build Docker image
- `make push` - Push Docker image to registry

### Code Quality Tools

The project uses a comprehensive set of code quality tools:

- **Ruff** - Fast Python linter and formatter
- **Black** - Code formatter
- **isort** - Import sorter
- **MyPy** - Static type checker
- **Flake8** - Style guide enforcement
- **Pre-commit** - Git hooks for automated quality checks
- **Pytest** - Testing framework with parallel execution

### Project Structure

```
services/webapi/
├── app/                    # Main application code
│   ├── api/v1/            # API endpoints
│   ├── core/              # Core configuration and middleware
│   ├── db/                # Database session and base
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   └── security/          # Authentication and security
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── Dockerfile             # Container configuration
├── pyproject.toml         # Project dependencies and configuration
├── .pre-commit-config.yaml # Pre-commit hooks configuration
└── Makefile              # Development commands
```

### API Endpoints

Once running, the API provides endpoints for:

- **Authentication** (`/api/v1/auth/`) - Login/logout/token management
- **Users** (`/api/v1/users/`) - User management with password setting
- **User Groups** (`/api/v1/groups/`) - Group management and membership
- **Connections** (`/api/v1/connections/`) - Connection and connection group management
- **Permissions** (`/api/v1/permissions/`) - Grant/revoke permissions for all resource types
- **Sharing Profiles** (`/api/v1/sharing-profiles/`) - Sharing profile management
- **Attributes** (`/api/v1/attributes/`) - CRUD operations for user/group/connection attributes
- **History** (`/api/v1/history/`) - Read-only access to connection and user history

All endpoints are fully documented with OpenAPI/Swagger at `/docs`.
