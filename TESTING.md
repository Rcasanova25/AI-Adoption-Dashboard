# Testing Guide for AI Adoption Dashboard

## Overview

This guide covers all aspects of testing the AI Adoption Dashboard, from unit tests to integration tests and performance benchmarks.

## Prerequisites

Before running tests, ensure you have:

1. Python 3.8+ installed
2. All dependencies installed (see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md))
3. Virtual environment activated
4. Environment configured (`.env` file)

## Quick Start

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_data_manager.py

# Run tests with verbose output
python -m pytest -v
```

## Test Structure

```
tests/
├── __init__.py
├── unit/                    # Unit tests
│   ├── test_data_loaders.py
│   ├── test_views.py
│   └── test_components.py
├── integration/             # Integration tests
│   ├── test_app_integration.py
│   └── test_data_flow.py
├── performance/             # Performance tests
│   └── test_performance.py
├── security/                # Security tests
│   └── test_input_validation.py
└── conftest.py             # Pytest configuration
```

## Types of Tests

### 1. Unit Tests

Test individual components in isolation:

```python
# Example: tests/unit/test_data_loaders.py
def test_mckinsey_loader():
    """Test McKinsey data loader."""
    loader = McKinseyLoader()
    data = loader.load_adoption_rates()
    assert not data.empty
    assert "Company Size" in data.columns
```

### 2. Integration Tests

Test how components work together:

```python
# Example: tests/integration/test_data_flow.py
def test_data_manager_integration():
    """Test data manager with multiple loaders."""
    manager = DataManager()
    data = manager.get_all_datasets()
    assert len(data) > 0
```

### 3. Performance Tests

Ensure the application meets performance requirements:

```python
# Example: tests/performance/test_performance.py
def test_view_render_time():
    """Test that views render within acceptable time."""
    import time
    start = time.time()
    render_adoption_rates(data)
    duration = time.time() - start
    assert duration < 0.5  # Should render in under 500ms
```

### 4. Security Tests

Validate input handling and security measures:

```python
# Example: tests/security/test_input_validation.py
def test_sql_injection_protection():
    """Test protection against SQL injection."""
    malicious_input = "'; DROP TABLE users; --"
    result = process_user_input(malicious_input)
    assert "DROP TABLE" not in str(result)
```

## Running Different Test Suites

### Run Only Unit Tests
```bash
python -m pytest tests/unit/ -v
```

### Run Only Integration Tests
```bash
python -m pytest tests/integration/ -v
```

### Run Tests with Markers
```bash
# Run only fast tests
python -m pytest -m "not slow"

# Run only critical tests
python -m pytest -m "critical"
```

## Code Coverage

### Generate Coverage Report
```bash
# Run tests with coverage
python -m pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Check coverage meets threshold
python check_coverage.py
```

### Coverage Requirements
- Overall coverage: ≥ 80%
- Critical modules: ≥ 90%
- New code: 100%

## Linting and Code Quality

### Run All Quality Checks
```bash
# Format code
python -m black .

# Check code style
python -m flake8

# Type checking
python -m mypy .

# Security scanning
python -m bandit -r .

# All checks at once
make lint
```

### Pre-commit Hooks

Install pre-commit hooks to run checks automatically:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Continuous Integration

### GitHub Actions

The project includes GitHub Actions workflow for automated testing:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Writing New Tests

### Test File Naming
- Unit tests: `test_<module_name>.py`
- Integration tests: `test_<feature>_integration.py`
- Use descriptive test function names

### Test Structure
```python
import pytest
from module import function_to_test

class TestFeatureName:
    """Test suite for Feature Name."""
    
    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return pd.DataFrame({...})
    
    def test_normal_case(self, sample_data):
        """Test normal operation."""
        result = function_to_test(sample_data)
        assert result is not None
    
    def test_edge_case(self):
        """Test edge cases."""
        with pytest.raises(ValueError):
            function_to_test(None)
    
    @pytest.mark.slow
    def test_performance(self, sample_data):
        """Test performance requirements."""
        # Performance test implementation
```

## Debugging Tests

### Run Tests with Debugging
```bash
# Drop into debugger on failure
python -m pytest --pdb

# Show local variables on failure
python -m pytest -l

# Verbose output with full diffs
python -m pytest -vv

# Run specific test
python -m pytest tests/test_file.py::TestClass::test_method
```

### Using VS Code
1. Install Python extension
2. Configure `.vscode/settings.json`:
```json
{
    "python.testing.pytestArgs": ["tests"],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```
3. Use Test Explorer to run/debug tests

## Common Issues and Solutions

### Issue: Import Errors
```bash
# Solution: Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Missing Dependencies
```bash
# Solution: Install test dependencies
pip install -r requirements-dev.txt
```

### Issue: Slow Tests
```bash
# Solution: Run tests in parallel
pip install pytest-xdist
pytest -n auto
```

### Issue: Flaky Tests
```bash
# Solution: Use pytest-rerunfailures
pip install pytest-rerunfailures
pytest --reruns 3 --reruns-delay 1
```

## Best Practices

1. **Write tests first** (TDD approach)
2. **Keep tests independent** - each test should be able to run alone
3. **Use fixtures** for common setup
4. **Mock external dependencies** (APIs, databases)
5. **Test edge cases** not just happy paths
6. **Keep tests fast** - mock slow operations
7. **Use descriptive names** for tests and assertions
8. **Document complex tests** with docstrings

## Makefile Commands

The project includes a Makefile with common commands:

```bash
make test          # Run all tests
make test-unit     # Run unit tests only
make test-cov      # Run tests with coverage
make lint          # Run all linters
make format        # Format code
make type-check    # Run type checking
make security      # Run security checks
make all           # Run all checks
```

## Next Steps

1. Run the syntax checker: `python syntax_check.py`
2. Install dependencies: See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
3. Run tests: `python -m pytest`
4. Check coverage: `python check_coverage.py`
5. Set up pre-commit hooks
6. Configure CI/CD

For questions or issues, please refer to the project documentation or create an issue in the repository.