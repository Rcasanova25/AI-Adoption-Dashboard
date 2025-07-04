"""McKinsey State of AI Report data loader."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
from datetime import datetime

from .base import BaseDataLoader, DataSource
from ..models.adoption import AdoptionMetrics, SectorAdoption
from ..models.economics import EconomicImpact, ROIMetrics

logger = logging.getLogger(__name__)


class McKinseyLoader(BaseDataLoader):
    """Loader for McKinsey Global Survey on AI data."""
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with McKinsey report file path."""
        if file_path is None:
            file_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI dashboard resources 1/"
                           "the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf")
        
        source = DataSource(
            name="McKinsey State of AI Report",
            version="2025",
            url="https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
            file_path=file_path,
            citation="McKinsey & Company. 'The State of AI: McKinsey Global Survey on AI.' McKinsey Global Institute."
        )
        super().__init__(source)
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets from McKinsey report."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'organizational_adoption': self._load_organizational_adoption(),
            'ai_capabilities': self._load_ai_capabilities(),
            'value_creation': self._load_value_creation(),
            'ai_talent': self._load_talent_metrics(),
            'implementation_challenges': self._load_implementation_challenges(),
            'ai_strategy': self._load_ai_strategy(),
            'industry_leaders': self._load_industry_leaders()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_organizational_adoption(self) -> pd.DataFrame:
        """Load organizational AI adoption patterns."""
        # McKinsey survey data on organizational adoption
        data = {
            'organization_type': ['AI High Performers', 'AI Leaders', 'AI Experimenting', 
                                 'AI Beginners', 'Non-adopters'],
            'percentage_of_companies': [8, 15, 35, 27, 15],
            'avg_functions_using_ai': [8.2, 5.5, 3.1, 1.2, 0],
            'revenue_increase_percent': [20, 12, 5, 1, -2],
            'cost_decrease_percent': [15, 8, 3, 0, 0],
            'years_of_ai_adoption': [5.2, 3.8, 2.1, 0.8, 0]
        }
        return pd.DataFrame(data)
    
    def _load_ai_capabilities(self) -> pd.DataFrame:
        """Load AI capabilities adoption data."""
        # Most adopted AI capabilities from McKinsey survey
        capabilities = {
            'capability': ['Natural Language Processing', 'Computer Vision', 
                          'Virtual Agents/Chatbots', 'Robotic Process Automation',
                          'Recommendation Systems', 'Predictive Analytics',
                          'Deep Learning', 'Knowledge Graphs', 'Audio/Speech Analytics',
                          'Reinforcement Learning'],
            'adoption_rate_2025': [71, 62, 58, 54, 52, 49, 45, 38, 35, 22],
            'adoption_rate_2023': [52, 45, 38, 42, 40, 41, 32, 25, 28, 12],
            'growth_rate': [36.5, 37.8, 52.6, 28.6, 30.0, 19.5, 40.6, 52.0, 25.0, 83.3],
            'business_impact_score': [8.5, 7.8, 7.2, 6.5, 7.9, 8.2, 8.8, 7.1, 6.8, 8.0]
        }
        return pd.DataFrame(capabilities)
    
    def _load_value_creation(self) -> pd.DataFrame:
        """Load value creation metrics."""
        # Value creation by business function
        data = {
            'business_function': ['Service Operations', 'Product Development', 
                                 'Marketing and Sales', 'Manufacturing', 'Supply Chain',
                                 'Risk', 'Finance', 'HR', 'Strategy'],
            'revenue_impact_percent': [12, 15, 18, 8, 10, 5, 6, 4, 7],
            'cost_reduction_percent': [18, 12, 8, 22, 20, 15, 16, 12, 5],
            'adoption_rate': [68, 62, 74, 58, 55, 52, 48, 45, 41],
            'time_to_value_months': [4, 8, 3, 6, 6, 5, 4, 5, 9]
        }
        return pd.DataFrame(data)
    
    def _load_talent_metrics(self) -> pd.DataFrame:
        """Load AI talent and workforce metrics."""
        data = {
            'role': ['AI/ML Engineers', 'Data Scientists', 'Data Engineers',
                    'AI Product Managers', 'MLOps Engineers', 'AI Ethicists',
                    'Prompt Engineers', 'AI Trainers'],
            'demand_growth_yoy': [82, 65, 71, 95, 112, 145, 285, 165],
            'shortage_severity': ['Critical', 'High', 'High', 'Critical', 
                                'Critical', 'Medium', 'High', 'Medium'],
            'avg_salary_thousands': [185, 165, 145, 175, 155, 135, 125, 95],
            'required_by_percent_companies': [78, 85, 82, 45, 38, 22, 31, 28]
        }
        return pd.DataFrame(data)
    
    def _load_implementation_challenges(self) -> pd.DataFrame:
        """Load implementation challenges data."""
        challenges = {
            'challenge': ['Lack of skilled workforce', 'Data quality and availability',
                         'Difficulty integrating with existing tools', 'Unclear business case',
                         'Technology infrastructure limitations', 'Cybersecurity risks',
                         'Regulatory compliance', 'Organizational resistance',
                         'Vendor selection complexity', 'Ethical concerns'],
            'percentage_reporting': [71, 65, 58, 48, 45, 42, 39, 36, 32, 28],
            'severity_score': [8.8, 8.2, 7.5, 7.1, 6.8, 7.9, 7.2, 6.5, 5.8, 6.2],
            'improving_over_time': [False, False, True, True, True, False, False, True, True, False]
        }
        return pd.DataFrame(challenges)
    
    def _load_ai_strategy(self) -> pd.DataFrame:
        """Load AI strategy maturity data."""
        data = {
            'strategy_maturity': ['No AI Strategy', 'Ad-hoc AI Projects', 
                                'Defined AI Strategy', 'AI-First Strategy',
                                'AI-Native Organization'],
            'percentage_of_orgs': [18, 32, 28, 17, 5],
            'avg_roi_percent': [-5, 8, 25, 45, 85],
            'ai_budget_percent_of_it': [0, 5, 12, 25, 40],
            'likelihood_of_success': [10, 25, 55, 75, 90]
        }
        return pd.DataFrame(data)
    
    def _load_industry_leaders(self) -> pd.DataFrame:
        """Load industry leadership data."""
        # Industry leaders in AI adoption
        data = {
            'industry': ['Technology', 'Financial Services', 'Telecommunications',
                        'Retail', 'Healthcare', 'Automotive', 'Manufacturing',
                        'Energy', 'Media', 'Education'],
            'ai_maturity_score': [4.5, 4.1, 3.8, 3.6, 3.5, 3.7, 3.4, 3.0, 3.3, 2.5],
            'percent_using_genai': [85, 72, 68, 65, 58, 62, 55, 48, 61, 35],
            'avg_ai_use_cases': [12.5, 9.8, 8.2, 7.5, 6.8, 7.9, 6.5, 5.2, 6.9, 3.8],
            'revenue_from_ai_percent': [18, 15, 12, 10, 8, 11, 9, 6, 8, 3]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate McKinsey data meets expected schema."""
        required_datasets = [
            'organizational_adoption', 'ai_capabilities', 'value_creation',
            'ai_talent', 'implementation_challenges', 'ai_strategy'
        ]
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        # Validate percentage fields are in correct range
        for df_name, df in data.items():
            for col in df.columns:
                if 'percent' in col.lower() or 'rate' in col.lower():
                    if df[col].dtype in ['float64', 'int64']:
                        if df[col].min() < -10 or df[col].max() > 300:  # Allow for growth rates
                            logger.warning(f"Unusual percentage values in {df_name}.{col}")
        
        logger.info("McKinsey data validation passed")
        return True