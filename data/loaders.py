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
        if safe_validate_data(data, "historical_data", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "sector_data", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "investment_data", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "financial_impact", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "token_economics", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "firm_size", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "geographic_data", show_warnings=True).is_valid:
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
        if safe_validate_data(data, "ai_maturity", show_warnings=True).is_valid:
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


@st.cache_data(ttl=7200, show_spinner=True)
def load_complete_datasets():
    """Load complete dataset collection from backup analysis"""
    try:
        # Historical trends data - UPDATED with AI Index 2025 findings
        historical_data = pd.DataFrame({
            'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],  # Updated: 78% in 2024
            'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]  # Updated: 71% in 2024
        })
        
        # 2018 Sector data
        sector_2018 = pd.DataFrame({
            'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                      'Finance & Insurance', 'Retail Trade', 'Construction'],
            'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
            'employment_weighted': [18, 22, 15, 14, 12, 8, 6]
        })
        
        # 2025 Sector data - NEW for industry-specific insights
        sector_2025 = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                      'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
            'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
        })
        
        # Firm size data
        firm_size = pd.DataFrame({
            'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                    '500-999', '1000-2499', '2500-4999', '5000+'],
            'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5]
        })
        
        # AI Maturity data
        ai_maturity = pd.DataFrame({
            'technology': ['Generative AI', 'AI Agents', 'Foundation Models', 'ModelOps', 
                          'AI Engineering', 'Cloud AI Services', 'Knowledge Graphs', 'Composite AI'],
            'adoption_rate': [71, 15, 45, 25, 30, 78, 35, 12],
            'maturity': ['Peak of Expectations', 'Peak of Expectations', 'Trough of Disillusionment',
                        'Trough of Disillusionment', 'Peak of Expectations', 'Slope of Enlightenment',
                        'Slope of Enlightenment', 'Peak of Expectations'],
            'risk_score': [85, 90, 60, 55, 80, 25, 40, 95],
            'time_to_value': [3, 3, 3, 3, 3, 1, 3, 7]
        })
        
        # Geographic data - enhanced with population and GDP
        geographic = pd.DataFrame({
            'city': ['San Francisco Bay Area', 'Nashville', 'San Antonio', 'Las Vegas', 
                    'New Orleans', 'San Diego', 'Seattle', 'Boston', 'Los Angeles',
                    'Phoenix', 'Denver', 'Austin', 'Portland', 'Miami', 'Atlanta',
                    'Chicago', 'New York', 'Philadelphia', 'Dallas', 'Houston'],
            'state': ['California', 'Tennessee', 'Texas', 'Nevada', 
                     'Louisiana', 'California', 'Washington', 'Massachusetts', 'California',
                     'Arizona', 'Colorado', 'Texas', 'Oregon', 'Florida', 'Georgia',
                     'Illinois', 'New York', 'Pennsylvania', 'Texas', 'Texas'],
            'lat': [37.7749, 36.1627, 29.4241, 36.1699, 
                   29.9511, 32.7157, 47.6062, 42.3601, 34.0522,
                   33.4484, 39.7392, 30.2672, 45.5152, 25.7617, 33.7490,
                   41.8781, 40.7128, 39.9526, 32.7767, 29.7604],
            'lon': [-122.4194, -86.7816, -98.4936, -115.1398, 
                   -90.0715, -117.1611, -122.3321, -71.0589, -118.2437,
                   -112.0740, -104.9903, -97.7431, -122.6784, -80.1918, -84.3880,
                   -87.6298, -74.0060, -75.1652, -96.7970, -95.3698],
            'rate': [9.5, 8.3, 8.3, 7.7, 
                    7.4, 7.4, 6.8, 6.7, 7.2,
                    6.5, 6.3, 7.8, 6.2, 6.9, 7.1,
                    7.0, 8.0, 6.6, 7.5, 7.3],
            'state_code': ['CA', 'TN', 'TX', 'NV', 
                          'LA', 'CA', 'WA', 'MA', 'CA',
                          'AZ', 'CO', 'TX', 'OR', 'FL', 'GA',
                          'IL', 'NY', 'PA', 'TX', 'TX'],
            'population_millions': [7.7, 0.7, 1.5, 0.6, 
                                   0.4, 1.4, 0.8, 0.7, 4.0,
                                   1.7, 0.7, 1.0, 0.7, 0.5, 0.5,
                                   2.7, 8.3, 1.6, 1.3, 2.3],
            'gdp_billions': [535, 48, 98, 68, 
                            25, 253, 392, 463, 860,
                            162, 201, 148, 121, 345, 396,
                            610, 1487, 388, 368, 356]
        })
        
        # State-level aggregation
        state_data = geographic.groupby(['state', 'state_code']).agg({
            'rate': 'mean'
        }).reset_index()
        
        # Add more states
        additional_states = pd.DataFrame({
            'state': ['Michigan', 'Ohio', 'North Carolina', 'Virginia', 'Maryland',
                     'Connecticut', 'New Jersey', 'Indiana', 'Missouri', 'Wisconsin'],
            'state_code': ['MI', 'OH', 'NC', 'VA', 'MD', 'CT', 'NJ', 'IN', 'MO', 'WI'],
            'rate': [5.5, 5.8, 6.0, 6.2, 6.4, 6.8, 6.9, 5.2, 5.4, 5.3]
        })
        state_data = pd.concat([state_data, additional_states], ignore_index=True)
        
        # Technology stack - Fixed percentages to sum to 100
        tech_stack = pd.DataFrame({
            'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
            'percentage': [15, 23, 24, 38]  # Sum = 100
        })
        
        # Productivity data with skill levels - ENHANCED
        productivity_data = pd.DataFrame({
            'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
            'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
            'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
        })
        
        # AI productivity by skill level - NEW
        productivity_by_skill = pd.DataFrame({
            'skill_level': ['Low-skilled', 'Medium-skilled', 'High-skilled'],
            'productivity_gain': [14, 9, 5],
            'skill_gap_reduction': [28, 18, 8]
        })
        
        # AI productivity estimates
        ai_productivity_estimates = pd.DataFrame({
            'source': ['Acemoglu (2024)', 'Brynjolfsson et al. (2023)', 'McKinsey (potential)', 
                      'Goldman Sachs (potential)', 'Richmond Fed'],
            'annual_impact': [0.07, 1.5, 2.0, 2.5, 0.1]
        })
        
        # OECD 2025 Report data
        oecd_g7_adoption = pd.DataFrame({
            'country': ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Japan'],
            'adoption_rate': [45, 38, 42, 40, 35, 32, 48],
            'manufacturing': [52, 45, 48, 55, 42, 40, 58],
            'ict_sector': [68, 62, 65, 63, 58, 55, 70]
        })
        
        # OECD AI Applications - ENHANCED with GenAI use cases
        oecd_applications = pd.DataFrame({
            'application': ['Content Generation', 'Code Generation', 'Customer Service Chatbots',
                           'Predictive Maintenance', 'Process Automation', 'Customer Analytics', 
                           'Quality Control', 'Supply Chain Optimization', 'Fraud Detection',
                           'Product Recommendation', 'Voice Recognition', 'Computer Vision',
                           'Natural Language Processing', 'Robotics Integration', 'Personalized Learning'],
            'usage_rate': [65, 58, 52, 45, 42, 38, 35, 32, 30, 28, 25, 23, 22, 18, 15],
            'category': ['GenAI', 'GenAI', 'GenAI', 'Traditional AI', 'Traditional AI', 
                        'Traditional AI', 'Traditional AI', 'Traditional AI', 'Traditional AI',
                        'Traditional AI', 'Traditional AI', 'Traditional AI', 'Traditional AI', 
                        'Traditional AI', 'GenAI']
        })
        
        # Barriers to AI Adoption
        barriers_data = pd.DataFrame({
            'barrier': ['Lack of skilled personnel', 'Data availability/quality', 'Integration with legacy systems',
                       'Regulatory uncertainty', 'High implementation costs', 'Security concerns',
                       'Unclear ROI', 'Organizational resistance'],
            'percentage': [68, 62, 58, 55, 52, 48, 45, 40]
        })
        
        # Support effectiveness
        support_effectiveness = pd.DataFrame({
            'support_type': ['Government education investment', 'University partnerships', 
                            'Public-private collaboration', 'Regulatory clarity',
                            'Tax incentives', 'Innovation grants', 'Technology centers'],
            'effectiveness_score': [82, 78, 75, 73, 68, 65, 62]
        })
        
        # NEW: Skill gap data - CRITICAL MISSING ANALYSIS
        skill_gap_data = pd.DataFrame({
            'skill': ['AI/ML Engineering', 'Data Science', 'AI Ethics', 'Prompt Engineering',
                     'AI Product Management', 'MLOps', 'AI Security', 'Change Management'],
            'gap_severity': [85, 78, 72, 68, 65, 62, 58, 55],
            'training_initiatives': [45, 52, 28, 38, 32, 35, 22, 48]
        })
        
        # NEW: AI governance data - CRITICAL MISSING ANALYSIS
        ai_governance = pd.DataFrame({
            'aspect': ['Ethics Guidelines', 'Data Privacy', 'Bias Detection', 'Transparency',
                      'Accountability Framework', 'Risk Assessment', 'Regulatory Compliance'],
            'adoption_rate': [62, 78, 45, 52, 48, 55, 72],
            'maturity_score': [3.2, 3.8, 2.5, 2.8, 2.6, 3.0, 3.5]  # Out of 5
        })
        
        # NEW: AI Investment data from AI Index 2025
        ai_investment_data = pd.DataFrame({
            'year': [2014, 2020, 2021, 2022, 2023, 2024],
            'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
            'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
            'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
            'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
            'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
        })
        
        # NEW: Regional AI adoption growth from AI Index 2025
        regional_growth = pd.DataFrame({
            'region': ['Greater China', 'Europe', 'North America', 'Asia-Pacific', 'Latin America'],
            'growth_2024': [27, 23, 15, 18, 12],
            'adoption_rate': [68, 65, 82, 58, 45],
            'investment_growth': [32, 28, 44, 25, 18]
        })
        
        # NEW: AI cost reduction data from AI Index 2025
        ai_cost_reduction = pd.DataFrame({
            'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
            'cost_per_million_tokens': [20.00, 0.14, 0.07],
            'year': [2022, 2024, 2024]
        })
        
        # CORRECTED: Financial impact by function from AI Index 2025
        financial_impact = pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                        'Product Development', 'IT', 'HR', 'Finance'],
            'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],  # % of companies
            'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],  # % of companies
            'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],  # Actual % reduction for those who see benefits
            'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]  # Actual % increase for those who see benefits
        })
        
        # NEW: Generational AI perception data from AI Index 2025
        ai_perception = pd.DataFrame({
            'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
            'expect_job_change': [67, 65, 58, 49],
            'expect_job_replacement': [42, 40, 34, 28]
        })
        
        # NEW: Training emissions data from AI Index 2025
        training_emissions = pd.DataFrame({
            'model': ['AlexNet (2012)', 'GPT-3 (2020)', 'GPT-4 (2023)', 'Llama 3.1 405B (2024)'],
            'carbon_tons': [0.01, 588, 5184, 8930]
        })
        
        # NEW: Skill gap data
        skill_gap_data = pd.DataFrame({
            'skill': ['AI/ML Engineering', 'Data Science', 'AI Ethics', 'Prompt Engineering',
                     'AI Product Management', 'MLOps', 'AI Security', 'Change Management'],
            'gap_severity': [85, 78, 72, 68, 65, 62, 58, 55],
            'training_initiatives': [45, 52, 28, 38, 32, 35, 22, 48]
        })
        
        # NEW: AI governance data
        ai_governance = pd.DataFrame({
            'aspect': ['Ethics Guidelines', 'Data Privacy', 'Bias Detection', 'Transparency',
                      'Accountability Framework', 'Risk Assessment', 'Regulatory Compliance'],
            'adoption_rate': [62, 78, 45, 52, 48, 55, 72],
            'maturity_score': [3.2, 3.8, 2.5, 2.8, 2.6, 3.0, 3.5]  # Out of 5
        })
        
        # 2025 GenAI by function (for backward compatibility)
        genai_2025 = pd.DataFrame({
            'function': ['Marketing & Sales', 'Product Development', 'Service Operations', 
                        'Software Engineering', 'IT', 'Knowledge Management', 'HR', 'Supply Chain'],
            'adoption': [42, 28, 23, 22, 23, 21, 13, 7]
        })
        
        # NEW: Token economics data
        token_economics = pd.DataFrame({
            'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B', 
                      'Claude 3 Haiku', 'Llama 3 70B', 'GPT-4', 'Claude 3.5 Sonnet'],
            'cost_per_million_input': [20.00, 0.14, 0.07, 0.25, 0.35, 15.00, 3.00],
            'cost_per_million_output': [20.00, 0.14, 0.07, 1.25, 0.40, 30.00, 15.00],
            'context_window': [4096, 16385, 1000000, 200000, 8192, 128000, 200000],
            'tokens_per_second': [50, 150, 200, 180, 120, 80, 100]
        })
        
        # Token usage patterns
        token_usage_patterns = pd.DataFrame({
            'use_case': ['Simple Chat', 'Document Analysis', 'Code Generation', 
                         'Creative Writing', 'Data Analysis', 'Reasoning Tasks'],
            'avg_input_tokens': [50, 5000, 500, 200, 2000, 1000],
            'avg_output_tokens': [200, 500, 1500, 2000, 1000, 5000],
            'input_output_ratio': [0.25, 10.0, 0.33, 0.10, 2.0, 0.20]
        })
        
        # Token optimization strategies
        token_optimization = pd.DataFrame({
            'strategy': ['Prompt Engineering', 'Context Caching', 'Batch Processing', 
                        'Model Selection', 'Response Streaming', 'Token Pruning'],
            'cost_reduction': [30, 45, 60, 70, 15, 25],
            'implementation_complexity': [2, 4, 3, 1, 2, 5],  # 1-5 scale
            'time_to_implement': [1.0, 7.0, 3.0, 0.5, 2.0, 14.0]  # days as float
        })
        
        # Token pricing evolution - Fixed with explicit date list
        token_pricing_evolution = pd.DataFrame({
            'date': pd.to_datetime(['2022-11-01', '2023-02-01', '2023-05-01', '2023-08-01', '2023-11-01',
                                   '2024-02-01', '2024-05-01', '2024-08-01', '2024-11-01', '2025-02-01', '2025-05-01']),
            'avg_price_input': [20.0, 18.0, 15.0, 10.0, 5.0, 3.0, 1.5, 0.8, 0.5, 0.3, 0.2],
            'avg_price_output': [20.0, 19.0, 16.0, 12.0, 8.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.8],
            'models_available': [5, 8, 12, 18, 25, 35, 45, 58, 72, 85, 95]
        })
        
        # Return as dictionary for modular system
        return {
            'historical_data': historical_data,
            'sector_2018': sector_2018,
            'sector_2025': sector_2025,
            'firm_size': firm_size,
            'ai_maturity': ai_maturity,
            'geographic': geographic,
            'state_data': state_data,
            'tech_stack': tech_stack,
            'productivity_data': productivity_data,
            'productivity_by_skill': productivity_by_skill,
            'ai_productivity_estimates': ai_productivity_estimates,
            'oecd_g7_adoption': oecd_g7_adoption,
            'oecd_applications': oecd_applications,
            'barriers_data': barriers_data,
            'support_effectiveness': support_effectiveness,
            'ai_investment_data': ai_investment_data,
            'regional_growth': regional_growth,
            'ai_cost_reduction': ai_cost_reduction,
            'financial_impact': financial_impact,
            'ai_perception': ai_perception,
            'training_emissions': training_emissions,
            'skill_gap_data': skill_gap_data,
            'ai_governance': ai_governance,
            'genai_2025': genai_2025,
            'token_economics': token_economics,
            'token_usage_patterns': token_usage_patterns,
            'token_optimization': token_optimization,
            'token_pricing_evolution': token_pricing_evolution
        }
    
    except Exception as e:
        logger.error(f"Error in complete data loading: {str(e)}")
        return None


