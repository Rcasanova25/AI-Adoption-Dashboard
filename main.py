"""
Main entry point for AI Adoption Dashboard
Refactored with modular architecture and comprehensive data validation
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import configuration
from config.constants import (
    APP_TITLE, APP_ICON, APP_VERSION, AUTHOR,
    VIEW_TYPES, DATA_SOURCES, ERROR_MESSAGES, SUCCESS_MESSAGES
)

# Import utilities
from Utils.data_validation import DataValidator, create_retry_button
from Utils.helpers import clean_filename, safe_execute, safe_data_check
from Utils.navigation import setup_navigation

# Import data infrastructure  
from data.loaders import (
    load_all_datasets, validate_all_loaded_data, 
    load_authentic_research_datasets, get_data_credibility_metrics
)
from data.models import safe_validate_data
from data.research_integration import display_data_authenticity_dashboard

# Import all migrated views
from views.adoption_rates import show_adoption_rates
from views.historical_trends import show_historical_trends
from views.industry_analysis import show_industry_analysis
from views.financial_impact import show_financial_impact
from views.investment_trends import show_investment_trends
from views.regional_growth import show_regional_growth
from views.ai_cost_trends import show_ai_cost_trends
from views.token_economics import show_token_economics
from views.labor_impact import show_labor_impact
from views.environmental_impact import show_environmental_impact
from views.skill_gap_analysis import show_skill_gap_analysis
from views.ai_governance import show_ai_governance
from views.productivity_research import show_productivity_research
from views.firm_size_analysis import show_firm_size_analysis
from views.technology_stack import show_technology_stack
from views.ai_maturity import show_ai_technology_maturity
from views.geographic_distribution import show_geographic_distribution
from views.oecd_findings import show_oecd_2025_findings
from views.barriers_support import show_barriers_support
from views.roi_analysis import show_roi_analysis
from views.causal_analysis import show_causal_analysis
from views.bibliography import show_bibliography_sources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        'About': f"# AI Adoption Dashboard\\nVersion {APP_VERSION}\\n\\nTrack AI adoption trends across industries and geographies.\\n\\nCreated by {AUTHOR}"
    }
)


@st.cache_data(ttl=3600)
def load_dashboard_data() -> Dict[str, Any]:
    """
    Load and validate all dashboard data with comprehensive error handling
    
    Returns:
        Dictionary containing all dashboard data
    """
    try:
        # Try McKinsey tools first
        logger.info("Attempting to load data with McKinsey tools...")
        
        # Import McKinsey tools (with fallback handling)
        try:
            from business.causal_analysis import causal_engine
            from data.kedro_pipeline import kedro_manager
            from visualization.vizro_dashboard import vizro_dashboard
            
            # Try Kedro pipeline
            pipeline_result = kedro_manager.run_pipeline(
                pipeline_name="ai_adoption_pipeline",
                runner_type="parallel", 
                tags=["data_ingestion", "data_processing"]
            )
            
            if pipeline_result.get('status') == 'completed':
                logger.info("✅ McKinsey Kedro pipeline completed successfully")
                dashboard_data = {
                    'summary': kedro_manager.catalog.load("dashboard_summary"),
                    'detailed': kedro_manager.catalog.load("dashboard_detailed"), 
                    'geographic': kedro_manager.catalog.load("dashboard_geographic"),
                    'source': 'kedro_pipeline'
                }
                st.success("✅ Data loaded using McKinsey Kedro pipeline")
                return dashboard_data
                
        except Exception as e:
            logger.warning(f"McKinsey tools unavailable: {e}")
        
        # Try authentic research data first
        logger.info("Loading authentic research data...")
        return load_authentic_dashboard_data()
        
    except Exception as e:
        logger.error(f"Critical data loading error: {e}")
        st.error(f"{ERROR_MESSAGES['data_loading_failed']}: {str(e)}")
        return {}


def load_authentic_dashboard_data() -> Dict[str, Any]:
    """
    Load authentic research data with comprehensive source attribution
    
    Returns:
        Dictionary with all authentic research datasets and credibility metrics
    """
    logger.info("Loading authentic research data...")
    
    try:
        # Load authentic research datasets
        authentic_datasets = load_authentic_research_datasets()
        
        # Get data credibility metrics
        credibility_metrics = get_data_credibility_metrics()
        
        # Extract individual components for backward compatibility
        dashboard_data = {
            'historical_data': authentic_datasets.get('historical_data', pd.DataFrame()),
            'sector_2025': authentic_datasets.get('sector_2025', pd.DataFrame()),
            'sector_2018': authentic_datasets.get('sector_2018', pd.DataFrame()),
            'financial_impact': authentic_datasets.get('financial_impact', pd.DataFrame()),
            'ai_investment': authentic_datasets.get('ai_investment', pd.DataFrame()),
            'productivity_data': authentic_datasets.get('productivity_data', pd.DataFrame()),
            'gdp_impact': authentic_datasets.get('gdp_impact', pd.DataFrame()),
            'token_economics': authentic_datasets.get('token_economics', pd.DataFrame()),
            'geographic': authentic_datasets.get('geographic', pd.DataFrame()),
            'source': 'authentic_research',
            'credibility_metrics': credibility_metrics,
            'data_authenticity': True
        }
        
        logger.info("✅ Authentic research data loaded successfully")
        logger.info(f"📊 Data credibility: {credibility_metrics['data_authenticity']['credibility_score']}")
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Failed to load authentic research data: {e}")
        logger.info("🔄 Falling back to synthetic data")
        return load_fallback_data()


def load_fallback_data() -> Dict[str, Any]:
    """
    Load enhanced fallback data with proper validation (legacy synthetic data)
    
    Returns:
        Dictionary with all required data components
    """
    logger.info("Loading fallback synthetic data...")
    
    try:
        # Historical trends data (synthetic)
        historical_data = pd.DataFrame({
            'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
            'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71],
            'data_source': ['Synthetic fallback data'] * 9
        })
        
        # 2025 Sector data  
        sector_2025 = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                      'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
            'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
        })
        
        # 2018 Sector data
        sector_2018 = pd.DataFrame({
            'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                      'Finance & Insurance', 'Retail Trade', 'Construction'],
            'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
            'employment_weighted': [8, 15, 6, 9, 7, 3, 2]
        })
        
        # Financial impact data
        financial_impact = pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations', 'Product Development', 
                        'Human Resources', 'Strategy & Corporate Finance', 'Manufacturing',
                        'Risk', 'Supply Chain'],
            'companies_reporting_revenue_gains': [71, 49, 52, 43, 47, 39, 35, 41],
            'companies_reporting_cost_savings': [58, 63, 45, 55, 42, 57, 48, 52]
        })
        
        # AI investment data
        ai_investment = pd.DataFrame({
            'year': [2014, 2020, 2021, 2022, 2023, 2024],
            'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
            'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
            'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
            'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
            'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
        })
        
        dashboard_data = {
            'historical_data': historical_data,
            'sector_2025': sector_2025,
            'sector_2018': sector_2018,
            'financial_impact': financial_impact,
            'ai_investment': ai_investment,
            'source': 'fallback'
        }
        
        # Validate all loaded data
        validator = DataValidator()
        for name, df in dashboard_data.items():
            if isinstance(df, pd.DataFrame):
                result = validator.validate_dataframe(df, name, show_warning=False)
                if not result.is_valid:
                    logger.warning(f"Validation issue with {name}: {result.message}")
        
        logger.info("✅ Fallback data loaded and validated successfully")
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Failed to load fallback data: {e}")
        st.error(f"Critical error loading fallback data: {str(e)}")
        return {}


def extract_data_components(dashboard_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Extract individual data components for backward compatibility
    
    Args:
        dashboard_data: Full dashboard data dictionary
        
    Returns:
        Dictionary with individual dataframe components
    """
    components = {}
    
    # Define expected components
    expected_components = [
        'historical_data', 'sector_2025', 'sector_2018', 'financial_impact',
        'ai_investment', 'regional_data', 'labor_impact', 'skill_gap_data',
        'governance_data', 'productivity_data', 'firm_size_data', 'tech_stack',
        'maturity_data', 'geographic_data', 'oecd_data', 'barriers_data',
        'roi_data', 'causal_data', 'environmental_data', 'token_economics'
    ]
    
    for component in expected_components:
        components[component] = dashboard_data.get(component, pd.DataFrame())
    
    return components


