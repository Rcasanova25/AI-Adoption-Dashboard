"""Central data service for managing data access across the application."""

import logging
from typing import Dict, Optional, Tuple

import pandas as pd
import streamlit as st

from ..data_manager import DataManager, create_optimized_manager

logger = logging.getLogger(__name__)


# Data mapping: Maps view requirements to data source and dataset names
DATA_MAPPING = {
    "historical_trends": {
        "milestones": ("ai_index", "milestones"),
        "convergence_factors": ("academic", "convergence_analysis"),
        "historical_data": ("ai_index", "adoption_trends"),
    },
    "roi_analysis": {
        "roi_data": ("mckinsey", "roi_by_investment_level"),
        "payback_data": ("mckinsey", "payback_scenarios"),
        "time_to_value": ("mckinsey", "time_to_value_by_capability"),
        "roi_components": ("mckinsey", "roi_components_by_sector"),
    },
    "environmental_impact": {
        "energy_data": ("academic", "ai_energy_consumption"),
        "mitigation": ("oecd", "mitigation_strategies"),
        "metrics": ("oecd", "sustainability_metrics"),
    },
    "geographic_distribution": {
        "enhanced_geographic": ("ai_index", "city_level_adoption"),
        "state_research_data": ("ai_index", "state_research_infrastructure"),
    },
    "sector_analysis": {
        "sector_2018": ("ai_index", "sector_adoption"),
        "sector_2025": ("mckinsey", "use_cases"),
    },
    "firm_size": {
        "firm_size": ("ai_index", "firm_size_adoption"),
    },
    "ai_maturity": {
        "ai_maturity": ("ai_index", "ai_maturity"),
    },
    "financial_impact": {
        "financial_impact": ("mckinsey", "financial_impact"),
        "ai_investment_data": ("ai_index", "investment_trends"),
    },
}


