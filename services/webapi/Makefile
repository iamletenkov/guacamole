# Spacer WebAPI Development Makefile

.PHONY: help install dev-install lint format check test ci build push clean

# Variables
IMAGE_NAME := spacer-webapi
TAG := latest
DOCKERFILE := Dockerfile

# Default target
help: ## Show this help message
	@echo "Spacer WebAPI Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development setup
install: ## Install dependencies (including dev dependencies for CI)
	@echo "Installing dependencies..."
	/home/neadmin/.local/bin/poetry install --with dev

dev-install: ## Install development dependencies
	@echo "Installing development dependencies..."
	/home/neadmin/.local/bin/poetry install --with dev

# Code quality
lint: ## Run linting tools (ruff, flake8)
	@echo "Running linters..."
	/home/neadmin/.local/bin/poetry run ruff check .
	/home/neadmin/.local/bin/poetry run flake8 --extend-ignore=E203,E501 .

format: ## Format code (black, isort, ruff)
	@echo "Formatting code..."
	/home/neadmin/.local/bin/poetry run black .
	/home/neadmin/.local/bin/poetry run isort .
	/home/neadmin/.local/bin/poetry run ruff format .

check: ## Run type checking (mypy)
	@echo "Running type checking..."
	/home/neadmin/.local/bin/poetry run mypy --python-version=3.11 --config-file=pyproject.toml .

# Testing
test: ## Run tests
	@echo "Running tests..."
	/home/neadmin/.local/bin/poetry run pytest -v

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	/home/neadmin/.local/bin/poetry run pytest --cov=app --cov-report=html --cov-report=term

test-parallel: ## Run tests in parallel
	@echo "Running tests in parallel..."
	/home/neadmin/.local/bin/poetry run pytest -n auto

# CI pipeline
ci: ## Run full CI pipeline (install deps, lint, format, check, test)
	@echo "Installing dependencies..."
	/home/neadmin/.local/bin/poetry install --with dev
	@echo "Running linters..."
	/home/neadmin/.local/bin/poetry run ruff check .
	/home/neadmin/.local/bin/poetry run flake8 --extend-ignore=E203,E501 .
	@echo "Formatting code..."
	/home/neadmin/.local/bin/poetry run black .
	/home/neadmin/.local/bin/poetry run isort .
	/home/neadmin/.local/bin/poetry run ruff format .
	@echo "Running type checking..."
	/home/neadmin/.local/bin/poetry run mypy --python-version=3.11 --config-file=pyproject.toml .
	@echo "Running tests..."
	@if [ -n "$$DATABASE_URL" ]; then \
		echo "DATABASE_URL detected. Applying migrations and running full tests..."; \
		/home/neadmin/.local/bin/poetry run alembic upgrade head; \
		/home/neadmin/.local/bin/poetry run pytest -v; \
	else \
		echo "No DATABASE_URL. Running DB-less tests only (skipping integration)..."; \
		/home/neadmin/.local/bin/poetry run pytest -v -m "not integration" -k "not migrations"; \
	fi
	@echo "Full CI pipeline completed!"

# Docker commands
build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(TAG) -f $(DOCKERFILE) .

push: ## Push Docker image to registry
	@echo "Pushing Docker image..."
	docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):$(TAG)

pull: ## Pull latest image from registry
	@echo "Pulling latest image..."
	docker pull $(IMAGE_NAME):$(TAG)

# Development workflow
dev: ## Setup development environment
	@echo "Setting up development environment..."
	$(MAKE) dev-install
	pre-commit install

# Cleanup
clean: ## Clean up build artifacts and cache
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	docker system prune -f
