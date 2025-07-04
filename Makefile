# Makefile for Economics of AI Dashboard
# Implements CLAUDE.md required commands

.PHONY: help fmt lint test test-unit test-integration test-e2e coverage clean install hooks run check-all

# Default target
help:
	@echo "Economics of AI Dashboard - Development Commands"
	@echo "=============================================="
	@echo "fmt          - Format code with black and isort"
	@echo "lint         - Run linting checks (flake8, mypy, bandit)"
	@echo "test         - Run all tests"
	@echo "test-unit    - Run unit tests only"
	@echo "test-integration - Run integration tests only"
	@echo "test-e2e     - Run end-to-end tests only"
	@echo "coverage     - Generate test coverage report"
	@echo "clean        - Clean up temporary files"
	@echo "install      - Install all dependencies"
	@echo "hooks        - Install pre-commit hooks"
	@echo "run          - Run the dashboard application"
	@echo "check-all    - Run all quality checks"

# Format code (CLAUDE.md requirement)
fmt:
	@echo "Formatting code..."
	@black . --line-length=100
	@isort . --profile=black --line-length=100
	@echo "✅ Code formatted successfully"

# Lint code (CLAUDE.md requirement)
lint:
	@echo "Running linting checks..."
	@flake8 . --max-line-length=100 --extend-ignore=E203,W503 --exclude=venv,env,.git,__pycache__
	@echo "✅ Flake8 passed"
	@mypy . --ignore-missing-imports --no-strict-optional
	@echo "✅ MyPy passed"
	@bandit -r . -ll -i -x './tests/*,./venv/*,./env/*'
	@echo "✅ Bandit security check passed"
	@echo "✅ All linting checks passed"

# Run tests (CLAUDE.md requirement)
test:
	@echo "Running all tests..."
	@pytest tests/ -v --tb=short

test-unit:
	@echo "Running unit tests..."
	@pytest tests/unit -v --tb=short

test-integration:
	@echo "Running integration tests..."
	@pytest tests/integration -v --tb=short

test-e2e:
	@echo "Running end-to-end tests..."
	@pytest tests/e2e -v --tb=short

# Generate coverage report
coverage:
	@echo "Generating coverage report..."
	@pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-fail-under=80
	@echo "✅ Coverage report generated in htmlcov/index.html"

# Clean temporary files
clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@rm -rf htmlcov/ 2>/dev/null || true
	@rm -rf .pytest_cache/ 2>/dev/null || true
	@rm -rf .mypy_cache/ 2>/dev/null || true
	@rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Install dependencies
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt 2>/dev/null || pip install pytest pytest-cov black flake8 mypy bandit pre-commit
	@echo "✅ Dependencies installed"

# Install pre-commit hooks
hooks:
	@echo "Installing pre-commit hooks..."
	@pre-commit install
	@pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# Run the application
run:
	@echo "Starting Economics of AI Dashboard..."
	@streamlit run app.py

# Run all checks (for CI/CD)
check-all: fmt lint test coverage
	@echo "=============================================="
	@echo "✅ All quality checks passed!"
	@echo "=============================================="

# Quick check before commit
pre-commit: fmt lint test-unit
	@echo "✅ Pre-commit checks passed"

# Development setup
dev-setup: install hooks
	@echo "✅ Development environment ready"

# Check for TODOs and placeholders (CLAUDE.md compliance)
check-todos:
	@echo "Checking for TODOs and placeholders..."
	@! grep -r "TODO\|FIXME\|XXX\|HACK" --include="*.py" . --exclude-dir=tests --exclude-dir=venv || (echo "❌ Found TODO comments" && exit 1)
	@! grep -r "pass.*#.*placeholder\|placeholder.*method" --include="*.py" . --exclude-dir=tests || (echo "❌ Found placeholder code" && exit 1)
	@echo "✅ No TODOs or placeholders found"

# Performance benchmarks
benchmark:
	@echo "Running performance benchmarks..."
	@pytest tests/performance -v --benchmark-only

# Security scan
security:
	@echo "Running security scan..."
	@bandit -r . -f json -o security-report.json -ll -i -x './tests/*,./venv/*'
	@safety check --json > safety-report.json 2>/dev/null || true
	@echo "✅ Security scan complete (reports saved)"

# Documentation
docs:
	@echo "Generating documentation..."
	@pydoc -w ./
	@echo "✅ Documentation generated"

# Docker build (if needed)
docker-build:
	@echo "Building Docker image..."
	@docker build -t economics-ai-dashboard .
	@echo "✅ Docker image built"

# Version info
version:
	@echo "Economics of AI Dashboard"
	@echo "Python: $$(python --version)"
	@echo "Streamlit: $$(streamlit --version)"
	@echo "Pytest: $$(pytest --version)"

.DEFAULT_GOAL := help