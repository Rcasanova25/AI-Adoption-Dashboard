"""
Geographic Data Handling for AI Adoption Dashboard
Provides geographic visualization data and country-specific AI adoption metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_geographic_data() -> pd.DataFrame:
    """
    Generate comprehensive geographic AI adoption data
    Returns data for interactive world map visualizations
    """
    
    # Updated geographic data based on global AI adoption patterns
    geographic_data = pd.DataFrame({
        'country': [
            'United States', 'China', 'United Kingdom', 'Germany', 'France', 'Japan',
            'Canada', 'South Korea', 'Australia', 'Netherlands', 'Singapore', 'Israel',
            'Sweden', 'Switzerland', 'India', 'Brazil', 'Russia', 'Italy', 'Spain',
            'Denmark', 'Finland', 'Norway', 'Belgium', 'Austria', 'Ireland'
        ],
        'iso_code': [
            'USA', 'CHN', 'GBR', 'DEU', 'FRA', 'JPN', 'CAN', 'KOR', 'AUS', 'NLD',
            'SGP', 'ISR', 'SWE', 'CHE', 'IND', 'BRA', 'RUS', 'ITA', 'ESP',
            'DNK', 'FIN', 'NOR', 'BEL', 'AUT', 'IRL'
        ],
        'ai_adoption_rate': [
            78, 82, 75, 72, 68, 70, 74, 85, 71, 76, 88, 80, 73, 77, 65, 58,
            60, 62, 64, 79, 81, 78, 69, 70, 72
        ],
        'genai_adoption_rate': [
            71, 68, 65, 62, 58, 55, 67, 72, 63, 68, 75, 70, 64, 66, 52, 45,
            48, 50, 54, 69, 71, 67, 59, 61, 64
        ],
        'ai_investment_billions': [
            67.2, 26.1, 8.5, 6.2, 4.8, 4.1, 3.2, 2.8, 1.9, 1.4, 1.2, 1.8,
            0.9, 1.1, 3.7, 2.1, 1.5, 1.3, 1.0, 0.8, 0.6, 0.7, 0.5, 0.4, 0.3
        ],
        'regulatory_maturity': [
            'Advanced', 'Emerging', 'Advanced', 'Advanced', 'Advanced', 'Advanced',
            'Advanced', 'Emerging', 'Advanced', 'Advanced', 'Advanced', 'Advanced',
            'Advanced', 'Advanced', 'Emerging', 'Emerging', 'Basic', 'Advanced', 'Advanced',
            'Advanced', 'Advanced', 'Advanced', 'Advanced', 'Advanced', 'Advanced'
        ],
        'talent_index': [
            92, 85, 88, 84, 82, 81, 87, 89, 83, 86, 90, 88, 85, 87, 78, 72,
            75, 79, 77, 84, 86, 83, 81, 82, 84
        ],
        'digital_infrastructure_score': [
            95, 78, 92, 89, 87, 94, 91, 96, 88, 93, 98, 85, 90, 91, 68, 74,
            72, 81, 83, 94, 92, 89, 88, 86, 90
        ]
    })
    
    # Add derived metrics
    geographic_data['ai_readiness_index'] = (
        geographic_data['ai_adoption_rate'] * 0.3 +
        geographic_data['talent_index'] * 0.25 +
        geographic_data['digital_infrastructure_score'] * 0.25 +
        geographic_data['ai_investment_billions'].rank(pct=True) * 100 * 0.2
    )
    
    # Add competitive tiers
    geographic_data['competitive_tier'] = pd.cut(
        geographic_data['ai_readiness_index'],
        bins=[0, 60, 75, 85, 100],
        labels=['Emerging', 'Developing', 'Advanced', 'Leader']
    )
    
    return geographic_data

def get_regional_analysis() -> Dict[str, pd.DataFrame]:
    """
    Get regional AI adoption analysis grouped by continents/regions
    """
    
    regional_data = {
        'North America': pd.DataFrame({
            'country': ['United States', 'Canada'],
            'ai_adoption_rate': [78, 74],
            'genai_adoption_rate': [71, 67],
            'investment_billions': [67.2, 3.2],
            'population_millions': [331.9, 38.2]
        }),
        
        'Europe': pd.DataFrame({
            'country': ['United Kingdom', 'Germany', 'France', 'Netherlands', 'Sweden', 
                       'Switzerland', 'Denmark', 'Finland', 'Norway', 'Belgium', 'Austria', 'Ireland'],
            'ai_adoption_rate': [75, 72, 68, 76, 73, 77, 79, 81, 78, 69, 70, 72],
            'genai_adoption_rate': [65, 62, 58, 68, 64, 66, 69, 71, 67, 59, 61, 64],
            'investment_billions': [8.5, 6.2, 4.8, 1.4, 0.9, 1.1, 0.8, 0.6, 0.7, 0.5, 0.4, 0.3],
            'population_millions': [67.8, 83.2, 67.8, 17.4, 10.4, 8.7, 5.8, 5.5, 5.4, 11.5, 9.0, 5.0]
        }),
        
        'Asia Pacific': pd.DataFrame({
            'country': ['China', 'Japan', 'South Korea', 'Australia', 'Singapore', 'India'],
            'ai_adoption_rate': [82, 70, 85, 71, 88, 65],
            'genai_adoption_rate': [68, 55, 72, 63, 75, 52],
            'investment_billions': [26.1, 4.1, 2.8, 1.9, 1.2, 3.7],
            'population_millions': [1439.3, 125.8, 51.8, 25.7, 5.9, 1380.0]
        })
    }
    
    return regional_data

def get_country_details(country_name: str) -> Optional[Dict]:
    """
    Get detailed information for a specific country
    
    Args:
        country_name: Name of the country to get details for
        
    Returns:
        Dictionary with country-specific AI adoption details
    """
    
    geo_data = get_geographic_data()
    country_data = geo_data[geo_data['country'] == country_name]
    
    if country_data.empty:
        logger.warning(f"Country '{country_name}' not found in geographic data")
        return None
    
    country_row = country_data.iloc[0]
    
    # Generate additional insights based on the data
    adoption_level = "High" if country_row['ai_adoption_rate'] >= 75 else \
                    "Medium" if country_row['ai_adoption_rate'] >= 60 else "Low"
    
    investment_rank = geo_data['ai_investment_billions'].rank(ascending=False)[country_data.index[0]]
    
    details = {
        'country': country_row['country'],
        'iso_code': country_row['iso_code'],
        'ai_adoption_rate': country_row['ai_adoption_rate'],
        'genai_adoption_rate': country_row['genai_adoption_rate'],
        'ai_investment_billions': country_row['ai_investment_billions'],
        'regulatory_maturity': country_row['regulatory_maturity'],
        'talent_index': country_row['talent_index'],
        'digital_infrastructure_score': country_row['digital_infrastructure_score'],
        'ai_readiness_index': country_row['ai_readiness_index'],
        'competitive_tier': country_row['competitive_tier'],
        'adoption_level': adoption_level,
        'investment_rank': int(investment_rank),
        'key_strengths': _get_country_strengths(country_row),
        'development_areas': _get_development_areas(country_row)
    }
    
    return details

def _get_country_strengths(country_data) -> List[str]:
    """Identify key strengths for a country based on its metrics"""
    strengths = []
    
    if country_data['ai_adoption_rate'] >= 80:
        strengths.append("High AI adoption rate")
    if country_data['genai_adoption_rate'] >= 70:
        strengths.append("Strong generative AI adoption")
    if country_data['talent_index'] >= 85:
        strengths.append("Excellent AI talent pool")
    if country_data['digital_infrastructure_score'] >= 90:
        strengths.append("Advanced digital infrastructure")
    if country_data['ai_investment_billions'] >= 5.0:
        strengths.append("Significant AI investment")
    if country_data['regulatory_maturity'] == 'Advanced':
        strengths.append("Mature AI governance framework")
    
    return strengths if strengths else ["Developing AI capabilities"]

def _get_development_areas(country_data) -> List[str]:
    """Identify development areas for a country"""
    areas = []
    
    if country_data['ai_adoption_rate'] < 60:
        areas.append("Increase AI adoption across industries")
    if country_data['genai_adoption_rate'] < 50:
        areas.append("Expand generative AI implementation")
    if country_data['talent_index'] < 75:
        areas.append("Develop AI talent and skills")
    if country_data['digital_infrastructure_score'] < 80:
        areas.append("Strengthen digital infrastructure")
    if country_data['ai_investment_billions'] < 1.0:
        areas.append("Increase AI research and development investment")
    if country_data['regulatory_maturity'] == 'Basic':
        areas.append("Develop AI governance and regulatory frameworks")
    
    return areas if areas else ["Maintain leadership position"]

def generate_geographic_insights() -> Dict[str, str]:
    """
    Generate key insights about global AI adoption patterns
    """
    
    geo_data = get_geographic_data()
    
    # Calculate key metrics
    avg_adoption = geo_data['ai_adoption_rate'].mean()
    top_adopter = geo_data.loc[geo_data['ai_adoption_rate'].idxmax(), 'country']
    total_investment = geo_data['ai_investment_billions'].sum()
    leader_countries = len(geo_data[geo_data['competitive_tier'] == 'Leader'])
    
    insights = {
        'global_adoption': f"Average global AI adoption rate is {avg_adoption:.1f}%",
        'top_adopter': f"{top_adopter} leads in AI adoption with {geo_data['ai_adoption_rate'].max()}%",
        'investment_scale': f"Global AI investment totals ${total_investment:.1f}B across tracked countries",
        'leader_count': f"{leader_countries} countries classified as AI leaders",
        'regional_disparity': "Significant variation in AI readiness between developed and emerging markets",
        'genai_trend': f"GenAI adoption averaging {geo_data['genai_adoption_rate'].mean():.1f}% globally"
    }
    
    return insights

def validate_geographic_data() -> bool:
    """
    Validate the integrity of geographic data
    """
    try:
        geo_data = get_geographic_data()
        
        # Check required columns
        required_columns = ['country', 'iso_code', 'ai_adoption_rate', 'genai_adoption_rate']
        if not all(col in geo_data.columns for col in required_columns):
            logger.error("Missing required columns in geographic data")
            return False
        
        # Check data ranges
        if not geo_data['ai_adoption_rate'].between(0, 100).all():
            logger.error("AI adoption rates outside valid range (0-100)")
            return False
        
        if not geo_data['genai_adoption_rate'].between(0, 100).all():
            logger.error("GenAI adoption rates outside valid range (0-100)")
            return False
        
        # Check for duplicates
        if geo_data['country'].duplicated().any():
            logger.error("Duplicate countries found in geographic data")
            return False
        
        logger.info("Geographic data validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Geographic data validation failed: {e}")
        return False

# Export functions for easy importing
__all__ = [
    'get_geographic_data',
    'get_regional_analysis', 
    'get_country_details',
    'generate_geographic_insights',
    'validate_geographic_data'
]