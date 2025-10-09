# Spacer

Modern containerized workspace management system with Apache Guacamole integration.

## Architecture

This project provides a complete solution for managing remote desktop connections through Apache Guacamole with a modern REST API backend.

### Components

- **Apache Guacamole** - Remote desktop gateway
- **PostgreSQL** - Database for Guacamole and API data
- **PgAdmin** - Database management interface
- **WebAPI** - REST API for managing users, groups, connections, and permissions
- **Docker Compose** - Container orchestration

## Quick Start

1. **Start all services:**
   ```bash
   make deploy
   ```

2. **Access applications:**
   - Guacamole: http://localhost:8080/guacamole/
   - WebAPI: http://localhost:8001/docs (Swagger UI)
   - PgAdmin: http://localhost:8999

3. **View logs:**
   ```bash
   make logs
   ```

## Development

### WebAPI Development

For detailed WebAPI development documentation, see [services/webapi/README.md](services/webapi/README.md).

Run commands from the `services/webapi/` directory:
- `make install` - Install dependencies
- `make dev-install` - Install development dependencies
- `make ci` - Run full CI pipeline (lint, format, test, type check)
- `make build` - Build Docker image
- `make push` - Push Docker image

### Database Management

- **Migrations:** `cd services/webapi && alembic upgrade head`
- **Seed admin user:** Set `SEED_GUACADMIN=true` before running migrations

## Project Structure

```
├── services/
│   └── webapi/           # REST API service
│       ├── app/          # Application code
│       ├── alembic/      # Database migrations
│       ├── tests/        # Test suite
│       └── Dockerfile    # Container configuration
├── _data/               # Persistent data volumes
├── docker-compose.yml   # Service orchestration
└── Makefile            # Development commands
```

## API Documentation

- **WebAPI Swagger:** http://localhost:8001/docs
- **Guacamole:** http://localhost:8080/guacamole/

## Contributing

1. **WebAPI Development:**
   - Navigate to `services/webapi/`
   - Install dependencies: `make dev-install`
   - Run tests: `make test`
   - Check code quality: `make ci`
   - Build Docker image: `make build`

2. **Deploy:** `make deploy` (from project root)