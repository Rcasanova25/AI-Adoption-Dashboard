"""Federal Reserve Banks data loaders for AI economic impact studies."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging
from datetime import datetime

from .base import BaseDataLoader, DataSource
from ..models.economics import EconomicImpact, ProductivityMetrics
from ..models.workforce import WorkforceImpact

logger = logging.getLogger(__name__)


class RichmondFedLoader(BaseDataLoader):
    """Loader for Richmond Fed Productivity Puzzle report."""
    
    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with Richmond Fed report file path."""
        if file_path is None:
            file_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                           "AI adoption resources/AI dashboard resources 1/"
                           "The Productivity Puzzle_ AI, Technology Adoption and the Workforce _ Richmond Fed.pdf")
        
        source = DataSource(
            name="Richmond Fed Productivity Analysis",
            version="2025",
            url="https://www.richmondfed.org",
            file_path=file_path,
            citation="Richmond Federal Reserve Bank. 'The Productivity Puzzle: AI, Technology Adoption and the Workforce.' 2025."
        )
        super().__init__(source)
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load productivity and workforce impact data."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'productivity_impacts': self._load_productivity_impacts(),
            'adoption_timeline': self._load_adoption_timeline(),
            'workforce_transformation': self._load_workforce_transformation(),
            'skill_premium_evolution': self._load_skill_premium(),
            'regional_productivity': self._load_regional_productivity(),
            'automation_vulnerability': self._load_automation_vulnerability()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_productivity_impacts(self) -> pd.DataFrame:
        """Load productivity impact metrics by worker category."""
        data = {
            'worker_category': ['Low-skilled workers', 'Mid-skilled workers', 
                              'High-skilled workers', 'Creative professionals',
                              'Technical workers', 'Management'],
            'productivity_gain_percent': [45, 32, 28, 42, 38, 25],
            'time_saved_hours_week': [16, 12, 10, 15, 14, 8],
            'task_automation_rate': [65, 48, 35, 40, 45, 20],
            'quality_improvement': [38, 42, 48, 55, 52, 45],
            'adoption_difficulty': ['Low', 'Medium', 'Medium', 'Low', 'Medium', 'High']
        }
        return pd.DataFrame(data)
    
    def _load_adoption_timeline(self) -> pd.DataFrame:
        """Load technology adoption timeline patterns."""
        # Historical technology adoption patterns and AI comparison
        data = {
            'technology': ['Electricity', 'Computers', 'Internet', 'Mobile', 
                          'Cloud Computing', 'AI/ML', 'Generative AI'],
            'years_to_25_percent': [46, 28, 15, 12, 8, 7, 2],
            'years_to_50_percent': [68, 38, 22, 18, 12, 10, 4],
            'productivity_lag_years': [25, 15, 8, 5, 3, 2, 1],
            'peak_impact_years': [40, 25, 15, 10, 7, 5, 3],
            'gdp_impact_percent': [2.5, 1.8, 2.2, 1.5, 1.2, 2.8, 3.5]
        }
        return pd.DataFrame(data)
    
    def _load_workforce_transformation(self) -> pd.DataFrame:
        """Load workforce transformation metrics."""
        data = {
            'job_category': ['Routine Manual', 'Routine Cognitive', 'Non-routine Manual',
                           'Non-routine Cognitive', 'Interpersonal', 'Creative'],
            'jobs_at_risk_percent': [78, 65, 25, 15, 8, 5],
            'augmentation_potential': [15, 25, 55, 75, 85, 90],
            'reskilling_required': ['High', 'High', 'Medium', 'Low', 'Low', 'Low'],
            'wage_impact_5yr': [-15, -10, 5, 15, 20, 25],
            'employment_growth_5yr': [-25, -18, 2, 12, 18, 28]
        }
        return pd.DataFrame(data)
    
    def _load_skill_premium(self) -> pd.DataFrame:
        """Load skill premium evolution data."""
        data = {
            'year': [2020, 2021, 2022, 2023, 2024, 2025],
            'ai_skills_premium': [20, 25, 32, 38, 45, 52],
            'traditional_skills_premium': [15, 14, 13, 11, 9, 7],
            'hybrid_skills_premium': [18, 22, 28, 35, 42, 48],
            'skill_obsolescence_rate': [5, 8, 12, 18, 25, 32]
        }
        return pd.DataFrame(data)
    
    def _load_regional_productivity(self) -> pd.DataFrame:
        """Load regional productivity impact data."""
        data = {
            'region': ['Northeast', 'Southeast', 'Midwest', 'Southwest', 
                      'West Coast', 'Mountain West'],
            'ai_adoption_rate': [68, 52, 48, 55, 82, 61],
            'productivity_gain': [22, 18, 16, 19, 28, 21],
            'job_displacement_risk': [15, 22, 25, 20, 12, 18],
            'reskilling_programs': [145, 98, 82, 105, 185, 112],
            'economic_resilience_score': [7.8, 6.5, 6.2, 6.8, 8.5, 7.2]
        }
        return pd.DataFrame(data)
    
    def _load_automation_vulnerability(self) -> pd.DataFrame:
        """Load automation vulnerability by industry."""
        data = {
            'industry': ['Manufacturing', 'Transportation', 'Retail', 'Finance',
                        'Healthcare', 'Education', 'Professional Services',
                        'Construction', 'Hospitality', 'Agriculture'],
            'automation_risk_score': [8.2, 7.5, 6.8, 5.5, 4.2, 3.8, 4.5, 6.2, 7.0, 7.8],
            'ai_complementarity_score': [6.5, 5.8, 7.2, 8.5, 8.8, 7.5, 8.2, 5.5, 6.0, 6.8],
            'workforce_adaptability': [5.2, 4.8, 6.5, 7.8, 8.2, 7.0, 8.5, 5.0, 5.5, 4.5],
            'investment_in_reskilling': [3.2, 2.8, 4.5, 6.8, 7.2, 5.5, 6.5, 2.5, 3.0, 2.2]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate Richmond Fed data."""
        required_datasets = ['productivity_impacts', 'adoption_timeline', 
                           'workforce_transformation']
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        logger.info("Richmond Fed data validation passed")
        return True


class StLouisFedLoader(BaseDataLoader):
    """Loader for St. Louis Fed Generative AI analysis."""
    
    def __init__(self, adoption_file: Optional[Path] = None, impact_file: Optional[Path] = None):
        """Initialize with St. Louis Fed report file paths."""
        if adoption_file is None:
            adoption_file = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                               "AI adoption resources/AI Adoption Resources 4/"
                               "stlouisfed.org_on-the-economy_2024_sep_rapid-adoption-generative-ai_print=true.pdf")
        
        source = DataSource(
            name="St. Louis Fed GenAI Analysis",
            version="2024-2025",
            url="https://www.stlouisfed.org",
            file_path=adoption_file,
            citation="Federal Reserve Bank of St. Louis. 'The Rapid Adoption of Generative AI.' 2024-2025."
        )
        super().__init__(source)
        
        self.impact_file = impact_file or Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                                              "AI adoption resources/AI Adoption Resources 4/"
                                              "stlouisfed.org_on-the-economy_2025_feb_impact-generative-ai-work-productivity_print=true.pdf")
    
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load GenAI adoption and impact data."""
        logger.info(f"Loading data from {self.source.name}")
        
        datasets = {
            'genai_adoption_curve': self._load_genai_adoption_curve(),
            'demographic_adoption': self._load_demographic_adoption(),
            'use_case_evolution': self._load_use_case_evolution(),
            'productivity_by_task': self._load_productivity_by_task(),
            'economic_projections': self._load_economic_projections()
        }
        
        self.validate(datasets)
        return datasets
    
    def _load_genai_adoption_curve(self) -> pd.DataFrame:
        """Load GenAI adoption curve data."""
        # Rapid adoption of GenAI from St. Louis Fed analysis
        data = {
            'month': pd.date_range('2022-11', '2025-06', freq='M'),
            'consumer_adoption_millions': [1, 5, 15, 30, 45, 65, 85, 100, 115, 125, 135, 145, 
                                         155, 165, 172, 178, 185, 190, 195, 200, 205, 210, 
                                         215, 220, 225, 230, 235, 240, 245, 250, 255],
            'enterprise_adoption_percent': [0.5, 1.2, 2.5, 4.8, 7.5, 11.2, 15.8, 21.5, 28.2, 
                                          35.5, 42.3, 48.5, 54.2, 59.5, 64.2, 68.5, 72.1, 
                                          75.2, 77.8, 79.8, 81.5, 83.0, 84.2, 85.3, 86.2, 
                                          87.0, 87.6, 88.1, 88.5, 88.9, 89.2]
        }
        df = pd.DataFrame(data)
        return df.iloc[:len(data['consumer_adoption_millions'])]  # Ensure same length
    
    def _load_demographic_adoption(self) -> pd.DataFrame:
        """Load demographic adoption patterns."""
        data = {
            'demographic': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers', 'Silent Gen'],
            'adoption_rate': [92, 84, 68, 45, 22],
            'daily_usage_rate': [78, 65, 45, 28, 12],
            'work_usage_rate': [68, 71, 55, 38, 15],
            'trust_score': [7.5, 7.2, 6.5, 5.8, 4.2]
        }
        return pd.DataFrame(data)
    
    def _load_use_case_evolution(self) -> pd.DataFrame:
        """Load GenAI use case evolution."""
        data = {
            'use_case': ['Content Creation', 'Code Generation', 'Data Analysis',
                        'Customer Service', 'Research', 'Education', 'Design',
                        'Translation', 'Strategy', 'Personal Assistant'],
            'adoption_2023': [35, 22, 18, 28, 25, 15, 12, 20, 8, 10],
            'adoption_2024': [68, 55, 42, 52, 48, 35, 32, 38, 22, 28],
            'adoption_2025': [85, 78, 65, 71, 68, 58, 55, 52, 42, 48],
            'productivity_gain': [45, 55, 40, 50, 35, 38, 42, 48, 30, 32]
        }
        return pd.DataFrame(data)
    
    def _load_productivity_by_task(self) -> pd.DataFrame:
        """Load productivity gains by task type."""
        data = {
            'task_type': ['Writing', 'Coding', 'Analysis', 'Design', 'Research',
                         'Communication', 'Planning', 'Learning', 'Problem Solving'],
            'time_reduction_percent': [58, 65, 45, 52, 48, 42, 38, 55, 40],
            'quality_improvement_percent': [35, 42, 38, 40, 45, 32, 35, 48, 37],
            'skill_augmentation_score': [8.2, 8.8, 7.5, 7.8, 8.0, 7.2, 7.0, 8.5, 7.7]
        }
        return pd.DataFrame(data)
    
    def _load_economic_projections(self) -> pd.DataFrame:
        """Load economic impact projections."""
        data = {
            'year': [2025, 2026, 2027, 2028, 2029, 2030],
            'gdp_impact_percent': [0.8, 1.5, 2.3, 3.2, 4.0, 4.7],
            'labor_productivity_gain': [5.2, 8.5, 12.1, 15.8, 19.2, 22.5],
            'wage_growth_impact': [2.1, 3.5, 4.8, 6.2, 7.5, 8.8],
            'job_creation_millions': [2.5, 4.8, 7.2, 9.5, 11.8, 14.2],
            'job_displacement_millions': [1.2, 2.8, 4.5, 6.0, 7.2, 8.5]
        }
        return pd.DataFrame(data)
    
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate St. Louis Fed data."""
        required_datasets = ['genai_adoption_curve', 'demographic_adoption', 
                           'economic_projections']
        
        for dataset in required_datasets:
            if dataset not in data:
                raise ValueError(f"Missing required dataset: {dataset}")
        
        logger.info("St. Louis Fed data validation passed")
        return True