import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

@pytest.fixture
def sample_historical_data():
    """Sample historical AI adoption data"""
    return pd.DataFrame({
        'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [5.8, 12.1, 18.5, 27.3, 37.2, 55.0, 78.0, 82.1],
        'genai_use': [0, 0, 0, 2.1, 33.0, 50.0, 70.0, 75.0],
        'confidence_level': [0.8, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95, 0.92]
    })

@pytest.fixture
def sample_sector_data():
    """Sample sector adoption and ROI data"""
    return pd.DataFrame({
        'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                   'Retail', 'Education', 'Energy', 'Government'],
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'avg_roi': [4.2, 3.8, 3.1, 2.9, 3.3, 2.7, 2.5, 2.2],
        'genai_adoption': [85, 70, 60, 55, 60, 50, 45, 40],
        'avg_implementation_time': [8, 12, 15, 18, 14, 20, 22, 24]  # months
    })

@pytest.fixture
def sample_investment_data():
    """Sample AI investment data"""
    return pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'total_investment': [67.9, 124.5, 174.5, 207.8, 252.3],
        'genai_investment': [0.5, 2.1, 5.2, 18.7, 33.9],
        'private_investment': [45.2, 89.3, 142.1, 169.4, 201.8],
        'public_investment': [22.7, 35.2, 32.4, 38.4, 50.5]
    })

@pytest.fixture
def sample_cost_data():
    """Sample AI cost reduction data"""
    return pd.DataFrame({
        'model': ['GPT-3 (2020)', 'GPT-3.5 (2022)', 'GPT-4 (2023)', 'GPT-4 Turbo (2024)'],
        'cost_per_million_tokens': [20.0, 2.0, 0.50, 0.07],
        'year': [2020, 2022, 2023, 2024],
        'performance_score': [65, 78, 89, 92]
    })

@pytest.fixture
def sample_firm_size_data():
    """Sample data by firm size"""
    return pd.DataFrame({
        'size': ['1-50', '51-250', '251-1000', '1000-5000', '5000+'],
        'adoption': [3, 12, 25, 42, 58],
        'avg_investment': [15000, 75000, 250000, 850000, 2500000],
        'success_rate': [0.65, 0.72, 0.78, 0.83, 0.87]
    })

@pytest.fixture
def empty_dataframe():
    """Empty DataFrame for testing edge cases"""
    return pd.DataFrame()

