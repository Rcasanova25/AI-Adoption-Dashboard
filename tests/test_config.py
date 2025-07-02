"""
Test configuration and utilities for AI Adoption Dashboard testing suite
Provides test settings, mock objects, and utility functions
"""

import os
import sys
import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any, List, Optional
import tempfile
import shutil
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration
TEST_CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'chunk_size': 1000,
    'performance_threshold_ms': 5000,
    'memory_threshold_mb': 500,
    'cache_ttl': 300,  # Shorter for tests
    'test_data_dir': 'tests/fixtures',
    'temp_dir': 'tests/temp',
    'coverage_threshold': 80,
    'parallel_workers': 2
}

# Test environment setup
TEST_ENV = {
    'TESTING': 'true',
    'STREAMLIT_SERVER_HEADLESS': 'true',
    'STREAMLIT_SERVER_PORT': '8501',
    'CACHE_DISABLED': 'true',
    'LOG_LEVEL': 'DEBUG'
}

# Mock Streamlit components
class MockStreamlit:
    """Mock Streamlit interface for testing"""
    
    def __init__(self):
        self.session_state = {}
        self.sidebar = MockSidebar()
        self.columns_data = []
        self.metrics_data = []
        self.charts_data = []
        self.downloads_data = []
        
    def write(self, text):
        return text
        
    def markdown(self, text):
        return text
        
    def subheader(self, text):
        return text
        
    def metric(self, label, value, delta=None, delta_color="normal"):
        metric_data = {'label': label, 'value': value, 'delta': delta}
        self.metrics_data.append(metric_data)
        return metric_data
        
    def columns(self, num_cols):
        cols = [MockColumn(i) for i in range(num_cols)]
        self.columns_data.append(cols)
        return cols
        
    def tabs(self, tab_names):
        return [MockTab(name) for name in tab_names]
        
    def selectbox(self, label, options, index=0, help=None):
        return options[index] if options else None
        
    def multiselect(self, label, options, default=None):
        return default or []
        
    def slider(self, label, min_value, max_value, value=None, step=1):
        return value or min_value
        
    def button(self, label, key=None, help=None):
        return False  # Default to not clicked
        
    def plotly_chart(self, fig, use_container_width=True):
        chart_data = {'type': 'plotly', 'figure': fig}
        self.charts_data.append(chart_data)
        return chart_data
        
    def dataframe(self, data, hide_index=True, use_container_width=True):
        return data
        
    def download_button(self, label, data, file_name, mime=None, key=None, help=None):
        download_data = {
            'label': label, 
            'data': data, 
            'file_name': file_name,
            'key': key
        }
        self.downloads_data.append(download_data)
        return download_data
        
    def success(self, text):
        return text
        
    def info(self, text):
        return text
        
    def warning(self, text):
        return text
        
    def error(self, text):
        return text
        
    def expander(self, label, expanded=False):
        return MockExpander(label, expanded)
        
    def spinner(self, text="Loading..."):
        return MockSpinner(text)
        
    def progress(self, value):
        return value
        
    def cache_data(self, ttl=None, show_spinner=True):
        def decorator(func):
            return func  # No caching in tests
        return decorator


class MockSidebar:
    """Mock Streamlit sidebar"""
    
    def __init__(self):
        self.components = []
        
    def selectbox(self, label, options, index=0):
        return options[index] if options else None
        
    def slider(self, label, min_value, max_value, value=None):
        return value or min_value
        
    def button(self, label):
        return False


class MockColumn:
    """Mock Streamlit column"""
    
    def __init__(self, index):
        self.index = index
        self.content = []
        
    def metric(self, label, value, delta=None):
        metric = {'label': label, 'value': value, 'delta': delta}
        self.content.append(metric)
        return metric
        
    def plotly_chart(self, fig, use_container_width=True):
        chart = {'type': 'plotly', 'figure': fig}
        self.content.append(chart)
        return chart
        
    def write(self, text):
        self.content.append(text)
        return text


class MockTab:
    """Mock Streamlit tab"""
    
    def __init__(self, name):
        self.name = name
        self.content = []
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockExpander:
    """Mock Streamlit expander"""
    
    def __init__(self, label, expanded=False):
        self.label = label
        self.expanded = expanded
        self.content = []
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockSpinner:
    """Mock Streamlit spinner"""
    
    def __init__(self, text):
        self.text = text
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Mock Plotly figures
class MockPlotlyFigure:
    """Mock Plotly figure for testing"""
    
    def __init__(self, data=None, layout=None):
        self.data = data or []
        self.layout = layout or {}
        self.traces = []
        
    def add_trace(self, trace):
        self.traces.append(trace)
        
    def update_layout(self, **kwargs):
        self.layout.update(kwargs)
        
    def update_xaxes(self, **kwargs):
        pass
        
    def update_yaxes(self, **kwargs):
        pass


