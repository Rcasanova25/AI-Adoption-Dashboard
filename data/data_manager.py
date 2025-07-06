"""Optimized data manager with multi-layer caching and lazy loading."""

import asyncio
import concurrent.futures
import logging
import asyncio
import concurrent.futures
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

from config.settings import settings

from .loaders import (
    AcademicPapersLoader,
    AIIndexLoader,
    BaseDataLoader,
    GoldmanSachsLoader,
    IMFLoader,
    McKinseyLoader,
    NVIDIATokenLoader,
    OECDLoader,
    RichmondFedLoader,
    StLouisFedLoader,
)
from .loaders.strategy import AIStrategyLoader, AIUseCaseLoader, PublicSectorLoader

logger = logging.getLogger(__name__)


class DataManager:
    """Manages all data sources and provides unified access to dashboard data."""

    def __init__(self, resources_path: Optional[Path] = None):
        """Initialize data manager with path to resources directory."""
        if resources_path is None:
            resources_path = settings.get_resources_path()

        # Ensure the path exists
        if not resources_path.exists():
            logger.warning(f"Resources path does not exist: {resources_path}")
            logger.info(f"Creating resources directory at: {resources_path}")
            resources_path.mkdir(parents=True, exist_ok=True)

        self.resources_path = resources_path
        self.loaders: Dict[str, BaseDataLoader] = {}
        self._cache: Dict[str, pd.DataFrame] = {}

        # Initialize loaders
        self._initialize_loaders()

    def _initialize_loaders(self):
        """Initialize all data loaders."""
        logger.info("Initializing data loaders...")

        # AI Index loader - Stanford HAI
        ai_index_path = (
            self.resources_path / "AI dashboard resources 1/hai_ai_index_report_2025.pdf"
        )
        self.loaders["ai_index"] = AIIndexLoader(ai_index_path)

        # McKinsey State of AI
        mckinsey_path = (
            self.resources_path
            / "AI dashboard resources 1/the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf"
        )
        self.loaders["mckinsey"] = McKinseyLoader(mckinsey_path)

        # OECD 2025 AI Report
        oecd_path = (
            self.resources_path
            / "AI dashboard resources 1/oecd-artificial-intelligence-review-2025.pdf"
        )
        self.loaders["oecd"] = OECDLoader(oecd_path)

        # Federal Reserve - Richmond
        fed_richmond_path = (
            self.resources_path
            / "AI dashboard resources 1/cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf"
        )
        self.loaders["fed_richmond"] = RichmondFedLoader(fed_richmond_path)

        # Federal Reserve - St. Louis
        fed_stlouis_path = (
            self.resources_path
            / "AI dashboard resources 1/the-economic-impact-of-large-language-models.pdf"
        )
        self.loaders["fed_stlouis"] = StLouisFedLoader(fed_stlouis_path)

        # Goldman Sachs
        goldman_path = self.resources_path / "AI dashboard resources 1/gs-new-decade-begins.pdf"
        self.loaders["goldman_sachs"] = GoldmanSachsLoader(goldman_path)

        # NVIDIA Token Economics
        nvidia_path = (
            self.resources_path
            / "AI dashboard resources 1/nvidia-cost-trends-ai-inference-at-scale.pdf"
        )
        self.loaders["nvidia"] = NVIDIATokenLoader(nvidia_path)

        # IMF Working Paper
        imf_path = self.resources_path / "AI dashboard resources 1/wpiea2024231-print-pdf.pdf"
        self.loaders["imf"] = IMFLoader(imf_path)

        # Academic Papers
        papers_path = self.resources_path / "AI dashboard resources 1"
        self.loaders["academic"] = AcademicPapersLoader(papers_path)

        # Strategy loaders
        self.loaders["ai_strategy"] = AIStrategyLoader(self.resources_path)
        self.loaders["ai_use_cases"] = AIUseCaseLoader(self.resources_path)
        self.loaders["public_sector"] = PublicSectorLoader(self.resources_path)

        logger.info(f"Initialized {len(self.loaders)} data loaders")

    @lru_cache(maxsize=128)
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get a specific dataset by name.

        Args:
            dataset_name: Name of the dataset (e.g., 'adoption_trends')
            source: Optional specific source to load from

        Returns:
            DataFrame containing the requested data
        """
        cache_key = f"{source or 'all'}:{dataset_name}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        # If specific source requested
        if source:
            if source not in self.loaders:
                raise ValueError(f"Unknown source: {source}")

            loader = self.loaders[source]
            data = loader.get_dataset(dataset_name)
            if data is not None:
                self._cache[cache_key] = data
                return data
            else:
                raise ValueError(f"Dataset '{dataset_name}' not found in source '{source}'")

        # Otherwise, search all sources
        for source_name, loader in self.loaders.items():
            data = loader.get_dataset(dataset_name)
            if data is not None:
                logger.info(f"Found dataset '{dataset_name}' in source '{source_name}'")
                self._cache[cache_key] = data
                return data

        raise ValueError(f"Dataset '{dataset_name}' not found in any source")

    def get_combined_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Get combined dataset from all sources.

        Args:
            dataset_name: Name of the dataset to combine

        Returns:
            Combined DataFrame from all sources that have this dataset
        """
        combined_data = []

        for source_name, loader in self.loaders.items():
            try:
                data = loader.get_dataset(dataset_name)
                if data is not None:
                    # Add source column for tracking
                    data["data_source"] = source_name
                    combined_data.append(data)
            except Exception as e:
                logger.warning(f"Error loading {dataset_name} from {source_name}: {e}")

        if not combined_data:
            raise ValueError(f"Dataset '{dataset_name}' not found in any source")

        # Combine and return
        return pd.concat(combined_data, ignore_index=True)

    def list_all_datasets(self) -> Dict[str, List[str]]:
        """List all available datasets from all sources.

        Returns:
            Dictionary mapping source names to list of dataset names
        """
        all_datasets = {}

        for source_name, loader in self.loaders.items():
            try:
                datasets = loader.list_datasets()
                all_datasets[source_name] = datasets
            except Exception as e:
                logger.error(f"Error listing datasets from {source_name}: {e}")
                all_datasets[source_name] = []

        return all_datasets

    def get_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all data sources.

        Returns:
            Dictionary mapping source names to metadata
        """
        metadata = {}

        for source_name, loader in self.loaders.items():
            metadata[source_name] = loader.get_metadata()

        return metadata

    def refresh_cache(self):
        """Clear and refresh all cached data."""
        logger.info("Refreshing data cache...")
        self._cache.clear()
        self.get_dataset.cache_clear()

    def get_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """Get all available datasets.

        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        all_data = {}
        datasets_by_source = self.list_all_datasets()

        for source, datasets in datasets_by_source.items():
            for dataset in datasets:
                if dataset not in all_data:
                    try:
                        all_data[dataset] = self.get_dataset(dataset, source)
                    except Exception as e:
                        logger.warning(f"Error loading {dataset} from {source}: {e}")

        return all_data

    def get_data(self, source: str) -> Dict[str, pd.DataFrame]:
        """Get all data from a specific source.

        Args:
            source: Name of the data source (e.g., 'ai_index', 'mckinsey')

        Returns:
            Dictionary mapping dataset names to DataFrames from the specified source
        """
        if source not in self.loaders:
            logger.error(f"Unknown data source: {source}")
            return {}

        loader = self.loaders[source]
        try:
            datasets = loader.list_datasets()
            result = {}
            for dataset in datasets:
                try:
                    data = loader.get_dataset(dataset)
                    if data is not None:
                        result[dataset] = data
                except Exception as e:
                    logger.warning(f"Error loading dataset '{dataset}' from '{source}': {e}")
            return result
        except Exception as e:
            logger.error(f"Error accessing data from source '{source}': {e}")
            return {}


    @st.cache_data(ttl=settings.CACHE_TTL)
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get a specific dataset by name using Streamlit's caching."""
        # If specific source requested
        if source:
            if source not in self.loaders:
                raise ValueError(f"Unknown source: {source}")

            loader = self.loaders[source]
            data = loader.get_dataset(dataset_name)
            if data is not None:
                return data
            else:
                raise ValueError(f"Dataset '{dataset_name}' not found in source '{source}'")

        # Otherwise, search all sources
        for source_name, loader in self.loaders.items():
            data = loader.get_dataset(dataset_name)
            if data is not None:
                logger.info(f"Found dataset '{dataset_name}' in source '{source_name}'")
                return data

        raise ValueError(f"Dataset '{dataset_name}' not found in any source")

    def refresh_cache(self):
        """Clear and refresh all cached data."""
        logger.info("Refreshing data cache...")
        self.get_dataset.clear()

    """Optimized data manager with multi-layer caching and lazy loading."""