class DataService:
    """Service for managing data access with strict validation and error handling."""

    def __init__(self, data_manager: Optional[DataManager] = None):
        """Initialize the data service.
        
        Args:
            data_manager: Optional data manager instance. If not provided, creates a new one.
        """
        self._data_manager = data_manager or create_optimized_manager()
        self._cache = {}
        
    def get_required_data(self, view_name: str, dataset_name: str) -> pd.DataFrame:
        """Get required data for a view with strict validation.
        
        Args:
            view_name: Name of the view requesting data
            dataset_name: Name of the dataset needed
            
        Returns:
            DataFrame with the requested data
            
        Raises:
            ValueError: If data is not available or invalid
        """
        # Check if mapping exists
        if view_name not in DATA_MAPPING:
            raise ValueError(
                f"❌ Configuration Error: View '{view_name}' not found in data mapping. "
                f"Available views: {list(DATA_MAPPING.keys())}"
            )
            
        if dataset_name not in DATA_MAPPING[view_name]:
            raise ValueError(
                f"❌ Configuration Error: Dataset '{dataset_name}' not found for view '{view_name}'. "
                f"Available datasets: {list(DATA_MAPPING[view_name].keys())}"
            )
            
        # Get source and dataset info
        source_name, source_dataset = DATA_MAPPING[view_name][dataset_name]
        
        # Check cache first
        cache_key = f"{source_name}:{source_dataset}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        # Try to load data
        try:
            logger.info(f"Loading {source_dataset} from {source_name} for {view_name}")
            
            # Get data from the manager
            source_data = self._data_manager.get_data(source_name)
            
            if source_data is None:
                raise ValueError(
                    f"❌ Data Source Error: Source '{source_name}' returned no data. "
                    f"Please ensure the {source_name} data files are available."
                )
                
            # Extract specific dataset
            if source_dataset not in source_data:
                available = list(source_data.keys()) if isinstance(source_data, dict) else []
                raise ValueError(
                    f"❌ Dataset Error: Dataset '{source_dataset}' not found in {source_name}. "
                    f"Available datasets: {available}"
                )
                
            df = source_data[source_dataset]
            
            # Validate data
            if df is None or df.empty:
                raise ValueError(
                    f"❌ Empty Data Error: Dataset '{source_dataset}' from {source_name} is empty. "
                    f"This may indicate a problem with data extraction or the source file."
                )
                
            # Cache successful load
            self._cache[cache_key] = df
            
            logger.info(f"Successfully loaded {len(df)} records from {source_name}:{source_dataset}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load {dataset_name} for {view_name}: {str(e)}")
            raise
            
    def get_optional_data(self, view_name: str, dataset_name: str, default: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get optional data that may not be critical for view operation.
        
        Args:
            view_name: Name of the view requesting data
            dataset_name: Name of the dataset needed
            default: Default DataFrame to return if data unavailable
            
        Returns:
            DataFrame with the requested data or default
        """
        try:
            return self.get_required_data(view_name, dataset_name)
        except ValueError as e:
            logger.warning(f"Optional data not available: {str(e)}")
            return default if default is not None else pd.DataFrame()
            
    def validate_data_availability(self) -> Dict[str, Dict[str, bool]]:
        """Check availability of all configured data sources.
        
        Returns:
            Nested dict of view -> dataset -> availability status
        """
        availability = {}
        
        for view_name, datasets in DATA_MAPPING.items():
            availability[view_name] = {}
            
            for dataset_name, (source_name, source_dataset) in datasets.items():
                try:
                    df = self.get_required_data(view_name, dataset_name)
                    availability[view_name][dataset_name] = not df.empty
                except Exception:
                    availability[view_name][dataset_name] = False
                    
        return availability
        
    def get_data_status_summary(self) -> pd.DataFrame:
        """Get a summary of data availability across all views.
        
        Returns:
            DataFrame with columns: view, dataset, source, available, records
        """
        status_data = []
        
        for view_name, datasets in DATA_MAPPING.items():
            for dataset_name, (source_name, source_dataset) in datasets.items():
                try:
                    df = self.get_required_data(view_name, dataset_name)
                    status_data.append({
                        "view": view_name,
                        "dataset": dataset_name,
                        "source": source_name,
                        "available": True,
                        "records": len(df)
                    })
                except Exception:
                    status_data.append({
                        "view": view_name,
                        "dataset": dataset_name,
                        "source": source_name,
                        "available": False,
                        "records": 0
                    })
                    
        return pd.DataFrame(status_data)
        
    def clear_cache(self):
        """Clear the data cache."""
        self._cache.clear()
        logger.info("Data service cache cleared")


# Singleton instance
_data_service_instance = None


def get_data_service() -> DataService:
    """Get the singleton data service instance.
    
    Returns:
        The data service instance
    """
    global _data_service_instance
    
    if _data_service_instance is None:
        _data_service_instance = DataService()
        
    return _data_service_instance


def show_data_error(error_message: str, recovery_suggestions: Optional[list] = None):
    """Display a data error in the Streamlit UI with recovery suggestions.
    
    Args:
        error_message: The error message to display
        recovery_suggestions: Optional list of recovery suggestions
    """
    st.error(error_message)
    
    if recovery_suggestions:
        with st.expander("🔧 Troubleshooting Steps"):
            for i, suggestion in enumerate(recovery_suggestions, 1):
                st.write(f"{i}. {suggestion}")
                
    # Add data status check button
    if st.button("🔍 Check Data Status"):
        with st.spinner("Checking data availability..."):
            service = get_data_service()
            status_df = service.get_data_status_summary()
            
            # Show summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                total = len(status_df)
                st.metric("Total Datasets", total)
            with col2:
                available = status_df["available"].sum()
                st.metric("Available", available, delta=f"{available/total*100:.0f}%")
            with col3:
                missing = total - available
                st.metric("Missing", missing, delta=f"-{missing/total*100:.0f}%")
                
            # Show detailed status
            st.dataframe(
                status_df.style.apply(
                    lambda x: ["background-color: #90EE90" if v else "background-color: #FFB6C1" 
                              for v in x == True] if x.name == "available" else [""] * len(x),
                    axis=0
                ),
                use_container_width=True
            )
            
    st.stop()