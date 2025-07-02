"""
Navigation utilities for AI Adoption Dashboard
Provides navigation setup and management functionality
"""

import streamlit as st
from typing import Dict, List, Optional, Any

def setup_navigation():
    """
    Setup navigation system for the AI Adoption Dashboard
    Configures sidebar navigation and page routing
    """
    
    # Initialize navigation state if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main_dashboard'
    
    if 'navigation_history' not in st.session_state:
        st.session_state.navigation_history = ['main_dashboard']
    
    if 'breadcrumbs' not in st.session_state:
        st.session_state.breadcrumbs = []
    
    # Set up page configuration for navigation
    _configure_page_navigation()
    
    # Initialize navigation tracking
    _track_navigation_analytics()

def _configure_page_navigation():
    """Configure page navigation settings"""
    
    # Navigation configuration
    nav_config = {
        'main_dashboard': {
            'title': 'AI Adoption Dashboard',
            'description': 'Main dashboard with comprehensive AI adoption analytics',
            'breadcrumb': 'Home'
        },
        'causal_analysis': {
            'title': 'Causal Analysis',
            'description': 'McKinsey CausalNx powered causal analysis',
            'breadcrumb': 'Causal Analysis'
        },
        'executive_dashboard': {
            'title': 'Executive Dashboard',
            'description': 'Executive-focused analytics and insights',
            'breadcrumb': 'Executive'
        },
        'realtime_analysis': {
            'title': 'Real-time Economic Analysis',
            'description': 'Live OECD data integration with AI adoption metrics',
            'breadcrumb': 'Real-time Analysis'
        }
    }
    
    # Store navigation config in session state
    st.session_state.nav_config = nav_config

def _track_navigation_analytics():
    """Track navigation analytics for user experience optimization"""
    
    # Simple navigation tracking
    if 'page_visits' not in st.session_state:
        st.session_state.page_visits = {}
    
    current_page = st.session_state.get('current_page', 'main_dashboard')
    
    # Increment visit count
    if current_page in st.session_state.page_visits:
        st.session_state.page_visits[current_page] += 1
    else:
        st.session_state.page_visits[current_page] = 1

def navigate_to_page(page_name: str):
    """
    Navigate to a specific page
    
    Args:
        page_name: Name of the page to navigate to
    """
    
    if page_name != st.session_state.get('current_page'):
        # Update navigation history
        if 'navigation_history' not in st.session_state:
            st.session_state.navigation_history = []
        
        st.session_state.navigation_history.append(page_name)
        st.session_state.current_page = page_name
        
        # Limit history to last 10 pages
        if len(st.session_state.navigation_history) > 10:
            st.session_state.navigation_history = st.session_state.navigation_history[-10:]

def get_current_page() -> str:
    """Get the current page name"""
    return st.session_state.get('current_page', 'main_dashboard')

def get_navigation_history() -> List[str]:
    """Get navigation history"""
    return st.session_state.get('navigation_history', ['main_dashboard'])

def create_breadcrumbs() -> str:
    """Create breadcrumb navigation string"""
    
    nav_config = st.session_state.get('nav_config', {})
    current_page = get_current_page()
    
    if current_page in nav_config:
        return nav_config[current_page].get('breadcrumb', 'Home')
    
    return 'Home'

def setup_sidebar_navigation():
    """Setup sidebar navigation menu"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    
    # Quick navigation buttons
    nav_options = {
        'main_dashboard': '🏠 Main Dashboard',
        'causal_analysis': '🔗 Causal Analysis',
        'executive_dashboard': '👔 Executive View',
        'realtime_analysis': '🌍 Real-time Analysis'
    }
    
    current_page = get_current_page()
    
    for page_key, page_label in nav_options.items():
        if page_key != current_page:
            if st.sidebar.button(page_label, key=f"nav_{page_key}"):
                navigate_to_page(page_key)
                st.rerun()
    
    # Show current page
    if current_page in nav_options:
        st.sidebar.info(f"📍 Current: {nav_options[current_page]}")

def get_page_analytics() -> Dict[str, Any]:
    """Get page navigation analytics"""
    
    return {
        'current_page': get_current_page(),
        'page_visits': st.session_state.get('page_visits', {}),
        'navigation_history': get_navigation_history(),
        'total_page_changes': len(get_navigation_history())
    }

def reset_navigation():
    """Reset navigation to default state"""
    
    st.session_state.current_page = 'main_dashboard'
    st.session_state.navigation_history = ['main_dashboard']
    st.session_state.breadcrumbs = []
    st.session_state.page_visits = {}

# Export main functions
__all__ = [
    'setup_navigation',
    'navigate_to_page', 
    'get_current_page',
    'get_navigation_history',
    'create_breadcrumbs',
    'setup_sidebar_navigation',
    'get_page_analytics',
    'reset_navigation'
]