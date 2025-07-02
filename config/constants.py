"""
Configuration constants for AI Adoption Dashboard
Centralizes all hardcoded values for easier maintenance
"""

from datetime import datetime
from typing import Dict, List, Any

# Application metadata
APP_VERSION = "2.2.0"
APP_TITLE = "AI Adoption Dashboard | 2018-2025 Analysis"
APP_ICON = "🤖"
AUTHOR = "Robert Casanova"
LAST_UPDATED = "2025-01-01"

# Data source information
DATA_SOURCES = {
    'mckinsey': {
        'name': "McKinsey Global Survey on AI",
        'year': 2024,
        'description': "Survey of 1,363 participants from organizations using AI, representing the full range of regions, industries, company sizes, functional specialties, and seniority levels.",
        'url': "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"
    },
    'ai_index': {
        'name': "AI Index Report",
        'year': 2025,
        'description': "Annual report tracking AI progress across multiple dimensions including R&D, industry adoption, policy, and more.",
        'url': "https://aiindex.stanford.edu/report/"
    },
    'oecd': {
        'name': "OECD AI Employment Outlook",
        'year': 2025,
        'description': "OECD analysis of AI impact on employment and skills across member countries.",
        'url': "https://www.oecd.org/employment/artificial-intelligence-employment-outlook.htm"
    }
}

# View configuration
VIEW_TYPES = [
    "Executive Dashboard",  # NEW - Executive summary view
    "Real-time Analysis",  # NEW - OECD economic data integration
    "Historical Trends",
    "Industry Analysis", 
    "Financial Impact",
    "Investment Trends",
    "Regional Growth",
    "AI Cost Trends",
    "Token Economics",
    "Labor Impact",
    "Environmental Impact",
    "Adoption Rates",
    "Skill Gap Analysis",
    "AI Governance",
    "Productivity Research",
    "Firm Size Analysis",
    "Technology Stack",
    "AI Technology Maturity",
    "Geographic Distribution",
    "OECD 2025 Findings",
    "Barriers & Support",
    "ROI Analysis",
    "Causal Analysis",
    "Bibliography & Sources",
    "Research Scanner",  # NEW - Automated research integration
    "Technical Research",  # NEW - Phase 2C Technical Analysis
    "Implementation Guides",  # NEW - Stakeholder-specific guidance
    "Governance & Compliance",  # NEW - Phase 3 Governance Analysis
    "Research Meta-Analysis"  # NEW - Phase 4 100% Complete Integration
]

# Color schemes for consistent visualization
COLOR_SCHEMES = {
    'primary': '#3498DB',
    'secondary': '#2ECC71',
    'accent': '#E74C3C',
    'warning': '#F39C12',
    'info': '#17A2B8',
    'success': '#28A745',
    'blues': 'blues',
    'greens': 'greens',
    'viridis': 'viridis',
    'plasma': 'plasma'
}

# Data validation thresholds
VALIDATION_THRESHOLDS = {
    'min_rows_default': 1,
    'min_rows_plotting': 3,
    'max_missing_percentage': 0.5,  # 50% missing data threshold
    'cache_ttl_hours': 1,
    'retry_attempts': 3
}

# File export settings
EXPORT_SETTINGS = {
    'csv_encoding': 'utf-8',
    'date_format': '%Y-%m-%d',
    'float_precision': 2,
    'max_filename_length': 100
}

# Layout configuration
LAYOUT_CONFIG = {
    'sidebar_width': 300,
    'chart_height_default': 500,
    'chart_height_small': 300,
    'chart_height_large': 700,
    'columns_default': 2,
    'expander_expanded_default': False
}

# Data schemas for validation
DATA_SCHEMAS = {
    'historical_data': {
        'required_columns': ['year', 'ai_use'],
        'optional_columns': ['genai_use'],
        'numeric_columns': ['year', 'ai_use', 'genai_use'],
        'year_range': (2017, 2025)
    },
    'sector_data': {
        'required_columns': ['sector'],
        'optional_columns': ['adoption_rate', 'genai_adoption', 'avg_roi'],
        'numeric_columns': ['adoption_rate', 'genai_adoption', 'avg_roi'],
        'string_columns': ['sector']
    },
    'investment_data': {
        'required_columns': ['year', 'total_investment'],
        'optional_columns': ['genai_investment', 'us_investment', 'china_investment'],
        'numeric_columns': ['year', 'total_investment', 'genai_investment', 'us_investment', 'china_investment'],
        'year_range': (2014, 2025)
    },
    'financial_impact': {
        'required_columns': ['function'],
        'optional_columns': ['companies_reporting_revenue_gains', 'companies_reporting_cost_savings'],
        'numeric_columns': ['companies_reporting_revenue_gains', 'companies_reporting_cost_savings'],
        'string_columns': ['function']
    }
}

# Error messages
ERROR_MESSAGES = {
    'data_loading_failed': "Failed to load data. Please try refreshing the page.",
    'data_empty': "No data available for this view.",
    'data_invalid': "Data validation failed. Please check the data source.",
    'columns_missing': "Required columns are missing from the dataset.",
    'export_failed': "Failed to export data. Please try again.",
    'chart_render_failed': "Unable to render chart. Please check the data.",
    'connection_failed': "Unable to connect to data source. Please check your internet connection."
}

# Success messages  
SUCCESS_MESSAGES = {
    'data_loaded': "Data loaded successfully",
    'export_complete': "Data exported successfully",
    'validation_passed': "Data validation completed",
    'cache_cleared': "Cache cleared successfully"
}

# Help text
HELP_TEXT = {
    'data_year_filter': "Select which year's data to display in the visualizations",
    'weighting_method': "Choose how to weight the data - by number of firms or by employment levels",
    'export_data': "Download the current view's data as a CSV file",
    'refresh_data': "Clear cache and reload data from source",
    'data_source': "View information about the data source and methodology"
}

# McKinsey specific constants
MCKINSEY_CONSTANTS = {
    'survey_participants': 1363,
    'survey_year': 2024,
    'genai_adoption_functions': [
        'Marketing & Sales',
        'Product Development', 
        'Service Operations',
        'Human Resources',
        'Strategy & Corporate Finance',
        'Manufacturing',
        'Risk',
        'Supply Chain'
    ],
    'top_adopting_sectors': [
        'Technology',
        'Financial Services', 
        'Healthcare',
        'Manufacturing'
    ]
}

# AI Index specific constants
AI_INDEX_CONSTANTS = {
    'report_year': 2025,
    'tracked_dimensions': [
        'R&D Investment',
        'Industry Adoption',
        'Policy Development',
        'Technical Performance',
        'Economic Impact'
    ],
    'investment_categories': [
        'Total AI Investment',
        'GenAI Investment',
        'Regional Investment',
        'Sector Investment'
    ]
}

# Regional data
REGIONS = {
    'North America': ['United States', 'Canada', 'Mexico'],
    'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
    'Asia Pacific': ['China', 'Japan', 'South Korea', 'Singapore', 'Australia', 'India'],
    'Other': ['Brazil', 'Israel', 'South Africa']
}