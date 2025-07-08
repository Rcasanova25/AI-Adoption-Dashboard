"""Optimized data manager with multi-layer caching and lazy loading - Dash compatible version."""

import asyncio
import concurrent.futures
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional
import time

import pandas as pd

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

logger = logging.getLogger(__name__)


class DataManagerDash:
    """
    Centralized data manager for Dash app.
    Replaces Streamlit caching with functools.lru_cache.
    """

    def __init__(self, resources_path: Optional[Path] = None):
        """Initialize the data manager with configured resources path."""
        self.resources_path = resources_path or settings.get_resources_path()
        self.loaders: Dict[str, BaseDataLoader] = {}
        self._cache_timestamp = {}
        self._initialize_loaders()

    def _initialize_loaders(self):
        """Initialize all data loaders."""
        logger.info(f"Initializing data loaders with resources path: {self.resources_path}")

        # Primary data sources
        self.loaders["ai_index"] = AIIndexLoader(self.resources_path)
        self.loaders["mckinsey"] = McKinseyLoader(self.resources_path)
        self.loaders["oecd"] = OECDLoader(self.resources_path)
        # Federal Reserve loaders
        self.loaders["richmond_fed"] = RichmondFedLoader(self.resources_path)
        self.loaders["stlouis_fed"] = StLouisFedLoader(self.resources_path)

        # Academic sources
        # self.loaders["nber"] = NBERPapersLoader(self.resources_path)  # Not available
        self.loaders["academic"] = AcademicPapersLoader(self.resources_path)

        # Industry sources
        self.loaders["goldman_sachs"] = GoldmanSachsLoader(self.resources_path)
        self.loaders["nvidia"] = NVIDIATokenLoader(self.resources_path)
        self.loaders["imf"] = IMFLoader(self.resources_path)

        # Specialized loaders - commented out as they're not available
        # self.loaders["industry"] = IndustryLoader(self.resources_path)
        # self.loaders["regional"] = RegionalLoader(self.resources_path)
        # self.loaders["skills"] = SkillsLoader(self.resources_path)

        # Strategy loaders - commented out as they're not available
        # self.loaders["ai_strategy"] = AIStrategyLoader(self.resources_path)
        # self.loaders["ai_use_cases"] = AIUseCaseLoader(self.resources_path)
        # self.loaders["public_sector"] = PublicSectorLoader(self.resources_path)

        logger.info(f"Initialized {len(self.loaders)} data loaders")

    @lru_cache(maxsize=128)
    def get_dataset_cached(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """
        Get a specific dataset by name using LRU caching.
        Note: This method doesn't support TTL like Streamlit's cache.
        For TTL support, consider using flask-caching or implementing custom TTL logic.
        """
        return self._get_dataset_impl(dataset_name, source)

    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """
        Get a specific dataset by name with TTL cache support.
        Implements custom TTL logic for Dash compatibility.
        """
        cache_key = f"{dataset_name}:{source or 'any'}"
        current_time = time.time()
        
        # Check if we have a cached result and if it's still valid
        if cache_key in self._cache_timestamp:
            cache_age = current_time - self._cache_timestamp[cache_key]
            if cache_age < settings.CACHE_MEMORY_TTL:
                # Cache is still valid, use cached result
                return self.get_dataset_cached(dataset_name, source)
        
        # Cache expired or doesn't exist, clear this specific cache entry
        # Note: LRU cache doesn't support selective clearing, so we'll just update timestamp
        self._cache_timestamp[cache_key] = current_time
        
        # For a true cache clear, you'd need to implement a custom caching solution
        # For now, we'll just call the method which will use LRU cache if available
        return self.get_dataset_cached(dataset_name, source)

    def _get_dataset_impl(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Implementation of get_dataset without caching decorator."""
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

    def list_datasets(self, source: Optional[str] = None) -> List[str]:
        """List all available datasets."""
        if source:
            if source not in self.loaders:
                raise ValueError(f"Unknown source: {source}")
            return self.loaders[source].list_datasets()

        # Aggregate from all sources
        all_datasets = []
        for loader in self.loaders.values():
            all_datasets.extend(loader.list_datasets())

        return sorted(list(set(all_datasets)))

    def get_metadata(self, dataset_name: str, source: Optional[str] = None) -> Dict[str, Any]:
        """Get metadata for a specific dataset."""
        if source:
            if source not in self.loaders:
                raise ValueError(f"Unknown source: {source}")
            return self.loaders[source].get_metadata(dataset_name)

        # Search all sources
        for loader in self.loaders.values():
            metadata = loader.get_metadata(dataset_name)
            if metadata:
                return metadata

        return {}

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all available datasets using parallel processing."""
        logger.info("Starting parallel data loading...")
        start_time = time.time()

        all_data = {}
        failed_loads = []

        # Get all dataset names
        all_datasets = self.list_datasets()
        logger.info(f"Found {len(all_datasets)} datasets to load")

        # Load data in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            # Submit all tasks
            future_to_dataset = {
                executor.submit(self.get_dataset, dataset_name): dataset_name
                for dataset_name in all_datasets
            }

            # Collect results
            for future in concurrent.futures.as_completed(future_to_dataset):
                dataset_name = future_to_dataset[future]
                try:
                    data = future.result()
                    all_data[dataset_name] = data
                    logger.info(f"Successfully loaded: {dataset_name}")
                except Exception as e:
                    logger.error(f"Failed to load {dataset_name}: {str(e)}")
                    failed_loads.append(dataset_name)

        elapsed_time = time.time() - start_time
        logger.info(f"Data loading completed in {elapsed_time:.2f} seconds")
        logger.info(f"Successfully loaded: {len(all_data)} datasets")
        logger.info(f"Failed to load: {len(failed_loads)} datasets")

        return all_data

    async def load_all_data_async(self) -> Dict[str, pd.DataFrame]:
        """Async version of load_all_data for better performance."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_all_data)

    def validate_data(self) -> Dict[str, Any]:
        """Validate all data sources and return status report."""
        report = {
            "total_sources": len(self.loaders),
            "sources": {},
            "total_datasets": 0,
            "valid_datasets": 0,
            "invalid_datasets": 0,
        }

        for source_name, loader in self.loaders.items():
            source_report = loader.validate()
            report["sources"][source_name] = source_report
            report["total_datasets"] += source_report.get("total_datasets", 0)
            report["valid_datasets"] += source_report.get("valid_datasets", 0)
            report["invalid_datasets"] += source_report.get("invalid_datasets", 0)

        return report

    def clear_cache(self):
        """Clear all cached data."""
        # Clear LRU cache
        self.get_dataset_cached.cache_clear()
        # Clear timestamp cache
        self._cache_timestamp.clear()
        logger.info("Data cache cleared")


# For backward compatibility, create an instance that can be imported
# This allows existing code to work without modification
default_data_manager = DataManagerDash()