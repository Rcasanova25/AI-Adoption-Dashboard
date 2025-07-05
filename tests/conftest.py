"""Pytest configuration and shared fixtures for all tests."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models import (
    AdoptionMetrics,
    ROIMetrics,
    TokenEconomics,
)


@pytest.fixture
def sample_roi_metrics():
    """Create sample ROI metrics."""
    return ROIMetrics(
        expected_roi=185.5,
        payback_period_months=18,
        confidence_level="high",
        cost_breakdown={
            "Infrastructure": 250000,
            "Talent": 450000,
            "Training": 100000,
            "Maintenance": 150000,
        },
        benefit_breakdown={
            "Productivity": 850000,
            "Cost Savings": 650000,
            "Revenue Growth": 1250000,
        },
        risk_factors=["Implementation complexity", "Change management"],
    )


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    dates = pd.date_range(start="2020-01-01", end="2024-12-01", freq="M")
    return pd.DataFrame(
        {
            "date": dates,
            "adoption_rate": np.random.uniform(50, 95, len(dates)),
            "investment": np.random.uniform(100000, 1000000, len(dates)),
            "productivity_gain": np.random.uniform(5, 30, len(dates)),
        }
    )


@pytest.fixture
def mock_streamlit_state():
    """Mock Streamlit session state."""

    class MockSessionState:
        def __init__(self):
            self.data = {}

        def __getitem__(self, key):
            return self.data.get(key)

        def __setitem__(self, key, value):
            self.data[key] = value

        def get(self, key, default=None):
            return self.data.get(key, default)

        def update(self, items):
            self.data.update(items)

    return MockSessionState()


@pytest.fixture
def test_data_path():
    """Path to test data directory."""
    return Path(__file__).parent / "fixtures" / "test_data"


@pytest.fixture
def performance_threshold():
    """Performance testing thresholds."""
    return {
        "data_load_time": 1.0,  # seconds
        "view_render_time": 0.5,  # seconds
        "memory_usage": 500,  # MB
        "cache_hit_ratio": 0.8,  # 80%
    }


@pytest.fixture
def test_pdf_content():
    """Mock PDF content for testing extractors."""
    return {
        "text": """
        AI Adoption Report 2024
        
        Executive Summary:
        - Overall adoption rate: 87%
        - YoY growth: 15%
        - Leading industries: Technology, Finance, Healthcare
        
        Economic Impact:
        - GDP contribution: 7.2% by 2030
        - Job displacement: 12%
        - Job augmentation: 45%
        
        Investment Trends:
        - Average investment: $2.5M
        - ROI: 185%
        - Payback period: 18 months
        """,
        "tables": [
            pd.DataFrame(
                {
                    "Industry": ["Tech", "Finance", "Healthcare"],
                    "Adoption Rate": [92, 88, 75],
                    "Growth": [18, 15, 22],
                }
            )
        ],
    }


@pytest.fixture(autouse=True)
def reset_imports():
    """Reset imports between tests to avoid state pollution."""
    yield
    # Clean up any module-level state if needed


@pytest.fixture
def mock_plotly_figure():
    """Create a mock Plotly figure for testing."""
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4], y=[10, 15, 13, 17], mode="lines+markers", name="Test Data")
    )
    return fig


# Test environment configuration
@pytest.fixture(scope="session")
def test_env():
    """Configure test environment."""
    os.environ["TESTING"] = "true"
    os.environ["STREAMLIT_THEME_BASE"] = "light"
    yield
    os.environ.pop("TESTING", None)


# Utility functions for tests
def assert_dataframe_equal(df1: pd.DataFrame, df2: pd.DataFrame, **kwargs):
    """Assert two dataframes are equal with better error messages."""
    try:
        pd.testing.assert_frame_equal(df1, df2, **kwargs)
    except AssertionError as e:
        print(f"\nDataFrame comparison failed:")
        print(f"Expected shape: {df1.shape}, Actual shape: {df2.shape}")
        print(f"Expected columns: {list(df1.columns)}")
        print(f"Actual columns: {list(df2.columns)}")
        raise e


def create_test_file(path: Path, content: str):
    """Create a test file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


# Performance timing decorator
def time_function(func):
    """Decorator to time function execution."""
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n{func.__name__} took {end_time - start_time:.3f} seconds")
        return result

    return wrapper
