# AI Adoption Dashboard Testing Suite

## 🧪 Overview

This comprehensive testing suite ensures the reliability, performance, and quality of the AI Adoption Dashboard. The suite includes unit tests, integration tests, performance tests, and end-to-end tests with full coverage reporting.

## 📁 Test Structure

```
tests/
├── fixtures/           # Test data fixtures and mock objects
│   └── test_data.py    # Centralized test data generation
├── unit/              # Unit tests for individual components
│   ├── test_data_loaders.py      # Data loading function tests
│   ├── test_data_validation.py   # Data validation tests
│   └── test_business_logic.py    # Business logic tests
├── integration/       # Integration tests for component interaction
│   ├── test_view_components.py   # View integration tests
│   └── test_data_flow.py         # Data flow integration tests
├── performance/       # Performance and load testing
│   └── test_performance.py      # Performance benchmarks
├── e2e/              # End-to-end system tests
│   └── test_end_to_end.py       # Complete workflow tests
├── test_config.py    # Test configuration and utilities
├── test_runner.py    # Comprehensive test execution
└── README.md         # This documentation
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install testing dependencies
pip install -r requirements-test.txt

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run all tests with coverage
python tests/test_runner.py --all

# Run specific test types
python tests/test_runner.py --unit          # Unit tests only
python tests/test_runner.py --integration   # Integration tests only
python tests/test_runner.py --performance   # Performance tests only
python tests/test_runner.py --e2e           # End-to-end tests only

# Include slow tests
python tests/test_runner.py --all --include-slow

# Run with verbose output
python tests/test_runner.py --all --verbose

# Run linting and security checks
python tests/test_runner.py --lint --security
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=data --cov=Utils --cov=views --cov=business

# Run specific test types using markers
pytest -m unit           # Unit tests
pytest -m integration    # Integration tests  
pytest -m performance    # Performance tests
pytest -m e2e            # End-to-end tests

# Run tests in parallel
pytest -n auto

# Generate HTML coverage report
pytest --cov=data --cov-report=html
```

## 📊 Test Categories

### 1. Unit Tests (`tests/unit/`)

Test individual functions and classes in isolation.

**Coverage:**
- Data loading functions (`data/loaders.py`)
- Data validation utilities (`Utils/data_validation.py`)
- Research integration (`data/research_integration.py`)
- Business logic (`business/`)

**Example:**
```python
def test_load_historical_data_success(self, mock_research_integrator):
    """Test successful loading of historical data"""
    result = load_historical_data()
    assert not result.empty
    assert 'year' in result.columns
```

### 2. Integration Tests (`tests/integration/`)

Test component interactions and data flow between modules.

**Coverage:**
- View component rendering
- Data pipeline integration
- Navigation and routing
- Chart rendering with real data

**Example:**
```python
def test_complete_dashboard_data_pipeline(self, complete_dashboard_data):
    """Test complete data pipeline from loading to display"""
    show_historical_trends(
        data_year="2024",
        sources_data=complete_dashboard_data['sources_data'],
        historical_data=complete_dashboard_data['historical_data']
    )
```

### 3. Performance Tests (`tests/performance/`)

Test system performance, memory usage, and scalability.

**Coverage:**
- Large dataset handling
- Memory usage optimization
- Chart rendering performance
- Concurrent user simulation

**Example:**
```python
@pytest.mark.performance
def test_large_dataset_loading_time(self):
    """Test loading time for large datasets"""
    large_data = TestDataFixtures.get_large_dataset(size=50000)
    execution_time = TestUtils.assert_performance(
        process_data, max_time_ms=2000, data=large_data
    )
```

### 4. End-to-End Tests (`tests/e2e/`)

Test complete user workflows and system integration.

**Coverage:**
- Complete data flow pipelines
- User journey simulation
- Error recovery scenarios
- System integration

**Example:**
```python
@pytest.mark.e2e
def test_typical_user_session(self, complete_dashboard_data):
    """Simulate a typical user session through the dashboard"""
    # Test navigation through different views
    # Verify complete workflows work end-to-end
```

## 🎯 Test Fixtures and Data

### Test Data Fixtures (`tests/fixtures/test_data.py`)

Centralized test data generation with realistic mock data:

```python
# Historical data
historical_data = TestDataFixtures.get_historical_data()

# Sector analysis data  
sector_data = TestDataFixtures.get_sector_data()

# Large datasets for performance testing
large_data = TestDataFixtures.get_large_dataset(size=10000)

# Complete dashboard data
dashboard_data = TestDataFixtures.get_dashboard_data_complete()
```

### Mock Objects (`tests/test_config.py`)

Comprehensive mocking infrastructure:

```python
# Mock Streamlit components
mock_streamlit = MockStreamlit()

# Mock research integrator
mock_integrator = TestUtils.create_mock_research_integrator()

# Performance testing utilities
TestUtils.assert_performance(func, max_time_ms=1000)
TestUtils.assert_memory_usage(func, max_memory_mb=100)
```

## 📈 Coverage Reporting

### Coverage Targets

- **Overall Coverage:** ≥ 80%
- **Critical Modules:** ≥ 90%
  - `data/loaders.py`
  - `Utils/data_validation.py`
  - `data/research_integration.py`

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=data --cov=Utils --cov=views --cov-report=html

# View coverage report
open reports/coverage/complete/index.html

