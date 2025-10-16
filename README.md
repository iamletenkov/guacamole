# Spacer

Modern containerized remote desktop management system based on Apache Guacamole.

## Architecture

This project provides a complete solution for managing remote desktop connections through Apache Guacamole with PostgreSQL backend and comprehensive session recording capabilities.

### Components

- **Apache Guacamole** - Remote desktop gateway with WebSocket support
- **Guacd** - Guacamole daemon for protocol handling (VNC, RDP, SSH, Telnet)
- **PostgreSQL** - Database for Guacamole configuration and user data
- **PgAdmin** - Web-based database management interface
- **Session Recordings** - Tomcat-based server for viewing recorded sessions
- **Nginx** - Reverse proxy with WebSocket support for Guacamole
- **Extensions** - Additional Guacamole authentication and functionality extensions

## Quick Start

1. **Deploy all services:**
   ```bash
   make deploy
   ```

2. **Access applications:**
   - **Guacamole Web Interface:** http://localhost/guacamole/
   - **Session Recordings:** http://localhost/recordings/
   - **PgAdmin:** http://localhost:8999

3. **View logs:**
   ```bash
   docker compose logs -f
   ```

## Features

- **Multi-Protocol Support:** VNC, RDP, SSH, Telnet connections
- **Session Recording:** Complete session capture and playback
- **Database Authentication:** PostgreSQL-backed user management
- **WebSocket Tunneling:** Native browser-based remote access
- **Load Balancing:** Nginx reverse proxy for scalability
- **Health Monitoring:** Built-in health checks for all services

## Project Structure

```
├── _data/                    # Persistent data volumes
│   ├── guacamole/           # Guacamole configuration and extensions
│   ├── guacd/               # Guacamole daemon data and recordings
│   ├── postgres/            # PostgreSQL data and initialization
│   └── tomcat/              # Tomcat configuration for recordings
├── docker-compose.yml       # Service orchestration
├── env_files/               # Environment configuration
│   ├── guacamole.env        # Guacamole settings
│   ├── pgadmin.env         # PgAdmin settings
│   └── postgres.env        # PostgreSQL settings
├── nginx/                   # Reverse proxy configuration
│   ├── nginx.conf           # Main Nginx configuration
│   └── conf.d/              # Site-specific configuration
└── Makefile                # Development and deployment commands
```

## Configuration

### Environment Variables

Key configuration files in `env_files/`:

- **PostgreSQL:** Database connection and initialization settings
- **Guacamole:** Authentication and guacd connection configuration
- **PgAdmin:** Admin interface access credentials

### Extensions

Available Guacamole extensions in `_data/guacamole/extensions/`:
- **guacamole-auth-jdbc** - Database authentication
- **guacamole-auth-quickconnect** - Quick connection templates
- **guacamole-auth-sso** - Single sign-on authentication
- **guacamole-display-statistics** - Connection statistics
- **guacamole-history-recording-storage** - Session recording storage

## Available Commands

```bash
make help          # Show all available commands
make pull          # Pull all Docker images
make deploy        # Deploy all services
make down          # Stop and remove all containers
make prune         # Clean up Docker system
```

## Default Access

- **Guacamole:** Access the web interface and configure connections through the administrative interface
- **PgAdmin:** Use the default credentials from `env_files/pgadmin.env` to manage the PostgreSQL database
- **Admin Setup:** The system automatically creates a `guacadmin` user during initialization

## Troubleshooting

1. **Check service health:**
   ```bash
   docker compose ps
   ```

2. **View service logs:**
   ```bash
   docker compose logs [service-name]
   ```

3. **Restart specific service:**
   ```bash
   docker compose restart [service-name]
   ```

## Contributing

1. **Make changes to configuration files as needed**
2. **Test deployment:** `make deploy`
3. **Verify functionality** across all services
4. **Document any new features or changes**