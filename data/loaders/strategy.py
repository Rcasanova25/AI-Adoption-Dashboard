"""AI strategy and use case document loaders."""

import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from config.settings import settings

from .base import BaseDataLoader, DataSource
from ..extractors.pdf_extractor import PDFExtractor

logger = logging.getLogger(__name__)


class AIStrategyLoader(BaseDataLoader):
    """Loader for AI strategy document."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize with AI strategy file path."""
        if file_path is None:
            file_path = settings.get_resources_path() / "AI strategy.pdf"

        source = DataSource(
            name="AI Strategy Framework",
            version="2025",
            file_path=file_path,
            citation="AI Strategy Framework Document. 2025.",
        )
        super().__init__(source)
        self.extractor = None
        if self.source.file_path and self.source.file_path.exists():
            try:
                self.extractor = PDFExtractor(self.source.file_path)
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")

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
        """Extract strategic pillars from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for strategy pillars.")
            return pd.DataFrame(columns=["pillar", "description", "priority", "owner"])
        try:
            pages = self.extractor.find_pages_with_keyword("pillar")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("pillar" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting strategy pillars: {e}")
        return pd.DataFrame(columns=["pillar", "description", "priority", "owner"])

    def _load_implementation_roadmap(self) -> pd.DataFrame:
        """Extract implementation roadmap from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for implementation roadmap.")
            return pd.DataFrame(columns=["phase", "milestone", "timeline", "responsible_party"])
        try:
            pages = self.extractor.find_pages_with_keyword("roadmap")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("milestone" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting implementation roadmap: {e}")
        return pd.DataFrame(columns=["phase", "milestone", "timeline", "responsible_party"])

    def _load_success_metrics(self) -> pd.DataFrame:
        """Extract success metrics from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for success metrics.")
            return pd.DataFrame(columns=["metric", "target", "actual", "status"])
        try:
            pages = self.extractor.find_pages_with_keyword("metric")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("metric" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting success metrics: {e}")
        return pd.DataFrame(columns=["metric", "target", "actual", "status"])

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
            file_path = settings.get_resources_path() / "AI use case.pdf"

        source = DataSource(
            name="AI Use Case Catalog",
            version="2025",
            file_path=file_path,
            citation="Enterprise AI Use Case Catalog. 2025.",
        )
        super().__init__(source)
        self.extractor = None
        if self.source.file_path and self.source.file_path.exists():
            try:
                self.extractor = PDFExtractor(self.source.file_path)
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")

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
        """Extract use case catalog from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for use case catalog.")
            return pd.DataFrame(columns=["use_case", "category", "industry", "impact", "adoption_level"])
        try:
            pages = self.extractor.find_pages_with_keyword("use case")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("use case" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting use case catalog: {e}")
        return pd.DataFrame(columns=["use_case", "category", "industry", "impact", "adoption_level"])

    def _load_implementation_complexity(self) -> pd.DataFrame:
        """Extract implementation complexity from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for implementation complexity.")
            return pd.DataFrame(columns=["use_case", "complexity_score", "barriers", "resources_required"])
        try:
            pages = self.extractor.find_pages_with_keyword("complexity")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("complexity" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting implementation complexity: {e}")
        return pd.DataFrame(columns=["use_case", "complexity_score", "barriers", "resources_required"])

    def _load_value_impact_matrix(self) -> pd.DataFrame:
        """Extract value impact matrix from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for value impact matrix.")
            return pd.DataFrame(columns=["use_case", "value_score", "impact_area", "roi_estimate"])
        try:
            pages = self.extractor.find_pages_with_keyword("impact")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("impact" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting value impact matrix: {e}")
        return pd.DataFrame(columns=["use_case", "value_score", "impact_area", "roi_estimate"])

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
            file_path = (
                settings.get_resources_path()
                / "Exploring artificial intelligence adoption in public organizations  a comparative case study.pdf"
            )

        source = DataSource(
            name="Public Sector AI Adoption Study",
            version="2025",
            file_path=file_path,
            citation="Exploring Artificial Intelligence Adoption in Public Organizations: A Comparative Case Study. 2025.",
        )
        super().__init__(source)
        self.extractor = None
        if self.source.file_path and self.source.file_path.exists():
            try:
                self.extractor = PDFExtractor(self.source.file_path)
            except Exception as e:
                logger.error(f"Failed to initialize PDF extractor: {e}")

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
        """Extract public sector adoption patterns from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for public sector adoption.")
            return pd.DataFrame(columns=["government_level", "adoption_rate", "primary_use_cases", "budget_allocated_millions", "citizen_satisfaction_improvement", "efficiency_gain_percent"])
        try:
            pages = self.extractor.find_pages_with_keyword("adoption")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("adoption" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting public sector adoption: {e}")
        return pd.DataFrame(columns=["government_level", "adoption_rate", "primary_use_cases", "budget_allocated_millions", "citizen_satisfaction_improvement", "efficiency_gain_percent"])

    def _load_implementation_barriers(self) -> pd.DataFrame:
        """Extract public sector implementation barriers from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for implementation barriers.")
            return pd.DataFrame(columns=["barrier", "severity_score", "organizations_affected_percent", "mitigation_strategies_available"])
        try:
            pages = self.extractor.find_pages_with_keyword("barrier")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("barrier" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting implementation barriers: {e}")
        return pd.DataFrame(columns=["barrier", "severity_score", "organizations_affected_percent", "mitigation_strategies_available"])

    def _load_success_factors(self) -> pd.DataFrame:
        """Extract public sector success factors from the PDF."""
        if not self.extractor:
            logger.error("PDF extractor not available for success factors.")
            return pd.DataFrame(columns=["success_factor", "importance_score", "implementation_rate", "impact_on_success"])
        try:
            pages = self.extractor.find_pages_with_keyword("success")
            tables = []
            for page in pages:
                tables.extend(self.extractor.extract_tables(page_range=(page, page)))
            for table in tables:
                if not table.empty and any("success" in str(col).lower() for col in table.columns):
                    return table
        except Exception as e:
            logger.error(f"Error extracting success factors: {e}")
        return pd.DataFrame(columns=["success_factor", "importance_score", "implementation_rate", "impact_on_success"])

    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate public sector data."""
        required = ["public_sector_adoption", "implementation_barriers"]
        if not all(dataset in data for dataset in required):
            raise ValueError("Missing required public sector datasets")
        return True
