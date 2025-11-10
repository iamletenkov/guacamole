
DOCKER_STACK_NAME := guacamole
DOCKER_COMPOSE_FILE := docker-compose.yml
LOCAL_IP := $(shell hostname -I | cut -d' ' -f1)
HOSTNAME := $(shell hostname)

.PHONY: \
all \
pull \
deploy \
down \
prune \
help

all: pull deploy ## Pull and deploy all services

help: ## Show this help message
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

pull: ## Pull all images
	@echo "#######################################################"
	@echo "[step] pull"
	@echo "#######################################################"
	@echo "LOCAL_IP:           		$(LOCAL_IP)"
	@echo "HOSTNAME:           		$(HOSTNAME)"
	@echo "DOCKER_STACK_NAME:  		$(DOCKER_STACK_NAME)"
	@echo "DOCKER_COMPOSE_FILE:		$(DOCKER_COMPOSE_FILE)"
	COMPOSE_DOCKER_CLI_BUILD=1 \
	DOCKER_BUILDKIT=1 \
	HOSTNAME=$(HOSTNAME) \
	docker compose -f $(DOCKER_COMPOSE_FILE) -p "$(DOCKER_STACK_NAME)" pull

deploy: ## Deploy all services
	@echo "#######################################################"
	@echo "[step] deploy"
	@echo "#######################################################"
	@echo "LOCAL_IP:           		$(LOCAL_IP)"
	@echo "HOSTNAME:           		$(HOSTNAME)"
	@echo "DOCKER_STACK_NAME:  		$(DOCKER_STACK_NAME)"
	@echo "DOCKER_COMPOSE_FILE:		$(DOCKER_COMPOSE_FILE)"

	sudo mkdir -p _data/guacd/record
	sudo chown -R 1000:1001 _data/guacd/record
	sudo chmod -R 775 _data/guacd/record
	
	COMPOSE_DOCKER_CLI_BUILD=1 \
	DOCKER_BUILDKIT=1 \
	HOSTNAME=$(HOSTNAME) \
	docker compose -f $(DOCKER_COMPOSE_FILE) -p "$(DOCKER_STACK_NAME)" up -d

down: ## Stop and remove containers
	@echo "#######################################################"
	@echo "[step] down"
	@echo "#######################################################"
	@echo "LOCAL_IP:           		$(LOCAL_IP)"
	@echo "HOSTNAME:           		$(HOSTNAME)"
	@echo "DOCKER_STACK_NAME:  		$(DOCKER_STACK_NAME)"
	@echo "DOCKER_COMPOSE_FILE:		$(DOCKER_COMPOSE_FILE)"
	COMPOSE_DOCKER_CLI_BUILD=1 \
	DOCKER_BUILDKIT=1 \
	HOSTNAME=$(HOSTNAME) \
	docker compose -f $(DOCKER_COMPOSE_FILE) -p "$(DOCKER_STACK_NAME)" down --volumes

prune: ## Clean up Docker system
	@echo "#######################################################"
	@echo "[step] prune"
	@echo "#######################################################"
	@echo "LOCAL_IP:           		$(LOCAL_IP)"
	@echo "HOSTNAME:           		$(HOSTNAME)"
	@echo "DOCKER_STACK_NAME:  		$(DOCKER_STACK_NAME)"
	@echo "DOCKER_COMPOSE_FILE:		$(DOCKER_COMPOSE_FILE)"
	docker system prune -a -f

