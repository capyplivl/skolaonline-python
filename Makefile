.DEFAULT_GOAL := help

.PHONY: help format lint typecheck test coverage build

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

format: ## Format the codebase with Ruff
	uv run ruff format .

lint: ## Lint the codebase with Ruff
	uv run ruff check .

typecheck: ## Check the package with strict mypy
	uv run mypy

test: ## Run the test suite
	uv run pytest tests/ -v

coverage: ## Run the test suite with a coverage report
	uv run pytest tests/ --cov=skolaonline --cov-report=term-missing

build: ## Build the source distribution and wheel
	uv build
