"""Fallback data manager for compatibility - redirects to Dash version."""

import logging

logger = logging.getLogger(__name__)

# Import the Dash version
try:
    from .data_manager_dash import DataManagerDash as DataManager
    logger.info("Using Dash-compatible DataManager")
except ImportError as e:
    logger.error(f"Failed to import DataManagerDash: {e}")
    # Provide a minimal fallback
    class DataManager:
        def __init__(self, resources_path=None):
            self.resources_path = resources_path
            logger.warning("Using minimal fallback DataManager")
        
        def get_dataset(self, dataset_name, source=None):
            logger.warning(f"Fallback: No data available for {dataset_name}")
            import pandas as pd
            return pd.DataFrame()
        
        def list_datasets(self, source=None):
            return []
        
        def load_all_data(self):
            return {}

# For backward compatibility
__all__ = ['DataManager']