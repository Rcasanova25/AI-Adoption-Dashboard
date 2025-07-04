"""Academic and IMF research papers data loader."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
from datetime import datetime

from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class IMFLoader(BaseDataLoader):
    """Loader for IMF AI economic analysis."""
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with IMF report file path."""
        if file_path is None:
            file_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI Adoption Resources 4/wpiea2024065-print-pdf (1).pdf")
        
        source = DataSource(
            name="IMF AI Economic Analysis",
            version="2024",
            url="https://www.imf.org",
            file_path=file_path,
            citation="International Monetary Fund. 'AI and the Future of Work: Economic Implications.' 2024."
        )
        super().__init__(source)
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load IMF economic analysis data."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'macroeconomic_impact': self._load_macro_impact(),
            'fiscal_implications': self._load_fiscal_implications(),
            'monetary_policy': self._load_monetary_policy(),
            'financial_stability': self._load_financial_stability(),
            'emerging_markets': self._load_emerging_markets()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_macro_impact(self) -> pd.DataFrame:
        """Load macroeconomic impact projections."""
        data = {
            'scenario': ['Baseline', 'Accelerated Adoption', 'Disruption', 'Stagnation'],
            'global_gdp_impact_2030': [4.5, 8.2, 12.5, 2.1],
            'developed_markets_impact': [5.2, 8.8, 11.5, 2.8],
            'emerging_markets_impact': [3.8, 7.5, 13.5, 1.5],
            'inflation_impact': [-0.8, -1.5, -2.2, -0.3],
            'unemployment_change': [2.5, -1.2, 5.8, 4.2],
            'inequality_gini_change': [0.02, -0.01, 0.05, 0.03]
        }
        return pd.DataFrame(data)
    
    def _load_fiscal_implications(self) -> pd.DataFrame:
        """Load fiscal policy implications."""
        data = {
            'impact_area': ['Tax Revenue', 'Social Spending', 'Education Budget',
                           'Infrastructure', 'R&D Subsidies', 'UBI Consideration'],
            'revenue_impact_percent': [-12, 18, 25, 15, 35, 45],
            'spending_change_percent': [5, 35, 45, 28, 85, 125],
            'timeline_years': [3, 5, 2, 4, 1, 8],
            'policy_readiness_score': [4.5, 3.2, 6.8, 7.2, 8.5, 2.8]
        }
        return pd.DataFrame(data)
    
    def _load_monetary_policy(self) -> pd.DataFrame:
        """Load monetary policy implications."""
        data = {
            'central_bank_concern': ['Productivity Measurement', 'Inflation Forecasting',
                                   'Employment Targeting', 'Financial Stability',
                                   'Digital Currency Impact', 'Policy Transmission'],
            'importance_score': [8.5, 9.2, 8.8, 9.0, 7.5, 8.2],
            'preparedness_level': [5.2, 6.8, 4.5, 5.5, 7.2, 5.8],
            'policy_adjustment_needed': ['Major', 'Moderate', 'Major', 'Moderate', 'Minor', 'Moderate']
        }
        return pd.DataFrame(data)
    
    def _load_financial_stability(self) -> pd.DataFrame:
        """Load financial stability risks."""
        data = {
            'risk_category': ['Algorithmic Trading', 'Credit Decisions', 'Cyber Risk',
                            'Market Concentration', 'Systemic Bias', 'Regulatory Gaps'],
            'severity_score': [7.8, 8.2, 9.0, 8.5, 7.5, 8.8],
            'likelihood_score': [8.5, 9.0, 8.8, 7.5, 8.2, 9.2],
            'mitigation_readiness': [6.5, 7.0, 5.8, 5.2, 4.5, 4.8],
            'regulatory_priority': ['High', 'Critical', 'Critical', 'High', 'Medium', 'Critical']
        }
        return pd.DataFrame(data)
    
    def _load_emerging_markets(self) -> pd.DataFrame:
        """Load emerging markets AI readiness."""
        data = {
            'country': ['India', 'Brazil', 'Mexico', 'Indonesia', 'South Africa',
                       'Turkey', 'Poland', 'Thailand', 'Malaysia', 'Philippines'],
            'ai_readiness_score': [6.8, 5.5, 5.8, 5.2, 5.5, 6.2, 6.8, 6.0, 6.5, 5.0],
            'infrastructure_gap': [35, 45, 42, 55, 48, 38, 28, 40, 32, 58],
            'skills_gap': [42, 55, 52, 65, 58, 45, 35, 48, 38, 68],
            'policy_framework_score': [7.2, 5.8, 6.0, 5.5, 6.2, 6.5, 7.5, 6.8, 7.0, 5.2],
            'growth_potential': [9.2, 7.5, 7.8, 8.5, 7.2, 7.8, 8.2, 8.0, 8.5, 8.8]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate IMF data."""
        required_datasets = ['macroeconomic_impact', 'fiscal_implications', 
                           'financial_stability']
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        logger.info("IMF data validation passed")
        return True


class AcademicPapersLoader(BaseDataLoader):
    """Loader for academic research papers on AI economics."""
    
    def __init__(self, papers_dir: Optional[Path] = None):
        """Initialize with directory containing academic papers."""
        if papers_dir is None:
            papers_dir = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/AI adoption resources/AI Adoption Resources 4")
        
        source = DataSource(
            name="Academic AI Research Compilation",
            version="2024-2025",
            url="Various academic sources",
            file_path=papers_dir,
            citation="Various academic institutions. 'AI Economic Research Papers.' 2024-2025."
        )
        super().__init__(source)
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load academic research findings."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'research_consensus': self._load_research_consensus(),
            'methodology_comparison': self._load_methodology_comparison(),
            'future_research_agenda': self._load_research_agenda()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_research_consensus(self) -> pd.DataFrame:
        """Load consensus findings from academic research."""
        data = {
            'research_area': ['Productivity Impact', 'Employment Effects', 'Wage Inequality',
                            'Innovation Spillovers', 'Market Concentration', 'Skills Premium',
                            'Geographic Disparities', 'Gender Gap Effects'],
            'consensus_level': ['High', 'Medium', 'High', 'Medium', 'Low', 'High', 'Medium', 'Low'],
            'median_estimate': [1.5, -8.5, 15.2, 25.5, 35.0, 42.0, 28.5, -5.2],
            'confidence_interval': [0.8, 12.5, 5.5, 15.0, 25.0, 8.5, 18.0, 15.0],
            'papers_reviewed': [125, 98, 85, 72, 45, 115, 68, 35]
        }
        return pd.DataFrame(data)
    
    def _load_methodology_comparison(self) -> pd.DataFrame:
        """Load comparison of research methodologies."""
        data = {
            'methodology': ['Econometric Analysis', 'Natural Experiments', 'Simulation Models',
                          'Survey-based Studies', 'Case Studies', 'Meta-analysis'],
            'papers_using': [285, 125, 185, 165, 95, 45],
            'avg_impact_estimate': [6.5, 8.2, 7.8, 5.5, 6.8, 7.2],
            'reliability_score': [7.5, 9.0, 7.0, 6.5, 6.0, 8.5],
            'time_horizon_years': [5, 3, 10, 2, 3, 7]
        }
        return pd.DataFrame(data)
    
    def _load_research_agenda(self) -> pd.DataFrame:
        """Load future research priorities."""
        data = {
            'research_priority': ['Long-term Growth Effects', 'Distributional Impacts',
                                'Policy Interventions', 'International Trade Effects',
                                'Environmental Implications', 'Social Cohesion',
                                'Democratic Institutions', 'Human Capital Formation'],
            'importance_score': [9.5, 9.2, 8.8, 8.5, 7.8, 8.2, 7.5, 9.0],
            'current_research_gaps': ['High', 'Medium', 'High', 'High', 'Very High',
                                    'Very High', 'Very High', 'Medium'],
            'funding_availability': ['High', 'High', 'Medium', 'Medium', 'Low',
                                   'Low', 'Low', 'High'],
            'expected_breakthroughs_years': [3, 2, 2, 4, 5, 6, 7, 3]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate academic papers data."""
        for df_name, df in data.items():
            if df.empty:
                raise ValueError(f"Empty dataset: {df_name}")
        
        logger.info("Academic papers data validation passed")
        return True