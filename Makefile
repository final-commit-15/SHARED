.PHONY: help install install-dev lint format typecheck test coverage test-fast
.PHONY: build release clean precommit bump-version check

PYTHON ?= python
POETRY ?= poetry

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime dependencies
	$(POETRY) install --only main

install-dev: ## Install runtime + dev dependencies
	$(POETRY) install

lint: ## Run Ruff linter
	$(POETRY) run ruff check src tests examples

format: ## Format code with Ruff formatter + Black
	$(POETRY) run ruff format src tests examples
	$(POETRY) run black src tests examples

typecheck: ## Run mypy type checker
	$(POETRY) run mypy src

test: ## Run the full test suite
	$(POETRY) run pytest

test-fast: ## Run tests without integration markers
	$(POETRY) run pytest -m "not integration"

coverage: ## Run tests with coverage report
	$(POETRY) run pytest --cov=agentforge_shared --cov-report=term-missing --cov-report=html

bandit: ## Run bandit security scanner
	$(POETRY) run bandit -r src -q -ll

build: ## Build sdist + wheel
	$(POETRY) build

check: lint typecheck test ## Full quality gate

release: ## Build and publish to PyPI (set PYPI_TOKEN)
	$(POETRY) build
	$(POETRY) publish

bump-version: ## Interactive version bump (patch/minor/major)
	$(POETRY) run agentforge-bump-version

clean: ## Remove build artifacts
	rm -rf dist build .coverage htmlcov .pytest_cache .mypy_cache .ruff_cache *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

precommit: ## Run pre-commit hooks
	pre-commit run --all-files