import asyncio
import concurrent.futures
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

from config.settings import settings

from .loaders import (
    AcademicPapersLoader,
    AIIndexLoader,
    BaseDataLoader,
    GoldmanSachsLoader,
    IMFLoader,
    McKinseyLoader,
    NVIDIATokenLoader,
    OECDLoader,
    RichmondFedLoader,
    StLouisFedLoader,
)
from .loaders.strategy import AIStrategyLoader, AIUseCaseLoader, PublicSectorLoader

logger = logging.getLogger(__name__)


class DataManager:
    """Manages all data sources and provides unified access to dashboard data."""

    def __init__(self, resources_path: Optional[Path] = None):
        """Initialize data manager with path to resources directory."""
        if resources_path is None:
            resources_path = settings.get_resources_path()

        # Ensure the path exists
        if not resources_path.exists():
            logger.warning(f"Resources path does not exist: {resources_path}")
            logger.info(f"Creating resources directory at: {resources_path}")
            resources_path.mkdir(parents=True, exist_ok=True)

        self.resources_path = resources_path
        self.loaders: Dict[str, BaseDataLoader] = {}

        # Initialize loaders
        self._initialize_loaders()

    def _initialize_loaders(self) -> None:
        """Initialize all data loaders."""
        logger.info("Initializing data loaders...")

        # AI Index loader - Stanford HAI
        ai_index_path = (
            self.resources_path / "AI dashboard resources 1/hai_ai_index_report_2025.pdf"
        )
        self.loaders["ai_index"] = AIIndexLoader(ai_index_path)

        # McKinsey State of AI
        mckinsey_path = (
            self.resources_path
            / "AI dashboard resources 1/the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf"
        )
        self.loaders["mckinsey"] = McKinseyLoader(mckinsey_path)

        # OECD 2025 AI Report
        oecd_path = (
            self.resources_path
            / "AI dashboard resources 1/oecd-artificial-intelligence-review-2025.pdf"
        )
        self.loaders["oecd"] = OECDLoader(oecd_path)

        # Federal Reserve - Richmond
        fed_richmond_path = (
            self.resources_path
            / "AI dashboard resources 1/cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf"
        )
        self.loaders["fed_richmond"] = RichmondFedLoader(fed_richmond_path)

        # Federal Reserve - St. Louis
        fed_stlouis_path = (
            self.resources_path
            / "AI dashboard resources 1/the-economic-impact-of-large-language-models.pdf"
        )
        self.loaders["fed_stlouis"] = StLouisFedLoader(fed_stlouis_path)

        # Goldman Sachs
        goldman_path = self.resources_path / "AI dashboard resources 1/gs-new-decade-begins.pdf"
        self.loaders["goldman_sachs"] = GoldmanSachsLoader(goldman_path)

        # NVIDIA Token Economics
        nvidia_path = (
            self.resources_path
            / "AI dashboard resources 1/nvidia-cost-trends-ai-inference-at-scale.pdf"
        )
        self.loaders["nvidia"] = NVIDIATokenLoader(nvidia_path)

        # IMF Working Paper
        imf_path = self.resources_path / "AI dashboard resources 1/wpiea2024231-print-pdf.pdf"
        self.loaders["imf"] = IMFLoader(imf_path)

        # Academic Papers
        papers_path = self.resources_path / "AI dashboard resources 1"
        self.loaders["academic"] = AcademicPapersLoader(papers_path)

        # Strategy loaders
        self.loaders["ai_strategy"] = AIStrategyLoader(self.resources_path)
        self.loaders["ai_use_cases"] = AIUseCaseLoader(self.resources_path)
        self.loaders["public_sector"] = PublicSectorLoader(self.resources_path)

        logger.info(f"Initialized {len(self.loaders)} data loaders")

    @st.cache_data(ttl=settings.CACHE_TTL)
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get a specific dataset by name using Streamlit's caching."""
        # If specific source requested
        if source:
            if source not in self.loaders:
                raise ValueError(f"Unknown source: {source}")

            loader = self.loaders[source]
            data = loader.get_dataset(dataset_name)
            if data is not None:
                return data
            else:
                raise ValueError(f"Dataset '{dataset_name}' not found in source '{source}'")

        # Otherwise, search all sources
        for source_name, loader in self.loaders.items():
            data = loader.get_dataset(dataset_name)
            if data is not None:
                logger.info(f"Found dataset '{dataset_name}' in source '{source_name}'")
                return data

        raise ValueError(f"Dataset '{dataset_name}' not found in any source")

    def get_combined_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Get combined dataset from all sources.

        Args:
            dataset_name: Name of the dataset to combine

        Returns:
            Combined DataFrame from all sources that have this dataset
        """
        combined_data = []

        for source_name, loader in self.loaders.items():
            try:
                data = loader.get_dataset(dataset_name)
                if data is not None:
                    # Add source column for tracking
                    data["data_source"] = source_name
                    combined_data.append(data)
            except Exception as e:
                logger.warning(f"Error loading {dataset_name} from {source_name}: {e}")

        if not combined_data:
            raise ValueError(f"Dataset '{dataset_name}' not found in any source")

        # Combine and return
        return pd.concat(combined_data, ignore_index=True)

    def list_all_datasets(self) -> Dict[str, List[str]]:
        """List all available datasets from all sources.

        Returns:
            Dictionary mapping source names to list of dataset names
        """
        all_datasets = {}

        for source_name, loader in self.loaders.items():
            try:
                datasets = loader.list_datasets()
                all_datasets[source_name] = datasets
            except Exception as e:
                logger.error(f"Error listing datasets from {source_name}: {e}")
                all_datasets[source_name] = []

        return all_datasets

    def get_metadata(self) -> Dict[str, Dict]:
        """Get metadata for all data sources.

        Returns:
            Dictionary mapping source names to metadata
        """
        metadata = {}

        for source_name, loader in self.loaders.items():
            metadata[source_name] = loader.get_metadata()

        return metadata

    def refresh_cache(self) -> None:
        """Clear and refresh all cached data."""
        logger.info("Refreshing data cache...")
        self.get_dataset.clear()

    def get_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """Get all available datasets.

        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        all_data = {}
        datasets_by_source = self.list_all_datasets()

        for source, datasets in datasets_by_source.items():
            for dataset in datasets:
                if dataset not in all_data:
                    try:
                        all_data[dataset] = self.get_dataset(dataset, source)
                    except Exception as e:
                        logger.warning(f"Error loading {dataset} from {source}: {e}")

        return all_data

    def get_data(self, source: str) -> Dict[str, pd.DataFrame]:
        """Get all data from a specific source.

        Args:
            source: Name of the data source (e.g., 'ai_index', 'mckinsey')

        Returns:
            Dictionary mapping dataset names to DataFrames from the specified source
        """
        if source not in self.loaders:
            logger.error(f"Unknown data source: {source}")
            return {}

        loader = self.loaders[source]
        try:
            datasets = loader.list_datasets()
            result = {}
            for dataset in datasets:
                try:
                    data = loader.get_dataset(dataset)
                    if data is not None:
                        result[dataset] = data
                except Exception as e:
                    logger.warning(f"Error loading dataset '{dataset}' from '{source}': {e}")
            return result
        except Exception as e:
            logger.error(f"Error accessing data from source '{source}': {e}")
            return {}


def init_data_manager(resources_path: Optional[Path] = None) -> DataManager:
    """Factory function to create DataManager instance."""
    return DataManager(resources_path)

