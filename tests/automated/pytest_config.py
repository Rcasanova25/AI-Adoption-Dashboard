"""
Pytest Configuration for Automated Testing
Custom configuration, fixtures, and markers for the test suite
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
import tempfile
import os
from unittest.mock import Mock, patch

# Import modules that need testing
try:
    from data.pipeline_integration import integration_manager
    from data.automated_loaders import automated_loader
    from data.models import safe_validate_data
except ImportError:
    # Handle case where modules aren't available in test environment
    integration_manager = None
    automated_loader = None
    safe_validate_data = None


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "accessibility: marks tests as accessibility tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Mark tests containing certain keywords
        if "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
        
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)
        
        if "accessibility" in item.nodeid.lower():
            item.add_marker(pytest.mark.accessibility)
        
        if "test_large" in item.nodeid.lower() or "test_memory" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)


# Global fixtures available to all tests
@pytest.fixture(scope="session")
def test_data_dir():
    """Temporary directory for test data"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="session") 
def sample_pdf_content():
    """Sample PDF content for testing extraction"""
    return """
    AI Adoption Report 2024
    
    Key Findings:
    • AI adoption reached 78% in 2024
    • GenAI adoption reached 71% in 2024
    • Technology sector leads with 92% adoption
    • Financial services at 85% adoption
    
    Investment Data:
    Total AI investment: $252.3 billion
    GenAI investment: $33.9 billion
    
    Productivity Impact:
    • 15-25% productivity gains reported
    • Cost savings of 7-8% on average
    • Revenue increases of 3-4%
    """


@pytest.fixture
def valid_historical_data():
    """Standard valid historical data for testing"""
    return pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'ai_use': [45.0, 50.0, 55.0, 65.0, 78.0],
        'genai_use': [0.0, 0.0, 33.0, 55.0, 71.0],
        'data_source': ['Stanford AI Index'] * 5,
        'confidence_level': ['High'] * 5
    })


@pytest.fixture
def valid_sector_data():
    """Standard valid sector data for testing"""
    return pd.DataFrame({
        'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing'],
        'adoption_rate': [92.0, 85.0, 78.0, 75.0],
        'genai_adoption': [88.0, 78.0, 65.0, 58.0],
        'avg_roi': [4.2, 3.8, 3.2, 3.5],
        'data_source': ['McKinsey Global Survey 2024'] * 4
    })


@pytest.fixture 
def valid_financial_data():
    """Standard valid financial impact data for testing"""
    return pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'IT'],
        'companies_reporting_revenue_gains': [71, 57, 63, 40],
        'companies_reporting_cost_savings': [38, 49, 43, 37],
        'avg_cost_reduction': [7, 8, 9, 7],
        'avg_revenue_increase': [4, 3, 4, 3],
        'data_source': ['McKinsey Global Survey 2024'] * 4
    })


