# AI Adoption Dashboard

A comprehensive, accessible dashboard providing strategic insights into AI adoption trends from 2018-2025, featuring automated PDF data extraction, WCAG 2.1 compliance, and real-time intelligence from authoritative sources.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![WCAG 2.1 AA](https://img.shields.io/badge/accessibility-WCAG%202.1%20AA-green.svg)](https://www.w3.org/WAI/WCAG21/quickref/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

## 🚀 Key Features

### 🤖 Automated Data Intelligence
- **PDF Extraction Pipeline**: Automatically processes 18+ research PDFs from Stanford, McKinsey, Goldman Sachs, OECD, and more
- **Hybrid Data Loading**: Seamless integration of automated PDF extraction with manual data curation
- **Real-time Validation**: Pydantic-based data validation ensuring accuracy and consistency
- **Smart Caching**: Performance-optimized data loading with 1-hour TTL caching

### 📊 Executive Decision Support
- **Strategic Brief**: 5-minute executive intelligence with market reality checks
- **Competitive Position Assessor**: Real-time competitive gap analysis powered by McKinsey tools
- **Investment Case Builder**: ROI analysis and business case generation with downloadable reports
- **Market Intelligence**: Live market trends and competitive dynamics
- **Action Planning Engine**: Evidence-based strategic decisions with implementation timelines

### 🎯 Comprehensive Analytics
- **Historical Trends**: AI adoption evolution from 2017-2025 with milestone annotations
- **Industry Analysis**: Sector-specific adoption rates, ROI, and competitive positioning across 8+ industries
- **Geographic Distribution**: Regional adoption patterns and investment hubs with interactive maps
- **Firm Size Analysis**: Adoption rates by company size with competitive intelligence
- **Technology Stack**: Implementation approaches and integration strategies

### ♿ Universal Accessibility (WCAG 2.1 AA Compliant)
- **High Contrast Themes**: Multiple themes including high contrast mode for visual impairments
- **Screen Reader Support**: Complete alt text, semantic markup, and ARIA labels
- **Keyboard Navigation**: Full functionality available without mouse interaction
- **Colorblind Friendly**: Patterns and textures supplement color-coding
- **Scalable Interface**: Works perfectly at 200% browser zoom

### 🧪 Enterprise-Grade Testing
- **Automated Test Suite**: 4 test categories with 100+ test cases
- **Data Validation Testing**: Comprehensive validation of all data sources and transformations
- **View Rendering Testing**: Automated testing of all dashboard components
- **Accessibility Testing**: WCAG compliance verification and color contrast analysis
- **Performance Testing**: Load testing and memory usage monitoring

## 📚 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **Git** for version control
- **4GB+ RAM** recommended for optimal performance

### 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Adoption-Dashboard.git
   cd AI-Adoption-Dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   # Using venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Or using conda
   conda create -n ai-dashboard python=3.9
   conda activate ai-dashboard
   ```

3. **Install dependencies**
   ```bash
   # Install all dependencies
   pip install -r requirements.txt
   
   # For development (includes testing and linting tools)
   pip install -r requirements-dev.txt
   ```

4. **Set up PDF automation** (optional but recommended)
   ```bash
   # Install PDF processing dependencies and validate setup
   python setup_automation.py
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - The dashboard will automatically load with sample data
   - PDF automation will activate if properly configured

### 🚀 Quick Commands

```bash
# Run with automated PDF extraction
streamlit run app.py

# Run accessibility audit
python run_accessibility_audit.py

# Run comprehensive tests
python run_tests.py --full

# Run quick tests only
python run_tests.py --quick

# Check system status
python -c "from data.pipeline_integration import integration_manager; print(integration_manager.get_system_status())"
```

## 📊 Data Sources & Architecture

### Authoritative Data Sources (18+ PDFs)
- **Stanford AI Index Report 2025** - Comprehensive AI trends and metrics
- **McKinsey Global Survey on AI 2024** - Enterprise adoption and ROI data
- **Goldman Sachs AI Research** - Economic impact and investment analysis
- **OECD AI Policy Observatory** - Global policy and governance insights
- **Federal Reserve Research** - Productivity and economic impact studies
- **NBER Working Papers** - Academic research on AI economics
- **IMF Analysis** - Macroeconomic AI impact assessments

### Data Processing Pipeline

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Files     │───▶│  Automated       │───▶│  Validated      │
│  (18+ Sources)  │    │  Extraction      │    │  Datasets       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Manual Data   │───▶│  Data Merger     │───▶│  Dashboard      │
│  (Fallback)     │    │  & Validator     │    │  Views          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Data Categories
- **Historical Trends**: 2017-2025 adoption timelines
- **Sector Analysis**: Industry-specific metrics across 8+ sectors  
- **Financial Impact**: ROI, cost savings, and revenue data
- **Geographic Data**: Regional adoption and investment patterns
- **Investment Trends**: Global AI funding and venture capital
- **Productivity Research**: Workplace impact and efficiency gains
- **Governance & Compliance**: Policy frameworks and regulations

## 🧪 Testing & Quality Assurance

### Test Categories

| Test Type | Coverage | Purpose |
|-----------|----------|---------|
| **Data Validation** | Pipeline integration, PDF extraction, data models | Ensure data accuracy and consistency |
| **View Rendering** | All dashboard components, error handling | Verify UI functionality and robustness |
| **Accessibility** | WCAG compliance, color contrast, screen readers | Ensure universal usability |
| **Performance** | Load times, memory usage, large datasets | Maintain responsive user experience |

### Running Tests

```bash
# Complete test suite with coverage
python run_tests.py --full

# Quick unit tests only
python run_tests.py --quick

# Specific test categories
python run_tests.py --suite data        # Data validation tests
python run_tests.py --suite views       # View rendering tests
python run_tests.py --suite integration # Integration tests

# Automated test pipeline
python run_tests.py --automated

# CI/CD mode
python run_tests.py --ci
```

### Test Reports
- **HTML Reports**: `test_results/test_report.html`
- **Coverage Reports**: `test_results/coverage_html/index.html`
- **JSON Results**: `test_results/test_results.json`

## ♿ Accessibility Features

### WCAG 2.1 AA Compliance

✅ **Visual Accessibility**
- High contrast color schemes (≥4.5:1 ratio)
- Colorblind-friendly palettes
- Scalable text (works at 200% zoom)
- Multiple theme options

✅ **Motor Accessibility**  
- Full keyboard navigation
- Minimum 44px touch targets
- Skip navigation links
- Clear focus indicators

✅ **Cognitive Accessibility**
- Clear information hierarchy
- Consistent navigation patterns
- Helpful error messages
- Progressive disclosure

✅ **Screen Reader Support**
- Semantic HTML structure
- Comprehensive alt text
- ARIA labels and roles
- Data table alternatives

### Accessibility Controls

Users can customize their experience via the sidebar:
- **Theme Selection**: Default or High Contrast
- **Font Size**: Normal, Large, or Extra Large
- **Motion Settings**: Reduce animations
- **Screen Reader Mode**: Optimized for assistive technology

### Testing Accessibility

```bash
# Full accessibility audit
python run_accessibility_audit.py

# Color contrast analysis
python run_accessibility_audit.py --contrast

# Colorblind accessibility test
python run_accessibility_audit.py --colorblind

# Quick summary
python run_accessibility_audit.py --quick
```

## 🔧 Configuration & Customization

### Environment Variables

```bash
# Optional: Custom data source paths
export AI_RESOURCES_PATH="path/to/your/pdfs"

# Optional: Cache configuration
export CACHE_TTL=3600  # 1 hour default

# Optional: Performance monitoring
export ENABLE_PERFORMANCE_MONITORING=true
```

### Configuration Files

- **`config/settings.py`**: Application settings
- **`config/constants.py`**: Data schemas and constants
- **`pytest.ini`**: Test configuration
- **`accessibility/`**: Accessibility themes and components

### Customizing Data Sources

1. **Add PDF files** to `AI adoption resources/` folder
2. **Restart the application** - new PDFs are automatically detected
3. **Verify processing** via the sidebar status panel

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

#### Docker (Recommended)
```bash
# Build image
docker build -t ai-dashboard .

# Run container
docker run -p 8501:8501 ai-dashboard
```

#### Cloud Platforms

**Streamlit Cloud**
1. Connect GitHub repository
2. Set Python version to 3.9+
3. Deploy with `streamlit run app.py`

**Heroku**
```bash
# Add Procfile: web: streamlit run app.py --server.port=$PORT
git push heroku main
```

**AWS/Azure/GCP**
- Use Docker container deployment
- Ensure 4GB+ memory allocation
- Configure health checks on `/health`

### Performance Optimization

For production deployments:
- Enable caching: `streamlit run app.py --server.enableCORS=false`
- Set memory limits: `--server.maxUploadSize=100`
- Configure CDN for static assets
- Use load balancer for high traffic

## 📖 Documentation

### Developer Documentation
- **[Accessibility Guide](accessibility/ACCESSIBILITY_GUIDE.md)**: Complete accessibility implementation guide
- **[API Documentation](docs/API.md)**: Data models and pipeline APIs
- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and data flow
- **[Testing Guide](docs/TESTING.md)**: Testing strategies and best practices

### User Documentation
- **[User Guide](docs/USER_GUIDE.md)**: Dashboard navigation and features
- **[Data Sources](docs/DATA_SOURCES.md)**: Information about data sources and methodology
- **[FAQ](docs/FAQ.md)**: Common questions and troubleshooting

## 🛠️ Development

### Code Structure

```
AI-Adoption-Dashboard/
├── accessibility/          # Accessibility components and themes
├── business/              # Business logic and analytics
├── components/            # Reusable UI components
├── data/                  # Data loading and processing
├── tests/                 # Comprehensive test suite
├── views/                 # Dashboard view components
├── Utils/                 # Utility functions
├── exports/               # Data export functionality
├── performance/           # Performance monitoring
└── config/                # Configuration files
```

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests during development**
   ```bash
   python run_tests.py --quick
   ```

4. **Check accessibility compliance**
   ```bash
   python run_accessibility_audit.py --quick
   ```

5. **Commit with descriptive message**
   ```bash
   git commit -m "feat: add new dashboard feature"
   ```

### Code Quality

```bash
# Format code
black .

# Type checking
mypy .

# Linting
pylint data/ views/ business/

# Security scanning
bandit -r .
```

## 📊 Performance Benchmarks

| Metric | Target | Current |
|--------|---------|---------|
| Initial Load Time | <3 seconds | ~2.1 seconds |
| Chart Render Time | <1 second | ~0.7 seconds |
| Data Validation | <2 seconds | ~1.4 seconds |
| Memory Usage | <1GB | ~650MB |
| Accessibility Score | 90+ | 95/100 |

## 🔍 Troubleshooting

### Common Issues

**PDF Extraction Not Working**
```bash
# Check PDF dependencies
python -c "import PyPDF2, pdfplumber; print('PDF libraries installed')"

# Validate resources folder
python setup_automation.py
```

**Slow Performance**
```bash
# Clear cache
rm -rf .streamlit/
streamlit cache clear

# Check system resources
python -c "from data.pipeline_integration import integration_manager; print(integration_manager.get_system_status())"
```

**Accessibility Issues**
```bash
# Run accessibility audit
python run_accessibility_audit.py

# Check color contrast
python run_accessibility_audit.py --contrast
```

**Test Failures**
```bash
# Run specific test category
python run_tests.py --suite data

# Verbose test output
python run_tests.py --full --verbose
```

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Check the `docs/` folder for detailed guides
- **Accessibility**: Review `accessibility/ACCESSIBILITY_GUIDE.md`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- **Data Sources**: Adding new authoritative sources
- **Accessibility**: Enhancing WCAG compliance
- **Testing**: Expanding test coverage
- **Documentation**: Improving guides and examples
- **Performance**: Optimizing load times and memory usage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Stanford HAI** for the AI Index Report 2025
- **McKinsey & Company** for the Global Survey on AI
- **Goldman Sachs Research** for economic impact analysis
- **OECD** for policy and governance insights
- **Federal Reserve** for productivity research
- **Streamlit** for the dashboard framework
- **Plotly** for interactive visualizations

## 📞 Support

- **Technical Issues**: Create a GitHub issue
- **Feature Requests**: Use the feature request template
- **Security Issues**: Email security@project.com
- **Accessibility**: Check the accessibility guide first

---

<div align="center">

**Built with ❤️ for the AI community**

[🚀 Get Started](#quick-start) · [📚 Documentation](#documentation) · [🤝 Contribute](#contributing)

</div>