# Generate JSON coverage data
pytest --cov=data --cov-report=json

# Coverage summary
python tests/test_runner.py --generate-report
```

### Coverage Files

- `reports/coverage/complete/` - Complete HTML coverage report
- `reports/coverage/unit/` - Unit test coverage
- `reports/coverage/integration/` - Integration test coverage
- `reports/coverage/coverage_summary.json` - Coverage summary data

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    e2e: End-to-end tests
    slow: Slow running tests
```

### Test Markers

Use markers to categorize and run specific test types:

```python
@pytest.mark.unit
def test_data_validation():
    """Unit test for data validation"""
    pass

@pytest.mark.integration  
def test_view_integration():
    """Integration test for view components"""
    pass

@pytest.mark.performance
def test_performance_benchmark():
    """Performance benchmark test"""
    pass

@pytest.mark.e2e
def test_end_to_end_workflow():
    """End-to-end workflow test"""
    pass

@pytest.mark.slow
def test_comprehensive_analysis():
    """Slow running comprehensive test"""
    pass
```

## 🔍 Code Quality Checks

### Linting

```bash
# Run flake8 linting
flake8 data/ Utils/ views/ business/ --max-line-length=120

# Run black code formatting
black data/ Utils/ views/ business/

# Run isort import sorting
isort data/ Utils/ views/ business/
```

### Security Scanning

```bash
# Run bandit security scan
bandit -r data/ Utils/ views/ business/

# Run safety vulnerability check
safety check
```

### Type Checking

```bash
# Run mypy type checking
mypy data/ Utils/ views/ business/
```

## 🚦 CI/CD Integration

### GitHub Actions

The test suite integrates with GitHub Actions for automated testing:

```yaml
# .github/workflows/ci.yml
name: AI Dashboard CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: python tests/test_runner.py --all
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📊 Performance Benchmarks

### Performance Targets

- **Data Loading:** < 2 seconds for 50k rows
- **View Rendering:** < 3 seconds for complete view
- **Memory Usage:** < 500MB for typical operations
- **Chart Creation:** < 2 seconds for 10k data points

### Performance Testing

```bash
# Run performance tests
pytest -m performance

# Run with benchmarking
pytest --benchmark-only

# Include slow performance tests
pytest -m "performance and slow"
```

### Memory Profiling

```bash
# Profile memory usage
python -m memory_profiler tests/performance/test_performance.py

# Monitor memory during tests
pytest --memray tests/performance/
```

## 🐛 Debugging Tests

### Debugging Failed Tests

```bash
# Run tests with detailed output
pytest -vvv --tb=long

# Run specific test with debugging
pytest tests/unit/test_data_loaders.py::TestDataLoaders::test_load_historical_data -vvv

# Drop into debugger on failure
pytest --pdb

# Profile test execution
pytest --profile
```

### Test Data Inspection

```python
# Inspect test data
def test_data_inspection():
    data = TestDataFixtures.get_historical_data()
    print(f"Data shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    print(f"Data types: {data.dtypes}")
    print(data.head())
```

## 📝 Writing New Tests

### Test Structure Template

```python
import pytest
from tests.test_config import TestUtils, TestDataFixtures
from tests.fixtures.test_data import *

class TestNewComponent:
    """Test suite for new component"""
    
    @pytest.mark.unit
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Arrange
        test_data = TestDataFixtures.get_historical_data()
        
        # Act
        result = component_function(test_data)
        
        # Assert
        assert result is not None
        assert len(result) > 0
    
    @pytest.mark.integration
    def test_component_integration(self, complete_dashboard_data):
        """Test component integration"""
        # Test integration with other components
        pass
    
    @pytest.mark.performance
    def test_performance(self):
        """Test performance requirements"""
        large_data = TestDataFixtures.get_large_dataset(size=10000)
        
        # Should complete within time limit
        result = TestUtils.assert_performance(
            component_function,
            max_time_ms=1000,
            data=large_data
        )
```

### Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Follow AAA pattern** (Arrange, Act, Assert)
3. **Use fixtures** for common test data
4. **Mock external dependencies** to ensure test isolation
5. **Test both success and failure cases**
6. **Include performance tests** for critical functions
7. **Use appropriate markers** to categorize tests

## 🔧 Troubleshooting

### Common Issues

**Issue: Tests fail with import errors**
```bash
# Solution: Ensure project root is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue: Coverage reports are incomplete**
```bash
# Solution: Run with explicit coverage paths
pytest --cov=. --cov-report=html
```

**Issue: Performance tests are flaky**
```bash
# Solution: Run performance tests multiple times
pytest -m performance --count=3
```

**Issue: Memory tests fail in CI**
```bash
# Solution: Adjust memory thresholds for CI environment
pytest -m performance --memray-threshold=200MB
```

### Getting Help

1. Check test output for detailed error messages
2. Run tests with verbose output (`-vvv`)
3. Use debugger (`--pdb`) to inspect test state
4. Review test fixtures and mock objects
5. Check CI logs for environment-specific issues

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Streamlit Testing Guide](https://docs.streamlit.io/library/advanced-features/testing)
- [Performance Testing Best Practices](https://pytest-benchmark.readthedocs.io/)

---

**🎯 The comprehensive testing suite ensures the AI Adoption Dashboard maintains high quality, performance, and reliability across all components and user workflows.**