@pytest.fixture
def invalid_dataframe():
    """DataFrame with invalid/missing data"""
    return pd.DataFrame({
        'col1': [1, 2, None, 4],
        'col2': ['a', None, 'c', 'd'],
        'col3': [np.nan, 2.5, 3.7, np.inf]
    })

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components for testing"""
    mock_st = Mock()
    mock_st.sidebar = Mock()
    mock_st.columns = Mock(return_value=[Mock(), Mock(), Mock()])
    mock_st.metric = Mock()
    mock_st.plotly_chart = Mock()
    mock_st.dataframe = Mock()
    mock_st.success = Mock()
    mock_st.warning = Mock()
    mock_st.error = Mock()
    mock_st.info = Mock()
    return mock_st

@pytest.fixture
def sample_competitive_assessment():
    """Sample competitive assessment data"""
    from business.metrics import CompetitivePosition
    
    class MockAssessment:
        def __init__(self):
            self.position = CompetitivePosition.COMPETITIVE
            self.score = 65.5
            self.gap_analysis = "Your organization is keeping pace with industry adoption..."
            self.recommendations = [
                "Accelerate pilot programs to production",
                "Invest in AI talent development",
                "Establish governance framework"
            ]
            self.risk_factors = ["Talent shortage", "Technology integration complexity"]
            self.opportunities = ["Process automation", "Customer experience enhancement"]
            self.industry_benchmark = 75
            self.size_benchmark = 42
            self.urgency_level = 6
    
    return MockAssessment()

@pytest.fixture
def sample_investment_case():
    """Sample investment case data"""
    from business.metrics import InvestmentRecommendation
    
    class MockInvestmentCase:
        def __init__(self):
            self.investment_amount = 500000
            self.timeline_months = 12
            self.expected_roi = 3.2
            self.total_return = 1600000
            self.net_benefit = 1100000
            self.payback_months = 8
            self.monthly_benefit = 91667
            self.confidence_level = "High"
            self.recommendation = InvestmentRecommendation.APPROVE
            self.risk_factors = ["Implementation complexity", "Change management"]
            self.success_factors = ["Strong leadership support", "Clear use cases"]
            self.market_context = "Technology sector shows 92% adoption with 4.2x average ROI"
    
    return MockInvestmentCase()

# Test data generators for property-based testing
from hypothesis import strategies as st

@st.composite
def generate_historical_data(draw):
    """Generate random but realistic historical data"""
    years = draw(st.lists(st.integers(min_value=2017, max_value=2025), 
                         min_size=3, max_size=8, unique=True))
    years.sort()
    
    ai_adoption = []
    genai_adoption = []
    
    # Generate realistic adoption curves
    for i, year in enumerate(years):
        if year < 2022:
            ai_rate = draw(st.floats(min_value=1, max_value=30))
            genai_rate = 0
        elif year == 2022:
            ai_rate = draw(st.floats(min_value=25, max_value=45))
            genai_rate = draw(st.floats(min_value=0, max_value=5))
        else:
            ai_rate = draw(st.floats(min_value=50, max_value=95))
            genai_rate = draw(st.floats(min_value=30, max_value=80))
        
        ai_adoption.append(ai_rate)
        genai_adoption.append(genai_rate)
    
    return pd.DataFrame({
        'year': years,
        'ai_use': ai_adoption,
        'genai_use': genai_adoption
    })

@st.composite
def generate_sector_data(draw):
    """Generate random but realistic sector data"""
    sectors = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 
               'Retail', 'Education', 'Energy', 'Government']
    
    selected_sectors = draw(st.lists(st.sampled_from(sectors), 
                                   min_size=3, max_size=len(sectors), unique=True))
    
    return pd.DataFrame({
        'sector': selected_sectors,
        'adoption_rate': draw(st.lists(st.floats(min_value=20, max_value=95), 
                                     min_size=len(selected_sectors), 
                                     max_size=len(selected_sectors))),
        'avg_roi': draw(st.lists(st.floats(min_value=1.5, max_value=5.0), 
                               min_size=len(selected_sectors), 
                               max_size=len(selected_sectors)))
    })

# Performance test fixtures
@pytest.fixture
def large_dataset():
    """Large dataset for performance testing"""
    np.random.seed(42)  # For reproducible tests
    n_rows = 50000
    
    return pd.DataFrame({
        'year': np.random.choice(range(2020, 2026), n_rows),
        'sector': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Retail'], n_rows),
        'adoption_rate': np.random.uniform(10, 95, n_rows),
        'roi': np.random.uniform(1.5, 5.0, n_rows),
        'investment': np.random.uniform(10000, 10000000, n_rows)
    })

@pytest.fixture(scope="session")
def benchmark_data():
    """Benchmark data that persists across test session"""
    return {
        'load_time_threshold': 2.0,  # seconds
        'memory_threshold': 100,      # MB
        'chart_render_threshold': 1.0 # seconds
    }

# Mock external dependencies
@pytest.fixture
def mock_plotly():
    """Mock Plotly for testing"""
    mock_fig = Mock()
    mock_fig.add_trace = Mock()
    mock_fig.update_layout = Mock()
    mock_fig.show = Mock()
    return mock_fig

@pytest.fixture
def mock_data_loader():
    """Mock data loader for testing"""
    def _loader(data_type=None):
        if data_type == "historical":
            return sample_historical_data()
        elif data_type == "sector":
            return sample_sector_data()
        else:
            return {
                'historical_data': sample_historical_data(),
                'sector_2025': sample_sector_data(),
                'investment_data': sample_investment_data()
            }
    return _loader 