def create_navigation() -> str:
    """Create sidebar navigation and return selected view"""
    st.sidebar.title("🤖 AI Adoption Dashboard")
    st.sidebar.markdown(f"*Version {APP_VERSION}*")
    
    # View selection
    view_type = st.sidebar.selectbox(
        "Select Analysis View:",
        VIEW_TYPES,
        index=0,
        help="Choose which aspect of AI adoption to analyze"
    )
    
    # Data year filter
    data_year = st.sidebar.selectbox(
        "Data Year Focus:",
        ["2025", "2018", "Historical"],
        index=0,
        help="Select which year's data to emphasize in the analysis"
    )
    
    # Data source info
    with st.sidebar.expander("📊 Data Sources", expanded=False):
        for source_key, source_info in DATA_SOURCES.items():
            st.write(f"**{source_info['name']} ({source_info['year']})**")
            st.write(f"_{source_info['description']}_")
            st.write("")
    
    # Store in session state for access across components
    st.session_state.view_type = view_type
    st.session_state.data_year = data_year
    
    return view_type


def route_to_view(view_type: str, data_components: Dict[str, pd.DataFrame], dashboard_data: Dict[str, Any]) -> None:
    """
    Route to the appropriate view function based on selection
    
    Args:
        view_type: Selected view type
        data_components: Individual dataframe components
        dashboard_data: Full dashboard data dictionary
    """
    data_year = st.session_state.get('data_year', '2025')
    
    try:
        if view_type == "Historical Trends":
            show_historical_trends(
                data_year=data_year,
                historical_data=data_components.get('historical_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Industry Analysis":
            show_industry_analysis(
                data_year=data_year,
                sector_2025=data_components.get('sector_2025', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Financial Impact":
            show_financial_impact(
                data_year=data_year,
                financial_impact=data_components.get('financial_impact', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Investment Trends":
            show_investment_trends(
                data_year=data_year,
                ai_investment=data_components.get('ai_investment', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Regional Growth":
            show_regional_growth(
                data_year=data_year,
                regional_data=data_components.get('regional_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "AI Cost Trends":
            show_ai_cost_trends(
                data_year=data_year,
                cost_data=data_components.get('cost_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Token Economics":
            show_token_economics(
                data_year=data_year,
                token_economics=data_components.get('token_economics', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Labor Impact":
            show_labor_impact(
                data_year=data_year,
                labor_impact=data_components.get('labor_impact', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Environmental Impact":
            show_environmental_impact(
                data_year=data_year,
                environmental_data=data_components.get('environmental_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Adoption Rates":
            show_adoption_rates(
                data_year=data_year,
                financial_impact=data_components.get('financial_impact', pd.DataFrame()),
                sector_2018=data_components.get('sector_2018', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Skill Gap Analysis":
            show_skill_gap_analysis(
                data_year=data_year,
                skill_gap_data=data_components.get('skill_gap_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "AI Governance":
            show_ai_governance(
                data_year=data_year,
                governance_data=data_components.get('governance_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Productivity Research":
            show_productivity_research(
                data_year=data_year,
                productivity_data=data_components.get('productivity_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Firm Size Analysis":
            show_firm_size_analysis(
                data_year=data_year,
                firm_size_data=data_components.get('firm_size_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Technology Stack":
            show_technology_stack(
                data_year=data_year,
                tech_stack=data_components.get('tech_stack', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "AI Technology Maturity":
            show_ai_technology_maturity(
                data_year=data_year,
                maturity_data=data_components.get('maturity_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Geographic Distribution":
            show_geographic_distribution(
                data_year=data_year,
                geographic_data=data_components.get('geographic_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "OECD 2025 Findings":
            show_oecd_2025_findings(
                data_year=data_year,
                oecd_data=data_components.get('oecd_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Barriers & Support":
            show_barriers_support(
                data_year=data_year,
                barriers_data=data_components.get('barriers_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "ROI Analysis":
            show_roi_analysis(
                data_year=data_year,
                roi_data=data_components.get('roi_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Causal Analysis":
            show_causal_analysis(
                data_year=data_year,
                causal_data=data_components.get('causal_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        elif view_type == "Bibliography & Sources":
            show_bibliography_sources(
                data_year=data_year,
                sources_data=data_components.get('sources_data', pd.DataFrame()),
                dashboard_data=dashboard_data
            )
        else:
            st.error(f"Unknown view type: {view_type}")
            st.info("Please select a valid view from the sidebar.")
            
    except Exception as e:
        logger.error(f"Error rendering {view_type} view: {e}")
        st.error(f"Error displaying {view_type}: {str(e)}")
        
        # Offer retry option
        create_retry_button(
            key=f"retry_{view_type.lower().replace(' ', '_')}",
            callback=lambda: st.cache_data.clear(),
            message=f"Failed to load {view_type} view"
        )


def main():
    """Main application entry point"""
    st.title(f"{APP_ICON} AI Adoption Dashboard")
    st.markdown(f"*Comprehensive analysis of AI adoption trends (2018-2025)*")
    
    # Create navigation
    view_type = create_navigation()
    
    # Load dashboard data
    with st.spinner("Loading dashboard data..."):
        dashboard_data = load_dashboard_data()
    
    if not dashboard_data:
        st.error("Unable to load any data. Please refresh the page or contact support.")
        return
    
    # Extract data components
    data_components = extract_data_components(dashboard_data)
    
    # Display data source info and authenticity status
    source = dashboard_data.get('source', 'unknown')
    data_authenticity = dashboard_data.get('data_authenticity', False)
    
    if source == 'kedro_pipeline':
        st.success("🔧 Using McKinsey Kedro pipeline data")
    elif source == 'authentic_research':
        st.success("🎓 Using authentic research data from Stanford AI Index, McKinsey, Goldman Sachs & Federal Reserve")
        
        # Show data credibility metrics
        if 'credibility_metrics' in dashboard_data:
            credibility = dashboard_data['credibility_metrics']
            with st.expander("📊 Data Authenticity Verification", expanded=False):
                display_data_authenticity_dashboard()
    elif source == 'fallback':
        st.warning("⚠️ Using synthetic fallback data - Research integration temporarily unavailable")
        st.info("💡 Dashboard normally uses authentic data from Stanford AI Index, McKinsey Global Survey, and other authoritative sources")
    
    # Route to appropriate view
    route_to_view(view_type, data_components, dashboard_data)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Version {APP_VERSION}")
    with col2:
        st.caption(f"Created by {AUTHOR}")
    with col3:
        st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    main()