"""
Updated data loading functions with type safety and validation
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Optional, Tuple, Any
from datetime import datetime

# Import our new validation models
from .models import (
    validate_dataset, safe_validate_data, ValidationResult,
    HistoricalDataPoint, SectorData, InvestmentData, FinancialImpactData,
    GeographicData, TokenEconomicsData, AIMaturityData, FirmSizeData
)

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Custom exception for data loading errors"""
    pass


@st.cache_data(ttl=3600, show_spinner=True)
def load_historical_data() -> pd.DataFrame:
    """Load and validate historical AI adoption trends data (2017-2025)"""
    try:
        data = pd.DataFrame({
            'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
            'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
        })
        
        # Validate the data
        if safe_validate_data(data, "historical_data", show_warnings=True):
            logger.info("✅ Historical data loaded and validated successfully")
            return data
        else:
            logger.warning("⚠️ Historical data validation failed, but proceeding with data")
            return data
            
    except Exception as e:
        logger.error(f"Failed to load historical data: {e}")
        raise DataLoadError(f"Historical data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_sector_2025() -> pd.DataFrame:
    """Load and validate 2025 sector data with ROI information"""
    try:
        data = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                      'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
            'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
        })
        
        # Validate the data
        if safe_validate_data(data, "sector_data", show_warnings=True):
            logger.info("✅ 2025 sector data loaded and validated successfully")
        else:
            logger.warning("⚠️ Sector data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load 2025 sector data: {e}")
        raise DataLoadError(f"2025 sector data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_ai_investment_data() -> pd.DataFrame:
    """Load and validate AI investment data from AI Index 2025"""
    try:
        data = pd.DataFrame({
            'year': [2014, 2020, 2021, 2022, 2023, 2024],
            'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
            'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
            'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
            'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
            'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
        })
        
        # Validate the data
        if safe_validate_data(data, "investment_data", show_warnings=True):
            logger.info("✅ AI investment data loaded and validated successfully")
        else:
            logger.warning("⚠️ Investment data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load AI investment data: {e}")
        raise DataLoadError(f"AI investment data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_financial_impact_data() -> pd.DataFrame:
    """Load and validate financial impact by business function"""
    try:
        data = pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                        'Product Development', 'IT', 'HR', 'Finance'],
            'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],
            'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],
            'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],
            'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]
        })
        
        # Validate the data
        if safe_validate_data(data, "financial_impact", show_warnings=True):
            logger.info("✅ Financial impact data loaded and validated successfully")
        else:
            logger.warning("⚠️ Financial impact data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load financial impact data: {e}")
        raise DataLoadError(f"Financial impact data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_token_economics_data() -> pd.DataFrame:
    """Load and validate token economics and pricing data"""
    try:
        data = pd.DataFrame({
            'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B', 
                      'Claude 3 Haiku', 'Llama 3 70B', 'GPT-4', 'Claude 3.5 Sonnet'],
            'cost_per_million_input': [20.00, 0.14, 0.07, 0.25, 0.35, 15.00, 3.00],
            'cost_per_million_output': [20.00, 0.14, 0.07, 1.25, 0.40, 30.00, 15.00],
            'context_window': [4096, 16385, 1000000, 200000, 8192, 128000, 200000],
            'tokens_per_second': [50, 150, 200, 180, 120, 80, 100]
        })
        
        # Validate the data
        if safe_validate_data(data, "token_economics", show_warnings=True):
            logger.info("✅ Token economics data loaded and validated successfully")
        else:
            logger.warning("⚠️ Token economics data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load token economics data: {e}")
        raise DataLoadError(f"Token economics data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_firm_size_data() -> pd.DataFrame:
    """Load and validate firm size adoption data"""
    try:
        data = pd.DataFrame({
            'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                    '500-999', '1000-2499', '2500-4999', '5000+'],
            'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5]
        })
        
        # Validate the data
        if safe_validate_data(data, "firm_size", show_warnings=True):
            logger.info("✅ Firm size data loaded and validated successfully")
        else:
            logger.warning("⚠️ Firm size data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load firm size data: {e}")
        raise DataLoadError(f"Firm size data loading failed: {e}")


@st.cache_data(ttl=3600)
def load_geographic_data() -> pd.DataFrame:
    """Load and validate geographic AI adoption data"""
    try:
        data = pd.DataFrame({
            'city': ['San Francisco Bay Area', 'Nashville', 'San Antonio', 'Las Vegas', 
                    'New Orleans', 'San Diego', 'Seattle', 'Boston'],
            'state': ['California', 'Tennessee', 'Texas', 'Nevada', 
                     'Louisiana', 'California', 'Washington', 'Massachusetts'],
            'lat': [37.7749, 36.1627, 29.4241, 36.1699, 
                   29.9511, 32.7157, 47.6062, 42.3601],
            'lon': [-122.4194, -86.7816, -98.4936, -115.1398, 
                   -90.0715, -117.1611, -122.3321, -71.0589],
            'rate': [9.5, 8.3, 8.3, 7.7, 7.4, 7.4, 6.8, 6.7],
            'state_code': ['CA', 'TN', 'TX', 'NV', 'LA', 'CA', 'WA', 'MA'],
            'population_millions': [7.7, 0.7, 1.5, 0.6, 0.4, 1.4, 0.8, 0.7],
            'gdp_billions': [535, 48, 98, 68, 25, 253, 392, 463]
        })
        
        # Validate the data
        if safe_validate_data(data, "geographic_data", show_warnings=True):
            logger.info("✅ Geographic data loaded and validated successfully")
        else:
            logger.warning("⚠️ Geographic data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load geographic data: {e}")
        raise DataLoadError(f"Geographic data loading failed: {e}")


@st.cache_data(ttl=3600) 
def load_ai_maturity_data() -> pd.DataFrame:
    """Load and validate AI technology maturity data"""
    try:
        data = pd.DataFrame({
            'technology': ['Generative AI', 'AI Agents', 'Foundation Models', 'ModelOps', 
                          'AI Engineering', 'Cloud AI Services', 'Knowledge Graphs', 'Composite AI'],
            'adoption_rate': [71, 15, 45, 25, 30, 78, 35, 12],
            'maturity': ['Peak of Expectations', 'Peak of Expectations', 'Trough of Disillusionment',
                        'Trough of Disillusionment', 'Peak of Expectations', 'Slope of Enlightenment',
                        'Slope of Enlightenment', 'Peak of Expectations'],
            'risk_score': [85, 90, 60, 55, 80, 25, 40, 95],
            'time_to_value': [3, 3, 3, 3, 3, 1, 3, 7]
        })
        
        # Validate the data
        if safe_validate_data(data, "ai_maturity", show_warnings=True):
            logger.info("✅ AI maturity data loaded and validated successfully")
        else:
            logger.warning("⚠️ AI maturity data validation had issues, but proceeding")
            
        return data
        
    except Exception as e:
        logger.error(f"Failed to load AI maturity data: {e}")
        raise DataLoadError(f"AI maturity data loading failed: {e}")


def validate_all_loaded_data(datasets: Dict[str, pd.DataFrame]) -> Dict[str, ValidationResult]:
    """
    Validate all loaded datasets and return comprehensive results
    
    Args:
        datasets: Dictionary of dataset name -> DataFrame
        
    Returns:
        Dictionary of dataset name -> ValidationResult
    """
    validation_results = {}
    
    for dataset_name, df in datasets.items():
        if df is not None:
            try:
                result = validate_dataset(df, dataset_name)
                validation_results[dataset_name] = result
                
                if result.is_valid:
                    logger.info(f"✅ {dataset_name}: {result.validated_rows}/{result.total_rows} rows valid")
                else:
                    logger.warning(f"⚠️ {dataset_name}: Validation issues - {result.error_message}")
                    
                # Log warnings
                for warning in result.warning_messages:
                    logger.warning(f"⚠️ {dataset_name}: {warning}")
                    
            except Exception as e:
                logger.error(f"❌ {dataset_name}: Validation failed - {e}")
                validation_results[dataset_name] = ValidationResult(
                    is_valid=False,
                    error_message=str(e),
                    total_rows=len(df),
                    validated_rows=0
                )
        else:
            logger.warning(f"⚠️ {dataset_name}: Dataset is None")
            validation_results[dataset_name] = ValidationResult(
                is_valid=False,
                error_message="Dataset is None",
                total_rows=0,
                validated_rows=0
            )
    
    return validation_results


def load_all_datasets() -> dict:
    """
    Load all datasets with comprehensive validation
    Returns a dictionary of all datasets
    """
    datasets = {}
    try:
        # Load each dataset individually with validation
        datasets['historical_data'] = load_historical_data()
        datasets['sector_2025'] = load_sector_2025() 
        datasets['ai_investment_data'] = load_ai_investment_data()
        datasets['financial_impact'] = load_financial_impact_data()
        datasets['token_economics'] = load_token_economics_data()
        datasets['firm_size'] = load_firm_size_data()
        datasets['geographic'] = load_geographic_data()
        datasets['ai_maturity'] = load_ai_maturity_data()
        if datasets['geographic'] is not None:
            datasets['state_data'] = create_state_data(datasets['geographic'])
        datasets['sector_2018'] = pd.DataFrame({
            'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services'],
            'firm_weighted': [12, 12, 8, 7],
            'employment_weighted': [18, 22, 15, 14]
        })
        datasets['tech_stack'] = pd.DataFrame({
            'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
            'percentage': [15, 23, 24, 38]
        })
        datasets['productivity_data'] = pd.DataFrame({
            'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
            'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
            'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
        })
        validation_results = validate_all_loaded_data(datasets)
        total_datasets = len(validation_results)
        valid_datasets = sum(1 for result in validation_results.values() if result.is_valid)
        if valid_datasets == total_datasets:
            logger.info(f"🎉 All {total_datasets} datasets passed validation!")
        else:
            logger.warning(f"⚠️ {valid_datasets}/{total_datasets} datasets passed validation")
        return datasets
    except Exception as e:
        logger.error(f"Critical error in data loading: {e}")
        return {}


