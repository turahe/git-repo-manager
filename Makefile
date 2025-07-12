# Makefile for GitLab Repository Manager

.PHONY: help install clean build-all build-windows build-debian build-rpm test

# Default target
help:
	@echo "GitLab Repository Manager - Build System"
	@echo "========================================"
	@echo ""
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  clean        - Clean build artifacts"
	@echo "  build-all    - Build all package types"
	@echo "  build-windows- Build Windows EXE"
	@echo "  build-debian - Build DEB package"
	@echo "  build-rpm    - Build RPM package"
	@echo "  test         - Run tests"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf deb_dist/
	rm -f *.deb
	rm -f *.rpm
	rm -f *.tar.gz
	rm -f *.spec
	rm -rf debian/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build all packages
build-all:
	@echo "Building all package types..."
	python build_scripts/build_all.py all

# Build Windows EXE
build-windows:
	@echo "Building Windows EXE..."
	python build_scripts/build_exe.py

# Build DEB package
build-debian:
	@echo "Building DEB package..."
	python build_scripts/build_deb.py

# Build RPM package
build-rpm:
	@echo "Building RPM package..."
	python build_scripts/build_rpm.py

# Run tests
test:
	@echo "Running tests..."
	python run_tests.py

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	pytest tests/ -v --tb=short --cov=src --cov-report=term-missing

# Run integration tests only
test-integration:
	@echo "Running integration tests..."
	pytest tests/ -m integration -v

# Run linting
lint:
	@echo "Running linting..."
	flake8 src/ cli.py

# Run type checking
type-check:
	@echo "Running type checking..."
	mypy src/ cli.py

# Generate coverage report
coverage:
	@echo "Generating coverage report..."
	pytest tests/ --cov=src --cov-report=html --cov-report=xml

# Development setup
dev-setup: install
	@echo "Development setup complete!"

# Quick build for current platform
build: build-all 