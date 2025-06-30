# AI Dashboard Deployment Guide

This document outlines the deployment infrastructure and testing setup for the AI Adoption Dashboard.

## 🚀 CI/CD Infrastructure

### GitHub Actions Workflow

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/test-suite.yml`) that runs:

- **Unit Tests**: Across Python 3.8, 3.9, 3.10
- **Integration Tests**: Component interaction testing
- **Performance Tests**: Benchmark and regression detection
- **Security Tests**: Vulnerability scanning
- **Code Quality**: Formatting and linting checks

### Workflow Triggers

- **Push to main/develop**: Full test suite
- **Pull Requests**: Unit and integration tests
- **Scheduled (nightly)**: Performance regression tests

## 🧪 Testing Infrastructure

### Test Types

1. **Unit Tests** (`tests/unit/`)
   - Individual component testing
   - Business logic validation
   - Utility function testing

2. **Integration Tests** (`tests/integration/`)
   - Component interaction testing
   - Data flow validation
   - End-to-end functionality

3. **Performance Tests** (`tests/performance/`)
   - Benchmark critical operations
   - Memory usage monitoring
   - Regression detection

4. **Test Fixtures** (`tests/fixtures/`)
   - Sample data generation
   - Mock objects
   - Property-based test data

### Running Tests

#### Using Python Directly

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test types
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/performance/ -v

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

#### Using Test Runner Script

```bash
# Run all tests with quality checks
python scripts/test_runner.py --type all --quality

# Run only performance tests
python scripts/test_runner.py --type performance

# Run with verbose output
python scripts/test_runner.py --type all --verbose
```

#### Using Makefile (Linux/Mac)

```bash
# Install development environment
make install-dev

# Run tests
make test
make test-unit
make test-integration
make test-performance

# Code quality
make lint
make format
make security
```

## 📊 Performance Monitoring

### Regression Detection

The CI pipeline includes automatic performance regression detection:

- Compares current performance against baseline
- Fails builds if performance degrades by >20%
- Generates detailed performance reports

### Performance Scripts

- `scripts/performance_regression_check.py`: Detects performance regressions
- `scripts/test_runner.py`: Advanced test runner with reporting

## 🔒 Security

### Security Checks

- **Bandit**: Code security analysis
- **Safety**: Dependency vulnerability scanning
- **Input validation**: Safe data handling

### Running Security Checks

```bash
# Install security tools
pip install bandit[toml] safety

# Run security analysis
bandit -r . -f json -o reports/bandit-report.json
safety check --json --output safety-report.json
```

## 📈 Code Quality

### Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pylint**: Code analysis

### Running Quality Checks

```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint app.py business/ data/ Utils/
mypy app.py business/ data/ Utils/ --ignore-missing-imports
```

## 🏗️ Project Configuration

### pyproject.toml

Modern Python packaging configuration with:

- Build system requirements
- Project metadata
- Dependencies and optional dependencies
- Tool configurations (pytest, coverage, black, etc.)

### Configuration Files

- `pytest.ini`: Pytest configuration
- `.coveragerc`: Coverage reporting settings
- `requirements.txt`: Production dependencies
- `requirements-test.txt`: Test dependencies

## 🚀 Deployment Checklist

Before deploying to production:

1. **Run Full Test Suite**
   ```bash
   python scripts/test_runner.py --type all --quality
   ```

2. **Check Coverage**
   ```bash
   python -m pytest --cov=. --cov-report=term --cov-fail-under=80
   ```

3. **Security Scan**
   ```bash
   bandit -r . -ll
   safety check
   ```

4. **Performance Check**
   ```bash
   python scripts/performance_regression_check.py
   ```

5. **Code Quality**
   ```bash
   black --check .
   isort --check-only .
   flake8 .
   ```

## 📋 Environment Setup

### Development Environment

```bash
# Clone repository
git clone <repository-url>
cd AI-Adoption-Dashboard

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Install in development mode
pip install -e ".[test,dev]"
```

### Production Environment

```bash
# Install production dependencies only
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes project root
2. **Missing Dependencies**: Install from requirements-test.txt
3. **Test Failures**: Check function signatures match implementation
4. **Performance Issues**: Run regression detection script

### Debug Commands

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check installed packages
pip list

# Run tests with debug output
python -m pytest -v --tb=long

# Check configuration
python -c "import pytest; print(pytest.ini_options())"
```

## 📞 Support

For deployment issues:

1. Check the GitHub Actions logs
2. Review test output for specific failures
3. Verify environment configuration
4. Consult the main README.md for setup instructions

---

**Last Updated**: June 2025  
**Version**: 2.2.1 