@pytest.fixture
def invalid_data_samples():
    """Various invalid data samples for testing error handling"""
    return {
        'empty_df': pd.DataFrame(),
        'none_value': None,
        'missing_columns': pd.DataFrame({'wrong_col': [1, 2, 3]}),
        'invalid_types': pd.DataFrame({
            'year': ['not_a_year', 'also_not_a_year'],
            'ai_use': ['not_a_number', 'also_not_a_number']
        }),
        'out_of_range': pd.DataFrame({
            'year': [2024, 2025],
            'ai_use': [150.0, -50.0],  # Invalid percentages
            'genai_use': [71.0, 80.0]
        }),
        'inconsistent_data': pd.DataFrame({
            'year': [2024, 2024],
            'ai_use': [78.0, 78.0],
            'genai_use': [85.0, 85.0]  # GenAI > AI (invalid)
        })
    }


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for view testing"""
    class MockStreamlit:
        def __init__(self):
            self.outputs = []
            self.warnings = []
            self.errors = []
            self.plots = []
            
        def write(self, content):
            self.outputs.append(('write', content))
            
        def warning(self, content):
            self.warnings.append(content)
            
        def error(self, content):
            self.errors.append(content)
            
        def plotly_chart(self, fig, **kwargs):
            self.plots.append(fig)
            
        def metric(self, label, value, delta=None):
            self.outputs.append(('metric', label, value, delta))
            
        def columns(self, spec):
            return [Mock() for _ in range(spec if isinstance(spec, int) else len(spec))]
            
        def expander(self, label):
            return Mock()
            
        def button(self, label, key=None):
            return False
            
        def info(self, content):
            self.outputs.append(('info', content))
            
        def success(self, content):
            self.outputs.append(('success', content))
    
    return MockStreamlit()


@pytest.fixture
def mock_pdf_files(test_data_dir):
    """Mock PDF files for testing PDF extraction"""
    pdf_dir = test_data_dir / "pdfs"
    pdf_dir.mkdir()
    
    # Create mock PDF files
    pdf_files = []
    for i, filename in enumerate([
        "stanford_ai_index_2025.pdf",
        "mckinsey_ai_survey_2024.pdf", 
        "goldman_sachs_ai_impact.pdf"
    ]):
        pdf_path = pdf_dir / filename
        pdf_path.write_text(f"Mock PDF content for {filename}")
        pdf_files.append(pdf_path)
    
    return pdf_files


@pytest.fixture
def mock_extraction_results():
    """Mock results from PDF extraction"""
    return {
        'historical_data': pd.DataFrame({
            'year': [2023, 2024],
            'ai_use': [65.0, 78.0],
            'genai_use': [55.0, 71.0],
            'source': ['Auto-extracted'] * 2
        }),
        'sector_data': pd.DataFrame({
            'sector': ['Technology', 'Finance'],
            'adoption_rate': [92.0, 85.0],
            'source': ['Auto-extracted'] * 2
        }),
        'metadata': {
            'extraction_date': '2024-01-01',
            'files_processed': 3,
            'success_rate': 100.0
        }
    }


@pytest.fixture(scope="session")
def integration_test_setup():
    """Setup for integration tests"""
    # Only run if integration components are available
    if integration_manager is None or automated_loader is None:
        pytest.skip("Integration components not available")
    
    return {
        'integration_manager': integration_manager,
        'automated_loader': automated_loader,
        'validator': safe_validate_data
    }


@pytest.fixture
def performance_test_data():
    """Large datasets for performance testing"""
    np.random.seed(42)  # For reproducible tests
    
    return {
        'large_historical': pd.DataFrame({
            'year': np.random.choice(range(2020, 2025), 10000),
            'ai_use': np.random.uniform(30, 95, 10000),
            'genai_use': np.random.uniform(20, 80, 10000)
        }),
        'large_sector': pd.DataFrame({
            'sector': np.random.choice(['Tech', 'Finance', 'Healthcare'], 5000),
            'adoption_rate': np.random.uniform(40, 95, 5000),
            'genai_adoption': np.random.uniform(30, 85, 5000)
        })
    }


# Custom assertions
def assert_valid_dataframe(df, name="DataFrame"):
    """Custom assertion for DataFrame validity"""
    assert df is not None, f"{name} should not be None"
    assert isinstance(df, pd.DataFrame), f"{name} should be a DataFrame"
    assert not df.empty, f"{name} should not be empty"


def assert_valid_percentage(value, name="Value"):
    """Custom assertion for percentage values"""
    assert isinstance(value, (int, float)), f"{name} should be numeric"
    assert 0 <= value <= 100, f"{name} should be between 0 and 100"


def assert_valid_year(year, name="Year"):
    """Custom assertion for year values"""
    assert isinstance(year, int), f"{name} should be an integer"
    assert 2017 <= year <= 2025, f"{name} should be between 2017 and 2025"


# Test utilities
class TestHelpers:
    """Helper methods for testing"""
    
    @staticmethod
    def create_mock_datasets(size: int = 100) -> Dict[str, pd.DataFrame]:
        """Create mock datasets for testing"""
        np.random.seed(42)
        
        return {
            'historical_data': pd.DataFrame({
                'year': np.random.choice(range(2020, 2025), size),
                'ai_use': np.random.uniform(30, 95, size),
                'genai_use': np.random.uniform(20, 80, size)
            }),
            'sector_data': pd.DataFrame({
                'sector': np.random.choice(['Tech', 'Finance', 'Healthcare'], size//2),
                'adoption_rate': np.random.uniform(40, 95, size//2)
            })
        }
    
    @staticmethod
    def validate_test_output(output, expected_keys: list):
        """Validate test output structure"""
        assert isinstance(output, dict), "Output should be a dictionary"
        for key in expected_keys:
            assert key in output, f"Output should contain key: {key}"
    
    @staticmethod
    def mock_streamlit_components():
        """Create comprehensive Streamlit mocks"""
        with patch.multiple(
            'streamlit',
            write=Mock(),
            warning=Mock(), 
            error=Mock(),
            plotly_chart=Mock(),
            metric=Mock(),
            columns=Mock(return_value=[Mock(), Mock()]),
            expander=Mock(),
            button=Mock(return_value=False),
            info=Mock(),
            success=Mock()
        ) as mocks:
            return mocks


@pytest.fixture
def test_helpers():
    """Provide test helper utilities"""
    return TestHelpers


# Parameterized test data
@pytest.fixture(params=[
    {'year': 2024, 'ai_use': 78.0, 'genai_use': 71.0},
    {'year': 2023, 'ai_use': 65.0, 'genai_use': 55.0},
    {'year': 2022, 'ai_use': 55.0, 'genai_use': 33.0}
])
def historical_data_point(request):
    """Parameterized historical data points"""
    return request.param


@pytest.fixture(params=[
    {'sector': 'Technology', 'adoption_rate': 92.0},
    {'sector': 'Financial Services', 'adoption_rate': 85.0},
    {'sector': 'Healthcare', 'adoption_rate': 78.0}
])
def sector_data_point(request):
    """Parameterized sector data points"""
    return request.param