# Test utilities
class TestUtils:
    """Utility functions for testing"""
    
    @staticmethod
    def create_temp_directory():
        """Create temporary directory for test files"""
        temp_dir = tempfile.mkdtemp(prefix='ai_dashboard_test_')
        return temp_dir
        
    @staticmethod
    def cleanup_temp_directory(temp_dir):
        """Clean up temporary directory"""
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            
    @staticmethod
    def assert_dataframe_equals(df1, df2, check_dtype=True, check_names=True):
        """Assert two DataFrames are equal with detailed error messages"""
        try:
            pd.testing.assert_frame_equal(df1, df2, check_dtype=check_dtype, check_names=check_names)
            return True
        except AssertionError as e:
            print(f"DataFrame assertion failed: {e}")
            print(f"DF1 shape: {df1.shape}, DF2 shape: {df2.shape}")
            print(f"DF1 columns: {df1.columns.tolist()}")
            print(f"DF2 columns: {df2.columns.tolist()}")
            raise
            
    @staticmethod
    def assert_dataframe_structure(df, expected_columns, min_rows=1):
        """Assert DataFrame has expected structure"""
        assert isinstance(df, pd.DataFrame), f"Expected DataFrame, got {type(df)}"
        assert len(df) >= min_rows, f"Expected at least {min_rows} rows, got {len(df)}"
        
        missing_cols = set(expected_columns) - set(df.columns)
        assert not missing_cols, f"Missing columns: {missing_cols}"
        
        extra_cols = set(df.columns) - set(expected_columns)
        if extra_cols:
            print(f"Extra columns found: {extra_cols}")
            
    @staticmethod
    def assert_performance(func, max_time_ms=5000, *args, **kwargs):
        """Assert function executes within time limit"""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = (time.time() - start_time) * 1000
        
        assert execution_time <= max_time_ms, (
            f"Function took {execution_time:.2f}ms, "
            f"expected <= {max_time_ms}ms"
        )
        return result
        
    @staticmethod
    def assert_memory_usage(func, max_memory_mb=500, *args, **kwargs):
        """Assert function uses less than specified memory"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        result = func(*args, **kwargs)
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        
        assert memory_used <= max_memory_mb, (
            f"Function used {memory_used:.2f}MB, "
            f"expected <= {max_memory_mb}MB"
        )
        return result
        
    @staticmethod
    def create_mock_research_integrator():
        """Create mock research integrator"""
        mock_integrator = Mock()
        mock_integrator.get_authentic_historical_data.return_value = TestDataFixtures.get_historical_data()
        mock_integrator.get_authentic_sector_data_2025.return_value = TestDataFixtures.get_sector_data()
        mock_integrator.get_authentic_investment_data.return_value = TestDataFixtures.get_investment_data()
        mock_integrator.get_authentic_financial_impact_data.return_value = TestDataFixtures.get_financial_impact_data()
        return mock_integrator


# Import test data fixtures
from tests.fixtures.test_data import TestDataFixtures


# pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    for key, value in TEST_ENV.items():
        os.environ[key] = value
    yield
    # Cleanup
    for key in TEST_ENV.keys():
        os.environ.pop(key, None)


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for testing views"""
    with patch('streamlit.write') as mock_write, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.subheader') as mock_subheader, \
         patch('streamlit.metric') as mock_metric, \
         patch('streamlit.columns') as mock_columns, \
         patch('streamlit.tabs') as mock_tabs, \
         patch('streamlit.plotly_chart') as mock_plotly, \
         patch('streamlit.dataframe') as mock_dataframe:
        
        mock_st = MockStreamlit()
        yield mock_st


@pytest.fixture
def temp_directory():
    """Temporary directory for test files"""
    temp_dir = TestUtils.create_temp_directory()
    yield temp_dir
    TestUtils.cleanup_temp_directory(temp_dir)


@pytest.fixture
def mock_research_integrator():
    """Mock research integrator"""
    return TestUtils.create_mock_research_integrator()