"""Central data management system for the Economics of AI Dashboard."""

from typing import Dict, List, Optional, Union
import pandas as pd
import logging
from pathlib import Path
from functools import lru_cache

from .loaders import (
    BaseDataLoader,
    AIIndexLoader,
    # McKinseyLoader,
    # OECDLoader,
    # FederalReserveLoader
)

logger = logging.getLogger(__name__)


class DataManager:
    """Manages all data sources and provides unified access to dashboard data."""
    
    def __init__(self, resources_path: Optional[Path] = None):
        """Initialize data manager with path to resources directory."""
        if resources_path is None:
            resources_path = Path("/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/AI adoption resources")
        
        self.resources_path = resources_path
        self.loaders: Dict[str, BaseDataLoader] = {}
        self._cache: Dict[str, pd.DataFrame] = {}
        
        # Initialize loaders
        self._initialize_loaders()
    
    def _initialize_loaders(self):
        """Initialize all data loaders."""
        logger.info("Initializing data loaders...")
        
        # AI Index loader
        ai_index_path = self.resources_path / "AI dashboard resources 1/hai_ai_index_report_2025.pdf"
        self.loaders['ai_index'] = AIIndexLoader(ai_index_path)
        
        # TODO: Add other loaders as they are implemented
        # self.loaders['mckinsey'] = McKinseyLoader(mckinsey_path)
        # self.loaders['oecd'] = OECDLoader(oecd_path)
        # self.loaders['fed'] = FederalReserveLoader(fed_path)
        
        logger.info(f"Initialized {len(self.loaders)} data loaders")
    
    @lru_cache(maxsize=32)
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
                    data['data_source'] = source_name
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
        
        # Pre-load commonly used datasets
        common_datasets = ['adoption_trends', 'sector_adoption', 'geographic_adoption']
        for dataset in common_datasets:
            try:
                self.get_dataset(dataset)
            except Exception as e:
                logger.warning(f"Could not pre-load {dataset}: {e}")
    
    def validate_all_sources(self) -> Dict[str, bool]:
        """Validate all data sources.
        
        Returns:
            Dictionary mapping source names to validation status
        """
        validation_results = {}
        
        for source_name, loader in self.loaders.items():
            try:
                data = loader.load()
                is_valid = loader.validate(data)
                validation_results[source_name] = is_valid
            except Exception as e:
                logger.error(f"Validation failed for {source_name}: {e}")
                validation_results[source_name] = False
        
        return validation_results


# Singleton instance
_data_manager_instance = None


def get_data_manager(resources_path: Optional[Path] = None) -> DataManager:
    """Get or create the singleton DataManager instance.
    
    Args:
        resources_path: Optional path to resources directory
        
    Returns:
        DataManager instance
    """
    global _data_manager_instance
    
    if _data_manager_instance is None:
        _data_manager_instance = DataManager(resources_path)
    
    return _data_manager_instance