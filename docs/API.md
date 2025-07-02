# API Documentation

## Overview

The AI Adoption Dashboard provides a comprehensive API for data access, pipeline management, and component integration. This documentation covers all public APIs, data models, and integration patterns.

## 📡 Core APIs

### Data Loading APIs

#### Primary Data Loader
```python
from data.pipeline_integration import load_all_datasets_integrated

def load_all_datasets_integrated() -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """
    Load all datasets using integrated pipeline (automated + manual)
    
    Returns:
        Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]: 
            - Dictionary of dataset name to DataFrame
            - Integration metadata including strategy and performance metrics
    
    Example:
        datasets, metadata = load_all_datasets_integrated()
        historical_data = datasets['historical_data']
        strategy = metadata['integration_strategy']['primary_method']
    """
```

**Available Datasets:**
- `historical_data`: AI adoption trends 2017-2025
- `sector_data`: Industry-specific adoption rates
- `financial_impact`: ROI and cost impact data
- `investment_data`: Global AI investment trends
- `productivity_data`: Workplace productivity impact
- `skill_gap_data`: Skills and workforce analysis
- `geographic_data`: Regional adoption patterns
- `governance_data`: Policy and compliance data
- `environmental_data`: Sustainability impact
- `cost_trend_data`: Cost analysis and trends
- `token_economics_data`: AI token usage patterns
- `maturity_data`: AI maturity assessments
- `firm_size_data`: Adoption by company size

#### Automated Pipeline APIs
```python
from data.automated_loaders import automated_loader

# Load specific datasets with automated extraction
def load_historical_data_automated() -> pd.DataFrame:
    """Load historical data with PDF auto-extraction"""

def load_sector_data_automated() -> pd.DataFrame:
    """Load sector data with PDF auto-extraction"""

def load_financial_impact_automated() -> pd.DataFrame:
    """Load financial impact data with PDF auto-extraction"""

# Get extraction metadata
def get_extraction_metadata() -> pd.DataFrame:
    """Get metadata about processed PDF files"""

# Validate datasets
def validate_all_datasets() -> Dict[str, bool]:
    """Validate all automatically extracted datasets"""
```

#### PDF Processing APIs
```python
from data.pdf_data_pipeline import pdf_pipeline

# Scan and process PDFs
def run_pipeline() -> Dict[str, pd.DataFrame]:
    """Run complete PDF extraction pipeline"""

def scan_for_pdfs() -> List[Path]:
    """Scan resources folder for PDF files"""

def process_pdf(filepath: Path) -> Dict[str, Any]:
    """Process single PDF file"""

# Example usage
pipeline_results = pdf_pipeline.run_pipeline()
adoption_data = pipeline_results.get('adoption_rates', pd.DataFrame())
```

### Data Validation APIs

#### Pydantic Model Validation
```python
from data.models import (
    validate_dataset, safe_validate_data, ValidationResult,
    HistoricalDataPoint, SectorData, FinancialImpactData
)

def validate_dataset(data: pd.DataFrame, 
                    dataset_type: str, 
                    model: Type[BaseModel] = None) -> ValidationResult:
    """
    Validate dataset against Pydantic model
    
    Args:
        data: DataFrame to validate
        dataset_type: Type of dataset ('historical_data', 'sector_data', etc.)
        model: Optional specific Pydantic model
    
    Returns:
        ValidationResult with validation status and details
    """

def safe_validate_data(data: pd.DataFrame, 
                      name: str, 
                      show_warnings: bool = True) -> ValidationResult:
    """
    Safe validation with error handling and user feedback
    
    Args:
        data: DataFrame to validate
        name: Human-readable name for the dataset
        show_warnings: Whether to display warnings in UI
    
    Returns:
        ValidationResult with comprehensive validation details
    """

# Example usage
result = safe_validate_data(historical_df, "Historical Trends")
if result.is_valid:
    print("Data validation passed")
else:
    print(f"Validation errors: {result.errors}")
```

