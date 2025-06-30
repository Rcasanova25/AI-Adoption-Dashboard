.PHONY: help test test-unit test-integration test-performance lint format clean install-dev

help:
	@echo "Available commands:"
	@echo "  install-dev     Install development dependencies"
	@echo "  test           Run all tests"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-performance Run performance tests"
	@echo "  lint           Run code linting"
	@echo "  format         Format code with black and isort"
	@echo "  security       Run security checks"
	@echo "  clean          Clean up generated files"

install-dev:
	pip install -e ".[test,dev]"

test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-performance:
	pytest tests/performance/ -v -m performance

test-fast:
	pytest -v -m "not slow"

lint:
	flake8 .
	pylint app.py business/ data/ Utils/
	mypy app.py business/ data/ Utils/ --ignore-missing-imports

format:
	black .
	isort .

security:
	bandit -r . -f json -o reports/bandit-report.json
	safety check

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf reports/

coverage:
	pytest --cov=. --cov-report=html --cov-report=term

benchmark:
	pytest tests/performance/ -v --benchmark-sort=mean --benchmark-json=benchmark.json

# Development server
dev:
	streamlit run app.py

# Production check
prod-check:
	python -m pytest tests/ -v --tb=short
	python -m mypy app.py business/ data/ Utils/ --ignore-missing-imports
	python -m bandit -r . -ll
	python -m safety check 