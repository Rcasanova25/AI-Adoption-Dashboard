# AI Adoption Dashboard

Strategic AI adoption analysis dashboard providing comprehensive insights into AI adoption trends from 2018-2025, including the latest findings from the AI Index Report 2025.

## 🚀 Features

### Executive Decision Support
- **Strategic Brief**: 5-minute executive intelligence with market reality checks
- **Competitive Position Assessor**: Real-time competitive gap analysis
- **Investment Case Builder**: ROI analysis and business case generation with downloadable reports
- **Market Intelligence**: Real-time market trends and competitive dynamics
- **Action Planning Engine**: Evidence-based strategic decisions with timelines

### Comprehensive Analytics
- **Historical Trends**: AI adoption evolution from 2017-2025 with milestone annotations
- **Industry Analysis**: Sector-specific adoption rates, ROI, and competitive positioning
- **Geographic Distribution**: Regional adoption patterns and investment hubs
- **Firm Size Analysis**: Adoption rates by company size with competitive thresholds
- **Technology Stack**: Implementation approaches and integration strategies

### Advanced Data & Performance
- **28 Comprehensive Datasets**: From AI Index Report 2025, McKinsey, OECD, and Census Bureau
- **Advanced Performance System**: Multi-layer caching, async loading, and real-time monitoring
- **Data Validation**: Pydantic models for all datasets ensuring data integrity
- **Modular Architecture**: Clean, maintainable codebase with proper separation of concerns

## 📊 Data Sources

- Stanford AI Index Report 2025
- McKinsey Global Survey on AI
- OECD AI Policy Observatory
- US Census Bureau AI Use Supplement

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Adoption-Dashboard.git
   cd AI-Adoption-Dashboard
   ```

2. **Install dependencies**
   ```bash
   # Install production dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-test.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Test the performance system** (optional)
   ```bash
   # Run performance demo
   streamlit run performance/caching.py
   
   # Run performance tests
   python test_performance.py
   ```

## 🔧 Troubleshooting

If you encounter data loading issues, run the diagnostic script:

```bash
streamlit run diagnose_data_loading.py
```

This will help identify any problems with external dependencies or data files.

## 🧪 Testing Infrastructure

This project includes a comprehensive testing suite with automated CI/CD:

### Test Types

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions and data flow
- **Performance Tests**: Benchmark critical operations and detect regressions
- **Security Tests**: Vulnerability scanning and dependency checks

### Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
make test-performance

# Run with coverage
make coverage

# Run performance benchmarks
make benchmark
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Security checks
make security

# Full quality check
make prod-check
```

### Advanced Test Runner

```bash
# Run all tests with quality checks
python scripts/test_runner.py --type all --quality

# Run only performance tests
python scripts/test_runner.py --type performance

# Run with verbose output
python scripts/test_runner.py --type all --verbose
```

## 🔧 Development Workflow

### Using Makefile

The project includes a comprehensive Makefile for common development tasks:

```bash
# See all available commands
make help

# Install development environment
make install-dev

# Run tests
make test

# Format and lint code
make format
make lint

# Clean up generated files
make clean

# Start development server
make dev
```

### Using pyproject.toml

The project uses modern Python packaging with `pyproject.toml`:

```bash
# Install in development mode
pip install -e ".[test,dev]"

# Run tests with pytest
pytest tests/ -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🚀 CI/CD Pipeline

The project includes GitHub Actions workflows that run on:

- **Push to main/develop**: Full test suite
- **Pull Requests**: Unit and integration tests
- **Scheduled (nightly)**: Performance regression tests

### Workflow Jobs

1. **Test**: Unit and integration tests across Python 3.8, 3.9, 3.10
2. **Performance**: Performance benchmarks and regression detection
3. **Security**: Vulnerability scanning with Bandit and Safety
4. **Quality**: Code formatting and linting checks

### Performance Regression Detection

The CI pipeline includes automatic performance regression detection:

- Compares current performance against baseline
- Fails builds if performance degrades by >20%
- Generates detailed performance reports

## 📁 Project Structure

```
AI-Adoption-Dashboard/
├── .github/workflows/     # CI/CD workflows
├── business/              # Business logic modules (ROI, competitive analysis)
├── config/                # Centralized configuration and settings
├── data/                  # Data loading, models, and validation
│   ├── loaders.py        # Comprehensive dataset loading (28 datasets)
│   └── models.py         # Pydantic validation models
├── performance/           # Advanced performance optimization
│   ├── caching.py        # Multi-layer caching system
│   ├── memory_management.py # Memory optimization
│   └── integration.py    # Performance integration
├── components/            # Reusable UI components
├── Utils/                 # Utility functions and helpers
├── tests/                 # Comprehensive test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   ├── performance/      # Performance tests
│   └── fixtures/         # Test fixtures
├── scripts/              # Development and deployment scripts
├── reports/              # Generated reports and coverage
├── app.py                # Main Streamlit application
├── requirements.txt      # Production dependencies
├── requirements-test.txt # Test dependencies
├── pyproject.toml        # Modern Python packaging configuration
└── Makefile              # Development automation
```

