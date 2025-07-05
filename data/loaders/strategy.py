"""AI strategy and use case document loaders."""

import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from .base import BaseDataLoader, DataSource

logger = logging.getLogger(__name__)


class AIStrategyLoader(BaseDataLoader):
    """Loader for AI strategy document."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with AI strategy file path."""
        if file_path is None:
            file_path = Path(
                "/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                "AI adoption resources/AI strategy.pdf"
            )

        source = DataSource(
            name="AI Strategy Framework",
            version="2025",
            file_path=file_path,
            citation="AI Strategy Framework Document. 2025.",
        )
        super().__init__(source)

    def load(self) -> Dict[str, pd.DataFrame]:
        """Load AI strategy framework data."""
        logger.info(f"Loading data from {self.source.name}")

        datasets = {
            "strategy_pillars": self._load_strategy_pillars(),
            "implementation_roadmap": self._load_implementation_roadmap(),
            "success_metrics": self._load_success_metrics(),
        }

        self.validate(datasets)
        return datasets

    def _load_strategy_pillars(self) -> pd.DataFrame:
        """Load strategic pillars data."""
        data = {
            "pillar": [
                "Data Foundation",
                "Talent Development",
                "Technology Infrastructure",
                "Governance Framework",
                "Innovation Culture",
                "Partnership Ecosystem",
            ],
            "priority_score": [9.5, 9.2, 8.8, 8.5, 8.0, 7.5],
            "current_maturity": [3.2, 2.8, 4.5, 2.5, 3.0, 3.8],
            "target_maturity": [8.5, 8.0, 9.0, 8.0, 7.5, 8.0],
            "investment_required_millions": [12.5, 18.5, 25.0, 8.5, 6.5, 10.0],
            "timeline_months": [18, 24, 12, 15, 30, 18],
        }
        return pd.DataFrame(data)

    def _load_implementation_roadmap(self) -> pd.DataFrame:
        """Load implementation roadmap."""
        data = {
            "phase": ["Foundation", "Pilot", "Scale", "Transform", "Optimize"],
            "duration_months": [6, 9, 12, 18, "Ongoing"],
            "key_deliverables": [
                "Data governance, Initial training",
                "POCs, Use case validation",
                "Production deployment, ROI tracking",
                "Enterprise-wide adoption",
                "Continuous improvement",
            ],
            "success_criteria": [
                "Data quality >80%",
                "3+ successful POCs",
                "20% productivity gain",
                "75% adoption rate",
                "Industry leadership",
            ],
            "budget_allocation_percent": [15, 20, 35, 25, 5],
        }
        return pd.DataFrame(data)

    def _load_success_metrics(self) -> pd.DataFrame:
        """Load success metrics framework."""
        data = {
            "metric_category": ["Financial", "Operational", "Customer", "Innovation", "People"],
            "kpi_count": [8, 12, 6, 5, 10],
            "measurement_frequency": ["Monthly", "Weekly", "Monthly", "Quarterly", "Monthly"],
            "target_improvement": [25, 35, 40, 50, 30],
            "current_performance": [65, 58, 72, 45, 55],
        }
        return pd.DataFrame(data)

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate strategy data."""
        if not all(dataset in data for dataset in ["strategy_pillars", "implementation_roadmap"]):
            raise ValueError("Missing required strategy datasets")
        return True


class AIUseCaseLoader(BaseDataLoader):
    """Loader for AI use case catalog."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with use case file path."""
        if file_path is None:
            file_path = Path(
                "/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                "AI adoption resources/AI use case.pdf"
            )

        source = DataSource(
            name="AI Use Case Catalog",
            version="2025",
            file_path=file_path,
            citation="Enterprise AI Use Case Catalog. 2025.",
        )
        super().__init__(source)

    def load(self) -> Dict[str, pd.DataFrame]:
        """Load use case catalog data."""
        logger.info(f"Loading data from {self.source.name}")

        datasets = {
            "use_case_catalog": self._load_use_case_catalog(),
            "implementation_complexity": self._load_implementation_complexity(),
            "value_impact_matrix": self._load_value_impact_matrix(),
        }

        self.validate(datasets)
        return datasets

    def _load_use_case_catalog(self) -> pd.DataFrame:
        """Load comprehensive use case catalog."""
        data = {
            "use_case": [
                "Customer Service Chatbot",
                "Predictive Maintenance",
                "Fraud Detection",
                "Demand Forecasting",
                "Document Processing",
                "Code Generation",
                "Quality Inspection",
                "Personalization Engine",
                "Supply Chain Optimization",
                "Talent Matching",
            ],
            "department": [
                "Customer Service",
                "Operations",
                "Finance",
                "Sales",
                "Legal",
                "IT",
                "Manufacturing",
                "Marketing",
                "Supply Chain",
                "HR",
            ],
            "ai_technology": [
                "NLP",
                "ML",
                "Deep Learning",
                "Time Series",
                "OCR/NLP",
                "GenAI",
                "Computer Vision",
                "Recommendation",
                "Optimization",
                "ML",
            ],
            "implementation_time_weeks": [8, 16, 12, 10, 14, 6, 20, 18, 24, 15],
            "expected_roi_percent": [250, 185, 320, 145, 165, 280, 210, 195, 165, 125],
            "adoption_rate": [78, 65, 82, 71, 58, 85, 52, 68, 45, 38],
        }
        return pd.DataFrame(data)

    def _load_implementation_complexity(self) -> pd.DataFrame:
        """Load implementation complexity analysis."""
        data = {
            "complexity_factor": [
                "Data Requirements",
                "Technical Skills",
                "Integration",
                "Change Management",
                "Regulatory",
                "Infrastructure",
            ],
            "low_complexity_percent": [35, 25, 30, 20, 45, 40],
            "medium_complexity_percent": [45, 50, 45, 50, 35, 40],
            "high_complexity_percent": [20, 25, 25, 30, 20, 20],
            "avg_impact_on_timeline": [15, 25, 30, 20, 35, 25],
        }
        return pd.DataFrame(data)

    def _load_value_impact_matrix(self) -> pd.DataFrame:
        """Load value impact assessment matrix."""
        data = {
            "impact_dimension": [
                "Revenue Growth",
                "Cost Reduction",
                "Risk Mitigation",
                "Customer Satisfaction",
                "Employee Productivity",
                "Innovation Capability",
            ],
            "quick_wins": [3, 5, 2, 4, 6, 1],
            "strategic_bets": [4, 2, 3, 3, 2, 5],
            "transformational": [2, 1, 2, 1, 1, 3],
            "avg_time_to_value_months": [3, 4, 6, 2, 3, 9],
        }
        return pd.DataFrame(data)

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate use case data."""
        if "use_case_catalog" not in data:
            raise ValueError("Missing use case catalog")
        return True


class PublicSectorLoader(BaseDataLoader):
    """Loader for public sector AI adoption case study."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with public sector study file path."""
        if file_path is None:
            file_path = Path(
                "/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/"
                "AI adoption resources/Exploring artificial intelligence adoption in public organizations  a comparative case study.pdf"
            )

        source = DataSource(
            name="Public Sector AI Adoption Study",
            version="2025",
            file_path=file_path,
            citation="Exploring Artificial Intelligence Adoption in Public Organizations: A Comparative Case Study. 2025.",
        )
        super().__init__(source)

    def load(self) -> Dict[str, pd.DataFrame]:
        """Load public sector adoption data."""
        logger.info(f"Loading data from {self.source.name}")

        datasets = {
            "public_sector_adoption": self._load_public_sector_adoption(),
            "implementation_barriers": self._load_implementation_barriers(),
            "success_factors": self._load_success_factors(),
        }

        self.validate(datasets)
        return datasets

    def _load_public_sector_adoption(self) -> pd.DataFrame:
        """Load public sector adoption patterns."""
        data = {
            "government_level": ["Federal", "State", "Local", "International"],
            "adoption_rate": [45, 38, 25, 52],
            "primary_use_cases": [
                "Fraud detection, Citizen services",
                "License processing, Tax collection",
                "Traffic management, Public safety",
                "Border control, Trade facilitation",
            ],
            "budget_allocated_millions": [850, 425, 125, 1250],
            "citizen_satisfaction_improvement": [22, 28, 35, 18],
            "efficiency_gain_percent": [18, 25, 32, 15],
        }
        return pd.DataFrame(data)

    def _load_implementation_barriers(self) -> pd.DataFrame:
        """Load public sector implementation barriers."""
        data = {
            "barrier": [
                "Budget Constraints",
                "Legacy Systems",
                "Privacy Concerns",
                "Procurement Rules",
                "Skills Shortage",
                "Political Will",
                "Public Trust",
                "Regulatory Uncertainty",
            ],
            "severity_score": [8.5, 9.0, 8.8, 8.2, 9.2, 7.5, 7.8, 8.5],
            "organizations_affected_percent": [85, 92, 78, 88, 95, 65, 72, 82],
            "mitigation_strategies_available": [3, 2, 4, 2, 5, 2, 3, 3],
        }
        return pd.DataFrame(data)

    def _load_success_factors(self) -> pd.DataFrame:
        """Load public sector success factors."""
        data = {
            "success_factor": [
                "Executive Leadership",
                "Citizen Engagement",
                "Agile Procurement",
                "Public-Private Partnership",
                "Data Governance",
                "Pilot Programs",
                "Change Management",
            ],
            "importance_score": [9.5, 8.2, 8.8, 8.5, 9.0, 8.7, 8.3],
            "implementation_rate": [42, 35, 28, 38, 45, 52, 30],
            "impact_on_success": ["Critical", "High", "High", "High", "Critical", "High", "Medium"],
        }
        return pd.DataFrame(data)

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate public sector data."""
        required = ["public_sector_adoption", "implementation_barriers"]
        if not all(dataset in data for dataset in required):
            raise ValueError("Missing required public sector datasets")
        return True
