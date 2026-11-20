######################################################################
# sstewart Makefile
######################################################################

# ---------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------
 # Use pyenv's shim if available; fall back to system python3.
 PYTHON := $(shell pyenv which python 2>/dev/null || echo python3)
PIP          := $(PYTHON) -m pip
GIT          := git
PACKAGE_NAME := sstewart
VERSION_FILE := VERSION

# Extract version from pyproject.toml if VERSION file does not exist
VERSION := $(shell grep '^version' pyproject.toml | head -1 | cut -d '"' -f2)

# ---------------------------------------------------------------------
# Phony targets
# ---------------------------------------------------------------------
# Phony targets
.PHONY: help install requirements doc view clean publish run tag release start stop
######################################################################
# Help
######################################################################
help:
	@echo "Makefile for the sstewart project"
	@echo ""
	@echo "Available targets:"
	@echo "  install      - Install the package in editable mode"
	@echo "  requirements - Generate a pinned requirements.txt from pyproject.toml"
	@echo "  doc          - Build the MkDocs documentation"
	@echo "  view         - Serve the MkDocs site locally with live reload"
	@echo "  clean        - Remove generated artefacts (site/, __pycache__, etc.)"
	@echo "  publish      - Deploy the MkDocs site to GitHub Pages"
	@echo "  run          - Run the FastAPI application (uvicorn)"
	@echo "  tag          - Create a git tag for the current version"
	@echo "  release      - Tag and push the current version"
	@echo "  migrate      - Apply Alembic migrations (upgrade to head)"

######################################################################
# Development
######################################################################
install:
	$(PIP) install -e .

######################################################################
# Requirements
######################################################################
requirements:
	@echo "Generating requirements.txt from pyproject.toml..."
	@# Use pip-compile if available; fall back to a simple copy of direct deps
	@which pip-compile >/dev/null 2>&1 && \
	  pip-compile --output-file=requirements.txt pyproject.toml || \
	  (\
	      grep '^\s*"' pyproject.toml | tr -d '"' | tr -d ',' | sed -e 's/^\s*//g' > requirements.txt\
	  )

######################################################################
# Documentation
######################################################################
doc:
	@echo "Building MkDocs documentation..."
	mkdocs build

view:
	@echo "Serving MkDocs documentation locally..."
	mkdocs serve --livereload

clean:
	@echo "Cleaning generated artefacts..."
	rm -rf site/ .pytest_cache .coverage .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

publish:
	@echo "Deploying MkDocs site to GitHub Pages..."
	mkdocs gh-deploy --force

######################################################################
# Run FastAPI server
######################################################################
run:
	@echo "Starting FastAPI server..."
	uvicorn src.backend.app.main:app --reload

# ----------------------------------------------------------------------
# Docker compose helpers
# ----------------------------------------------------------------------
COMPOSE_FILE ?= docker-compose.yml

start:
	@echo "Starting services with Docker Compose..."
	@docker compose -f $(COMPOSE_FILE) up -d

stop:
	@echo "Stopping Docker Compose services..."
	@docker compose -f $(COMPOSE_FILE) down

######################################################################
# Git versioning
######################################################################
tag:
	@echo "Tagging version v$(VERSION)..."
	$(GIT) tag -a v$(VERSION) -m "Release v$(VERSION)"
	$(GIT) push origin v$(VERSION)

release: tag
	@echo "Release complete."

# ----------------------------------------------------------------------
# Database migrations
# ----------------------------------------------------------------------
migrate:
	@echo "Applying database migrations via Alembic..."
	@alembic upgrade head