### Key Components

- **`app.py`**: Main application with executive dashboard and analyst views
- **`business/`**: Business logic for ROI calculations and competitive analysis
- **`data/`**: Data loading system with 28 datasets and comprehensive validation
- **`performance/`**: Advanced caching, memory management, and optimization
- **`config/`**: Centralized configuration management
- **`tests/`**: Comprehensive test suite with 80%+ coverage target

## 🎯 Key Components

### Performance System (`performance/`)
- **Advanced Caching**: Multi-layer caching with memory and disk storage
- **Data Pipeline**: High-performance data processing with intelligent caching
- **Async Loading**: Parallel data loading with progress tracking
- **Performance Monitoring**: Real-time metrics and optimization recommendations
- **Smart Cache Decorator**: Easy-to-use caching for expensive operations
- **Memory Management**: Real-time memory monitoring and optimization
- **Chart Optimization**: LTTB downsampling and WebGL rendering
- **DataFrame Optimization**: Automatic dtype optimization and chunking

### Business Logic (`business/`)
- Competitive position assessment
- Investment case calculation
- ROI analysis and metrics

### Data Layer (`data/`)
- Modular data loading
- Data validation with Pydantic
- Dynamic metrics calculation

### Utilities (`Utils/`)
- Safe execution wrappers
- Performance monitoring
- Error handling utilities

## 📈 Performance Monitoring

The application includes built-in performance monitoring:

- Function execution time tracking
- Memory usage monitoring
- Chart rendering performance
- Data processing benchmarks

## 🧠 Memory Management System

The dashboard includes an advanced memory management system:

### Features
- **Real-time Monitoring**: Live memory usage tracking with alerts
- **Automatic Cleanup**: Background garbage collection and cache clearing
- **DataFrame Optimization**: Automatic dtype optimization and memory reduction
- **Session State Management**: TTL-based session state with automatic expiration
- **Memory Profiling**: Context managers for tracking memory usage
- **Chunking**: Large DataFrame processing in memory-efficient chunks

### Usage Examples
```python
from performance import MemoryMonitor, DataFrameOptimizer, SessionStateManager

# Initialize memory monitor
monitor = MemoryMonitor()
monitor.render_memory_dashboard()  # Shows in sidebar

# Optimize DataFrames
optimized_df, stats = DataFrameOptimizer.optimize_dtypes(large_df)

# Manage session state with TTL
SessionStateManager.set_with_timestamp('data', df, 3600)  # 1 hour TTL
data = SessionStateManager.get_with_expiry('data')

# Profile memory usage
with memory_profiler("operation_name", monitor):
    # Your memory-intensive operation
    result = expensive_operation()
```

### Memory Management Demo
```bash
# Run memory management demo
streamlit run memory_management_demo.py

# Run memory management tests
streamlit run test_memory_management.py
```

## 🔒 Security

- Dependency vulnerability scanning
- Code security analysis with Bandit
- Input validation and sanitization
- Safe file operations

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite: `make test`
5. Ensure code quality: `make lint`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AI-Adoption-Dashboard/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/AI-Adoption-Dashboard/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AI-Adoption-Dashboard/discussions)

## 🏆 Acknowledgments

- Stanford HAI for the AI Index Report
- McKinsey & Company for global AI survey data
- OECD for policy and adoption metrics
- US Census Bureau for business AI usage data

## 🧩 Complete Performance Integration System

The `performance/integration.py` module provides a unified interface for all performance optimizations:

### Features
- **Unified Configuration**: Master config for caching, chart, memory, and database optimization
- **Database Optimizer**: Connection pooling, query caching, and sample data generation
- **PerformanceIntegrator**: One-stop integration of caching, chart, memory, and database optimizations
- **Optimized Dashboard Rendering**: Fast, scalable, and interactive dashboard with real-time metrics
- **Performance Comparison**: Side-by-side comparison of optimized vs unoptimized loading

### Usage Example
```python
from performance import PerformanceIntegrator

integrator = PerformanceIntegrator()
# Render the optimized dashboard (in a Streamlit app)
integrator.render_optimized_dashboard(filters={})
```

### Demo
```bash
streamlit run performance/integration.py
```

This will launch a full demo of the integrated performance system, including caching, chart optimization, memory management, and database optimization.

---

**Version**: 2.2.1  
**Last Updated**: June 2025  
**Maintainer**: Your Name 