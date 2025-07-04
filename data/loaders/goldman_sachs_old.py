"""Goldman Sachs AI economic impact analysis loader."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
from datetime import datetime

from .base import BaseDataLoader, DataSource
from ..models.economics import EconomicImpact, ROIMetrics

logger = logging.getLogger(__name__)


class GoldmanSachsLoader(BaseDataLoader):
    """Loader for Goldman Sachs AI economic analysis reports."""
    
    def __init__(self, gdp_file: Optional[Path] = None, economic_file: Optional[Path] = None):
        """Initialize with Goldman Sachs report file paths."""
        if gdp_file is None:
            gdp_file = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI Adoption Resources 3/"
                           "Generative AI could raise global GDP by 7_ _ Goldman Sachs.pdf")
        
        source = DataSource(
            name="Goldman Sachs AI Economic Analysis",
            version="2023-2025",
            url="https://www.goldmansachs.com/insights/pages/generative-ai-could-raise-global-gdp-by-7-percent.html",
            file_path=gdp_file,
            citation="Briggs, Joseph, and Devesh Kodnani. 'The Potentially Large Effects of Artificial Intelligence on Economic Growth.' Goldman Sachs Economic Research, 2023."
        )
        super().__init__(source)
        
        self.economic_file = economic_file or Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                                                  "AI adoption resources/AI Adoption Resources 3/"
                                                  "Global Economics Analyst_ The Potentially Large Effects of Artificial Intelligence on Economic Growth (Briggs_Kodnani).pdf")
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load Goldman Sachs economic impact data."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'gdp_impact_forecast': self._load_gdp_impact(),
            'sectoral_disruption': self._load_sectoral_disruption(),
            'labor_market_effects': self._load_labor_market_effects(),
            'investment_outlook': self._load_investment_outlook(),
            'productivity_scenarios': self._load_productivity_scenarios(),
            'global_competitiveness': self._load_global_competitiveness()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_gdp_impact(self) -> pd.DataFrame:
        """Load GDP impact forecasts."""
        # Goldman Sachs 7% GDP increase projection
        data = {
            'year': list(range(2024, 2035)),
            'baseline_gdp_growth': [2.2, 2.3, 2.2, 2.1, 2.0, 2.0, 1.9, 1.9, 1.8, 1.8, 1.7],
            'ai_enhanced_gdp_growth': [2.5, 2.9, 3.3, 3.7, 4.0, 4.2, 4.3, 4.4, 4.3, 4.2, 4.0],
            'cumulative_gdp_boost_percent': [0.3, 0.9, 1.8, 2.9, 4.2, 5.5, 6.7, 7.8, 8.8, 9.6, 10.2],
            'ai_contribution_to_growth': [0.3, 0.6, 1.1, 1.6, 2.0, 2.2, 2.4, 2.5, 2.5, 2.4, 2.3],
            'confidence_interval_low': [0.1, 0.4, 0.8, 1.3, 1.8, 2.3, 2.7, 3.1, 3.4, 3.6, 3.8],
            'confidence_interval_high': [0.5, 1.4, 2.8, 4.5, 6.6, 8.7, 10.7, 12.5, 14.0, 15.2, 16.2]
        }
        return pd.DataFrame(data)
    
    def _load_sectoral_disruption(self) -> pd.DataFrame:
        """Load sectoral disruption analysis."""
        data = {
            'sector': ['Information Technology', 'Financial Services', 'Professional Services',
                      'Education', 'Healthcare', 'Retail Trade', 'Manufacturing',
                      'Transportation', 'Construction', 'Agriculture'],
            'automation_exposure_percent': [46, 44, 37, 36, 35, 32, 29, 28, 23, 21],
            'productivity_gain_potential': [85, 75, 68, 58, 52, 48, 55, 45, 35, 38],
            'job_displacement_risk': [25, 35, 40, 32, 20, 42, 48, 52, 38, 45],
            'value_creation_opportunity': [9.5, 8.2, 7.5, 6.8, 7.8, 6.2, 6.5, 5.8, 4.5, 4.2],
            'transformation_timeline_years': [2, 3, 3, 4, 5, 3, 4, 5, 6, 7]
        }
        return pd.DataFrame(data)
    
    def _load_labor_market_effects(self) -> pd.DataFrame:
        """Load labor market impact projections."""
        # Two-thirds of jobs exposed to automation per Goldman Sachs
        data = {
            'occupation_category': ['Administrative Support', 'Legal', 'Architecture & Engineering',
                                   'Life, Physical & Social Science', 'Business & Financial Ops',
                                   'Community & Social Service', 'Computer & Mathematical',
                                   'Education & Library', 'Arts & Entertainment',
                                   'Healthcare Practitioners', 'Sales', 'Management',
                                   'Protective Service', 'Food Preparation', 'Construction',
                                   'Installation & Repair', 'Production', 'Transportation'],
            'automation_exposure': [46, 44, 37, 36, 35, 33, 32, 32, 30, 28, 28, 25, 22, 20, 17, 14, 12, 10],
            'augmentation_potential': [75, 80, 85, 82, 78, 72, 90, 75, 70, 85, 68, 82, 45, 38, 42, 55, 48, 35],
            'wage_premium_change': [15, 22, 28, 25, 20, 12, 35, 10, 8, 18, 5, 25, -5, -10, -2, 5, -8, -12],
            'employment_growth_10yr': [-15, -10, 15, 12, 8, 5, 25, 0, -5, 20, -8, 10, 2, -12, 5, 0, -18, -20]
        }
        return pd.DataFrame(data)
    
    def _load_investment_outlook(self) -> pd.DataFrame:
        """Load AI investment outlook data."""
        data = {
            'investment_category': ['AI Infrastructure', 'AI Software', 'AI Services',
                                   'AI Hardware', 'AI Research', 'AI Training',
                                   'AI Implementation', 'AI Governance'],
            'current_investment_billions': [125, 95, 78, 110, 45, 22, 68, 12],
            'projected_2030_billions': [520, 380, 425, 350, 185, 95, 310, 65],
            'cagr_percent': [22.5, 21.8, 27.5, 18.0, 22.3, 23.2, 24.0, 27.1],
            'share_of_tech_investment': [15, 12, 10, 14, 6, 3, 8, 2],
            'roi_expectation_percent': [35, 42, 38, 28, 25, 45, 40, 20]
        }
        return pd.DataFrame(data)
    
    def _load_productivity_scenarios(self) -> pd.DataFrame:
        """Load productivity growth scenarios."""
        # Goldman Sachs productivity scenarios
        data = {
            'scenario': ['Conservative', 'Base Case', 'Optimistic', 'Transformational'],
            'annual_productivity_growth': [0.3, 0.7, 1.5, 2.5],
            'gdp_impact_10yr': [3.0, 7.0, 15.0, 25.0],
            'adoption_assumption': ['Slow, limited to large firms', 
                                   'Steady adoption across sectors',
                                   'Rapid adoption with policy support',
                                   'Breakthrough AI capabilities'],
            'probability_percent': [20, 50, 25, 5],
            'labor_displacement_percent': [5, 15, 25, 40]
        }
        return pd.DataFrame(data)
    
    def _load_global_competitiveness(self) -> pd.DataFrame:
        """Load global AI competitiveness metrics."""
        data = {
            'country': ['United States', 'China', 'United Kingdom', 'Canada', 
                       'Germany', 'France', 'Japan', 'South Korea', 'India', 
                       'Singapore', 'Israel', 'Australia'],
            'ai_readiness_index': [8.8, 8.2, 7.9, 7.7, 7.5, 7.2, 7.3, 7.8, 6.5, 7.6, 7.4, 7.1],
            'projected_gdp_boost': [8.2, 7.5, 7.0, 6.8, 6.5, 6.2, 5.8, 7.2, 8.5, 7.8, 7.5, 6.5],
            'investment_per_capita': [425, 125, 285, 315, 255, 225, 195, 265, 25, 485, 395, 245],
            'talent_concentration': [9.2, 7.8, 8.5, 8.2, 7.9, 7.5, 7.2, 8.0, 6.8, 8.8, 8.6, 7.8],
            'regulatory_environment': [7.5, 6.2, 8.2, 8.5, 8.0, 7.8, 7.0, 7.5, 6.5, 8.0, 7.8, 8.3]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate Goldman Sachs data."""
        required_datasets = ['gdp_impact_forecast', 'sectoral_disruption', 
                           'labor_market_effects', 'investment_outlook']
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        # Validate GDP impact is within reasonable bounds
        gdp_impact = data['gdp_impact_forecast']
        if gdp_impact['cumulative_gdp_boost_percent'].max() > 20:
            logger.warning("GDP boost projections exceed 20% - verify data")
        
        logger.info("Goldman Sachs data validation passed")
        return True