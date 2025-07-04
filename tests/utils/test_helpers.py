"""Test helper utilities."""

import streamlit as st
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional
from contextlib import contextmanager
import tempfile
import os


class StreamlitTestHelper:
    """Helper class for testing Streamlit components."""
    
    @staticmethod
    @contextmanager
    def mock_streamlit():
        """Context manager to mock Streamlit components."""
        with patch('streamlit.write') as mock_write, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.dataframe') as mock_dataframe, \
             patch('streamlit.expander') as mock_expander, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.slider') as mock_slider, \
             patch('streamlit.session_state', MockSessionState()):
            
            # Configure return values
            mock_columns.return_value = [Mock(), Mock(), Mock(), Mock()]
            mock_expander.return_value.__enter__ = Mock(return_value=Mock())
            mock_expander.return_value.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [Mock(), Mock(), Mock()]
            mock_button.return_value = False
            
            yield {
                'write': mock_write,
                'markdown': mock_markdown,
                'columns': mock_columns,
                'metric': mock_metric,
                'plotly_chart': mock_plotly,
                'dataframe': mock_dataframe,
                'expander': mock_expander,
                'tabs': mock_tabs,
                'button': mock_button,
                'selectbox': mock_selectbox,
                'slider': mock_slider
            }
    
    @staticmethod
    def verify_metric_called(mock_metric, label: str, value: Any):
        """Verify st.metric was called with specific parameters."""
        for call in mock_metric.call_args_list:
            args, kwargs = call
            if args and args[0] == label:
                if 'value' in kwargs and kwargs['value'] == value:
                    return True
                if len(args) > 1 and args[1] == value:
                    return True
        return False
    
    @staticmethod
    def get_markdown_content(mock_markdown) -> List[str]:
        """Extract all markdown content from calls."""
        content = []
        for call in mock_markdown.call_args_list:
            args, kwargs = call
            if args:
                content.append(args[0])
        return content


class MockSessionState:
    """Mock Streamlit session state for testing."""
    
    def __init__(self):
        self._state = {}
    
    def __getattr__(self, key):
        return self._state.get(key)
    
    def __setattr__(self, key, value):
        if key == '_state':
            super().__setattr__(key, value)
        else:
            self._state[key] = value
    
    def __getitem__(self, key):
        return self._state.get(key)
    
    def __setitem__(self, key, value):
        self._state[key] = value
    
    def get(self, key, default=None):
        return self._state.get(key, default)
    
    def update(self, items):
        self._state.update(items)


def create_test_dataframe(rows: int = 100, 
                         columns: List[str] = None,
                         dtypes: Dict[str, type] = None) -> pd.DataFrame:
    """Create a test DataFrame with specified characteristics."""
    if columns is None:
        columns = ['col1', 'col2', 'col3']
    
    if dtypes is None:
        dtypes = {col: float for col in columns}
    
    data = {}
    for col, dtype in dtypes.items():
        if dtype == float:
            data[col] = np.random.randn(rows)
        elif dtype == int:
            data[col] = np.random.randint(0, 100, rows)
        elif dtype == str:
            data[col] = [f'value_{i}' for i in range(rows)]
        elif dtype == bool:
            data[col] = np.random.choice([True, False], rows)
    
    return pd.DataFrame(data)


@contextmanager
def temporary_file(content: str, suffix: str = '.txt'):
    """Create a temporary file with content."""
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        yield temp_path
    finally:
        os.unlink(temp_path)


def assert_called_with_partial(mock_obj, **expected_kwargs):
    """Assert mock was called with at least the expected kwargs."""
    for call in mock_obj.call_args_list:
        _, actual_kwargs = call
        if all(actual_kwargs.get(k) == v for k, v in expected_kwargs.items()):
            return True
    
    raise AssertionError(
        f"Mock not called with expected kwargs: {expected_kwargs}\n"
        f"Actual calls: {mock_obj.call_args_list}"
    )


def mock_pdf_extractor():
    """Create a mock PDF extractor."""
    mock = MagicMock()
    mock.extract_text.return_value = "Sample PDF text content"
    mock.extract_tables.return_value = [
        pd.DataFrame({
            'Column1': ['A', 'B', 'C'],
            'Column2': [1, 2, 3]
        })
    ]
    return mock


def verify_data_structure(data: Any, expected_type: type, 
                         required_keys: Optional[List[str]] = None):
    """Verify data structure matches expected format."""
    assert isinstance(data, expected_type), \
        f"Expected {expected_type}, got {type(data)}"
    
    if required_keys and isinstance(data, dict):
        missing_keys = set(required_keys) - set(data.keys())
        assert not missing_keys, \
            f"Missing required keys: {missing_keys}"


def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, 
                      tolerance: float = 0.01) -> bool:
    """Compare two DataFrames with numeric tolerance."""
    if df1.shape != df2.shape:
        return False
    
    if list(df1.columns) != list(df2.columns):
        return False
    
    for col in df1.columns:
        if df1[col].dtype in [float, np.float64]:
            if not np.allclose(df1[col], df2[col], rtol=tolerance, equal_nan=True):
                return False
        else:
            if not df1[col].equals(df2[col]):
                return False
    
    return True


class PerformanceTimer:
    """Context manager for timing code execution."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print(f"{self.name} took {self.duration:.3f} seconds")
    
    def assert_faster_than(self, seconds: float):
        """Assert operation completed within time limit."""
        assert self.duration is not None, "Timer not used in context"
        assert self.duration < seconds, \
            f"{self.name} took {self.duration:.3f}s, expected < {seconds}s"


def mock_cache():
    """Create a mock cache for testing."""
    cache_data = {}
    
    def get(key, default=None):
        return cache_data.get(key, default)
    
    def set(key, value):
        cache_data[key] = value
    
    def clear():
        cache_data.clear()
    
    mock = MagicMock()
    mock.get = get
    mock.set = set
    mock.clear = clear
    mock.data = cache_data
    
    return mock