"""
Enhanced Session State Management for AI Adoption Dashboard
Implements safe data loading with proper error handling and validation
"""

import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Enhanced session state manager with error handling and cache invalidation
    """
    
    @staticmethod
    def get_cache_key(data_source: str, filters: Dict[str, Any] = None) -> str:
        """
        Generate consistent cache keys with dependency tracking
        
        Args:
            data_source: Name of the data source
            filters: Dictionary of filters applied to data
            
        Returns:
            Unique cache key string
        """
        filters = filters or {}
        key_data = f"{data_source}_{filters}_{datetime.now().date()}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    @staticmethod
    def safe_load_data(
        load_function: Callable,
        data_key: str,
        fallback_function: Optional[Callable] = None,
        force_reload: bool = False
    ) -> Optional[Any]:
        """
        Safely load data with error handling and fallback mechanisms
        
        Args:
            load_function: Function to load primary data
            data_key: Key to store data in session state
            fallback_function: Optional fallback function if primary fails
            force_reload: Force reload even if data exists
            
        Returns:
            Loaded data or None if all attempts fail
        """
        # Check if data exists and is valid (unless force reload)
        if not force_reload and data_key in st.session_state:
            data = st.session_state[data_key]
            if SessionManager._validate_session_data(data):
                logger.info(f"Using cached data for {data_key}")
                return data
            else:
                logger.warning(f"Cached data for {data_key} is invalid, reloading")
        
        # Attempt primary data loading
        try:
            logger.info(f"Loading primary data for {data_key}")
            data = load_function()
            
            if SessionManager._validate_loaded_data(data):
                st.session_state[data_key] = data
                st.session_state[f"{data_key}_timestamp"] = datetime.now()
                st.session_state[f"{data_key}_source"] = "primary"
                logger.info(f"Successfully loaded primary data for {data_key}")
                return data
            else:
                raise ValueError("Primary data validation failed")
                
        except Exception as e:
            logger.error(f"Primary data loading failed for {data_key}: {str(e)}")
            st.error(f"Primary data loading failed: {str(e)}")
            
            # Attempt fallback if available
            if fallback_function:
                try:
                    logger.info(f"Attempting fallback data for {data_key}")
                    st.info("Loading fallback data...")
                    
                    data = fallback_function()
                    if SessionManager._validate_loaded_data(data):
                        st.session_state[data_key] = data
                        st.session_state[f"{data_key}_timestamp"] = datetime.now()
                        st.session_state[f"{data_key}_source"] = "fallback"
                        st.warning("Using fallback data due to primary source failure")
                        logger.info(f"Successfully loaded fallback data for {data_key}")
                        return data
                    else:
                        raise ValueError("Fallback data validation failed")
                        
                except Exception as fallback_error:
                    logger.error(f"Fallback loading failed for {data_key}: {str(fallback_error)}")
                    st.error(f"Fallback loading also failed: {str(fallback_error)}")
            
            # All attempts failed
            st.error("No data available. Please check data sources and try again.")
            return None
    
    @staticmethod
    def _validate_session_data(data: Any) -> bool:
        """
        Validate data stored in session state
        
        Args:
            data: Data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if data is None:
            return False
            
        if isinstance(data, pd.DataFrame):
            return not data.empty and len(data.columns) > 0
            
        if isinstance(data, dict):
            return len(data) > 0 and any(v is not None for v in data.values())
            
        if isinstance(data, (list, tuple)):
            return len(data) > 0
            
        return True
    
    @staticmethod
    def _validate_loaded_data(data: Any) -> bool:
        """
        Validate freshly loaded data
        
        Args:
            data: Data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if data is None:
            logger.warning("Data is None")
            return False
            
        if isinstance(data, pd.DataFrame):
            if data.empty:
                logger.warning("DataFrame is empty")
                return False
            if len(data.columns) == 0:
                logger.warning("DataFrame has no columns")
                return False
            return True
            
        if isinstance(data, dict):
            if len(data) == 0:
                logger.warning("Dictionary is empty")
                return False
            if all(v is None for v in data.values()):
                logger.warning("All dictionary values are None")
                return False
            return True
            
        if isinstance(data, (list, tuple)):
            if len(data) == 0:
                logger.warning("List/tuple is empty")
                return False
            return True
            
        return True
    
    @staticmethod
    def check_data_freshness(data_key: str, max_age_hours: int = 24) -> bool:
        """
        Check if cached data is still fresh
        
        Args:
            data_key: Key of the data to check
            max_age_hours: Maximum age in hours before data is considered stale
            
        Returns:
            True if data is fresh, False if stale or missing
        """
        timestamp_key = f"{data_key}_timestamp"
        
        if timestamp_key not in st.session_state:
            return False
            
        timestamp = st.session_state[timestamp_key]
        age = datetime.now() - timestamp
        
        return age < timedelta(hours=max_age_hours)
    
    @staticmethod
    def get_data_info(data_key: str) -> Dict[str, Any]:
        """
        Get information about cached data
        
        Args:
            data_key: Key of the data to check
            
        Returns:
            Dictionary with data information
        """
        info = {
            'exists': data_key in st.session_state,
            'timestamp': None,
            'source': None,
            'age_hours': None,
            'size': None
        }
        
        if info['exists']:
            data = st.session_state[data_key]
            
            # Get timestamp
            timestamp_key = f"{data_key}_timestamp"
            if timestamp_key in st.session_state:
                info['timestamp'] = st.session_state[timestamp_key]
                age = datetime.now() - info['timestamp']
                info['age_hours'] = age.total_seconds() / 3600
            
            # Get source
            source_key = f"{data_key}_source"
            if source_key in st.session_state:
                info['source'] = st.session_state[source_key]
            
            # Get size
            if isinstance(data, pd.DataFrame):
                info['size'] = f"{len(data)} rows × {len(data.columns)} columns"
            elif isinstance(data, dict):
                info['size'] = f"{len(data)} items"
            elif isinstance(data, (list, tuple)):
                info['size'] = f"{len(data)} items"
        
        return info
    
    @staticmethod
    def clear_stale_data(max_age_hours: int = 24) -> int:
        """
        Clear stale data from session state
        
        Args:
            max_age_hours: Maximum age in hours before data is considered stale
            
        Returns:
            Number of stale data items cleared
        """
        cleared_count = 0
        keys_to_remove = []
        
        for key in st.session_state.keys():
            if key.endswith('_timestamp'):
                data_key = key.replace('_timestamp', '')
                if not SessionManager.check_data_freshness(data_key, max_age_hours):
                    keys_to_remove.extend([
                        data_key,
                        f"{data_key}_timestamp", 
                        f"{data_key}_source"
                    ])
                    cleared_count += 1
        
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        if cleared_count > 0:
            logger.info(f"Cleared {cleared_count} stale data items from session state")
        
        return cleared_count
    
    @staticmethod
    def reset_session(keep_settings: bool = True) -> None:
        """
        Reset session state with option to keep user settings
        
        Args:
            keep_settings: Whether to preserve user settings like view selections
        """
        settings_to_keep = {}
        
        if keep_settings:
            settings_keys = ['view_type', 'data_year', 'user_preferences']
            for key in settings_keys:
                if key in st.session_state:
                    settings_to_keep[key] = st.session_state[key]
        
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Restore settings
        for key, value in settings_to_keep.items():
            st.session_state[key] = value
        
        logger.info("Session state reset completed")


# Convenience functions for common operations
def safe_get_dashboard_data(force_reload: bool = False) -> Optional[Dict[str, Any]]:
    """
    Safely get dashboard data with proper error handling
    
    Args:
        force_reload: Force reload of data
        
    Returns:
        Dashboard data dictionary or None
    """
    from main import load_dashboard_data, load_fallback_data
    
    return SessionManager.safe_load_data(
        load_function=load_dashboard_data,
        data_key='dashboard_data',
        fallback_function=load_fallback_data,
        force_reload=force_reload
    )


def initialize_session_state() -> None:
    """Initialize session state with default values"""
    defaults = {
        'view_type': 'Historical Trends',
        'data_year': '2025',
        'first_load': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Clear stale data on first load
    if st.session_state.get('first_load', True):
        SessionManager.clear_stale_data(max_age_hours=24)
        st.session_state.first_load = False