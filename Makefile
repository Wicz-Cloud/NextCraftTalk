# NextCraftTalk Development Makefile
# Provides common development tasks and shortcuts

.PHONY: help install install-dev install-all test lint format check clean docker-build docker-run docker-stop docs serve stop

# Default target
help: ## Show this help message
	@echo "NextCraftTalk Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation targets
install: ## Install production dependencies
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

install-external: ## Install external AI mode dependencies
	pip install -e ".[external-ai]"

install-selfhosted: ## Install self-hosted mode dependencies
	pip install -e ".[self-hosted]"

install-all: ## Install all dependencies (dev + all modes)
	pip install -e ".[all]"
	pre-commit install

# Testing targets
test: ## Run all tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage (fast)
	pytest --tb=short

# Code quality targets
lint: ## Run all linting tools
	flake8 src tests
	mypy src
	bandit -r src

format: ## Format code with black and isort
	black src tests
	isort src tests

check: ## Run all quality checks (lint + format check)
	flake8 --ignore=E501,E203 src tests
	mypy src
	black --check src tests
	isort --check-only src tests

# Development server targets
serve: ## Start development server (auto-reload)
	python src/main.py

serve-external: ## Start development server in external AI mode
	DEPLOYMENT_MODE=external_ai python src/main.py

serve-selfhosted: ## Start development server in self-hosted mode
	DEPLOYMENT_MODE=self_hosted python src/main.py

stop: ## Stop development server (if running)
	pkill -f "python src/main.py" || true

# Docker targets
docker-build-external: ## Build external AI Docker image
	docker build -f docker/external_ai/Dockerfile -t nextcrafttalk:external .

docker-build-selfhosted: ## Build self-hosted Docker image
	docker build -f docker/self_hosted/Dockerfile -t nextcrafttalk:selfhosted .

docker-run-external: ## Run external AI mode in Docker
	docker-compose -f docker/external_ai/docker-compose.yml up -d

docker-run-selfhosted: ## Run self-hosted mode in Docker
	docker-compose -f docker/self_hosted/docker-compose.yml up -d

docker-stop-external: ## Stop external AI Docker containers
	docker-compose -f docker/external_ai/docker-compose.yml down

docker-stop-selfhosted: ## Stop self-hosted Docker containers
	docker-compose -f docker/self_hosted/docker-compose.yml down

# Documentation targets
docs: ## Generate documentation (if configured)
	@echo "Documentation generation not yet configured"

# Cleanup targets
clean: ## Clean up temporary files and caches
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-all: clean ## Clean everything including virtual environments
	rm -rf venv/
	rm -rf .venv/

# Deployment targets
deploy-external: ## Deploy external AI mode using deployment script
	./scripts/deploy.sh start external_ai

deploy-selfhosted: ## Deploy self-hosted mode using deployment script
	./scripts/deploy.sh start self_hosted

# Utility targets
env-check: ## Check environment configuration
	python -c "from src.core.config import get_config; print('Config loaded successfully:', get_config().deployment_mode)"

deps-update: ## Update dependencies
	pip-compile --upgrade
	pip-compile --upgrade requirements-external.in
	pip-compile --upgrade requirements-selfhosted.in

# Pre-commit hooks
pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	bash -c "source venv/bin/activate && pre-commit run --all-files"

# CI/CD simulation
ci: ## Run CI pipeline locally
	$(MAKE) check
	$(MAKE) test-cov
	$(MAKE) clean
