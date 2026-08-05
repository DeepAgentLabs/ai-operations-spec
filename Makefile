.DEFAULT_GOAL := help

.PHONY: help install test clean check

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --extra dev

test: ## Run schema validation tests
	uv run pytest

clean: ## Remove cache artifacts
	rm -rf .pytest_cache .ruff_cache __pycache__

check: test ## Run all quality gates
