"""
Test data fixtures for AI Adoption Dashboard
Provides mock data for testing all components without relying on actual research files
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
import pytest


class TestDataFixtures:
    """Centralized test data fixtures for the AI Adoption Dashboard"""
    
    @staticmethod
    def get_historical_data() -> pd.DataFrame:
        """Mock historical AI adoption data"""
        return pd.DataFrame({
            'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [20, 47, 58, 50, 56, 50, 55, 78, 78],
            'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71],
            'data_source': ['Test Stanford AI Index'] * 9,
            'confidence_level': ['High'] * 9,
            'sample_size': [1000, 1200, 1400, 900, 1100, 1300, 1500, 1800, 2000]
        })
    
    @staticmethod
    def get_sector_data() -> pd.DataFrame:
        """Mock sector adoption data"""
        return pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing'],
            'adoption_rate': [92, 85, 78, 75],
            'genai_adoption': [88, 78, 65, 58],
            'avg_roi': [4.2, 3.8, 3.2, 3.5],
            'data_source': ['Test McKinsey Survey'] * 4,
            'survey_participants': [1363] * 4,
            'confidence_interval': ['±3%'] * 4
        })
    
    @staticmethod
    def get_investment_data() -> pd.DataFrame:
        """Mock AI investment data"""
        return pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'total_investment': [72.5, 112.3, 148.5, 174.6, 252.3],
            'genai_investment': [0, 0, 3.95, 28.5, 33.9],
            'us_investment': [31.2, 48.7, 64.3, 75.6, 109.1],
            'data_source': ['Test Investment Data'] * 5,
            'currency': ['USD Billions'] * 5
        })
    
    @staticmethod
    def get_financial_impact_data() -> pd.DataFrame:
        """Mock financial impact data"""
        return pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'IT'],
            'companies_reporting_cost_savings': [38, 49, 43, 37],
            'companies_reporting_revenue_gains': [71, 57, 63, 40],
            'avg_cost_reduction': [7, 8, 9, 7],
            'avg_revenue_increase': [4, 3, 4, 3],
            'data_source': ['Test Financial Impact'] * 4,
            'sample_size': [1363] * 4
        })
    
    @staticmethod
    def get_geographic_data() -> pd.DataFrame:
        """Mock geographic distribution data"""
        return pd.DataFrame({
            'region': ['North America', 'Europe', 'Asia Pacific', 'Latin America'],
            'adoption_rate': [65, 58, 72, 45],
            'investment_billions': [120.5, 85.3, 98.7, 25.1],
            'regulatory_maturity': [75, 82, 68, 55],
            'data_source': ['Test Geographic Data'] * 4
        })
    
    @staticmethod
    def get_token_economics_data() -> pd.DataFrame:
        """Mock token economics data"""
        return pd.DataFrame({
            'model_type': ['GPT-4', 'GPT-3.5', 'Claude', 'Gemini'],
            'cost_per_million_tokens': [30.0, 2.0, 15.0, 7.0],
            'performance_score': [95, 85, 90, 88],
            'tokens_per_second': [50, 100, 75, 80],
            'data_source': ['Test Token Economics'] * 4
        })
    
    @staticmethod
    def get_governance_data() -> pd.DataFrame:
        """Mock AI governance data"""
        return pd.DataFrame({
            'governance_domain': ['Data Privacy', 'Algorithm Transparency', 'Bias Mitigation', 'Safety Standards'],
            'maturity_level_current': [65, 45, 55, 70],
            'maturity_level_target': [85, 75, 80, 90],
            'implementation_priority': [90, 85, 88, 95],
            'business_impact_score': [80, 75, 82, 88],
            'regulatory_requirement_level': [95, 80, 85, 90],
            'data_source': ['Test Governance Framework'] * 4
        })
    
    @staticmethod
    def get_skills_gap_data() -> pd.DataFrame:
        """Mock skills gap analysis data"""
        return pd.DataFrame({
            'skill_category': ['Machine Learning', 'Data Science', 'AI Engineering', 'AI Ethics'],
            'demand_growth_percent': [150, 120, 180, 90],
            'supply_shortage_percent': [75, 65, 85, 45],
            'salary_premium_percent': [35, 25, 45, 20],
            'experience_years_required': [5, 4, 6, 3],
            'training_program_availability': [60, 75, 45, 85],
            'data_source': ['Test Skills Gap Analysis'] * 4
        })
    
    @staticmethod
    def get_meta_analysis_data() -> pd.DataFrame:
        """Mock comprehensive meta-analysis data"""
        return pd.DataFrame({
            'research_category': ['Adoption Rates', 'ROI Analysis', 'Implementation Barriers', 'Success Factors'],
            'studies_analyzed': [28, 24, 31, 27],
            'consensus_level': [92, 88, 85, 90],
            'meta_finding_score': [94, 91, 87, 93],
            'sample_size_total': [125000, 98000, 145000, 112000],
            'geographic_coverage': [45, 42, 48, 44],
            'time_span_years': [8, 7, 9, 8],
            'data_source': ['Test Meta-Analysis'] * 4
        })
    
    @staticmethod
    def get_future_trends_data() -> pd.DataFrame:
        """Mock future trends forecast data"""
        return pd.DataFrame({
            'trend_category': ['Generative AI Evolution', 'Autonomous Systems', 'AI Governance', 'Edge AI Computing'],
            'current_maturity_2024': [75, 45, 35, 52],
            'projected_maturity_2027': [92, 72, 68, 78],
            'projected_maturity_2030': [98, 89, 85, 91],
            'adoption_velocity': [23, 27, 33, 26],
            'market_impact_billions': [450, 280, 125, 195],
            'disruption_probability': [95, 78, 85, 82],
            'strategic_priority': ['Critical', 'High', 'High', 'High'],
            'data_source': ['Test Future Trends'] * 4
        })
    
    @staticmethod
    def get_sources_data() -> pd.DataFrame:
        """Mock sources metadata"""
        return pd.DataFrame({
            'source_name': ['Stanford AI Index', 'McKinsey Survey', 'Goldman Sachs Research', 'OECD Report'],
            'authority': ['Stanford HAI', 'McKinsey & Company', 'Goldman Sachs Research', 'OECD'],
            'credibility_rating': ['A+', 'A+', 'A+', 'A+'],
            'publication_year': [2025, 2024, 2024, 2024],
            'sample_size': [2000, 1363, 500, 1500],
            'geographic_scope': ['Global', 'Global', 'Global', 'OECD Countries']
        })
    
    @staticmethod
    def get_invalid_data() -> pd.DataFrame:
        """Mock invalid data for error testing"""
        return pd.DataFrame({
            'invalid_column': [None, '', 'bad_data'],
            'missing_values': [np.nan, np.nan, np.nan],
            'wrong_type': ['string', 'another_string', 'third_string']
        })
    
    @staticmethod
    def get_large_dataset(size: int = 10000) -> pd.DataFrame:
        """Generate large dataset for performance testing"""
        np.random.seed(42)  # For reproducible tests
        
        return pd.DataFrame({
            'id': range(size),
            'value': np.random.normal(100, 15, size),
            'category': np.random.choice(['A', 'B', 'C', 'D'], size),
            'timestamp': pd.date_range(start='2020-01-01', periods=size, freq='D'),
            'metric_1': np.random.exponential(scale=10, size=size),
            'metric_2': np.random.beta(2, 5, size),
            'text_field': [f'Sample text {i}' for i in range(size)],
            'boolean_field': np.random.choice([True, False], size)
        })
    
    @staticmethod
    def get_dashboard_data_complete() -> Dict[str, pd.DataFrame]:
        """Complete dashboard data dictionary for integration testing"""
        return {
            'historical_data': TestDataFixtures.get_historical_data(),
            'sector_2025': TestDataFixtures.get_sector_data(),
            'ai_investment': TestDataFixtures.get_investment_data(),
            'financial_impact': TestDataFixtures.get_financial_impact_data(),
            'geographic_data': TestDataFixtures.get_geographic_data(),
            'token_economics': TestDataFixtures.get_token_economics_data(),
            'ai_governance_framework': TestDataFixtures.get_governance_data(),
            'ai_skills_gap_analysis': TestDataFixtures.get_skills_gap_data(),
            'comprehensive_ai_adoption_meta_study': TestDataFixtures.get_meta_analysis_data(),
            'ai_future_trends_forecast': TestDataFixtures.get_future_trends_data(),
            'sources_data': TestDataFixtures.get_sources_data()
        }


# Pytest fixtures for use across test files
@pytest.fixture
def historical_data():
    """Historical AI adoption data fixture"""
    return TestDataFixtures.get_historical_data()


@pytest.fixture
def sector_data():
    """Sector adoption data fixture"""
    return TestDataFixtures.get_sector_data()


@pytest.fixture
def investment_data():
    """AI investment data fixture"""
    return TestDataFixtures.get_investment_data()


@pytest.fixture
def financial_impact_data():
    """Financial impact data fixture"""
    return TestDataFixtures.get_financial_impact_data()


@pytest.fixture
def geographic_data():
    """Geographic distribution data fixture"""
    return TestDataFixtures.get_geographic_data()


@pytest.fixture
def token_economics_data():
    """Token economics data fixture"""
    return TestDataFixtures.get_token_economics_data()


@pytest.fixture
def governance_data():
    """AI governance data fixture"""
    return TestDataFixtures.get_governance_data()


@pytest.fixture
def skills_gap_data():
    """Skills gap analysis data fixture"""
    return TestDataFixtures.get_skills_gap_data()


@pytest.fixture
def meta_analysis_data():
    """Meta-analysis data fixture"""
    return TestDataFixtures.get_meta_analysis_data()


@pytest.fixture
def future_trends_data():
    """Future trends data fixture"""
    return TestDataFixtures.get_future_trends_data()


@pytest.fixture
def sources_data():
    """Sources metadata fixture"""
    return TestDataFixtures.get_sources_data()


@pytest.fixture
def invalid_data():
    """Invalid data for error testing"""
    return TestDataFixtures.get_invalid_data()


@pytest.fixture
def large_dataset():
    """Large dataset for performance testing"""
    return TestDataFixtures.get_large_dataset()


@pytest.fixture
def complete_dashboard_data():
    """Complete dashboard data for integration testing"""
    return TestDataFixtures.get_dashboard_data_complete()


@pytest.fixture
def empty_dataframe():
    """Empty DataFrame for edge case testing"""
    return pd.DataFrame()


@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        'data_year': '2024',
        'view_type': 'Historical Trends',
        'cache_ttl': 3600,
        'max_retries': 3,
        'timeout': 30
    }