#### Custom Validation Models
```python
# Create custom validation for historical data
class HistoricalDataPoint(BaseModel):
    year: int = Field(..., ge=2017, le=2025)
    ai_use: float = Field(..., ge=0, le=100)
    genai_use: float = Field(..., ge=0, le=100)
    
    @field_validator('genai_use')
    @classmethod
    def genai_cannot_exceed_ai(cls, v, info: ValidationInfo):
        if info.data and 'ai_use' in info.data and v > info.data['ai_use']:
            raise ValueError("GenAI adoption cannot exceed overall AI adoption")
        return v
```

### Integration Management APIs

#### Pipeline Integration Manager
```python
from data.pipeline_integration import integration_manager

# Check system status
def get_system_status() -> Dict[str, Any]:
    """Get comprehensive system status"""

def get_integration_strategy() -> Dict[str, str]:
    """Get current integration strategy"""

# Load data with strategy
def load_data_with_strategy(dataset_name: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Load data using optimal strategy (automated/manual)"""

# Example usage
status = integration_manager.get_system_status()
automation_enabled = status['automation_enabled']
prerequisites = status['prerequisites']
```

### Research Integration APIs

#### Research Data Access
```python
from data.research_integration import research_integrator

# Get authentic research data
def get_authentic_historical_data() -> pd.DataFrame:
    """Get historical data from Stanford AI Index"""

def get_authentic_sector_data_2025() -> pd.DataFrame:
    """Get sector data from McKinsey survey"""

def get_authentic_investment_data() -> pd.DataFrame:
    """Get investment data from multiple sources"""

# Get credibility metrics
def get_data_credibility_metrics() -> Dict[str, Any]:
    """Get credibility ratings for all data sources"""

# Example usage
historical = research_integrator.get_authentic_historical_data()
credibility = research_integrator.get_data_credibility_metrics()
```

## 🎨 Accessibility APIs

### Accessible Components
```python
from accessibility.accessible_components import (
    AccessibleChart, AccessibleMetric, AccessibleLayout, AccessibleColorPalette
)

# Create accessible chart
chart = AccessibleChart(
    title="AI Adoption Trends",
    accessibility_level=AccessibilityLevel.AA
)

fig = chart.create_accessible_figure(chart_type="line")
chart.add_accessible_trace(fig, data, 'year', 'adoption_rate', 'AI Adoption')
chart.add_data_table_alternative(data, "Historical adoption data")

# Create accessible metric
metric = AccessibleMetric()
metric.render(
    label="AI Adoption Rate",
    value="78%",
    delta="+13% vs 2023",
    help_text="Percentage of organizations using AI"
)

# Use accessible color palette
palette = AccessibleColorPalette()
primary_color = palette.text_primary
chart_colors = palette.data_colors
```

### Accessibility Integration
```python
from accessibility.integrate_accessibility import (
    make_chart_accessible, create_accessible_metric, initialize_accessibility
)

# Initialize accessibility features
initialize_accessibility()

# Make existing chart accessible
fig = create_your_plotly_chart()
make_chart_accessible(
    fig=fig,
    title="Chart Title",
    description="Detailed description for screen readers",
    data=your_dataframe
)

# Create accessible metric
create_accessible_metric(
    label="Metric Name",
    value="Value",
    delta="Change",
    help_text="Description"
)
```

### Accessibility Audit APIs
```python
from accessibility.accessibility_audit import accessibility_auditor

# Run comprehensive audit
def run_full_audit() -> Dict[str, Any]:
    """Run complete accessibility audit"""

# Analyze color contrast
def audit_color_schemes() -> List[AccessibilityIssue]:
    """Audit color schemes for WCAG compliance"""

# Test colorblind accessibility
def audit_chart_accessibility() -> List[AccessibilityIssue]:
    """Audit charts for colorblind accessibility"""

# Example usage
audit_results = accessibility_auditor.run_full_audit()
score = audit_results['overall_score']
issues = audit_results['issues']
```

## 🧪 Testing APIs

### Automated Test Runner
```python
from tests.automated.test_runner_automated import AutomatedTestRunner

# Create test runner
runner = AutomatedTestRunner()

# Run specific test suites
data_results = runner.run_data_validation_tests()
view_results = runner.run_view_rendering_tests()
accessibility_results = runner.run_accessibility_tests()

# Run all tests
all_results = runner.run_all_tests()

# CI/CD mode
exit_code = runner.run_ci_mode()
```

