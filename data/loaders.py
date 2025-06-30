"""
Data loading functions - Extract from your massive load_data() function
This makes data loading maintainable and testable
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

from config.settings import DashboardConfig
from Utils.helpers import safe_execute, DashboardError

logger = logging.getLogger(__name__)


class DataLoadError(DashboardError):
    """Custom exception for data loading errors"""
    pass


@st.cache_data(ttl=DashboardConfig.UI.CACHE_TTL, show_spinner=True)
def load_historical_data() -> pd.DataFrame:
    """
    Load historical AI adoption trends data
    Extracted from your original load_data() function
    """
    try:
        data = pd.DataFrame({
            'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
            'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
        })
        logger.info("Historical data loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to load historical data: {e}")
        raise DataLoadError(f"Historical data loading failed: {e}")


@st.cache_data(ttl=DashboardConfig.UI.CACHE_TTL)
def load_sector_data_2025() -> pd.DataFrame:
    """
    Load 2025 sector data
    Much cleaner than having this mixed in with everything else
    """
    try:
        data = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
                      'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
            'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
        })
        logger.info("Sector 2025 data loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to load sector data: {e}")
        raise DataLoadError(f"Sector data loading failed: {e}")


@st.cache_data(ttl=DashboardConfig.UI.CACHE_TTL)
def load_investment_data() -> pd.DataFrame:
    """Load AI investment data"""
    try:
        data = pd.DataFrame({
            'year': [2014, 2020, 2021, 2022, 2023, 2024],
            'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
            'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
            'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
            'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
            'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
        })
        logger.info("Investment data loaded successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to load investment data: {e}")
        raise DataLoadError(f"Investment data loading failed: {e}")


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all datasets - replaces your massive load_data() function
    Much more maintainable than one giant function
    """
    datasets = {}
    failed_datasets = []
    
    # Load each dataset safely
    datasets['historical_data'] = safe_execute(
        load_historical_data,
        error_message="Failed to load historical data"
    )
    
    datasets['sector_2025'] = safe_execute(
        load_sector_data_2025,
        error_message="Failed to load sector data"
    )
    
    datasets['investment_data'] = safe_execute(
        load_investment_data,
        error_message="Failed to load investment data"
    )
    
    # Add more datasets here as you extract them from your original function
    # datasets['firm_size'] = safe_execute(load_firm_size_data)
    # datasets['financial_impact'] = safe_execute(load_financial_impact_data)
    
    # Remove None values (failed loads)
    datasets = {k: v for k, v in datasets.items() if v is not None}
    
    logger.info(f"Successfully loaded {len(datasets)} datasets")
    return datasets


def get_dynamic_metrics(
    historical_data: Optional[pd.DataFrame],
    ai_cost_reduction: Optional[pd.DataFrame] = None,
    ai_investment_data: Optional[pd.DataFrame] = None,
    sector_2025: Optional[pd.DataFrame] = None
) -> Dict[str, str]:
    """
    Extract dynamic metrics - improved version of your function
    Now with proper error handling and fallbacks
    """
    try:
        metrics = {}
        
        # Market acceleration calculation
        if historical_data is not None and len(historical_data) >= 2:
            latest_adoption = historical_data['ai_use'].iloc[-1]
            previous_adoption = (historical_data['ai_use'].iloc[-3] 
                               if len(historical_data) >= 3 
                               else historical_data['ai_use'].iloc[-2])
            adoption_delta = latest_adoption - previous_adoption
            metrics['market_adoption'] = f"{latest_adoption}%"
            metrics['market_delta'] = f"+{adoption_delta}pp vs 2023"
            
            latest_genai = historical_data['genai_use'].iloc[-1]
            previous_genai = (historical_data['genai_use'].iloc[-3] 
                            if len(historical_data) >= 3 
                            else historical_data['genai_use'].iloc[-2])
            genai_delta = latest_genai - previous_genai
            metrics['genai_adoption'] = f"{latest_genai}%"
            metrics['genai_delta'] = f"+{genai_delta}pp from 2023"
        else:
            # Use defaults from config instead of hardcoded values
            metrics['market_adoption'] = f"{DashboardConfig.DATA.DEFAULT_ADOPTION_RATE}%"
            metrics['market_delta'] = "+23pp vs 2023"
            metrics['genai_adoption'] = f"{DashboardConfig.DATA.DEFAULT_GENAI_RATE}%"
            metrics['genai_delta'] = "+38pp from 2023"
        
        # Cost reduction calculation (add your logic here)
        metrics['cost_reduction'] = DashboardConfig.DATA.DEFAULT_COST_REDUCTION
        metrics['cost_period'] = "Since Nov 2022"
        
        # Investment calculations (add your logic here)
        metrics['investment_value'] = DashboardConfig.DATA.DEFAULT_INVESTMENT_VALUE
        metrics['investment_delta'] = "+44.5% YoY"
        
        # ROI calculation
        if sector_2025 is not None and 'avg_roi' in sector_2025.columns:
            avg_roi = sector_2025['avg_roi'].mean()
            metrics['avg_roi'] = f"{avg_roi:.1f}x"
        else:
            metrics['avg_roi'] = "3.2x"
        
        metrics['roi_desc'] = "Across sectors"
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating dynamic metrics: {e}")
        # Return safe defaults
        return {
            'market_adoption': f"{DashboardConfig.DATA.DEFAULT_ADOPTION_RATE}%",
            'market_delta': "+23pp vs 2023",
            'genai_adoption': f"{DashboardConfig.DATA.DEFAULT_GENAI_RATE}%", 
            'genai_delta': "+38pp from 2023",
            'cost_reduction': DashboardConfig.DATA.DEFAULT_COST_REDUCTION,
            'cost_period': "Since Nov 2022",
            'investment_value': DashboardConfig.DATA.DEFAULT_INVESTMENT_VALUE,
            'investment_delta': "+44.5% YoY",
            'avg_roi': "3.2x",
            'roi_desc': "Across sectors"
        }