def load_all_datasets() -> dict:
    """
    Load all datasets with comprehensive validation
    Returns a dictionary of all datasets
    """
    try:
        # Use the new comprehensive data loading function
        datasets = load_complete_datasets()
        
        if datasets is None:
            logger.error("Complete data loading failed")
            return {}
        
        # Validate all loaded datasets
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


# Updated get_dynamic_metrics function to work with complete data
def get_dynamic_metrics(datasets):
    """Extract dynamic metrics from complete loaded datasets"""
    
    if not datasets:
        # Fallback metrics if data loading fails
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
    
    historical_data = datasets.get('historical_data')
    ai_cost_reduction = datasets.get('ai_cost_reduction')
    ai_investment_data = datasets.get('ai_investment_data')
    sector_2025 = datasets.get('sector_2025')
    
    metrics = {}
    
    # Market acceleration calculation
    if historical_data is not None and len(historical_data) >= 2:
        try:
            latest_adoption = historical_data['ai_use'].iloc[-1]
            previous_adoption = historical_data['ai_use'].iloc[-3] if len(historical_data) >= 3 else historical_data['ai_use'].iloc[-2]
            adoption_delta = latest_adoption - previous_adoption
            metrics['market_adoption'] = f"{latest_adoption}%"
            metrics['market_delta'] = f"+{adoption_delta:.0f}pp vs 2023"
            
            # GenAI adoption
            latest_genai = historical_data['genai_use'].iloc[-1]
            previous_genai = historical_data['genai_use'].iloc[-3] if len(historical_data) >= 3 else historical_data['genai_use'].iloc[-2]
            genai_delta = latest_genai - previous_genai
            metrics['genai_adoption'] = f"{latest_genai}%"
            metrics['genai_delta'] = f"+{genai_delta:.0f}pp from 2023"
            
        except Exception as e:
            logger.warning(f"Error in historical data calculation: {e}")
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
    if ai_cost_reduction is not None and len(ai_cost_reduction) >= 2:
        try:
            earliest_cost = ai_cost_reduction['cost_per_million_tokens'].iloc[0]
            latest_cost = ai_cost_reduction['cost_per_million_tokens'].iloc[-1]
            cost_multiplier = earliest_cost / latest_cost
            metrics['cost_reduction'] = f"{cost_multiplier:.0f}x cheaper"
            metrics['cost_period'] = "Since Nov 2022"
            
        except Exception as e:
            logger.warning(f"Error in cost reduction calculation: {e}")
            metrics['cost_reduction'] = "280x cheaper"
            metrics['cost_period'] = "Since Nov 2022"
    else:
        metrics['cost_reduction'] = "280x cheaper"
        metrics['cost_period'] = "Since Nov 2022"
    
    # Investment growth calculation
    if ai_investment_data is not None and len(ai_investment_data) >= 2:
        try:
            latest_investment = ai_investment_data['total_investment'].iloc[-1]
            previous_investment = ai_investment_data['total_investment'].iloc[-2]
            investment_growth = ((latest_investment - previous_investment) / previous_investment) * 100
            metrics['investment_value'] = f"${latest_investment}B"
            metrics['investment_delta'] = f"+{investment_growth:.1f}% YoY"
            
        except Exception as e:
            logger.warning(f"Error in investment calculation: {e}")
            metrics['investment_value'] = "$252.3B"
            metrics['investment_delta'] = "+44.5% YoY"
    else:
        metrics['investment_value'] = "$252.3B"
        metrics['investment_delta'] = "+44.5% YoY"
    
    # Average ROI calculation
    if sector_2025 is not None and 'avg_roi' in sector_2025.columns:
        try:
            avg_roi = sector_2025['avg_roi'].mean()
            metrics['avg_roi'] = f"{avg_roi:.1f}x"
            metrics['roi_desc'] = "Across sectors"
            
        except Exception as e:
            logger.warning(f"Error in ROI calculation: {e}")
            metrics['avg_roi'] = "3.2x"
            metrics['roi_desc'] = "Across sectors"
    else:
        metrics['avg_roi'] = "3.2x"
        metrics['roi_desc'] = "Across sectors"
    
    return metrics