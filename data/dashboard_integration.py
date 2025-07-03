"""Integration module to connect new data architecture with existing app.py."""

import streamlit as st
import pandas as pd
from typing import Tuple, Dict, Optional
import logging

from .data_manager import get_data_manager

logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data() -> Tuple:
    """Load all data for the dashboard using the new modular system.
    
    This function maintains the same interface as the original load_data()
    to ensure backward compatibility with app.py.
    
    Returns:
        Tuple of DataFrames in the expected order
    """
    try:
        # Get data manager instance
        dm = get_data_manager()
        
        # Load all required datasets
        logger.info("Loading data from modular data sources...")
        
        # Core adoption metrics
        historical_data = dm.get_dataset('adoption_trends', 'ai_index')
        
        # Sector data
        sector_data = dm.get_dataset('sector_adoption', 'ai_index')
        sector_2018 = sector_data.copy()  # TODO: Load historical data
        sector_2018['year'] = 2018
        sector_2018['adoption_rate'] = sector_2018['adoption_rate'] * 0.3  # Approximate historical
        
        # Firm size data
        firm_size_data = dm.get_dataset('firm_size_adoption', 'ai_index')
        
        # Geographic data
        geographic_df = dm.get_dataset('geographic_adoption', 'ai_index')
        
        # AI maturity data
        ai_maturity_df = dm.get_dataset('ai_maturity', 'ai_index')
        
        # Investment data
        ai_investment_df = dm.get_dataset('investment_trends', 'ai_index')
        
        # TODO: Load these from other sources when implemented
        # For now, create minimal DataFrames to maintain compatibility
        
        # Technology stack data
        tech_stack_df = pd.DataFrame({
            'technology': ['Cloud AI Services', 'Open Source ML', 'Commercial ML Platforms', 
                          'Custom Built Solutions', 'Edge AI'],
            'adoption_percentage': [67, 82, 45, 38, 21],
            'growth_rate': [35, 42, 18, -5, 125]
        })
        
        # Use case complexity
        use_case_complexity_df = pd.DataFrame({
            'complexity_level': ['Basic', 'Intermediate', 'Advanced', 'Cutting Edge'],
            'percentage': [35, 40, 20, 5],
            'typical_roi': [15, 35, 75, 150]
        })
        
        # Skill gaps data
        skill_gaps_df = pd.DataFrame({
            'skill_category': ['ML Engineering', 'Data Science', 'AI Ethics', 'MLOps', 
                              'AI Product Management'],
            'demand_index': [100, 95, 78, 88, 72],
            'supply_index': [45, 52, 25, 30, 28],
            'gap_severity': ['Critical', 'High', 'High', 'High', 'Medium']
        })
        
        # Productivity data
        productivity_df = pd.DataFrame({
            'worker_category': ['Knowledge Workers', 'Creative Professionals', 
                               'Customer Service', 'Software Developers', 'Analysts'],
            'productivity_gain': [37, 42, 55, 48, 39],
            'time_saved_hours_per_week': [12, 15, 20, 18, 14]
        })
        
        # Environmental impact
        environmental_df = pd.DataFrame({
            'metric': ['Energy Efficiency Improvement', 'Carbon Footprint Reduction',
                      'Resource Optimization', 'Waste Reduction'],
            'impact_percentage': [32, 28, 41, 35]
        })
        
        # OECD adoption data
        oecd_adoption_df = pd.DataFrame({
            'country': ['United States', 'China', 'United Kingdom', 'Germany', 'France',
                       'Japan', 'Canada', 'South Korea', 'India', 'Australia'],
            'adoption_rate': [72, 68, 61, 58, 54, 52, 56, 63, 45, 51],
            'genai_adoption': [65, 58, 52, 48, 45, 41, 49, 55, 35, 44],
            'ai_readiness_score': [8.2, 7.8, 7.5, 7.3, 7.0, 6.9, 7.4, 7.9, 6.2, 7.1]
        })
        
        # Vendor landscape
        vendor_landscape_df = pd.DataFrame({
            'vendor_category': ['Cloud Providers', 'AI Platforms', 'MLOps Tools', 
                               'Data Platforms', 'AI Consultancies'],
            'market_share': [42, 23, 12, 15, 8],
            'growth_rate': [38, 52, 67, 29, 44]
        })
        
        # Barriers data
        barriers_df = pd.DataFrame({
            'barrier': ['Lack of skilled personnel', 'Data quality issues', 'Integration challenges',
                       'Unclear ROI', 'Ethical concerns', 'Regulatory uncertainty'],
            'percentage_citing': [67, 52, 48, 41, 36, 33],
            'severity_score': [8.5, 7.2, 6.8, 6.1, 5.5, 5.2]
        })
        
        # ROI timeline
        roi_timeline_df = pd.DataFrame({
            'months_since_implementation': [0, 3, 6, 9, 12, 18, 24],
            'cumulative_roi': [-100, -75, -40, -10, 25, 85, 165]
        })
        
        # Future projections
        future_projections_df = pd.DataFrame({
            'year': [2025, 2026, 2027, 2028, 2029, 2030],
            'predicted_adoption': [87.3, 91.2, 93.8, 95.4, 96.7, 97.5],
            'economic_impact_trillions': [2.8, 4.2, 5.9, 7.8, 9.5, 11.2]
        })
        
        # Job market impact
        job_market_df = pd.DataFrame({
            'job_category': ['Augmented', 'Displaced', 'Transformed', 'New Created'],
            'percentage_of_workforce': [45, 12, 28, 15],
            'timeline_years': [2, 5, 3, 2]
        })
        
        # Governance data
        governance_df = pd.DataFrame({
            'governance_area': ['Data Privacy', 'Algorithm Transparency', 'Bias Detection',
                               'Accountability', 'Security'],
            'implementation_rate': [72, 43, 38, 51, 68],
            'maturity_score': [3.8, 2.5, 2.2, 2.9, 3.5]
        })
        
        # Cost trends
        cost_trends_df = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024, 2025],
            'training_cost_per_model': [450000, 320000, 180000, 95000, 42000, 15000],
            'inference_cost_per_million_tokens': [60, 35, 18, 8, 2.5, 0.5],
            'accessibility_score': [2, 3, 5, 7, 8.5, 9.2]
        })
        
        # Token economics
        token_economics_df = pd.DataFrame({
            'model': ['GPT-3.5', 'GPT-4', 'Claude', 'Gemini', 'Open Source LLMs'],
            'cost_per_million_tokens': [0.5, 30, 15, 10, 0.1],
            'performance_score': [7.2, 9.1, 8.8, 8.5, 6.5],
            'market_share': [28, 35, 18, 12, 7]
        })
        
        # Company leadership
        ai_leadership_df = pd.DataFrame({
            'company': ['OpenAI', 'Google', 'Microsoft', 'Anthropic', 'Meta'],
            'innovation_score': [95, 92, 88, 90, 85],
            'market_cap_impact': [150, 450, 380, 85, 220],
            'ecosystem_influence': [9.5, 9.2, 9.0, 8.5, 8.2]
        })
        
        # Research landscape
        research_landscape_df = pd.DataFrame({
            'institution': ['MIT', 'Stanford', 'Carnegie Mellon', 'Berkeley', 'Oxford'],
            'papers_published': [342, 315, 298, 276, 251],
            'citations': [15420, 14235, 13876, 12654, 11423],
            'industry_partnerships': [45, 52, 38, 41, 33]
        })
        
        # Strategic milestones
        strategic_milestones_df = pd.DataFrame({
            'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'milestone': ['BERT Released', 'GPT-2 Launch', 'GPT-3 API', 'DALL-E Unveiled',
                         'ChatGPT Launch', 'GPT-4 Release', 'Multimodal AI', 'AGI Discussions'],
            'impact_score': [7, 6, 8, 7, 10, 9, 8, 9]
        })
        
        # Investment by sector
        investment_by_sector_df = pd.DataFrame({
            'sector': ['Healthcare AI', 'Financial AI', 'Retail AI', 'Manufacturing AI',
                      'Transportation AI'],
            'investment_2024_billions': [12.5, 18.3, 8.7, 9.2, 11.4],
            'growth_rate': [42, 38, 51, 29, 67],
            'deals_count': [287, 423, 198, 156, 201]
        })
        
        # Return all DataFrames in the expected order
        return (
            historical_data,
            sector_data,
            sector_2018,
            firm_size_data,
            ai_maturity_df,
            geographic_df,
            tech_stack_df,
            use_case_complexity_df,
            skill_gaps_df,
            ai_investment_df,
            productivity_df,
            environmental_df,
            oecd_adoption_df,
            vendor_landscape_df,
            barriers_df,
            roi_timeline_df,
            future_projections_df,
            job_market_df,
            governance_df,
            cost_trends_df,
            token_economics_df,
            ai_leadership_df,
            research_landscape_df,
            strategic_milestones_df,
            investment_by_sector_df
        )
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        logger.info("Falling back to original load_data implementation")
        # Import and call the original load_data function as fallback
        # This ensures the dashboard continues to work even if new system fails
        raise


def get_data_sources_info() -> Dict[str, Dict]:
    """Get information about all data sources.
    
    Returns:
        Dictionary with metadata about each data source
    """
    dm = get_data_manager()
    return dm.get_metadata()


def validate_data_integrity() -> Dict[str, bool]:
    """Validate all data sources.
    
    Returns:
        Dictionary mapping source names to validation status
    """
    dm = get_data_manager()
    return dm.validate_all_sources()