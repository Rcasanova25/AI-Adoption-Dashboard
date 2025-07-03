"""Base data loader interface for all data sources."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import pandas as pd
from pydantic import BaseModel, Field


class DataSource(BaseModel):
    """Metadata for a data source."""
    name: str = Field(..., description="Name of the data source")
    version: str = Field(..., description="Version or year of the data")
    url: Optional[str] = Field(None, description="Source URL if available")
    file_path: Optional[Path] = Field(None, description="Local file path")
    last_updated: datetime = Field(default_factory=datetime.now)
    citation: str = Field(..., description="Proper citation for the source")


class BaseDataLoader(ABC):
    """Abstract base class for all data loaders."""
    
    def __init__(self, source: DataSource):
        """Initialize loader with data source metadata."""
        self.source = source
        self._cache: Dict[str, pd.DataFrame] = {}
    
    @abstractmethod
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load all data from the source.
        
        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate loaded data meets expected schema.
        
        Args:
            data: Dictionary of DataFrames to validate
            
        Returns:
            True if valid, raises exception otherwise
        """
        pass
    
    def get_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset by name.
        
        Args:
            name: Name of the dataset
            
        Returns:
            DataFrame if found, None otherwise
        """
        if not self._cache:
            self._cache = self.load()
        return self._cache.get(name)
    
    def list_datasets(self) -> List[str]:
        """List all available datasets from this source.
        
        Returns:
            List of dataset names
        """
        if not self._cache:
            self._cache = self.load()
        return list(self._cache.keys())
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the data source.
        
        Returns:
            Dictionary with source metadata
        """
        return self.source.model_dump()