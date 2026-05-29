# ============================================================================
# CourseDB-AI: developer task runner
# ----------------------------------------------------------------------------
# Convenience wrapper around docker-compose, alembic, pytest and the linters.
# Run `make help` for a list of available targets.
# ============================================================================

.DEFAULT_GOAL := help
SHELL := /bin/bash

# Load variables from .env if present (DATABASE_URL, POSTGRES_*, etc.)
ifneq (,$(wildcard .env))
include .env
export
endif

PYTHON ?= python
PIP ?= pip
COMPOSE ?= docker compose

.PHONY: help install up down logs psql migrate revision seed embed \
        smoke run lint format test cov ci

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	$(PIP) install -r requirements.txt

up: ## Start the Postgres + pgvector container
	$(COMPOSE) up -d

down: ## Stop and remove containers
	$(COMPOSE) down

logs: ## Tail container logs
	$(COMPOSE) logs -f

psql: ## Open a psql shell in the running container
	$(COMPOSE) exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

migrate: ## Apply all Alembic migrations
	alembic upgrade head

revision: ## Autogenerate a new migration (usage: make revision m="message")
	alembic revision --autogenerate -m "$(m)"

seed: ## Load sample data
	$(PYTHON) scripts/seed_data.py

embed: ## Generate embeddings for all resources
	$(PYTHON) scripts/generate_embeddings.py

smoke: ## Run the semantic-search smoke test
	$(PYTHON) scripts/smoke_test_semantic_search.py

run: ## Start the FastAPI development server
	uvicorn app.backend.main:app --host $(API_HOST) --port $(API_PORT) --reload

lint: ## Run ruff
	ruff check .

format: ## Format code with black and fix with ruff
	black .
	ruff check --fix .

test: ## Run the test suite
	pytest -q

cov: ## Run tests with coverage report
	pytest --cov=app --cov=dbms_internals --cov-report=term-missing

ci: lint test ## Run the checks that CI runs
