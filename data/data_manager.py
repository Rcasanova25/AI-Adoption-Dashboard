"""Optimized data manager with multi-layer caching and lazy loading."""

import asyncio
import concurrent.futures
import logging
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from config.settings import settings
from performance.cache_manager import CacheKeyGenerator, MultiLayerCache, cache_result, get_cache
from performance.monitor import PerformanceContext, get_metrics, track_performance

from .loaders import (
    AcademicPapersLoader,
    AIIndexLoader,
    BaseDataLoader,
    DataSource,
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


class OptimizedDataManager(DataManager):
    """Enhanced data manager with performance optimizations."""

    def __init__(
        self,
        cache_memory_size: int = None,
        cache_memory_ttl: int = None,
        cache_disk_size: int = None,
        max_workers: int = None,
        resources_path: Optional[Path] = None,
    ):
        """Initialize optimized data manager.

        Args:
            cache_memory_size: Max items in memory cache
            cache_memory_ttl: Default TTL for memory cache (seconds)
            cache_disk_size: Max disk cache size in bytes
            max_workers: Max concurrent workers for parallel loading
            resources_path: Optional path to resources directory
        """
        # Use settings defaults if not provided
        if cache_memory_size is None:
            cache_memory_size = settings.CACHE_MEMORY_SIZE
        if cache_memory_ttl is None:
            cache_memory_ttl = settings.CACHE_MEMORY_TTL
        if cache_disk_size is None:
            cache_disk_size = settings.CACHE_DISK_SIZE
        if max_workers is None:
            max_workers = settings.MAX_WORKERS

        super().__init__(resources_path)

        # Initialize enhanced cache
        self.cache = MultiLayerCache(
            memory_size=cache_memory_size, memory_ttl=cache_memory_ttl, disk_size=cache_disk_size
        )

        # Thread pool for parallel operations
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        # Lazy loading state
        self._lazy_loaded: Dict[str, bool] = {}

        # Performance tracking
        self.load_times: Dict[str, float] = {}

    @track_performance
    @cache_result(ttl=600)
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get dataset with caching and performance tracking."""
        with PerformanceContext(f"load_dataset_{dataset_name}"):
            return super().get_dataset(dataset_name, source)

    def get_dataset_async(self, dataset_name: str, source: Optional[str] = None) -> asyncio.Future:
        """Asynchronously load dataset."""
        future = self.executor.submit(self.get_dataset, dataset_name, source)
        return future

    def preload_critical_datasets(self, datasets: List[str]):
        """Preload critical datasets in parallel."""
        logger.info(f"Preloading {len(datasets)} critical datasets...")

        futures = []
        for dataset in datasets:
            future = self.get_dataset_async(dataset)
            futures.append((dataset, future))

        # Wait for all to complete
        for dataset, future in futures:
            try:
                future.result(timeout=30)
                logger.info(f"Successfully preloaded: {dataset}")
            except Exception as e:
                logger.error(f"Failed to preload {dataset}: {e}")

    def get_lazy_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get dataset with lazy loading."""
        cache_key = f"{source or 'all'}:{dataset_name}"

        # Check if already loaded
        if cache_key in self._lazy_loaded and self._lazy_loaded[cache_key]:
            return self._cache.get(cache_key)

        # Load on demand
        data = self.get_dataset(dataset_name, source)
        self._lazy_loaded[cache_key] = True

        return data

    def get_optimized_combined_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Get combined dataset with parallel loading."""
        futures = []

        for source_name in self.loaders:
            future = self.executor.submit(self._load_from_source, dataset_name, source_name)
            futures.append((source_name, future))

        combined_data = []
        for source_name, future in futures:
            try:
                data = future.result(timeout=10)
                if data is not None:
                    data["data_source"] = source_name
                    combined_data.append(data)
            except Exception as e:
                logger.warning(f"Error loading {dataset_name} from {source_name}: {e}")

        if not combined_data:
            raise ValueError(f"Dataset '{dataset_name}' not found in any source")

        return pd.concat(combined_data, ignore_index=True)

    def _load_from_source(self, dataset_name: str, source_name: str) -> Optional[pd.DataFrame]:
        """Helper to load dataset from specific source."""
        try:
            loader = self.loaders[source_name]
            return loader.get_dataset(dataset_name)
        except Exception:
            return None

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        cache_stats = self.cache.get_stats()

        return {
            "cache_stats": cache_stats,
            "load_times": self.load_times,
            "lazy_loaded": len(self._lazy_loaded),
            "total_datasets": sum(len(datasets) for datasets in self.list_all_datasets().values()),
        }

    def cleanup(self):
        """Clean up resources."""
        self.executor.shutdown(wait=True)
        self.cache.cleanup()


def create_optimized_manager(**kwargs) -> OptimizedDataManager:
    """Factory function to create optimized data manager."""
    return OptimizedDataManager(**kwargs)