def create_state_data(geographic_data: pd.DataFrame) -> pd.DataFrame:
    """Create state-level aggregation from geographic data"""
    try:
        # State-level aggregation
        state_data = geographic_data.groupby(['state', 'state_code']).agg({
            'rate': 'mean'
        }).reset_index()
        
        # Add more states
        additional_states = pd.DataFrame({
            'state': ['Michigan', 'Ohio', 'North Carolina', 'Virginia', 'Maryland'],
            'state_code': ['MI', 'OH', 'NC', 'VA', 'MD'],
            'rate': [5.5, 5.8, 6.0, 6.2, 6.4]
        })
        state_data = pd.concat([state_data, additional_states], ignore_index=True)
        
        logger.info("State data created successfully")
        return state_data
    except Exception as e:
        logger.error(f"Failed to create state data: {e}")
        return pd.DataFrame()


# Keep your existing get_dynamic_metrics function exactly the same
def get_dynamic_metrics(
    historical_data: Optional[pd.DataFrame],
    ai_cost_reduction: Optional[pd.DataFrame] = None,
    ai_investment_data: Optional[pd.DataFrame] = None,
    sector_2025: Optional[pd.DataFrame] = None
) -> Dict[str, str]:
    """
    Extract dynamic metrics from loaded data - improved version
    """
    try:
        metrics = {}
        
        # Market acceleration calculation  
        if historical_data is not None and len(historical_data) >= 2:
            # DEBUG: Add debug output for historical data operations
            print("🔍 DEBUG: Historical Data Operations in loaders.py")
            print(f"• historical_data shape: {historical_data.shape}")
            print(f"• historical_data columns: {list(historical_data.columns)}")
            print(f"• historical_data length: {len(historical_data)}")
            
            try:
                latest_adoption = historical_data['ai_use'].iloc[-1]
                print(f"• latest_adoption: {latest_adoption}")
                print(f"• latest_adoption type: {type(latest_adoption)}")
                
                previous_adoption = (historical_data['ai_use'].iloc[-3] 
                                   if len(historical_data) >= 3 
                                   else historical_data['ai_use'].iloc[-2])
                print(f"• previous_adoption: {previous_adoption}")
                print(f"• previous_adoption type: {type(previous_adoption)}")
                
                adoption_delta = latest_adoption - previous_adoption
                print(f"• adoption_delta: {adoption_delta}")
                
                metrics['market_adoption'] = f"{latest_adoption}%"
                metrics['market_delta'] = f"+{adoption_delta}pp vs 2023"
                
                # GenAI adoption
                latest_genai = historical_data['genai_use'].iloc[-1]
                print(f"• latest_genai: {latest_genai}")
                previous_genai = (historical_data['genai_use'].iloc[-3] 
                                if len(historical_data) >= 3 
                                else historical_data['genai_use'].iloc[-2])
                print(f"• previous_genai: {previous_genai}")
                genai_delta = latest_genai - previous_genai
                print(f"• genai_delta: {genai_delta}")
                
                metrics['genai_adoption'] = f"{latest_genai}%"
                metrics['genai_delta'] = f"+{genai_delta}pp from 2023"
                
            except Exception as e:
                print(f"❌ Error in historical data calculation: {e}")
                print(f"• Error type: {type(e)}")
                print(f"• Error details: {str(e)}")
                # Use fallback values
                metrics['market_adoption'] = "78%"
                metrics['market_delta'] = "+23pp vs 2023"
                metrics['genai_adoption'] = "71%"
                metrics['genai_delta'] = "+38pp from 2023"
        else:
            metrics['market_adoption'] = "78%"
            metrics['market_delta'] = "+23pp vs 2023"
            metrics['genai_adoption'] = "71%"
            metrics['genai_delta'] = "+38pp from 2023"
        
        # Cost reduction calculation
        metrics['cost_reduction'] = "280x cheaper"
        metrics['cost_period'] = "Since Nov 2022"
        
        # Investment growth calculation
        if ai_investment_data is not None and len(ai_investment_data) >= 2:
            # DEBUG: Add debug output for investment operations
            print("🔍 DEBUG: Investment Operations in loaders.py")
            print(f"• ai_investment_data shape: {ai_investment_data.shape}")
            print(f"• ai_investment_data columns: {list(ai_investment_data.columns)}")
            
            try:
                latest_investment = ai_investment_data['total_investment'].iloc[-1]
                print(f"• latest_investment: {latest_investment}")
                print(f"• latest_investment type: {type(latest_investment)}")
                
                previous_investment = ai_investment_data['total_investment'].iloc[-2]
                print(f"• previous_investment: {previous_investment}")
                print(f"• previous_investment type: {type(previous_investment)}")
                
                investment_growth = ((latest_investment - previous_investment) / previous_investment) * 100
                print(f"• investment_growth: {investment_growth}")
                
                metrics['investment_value'] = f"${latest_investment}B"
                metrics['investment_delta'] = f"+{investment_growth:.1f}% YoY"
                
            except Exception as e:
                print(f"❌ Error in investment calculation: {e}")
                print(f"• Error type: {type(e)}")
                print(f"• Error details: {str(e)}")
                # Use fallback values
                metrics['investment_value'] = "$252.3B"
                metrics['investment_delta'] = "+44.5% YoY"
        else:
            metrics['investment_value'] = "$252.3B"
            metrics['investment_delta'] = "+44.5% YoY"
        
        # Average ROI calculation
        if sector_2025 is not None and 'avg_roi' in sector_2025.columns:
            # DEBUG: Add debug output for ROI operations
            print("🔍 DEBUG: ROI Operations in loaders.py")
            print(f"• sector_2025 shape: {sector_2025.shape}")
            print(f"• sector_2025 columns: {list(sector_2025.columns)}")
            
            try:
                avg_roi = sector_2025['avg_roi'].mean()
                print(f"• avg_roi: {avg_roi}")
                print(f"• avg_roi type: {type(avg_roi)}")
                
                metrics['avg_roi'] = f"{avg_roi:.1f}x"
                metrics['roi_desc'] = "Across sectors"
                
            except Exception as e:
                print(f"❌ Error in ROI calculation: {e}")
                print(f"• Error type: {type(e)}")
                print(f"• Error details: {str(e)}")
                # Use fallback values
                metrics['avg_roi'] = "3.2x"
                metrics['roi_desc'] = "Across sectors"
        else:
            metrics['avg_roi'] = "3.2x"
            metrics['roi_desc'] = "Across sectors"
        
        return metrics
        
    except Exception as e:
        print(f"❌ Critical error in get_dynamic_metrics: {e}")
        print(f"• Error type: {type(e)}")
        print(f"• Error details: {str(e)}")
        # Return fallback metrics
        return {
            'market_adoption': "78%",
            'market_delta': "+23pp vs 2023",
            'genai_adoption': "71%",
            'genai_delta': "+38pp from 2023",
            'cost_reduction': "280x cheaper",
            'cost_period': "Since Nov 2022",
            'investment_value': "$252.3B",
            'investment_delta': "+44.5% YoY",
            'avg_roi': "3.2x",
            'roi_desc': "Across sectors"
        }