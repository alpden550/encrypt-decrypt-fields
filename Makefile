SHELL := /bin/bash

test:
	@echo "Running tests..."
	pytest . -s -v

lint:
	@echo "Running Ruff linter..."
	ruff check .

format:
	@echo "Running Ruff formatter..."
	ruff format .
