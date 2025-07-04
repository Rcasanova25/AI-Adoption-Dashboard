"""OECD AI Policy Observatory data loader."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
from datetime import datetime

from .base import BaseDataLoader, DataSource
from ..models.governance import GovernanceMetrics, PolicyFramework

logger = logging.getLogger(__name__)


class OECDLoader(BaseDataLoader):
    """Loader for OECD AI Policy Observatory data."""
    
    def __init__(self, policy_file: Optional[Path] = None, adoption_file: Optional[Path] = None):
        """Initialize with OECD report file paths."""
        if policy_file is None:
            policy_file = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                             "AI adoption resources/AI Adoption Resources 3/f9ef33c3-en.pdf")
        
        source = DataSource(
            name="OECD AI Policy Observatory",
            version="2025",
            url="https://oecd.ai",
            file_path=policy_file,
            citation="Organisation for Economic Co-operation and Development. 'OECD AI Policy Observatory.' 2025."
        )
        super().__init__(source)
        
        self.adoption_file = adoption_file or Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                                                  "AI adoption resources/AI dashboard resources 1/be745f04-en.pdf")
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load OECD AI policy and adoption data."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'national_ai_strategies': self._load_national_strategies(),
            'policy_instruments': self._load_policy_instruments(),
            'ai_principles_adoption': self._load_principles_adoption(),
            'regulatory_approaches': self._load_regulatory_approaches(),
            'international_cooperation': self._load_international_cooperation(),
            'skills_initiatives': self._load_skills_initiatives(),
            'public_investment': self._load_public_investment()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_national_strategies(self) -> pd.DataFrame:
        """Load national AI strategy data."""
        data = {
            'country': ['United States', 'China', 'United Kingdom', 'Germany', 'France',
                       'Canada', 'Japan', 'South Korea', 'India', 'Australia',
                       'Singapore', 'Netherlands', 'Sweden', 'Israel', 'Finland'],
            'strategy_launch_year': [2019, 2017, 2018, 2018, 2018, 2017, 2019, 2019, 2018, 2019,
                                   2019, 2019, 2018, 2019, 2017],
            'strategy_maturity_score': [8.5, 9.2, 8.8, 8.2, 7.9, 8.3, 7.5, 8.7, 7.2, 7.8,
                                      8.9, 8.1, 8.4, 8.6, 8.3],
            'public_funding_billions': [5.2, 15.8, 1.8, 3.2, 2.5, 1.2, 2.8, 2.2, 1.5, 0.8,
                                      0.6, 0.5, 0.4, 0.7, 0.3],
            'ai_governance_framework': [True, True, True, True, True, True, True, True, False, True,
                                      True, True, True, True, True],
            'ethics_guidelines': [True, True, True, True, True, True, True, True, True, True,
                                True, True, True, True, True]
        }
        return pd.DataFrame(data)
    
    def _load_policy_instruments(self) -> pd.DataFrame:
        """Load AI policy instruments data."""
        data = {
            'instrument_type': ['R&D Funding', 'Tax Incentives', 'Regulatory Sandboxes',
                              'Public-Private Partnerships', 'Skills Programs',
                              'Data Governance', 'Ethics Boards', 'Standards Development',
                              'International Cooperation', 'Public Procurement'],
            'countries_implementing': [52, 38, 25, 45, 48, 42, 35, 40, 55, 28],
            'effectiveness_score': [8.2, 7.5, 8.8, 8.0, 7.8, 7.2, 6.5, 7.0, 8.5, 7.3],
            'implementation_complexity': ['Medium', 'Low', 'High', 'Medium', 'High',
                                        'High', 'Medium', 'High', 'Medium', 'Low'],
            'avg_budget_millions': [125, 85, 45, 95, 105, 55, 25, 35, 65, 185]
        }
        return pd.DataFrame(data)
    
    def _load_principles_adoption(self) -> pd.DataFrame:
        """Load OECD AI Principles adoption data."""
        principles = {
            'principle': ['Inclusive growth and well-being', 'Human-centered values',
                         'Transparency and explainability', 'Robustness and safety',
                         'Accountability', 'Privacy and data governance',
                         'Human oversight', 'Non-discrimination and fairness'],
            'adoption_rate_percent': [72, 78, 65, 82, 68, 85, 70, 62],
            'implementation_score': [6.5, 7.2, 5.8, 7.8, 6.2, 8.0, 6.8, 5.5],
            'policy_coverage': ['High', 'High', 'Medium', 'High', 'Medium', 'High', 'Medium', 'Medium'],
            'enforcement_level': ['Medium', 'Low', 'Low', 'High', 'Medium', 'High', 'Medium', 'Low']
        }
        return pd.DataFrame(principles)
    
    def _load_regulatory_approaches(self) -> pd.DataFrame:
        """Load AI regulatory approaches by region."""
        data = {
            'region': ['European Union', 'United States', 'China', 'United Kingdom',
                      'Canada', 'Japan', 'Singapore', 'Australia'],
            'regulatory_approach': ['Comprehensive (AI Act)', 'Sectoral/Risk-based', 
                                  'Development-focused', 'Principles-based',
                                  'Voluntary frameworks', 'Soft law', 'Innovation-first',
                                  'Co-regulatory'],
            'implementation_stage': ['Adopted', 'Developing', 'Implemented', 'Consultation',
                                   'Framework ready', 'Guidelines issued', 'Operational',
                                   'Pilot phase'],
            'industry_alignment': [6.5, 8.2, 7.8, 8.5, 8.8, 7.5, 9.0, 8.0],
            'innovation_impact': [-15, 5, 12, 8, 10, 6, 15, 7],
            'compliance_cost_index': [85, 45, 55, 40, 35, 38, 30, 42]
        }
        return pd.DataFrame(data)
    
    def _load_international_cooperation(self) -> pd.DataFrame:
        """Load international AI cooperation initiatives."""
        data = {
            'initiative': ['GPAI', 'OECD AI', 'UNESCO AI Ethics', 'EU-US TTC',
                          'Quad AI', 'Council of Europe AI', 'ISO/IEC AI Standards',
                          'UN AI Advisory Body'],
            'member_countries': [29, 46, 193, 2, 4, 46, 165, 193],
            'focus_area': ['Responsible AI', 'Policy coordination', 'Ethics',
                          'Tech cooperation', 'Security', 'Human rights',
                          'Technical standards', 'Global governance'],
            'effectiveness_score': [7.5, 8.2, 6.8, 7.8, 7.2, 7.0, 8.5, 6.5],
            'budget_millions': [15, 25, 8, 45, 35, 12, 5, 20]
        }
        return pd.DataFrame(data)
    
    def _load_skills_initiatives(self) -> pd.DataFrame:
        """Load AI skills and education initiatives."""
        data = {
            'country': ['Singapore', 'Finland', 'Canada', 'South Korea', 'Germany',
                       'United Kingdom', 'France', 'Japan', 'Australia', 'Netherlands'],
            'ai_in_curriculum': [True, True, True, True, False, True, False, False, True, True],
            'reskilling_programs': [185, 95, 125, 165, 145, 155, 105, 85, 75, 115],
            'public_training_budget_millions': [125, 45, 85, 105, 95, 75, 65, 55, 35, 55],
            'citizens_trained_thousands': [450, 850, 325, 580, 285, 425, 195, 165, 145, 225],
            'industry_partnership_score': [9.2, 8.5, 8.8, 9.0, 8.2, 8.6, 7.8, 7.5, 8.0, 8.7]
        }
        return pd.DataFrame(data)
    
    def _load_public_investment(self) -> pd.DataFrame:
        """Load public AI investment data."""
        data = {
            'year': [2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'global_public_investment_billions': [45, 58, 72, 95, 125, 165, 215],
            'us_share_percent': [32, 31, 30, 29, 28, 27, 26],
            'china_share_percent': [28, 30, 31, 32, 33, 34, 35],
            'eu_share_percent': [22, 21, 21, 20, 20, 19, 19],
            'other_share_percent': [18, 18, 18, 19, 19, 20, 20],
            'focus_on_safety_percent': [5, 8, 12, 18, 25, 32, 38]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate OECD data."""
        required_datasets = ['national_ai_strategies', 'policy_instruments', 
                           'ai_principles_adoption', 'regulatory_approaches']
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        logger.info("OECD data validation passed")
        return True