### Test Utilities
```python
from tests.automated.pytest_config import TestHelpers

# Create mock datasets
mock_data = TestHelpers.create_mock_datasets(size=100)

# Validate test output
TestHelpers.validate_test_output(result, ['status', 'data', 'metadata'])

# Mock Streamlit components
with TestHelpers.mock_streamlit_components() as mocks:
    your_view_function()
    assert mocks['write'].called
```

## 📊 Performance & Monitoring APIs

### Performance Monitoring
```python
from performance.caching import performance_monitor

# Start/stop timers
performance_monitor.start_timer('operation_name')
result = expensive_operation()
performance_monitor.end_timer('operation_name')

# Get performance metrics
metrics = performance_monitor.get_metrics()
memory_usage = performance_monitor.get_memory_usage()

# Render performance sidebar
performance_monitor.render_performance_sidebar()
```

### Caching APIs
```python
from performance.caching import smart_cache

# Smart caching with automatic invalidation
@smart_cache(ttl=3600, deps=['file1.csv', 'file2.csv'])
def expensive_computation(params):
    return complex_calculation(params)

# Manual cache operations
smart_cache.clear_cache('function_name')
smart_cache.get_cache_stats()
```

## 🔧 Configuration APIs

### Settings Management
```python
from config.settings import Settings
from config.constants import DataSchemas, UIConstants

# Access configuration
settings = Settings()
api_timeout = settings.API_TIMEOUT
cache_ttl = settings.CACHE_TTL

# Access data schemas
schemas = DataSchemas()
required_columns = schemas.HISTORICAL_DATA_COLUMNS
validation_rules = schemas.VALIDATION_RULES

# Access UI constants
ui = UIConstants()
theme_colors = ui.THEME_COLORS
chart_defaults = ui.CHART_DEFAULTS
```

## 🎯 Business Logic APIs

### Business Metrics
```python
from business.metrics import business_metrics

# Calculate business metrics
adoption_score = business_metrics.calculate_adoption_score(sector_data)
competitive_position = business_metrics.assess_competitive_position(
    company_size="large",
    industry="technology",
    current_adoption=0.85
)

# Generate recommendations
recommendations = business_metrics.generate_recommendations(
    current_state=adoption_data,
    target_metrics={'adoption_rate': 0.9, 'roi': 3.5}
)
```

### ROI Calculator
```python
from business.roi_calculator import roi_calculator

# Calculate ROI projections
roi_analysis = roi_calculator.calculate_roi(
    investment_amount=1000000,
    implementation_timeline=12,
    industry="financial_services",
    company_size="large"
)

# Get industry benchmarks
benchmarks = roi_calculator.get_industry_benchmarks("healthcare")

# Generate ROI report
report = roi_calculator.generate_roi_report(
    scenarios=['conservative', 'realistic', 'optimistic']
)
```

### Causal Analysis
```python
from business.causal_analysis import causal_engine

# Run causal analysis
causal_results = causal_engine.analyze_adoption_factors(
    data=historical_data,
    outcome_variable='adoption_rate',
    treatment_variables=['investment', 'training', 'leadership_support']
)

# Get productivity insights
productivity_analysis = causal_engine.analyze_productivity_impact(
    productivity_data=productivity_df,
    adoption_data=adoption_df
)
```

## 🌐 Geographic APIs

### Geographic Data
```python
from data.geographic import get_geographic_data, get_country_details

# Get geographic adoption data
geo_data = get_geographic_data()

# Get country-specific details
country_info = get_country_details('United States')
policy_score = country_info['ai_policy_score']
investment_total = country_info['total_investment']

# Generate geographic insights
insights = generate_geographic_insights(geo_data)
top_regions = insights['top_adoption_regions']
```

### OECD Real-time Integration
```python
from data.oecd_realtime import OECDRealTimeClient

# Create OECD client
client = OECDRealTimeClient()

# Get real-time indicators
cli_data = client.get_cli_indicator(['USA', 'CHN', 'GBR'])
gdp_data = client.get_gdp_growth(['OECD'])
productivity_data = client.get_productivity_indicator(['G7'])

# Align time series
aligned_data = client.align_indicators(['CLI', 'GDP_GROWTH'], countries=['USA'])
```

## 🔄 Export APIs

### Data Export
```python
from exports.core import export_manager

# Export data to various formats
csv_export = export_manager.export_to_csv(
    data=historical_data,
    filename="ai_adoption_trends.csv"
)

excel_export = export_manager.export_to_excel(
    datasets={'Historical': historical_data, 'Sectors': sector_data},
    filename="ai_dashboard_data.xlsx"
)

# Export charts
chart_export = export_manager.export_chart(
    figure=plotly_figure,
    format='png',
    filename="adoption_chart.png"
)
```

## 🐛 Error Handling

### Custom Exceptions
```python
from data.loaders import DataLoadError
from data.models import ValidationError
from accessibility.accessibility_audit import AccessibilityError

try:
    data = load_dataset()
except DataLoadError as e:
    logger.error(f"Data loading failed: {e}")
    # Handle with fallback data
except ValidationError as e:
    logger.warning(f"Validation issues: {e}")
    # Handle with warnings
except AccessibilityError as e:
    logger.error(f"Accessibility compliance failed: {e}")
    # Handle with alternative rendering
```

### Graceful Degradation
```python
def safe_data_operation(operation_func, fallback_func):
    """Safely execute data operation with fallback"""
    try:
        return operation_func()
    except Exception as e:
        logger.warning(f"Operation failed: {e}")
        return fallback_func()

# Usage
data = safe_data_operation(
    operation_func=lambda: load_automated_data(),
    fallback_func=lambda: load_manual_data()
)
```

## 📚 Usage Examples

### Complete Dashboard Integration
```python
# Initialize the dashboard with all features
from accessibility.integrate_accessibility import initialize_accessibility
from data.pipeline_integration import load_all_datasets_integrated

# Setup
initialize_accessibility()

# Load data
datasets, metadata = load_all_datasets_integrated()

# Create accessible visualizations
from accessibility.integrate_accessibility import make_chart_accessible

fig = create_historical_trends_chart(datasets['historical_data'])
make_chart_accessible(
    fig=fig,
    title="AI Adoption Trends 2017-2025",
    description="Line chart showing AI adoption rising from 20% in 2017 to 78% in 2024",
    data=datasets['historical_data']
)

# Display integration status
strategy = metadata['integration_strategy']['primary_method']
st.info(f"Data loaded using {strategy} method")
```

### Custom Data Pipeline
```python
# Create custom data processing pipeline
from data.pdf_data_pipeline import PDFTextProcessor
from data.models import safe_validate_data

processor = PDFTextProcessor()

# Process custom PDF
text = processor.extract_text_from_pdf('custom_report.pdf')
tables = processor.extract_tables_from_pdf('custom_report.pdf')
statistics = processor.extract_statistics(text)

# Validate extracted data
custom_data = create_dataframe_from_statistics(statistics)
validation_result = safe_validate_data(custom_data, "Custom Dataset")

if validation_result.is_valid:
    # Use the data
    display_custom_analysis(custom_data)
else:
    # Handle validation errors
    st.error(f"Data validation failed: {validation_result.errors}")
```

## 🔗 API Response Formats

### Standard Response Format
```python
{
    "data": pd.DataFrame,           # Main data payload
    "metadata": {                   # Response metadata
        "source": str,              # Data source identifier
        "timestamp": str,           # ISO timestamp
        "method": str,              # Loading method used
        "validation": {             # Validation results
            "is_valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }
    },
    "performance": {                # Performance metrics
        "load_time": float,         # Seconds
        "memory_usage": int,        # Bytes
        "cache_hit": bool          # Cache status
    }
}
```

### Error Response Format
```python
{
    "error": {
        "type": str,                # Error type
        "message": str,             # Human-readable message
        "code": int,                # Error code
        "details": Dict[str, Any],  # Additional context
        "timestamp": str,           # ISO timestamp
        "traceback": str            # Stack trace (dev mode only)
    },
    "fallback": {                   # Fallback data if available
        "data": pd.DataFrame,
        "source": str,
        "quality": str              # "degraded" | "cached" | "sample"
    }
}
```

---

This API documentation provides comprehensive coverage of all public interfaces in the AI Adoption Dashboard. For implementation examples and best practices, refer to the test files and example code in the repository.