"""AI Adoption Dashboard - Refactored Modular Version."""

from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st

# Import components
from components.accessibility import AccessibilityManager, create_accessible_dashboard_layout
from components.competitive_assessor import CompetitivePositionAssessor as CompetitiveAssessor

# Import economic insights
from components.economic_insights import EconomicInsights
from components.ui.metric_card import render_metric_card
from components.ui.theme import ThemeManager
from components.view_enhancements import ViewEnhancer as ViewEnhancements

# Import data management
from data.data_manager import DataManager, create_optimized_manager
from performance.cache_manager import get_cache
from performance.monitor import get_metrics, track_performance

# Import utilities
from utils.error_handler import ErrorHandler, handle_errors, setup_logging
from utils.types import DashboardData

# Import views
from views import VIEW_REGISTRY
from views.base import ViewRegistry

# Setup logging
setup_logging()

# Page config
st.set_page_config(
    page_title="AI Adoption Dashboard | 2018-2025 Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki",
        "Report a bug": "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        "About": "# AI Adoption Dashboard\nVersion 2.2.0\n\nTrack AI adoption trends across industries and geographies.",
    },
)

# Initialize managers
a11y = create_accessible_dashboard_layout()
theme_manager = ThemeManager()
error_handler = ErrorHandler()
view_registry = ViewRegistry()

# Register all views
for view_name, view_func in VIEW_REGISTRY.items():
    view_registry.register(view_name, view_func)


# Initialize data manager
@st.cache_resource
def init_data_manager():
    """Initialize the optimized data manager once per session."""
    return create_optimized_manager()


# Data loading function
@track_performance
@st.cache_data
@handle_errors(fallback_return={})
def load_data() -> DashboardData:
    """Load all dashboard data with caching and error handling."""
    data_manager = init_data_manager()

    # Load data from various sources
    data_sources = {
        "ai_index": data_manager.get_data("ai_index"),
        "mckinsey": data_manager.get_data("mckinsey"),
        "goldman_sachs": data_manager.get_data("goldman_sachs"),
        "nvidia": data_manager.get_data("nvidia"),
        "fed_richmond": data_manager.get_data("fed_richmond"),
        "fed_stlouis": data_manager.get_data("fed_stlouis"),
        "oecd": data_manager.get_data("oecd"),
        "imf": data_manager.get_data("imf"),
        "academic": data_manager.get_data("academic"),
    }

    # Consolidate data for views
    consolidated_data = {}

    # Historical trends
    consolidated_data["historical_data"] = data_sources["ai_index"].get(
        "adoption_trends", pd.DataFrame()
    )

    # Sector data
    consolidated_data["sector_2018"] = data_sources["ai_index"].get(
        "sector_adoption", pd.DataFrame()
    )
    consolidated_data["sector_2025"] = data_sources["mckinsey"].get("use_cases", pd.DataFrame())

    # Firm size
    consolidated_data["firm_size"] = data_sources["ai_index"].get("firm_size", pd.DataFrame())

    # AI maturity
    consolidated_data["ai_maturity"] = data_sources["ai_index"].get("ai_maturity", pd.DataFrame())

    # Geographic data
    consolidated_data["geographic"] = data_sources["ai_index"].get(
        "geographic_adoption", pd.DataFrame()
    )
    consolidated_data["state_data"] = data_sources["ai_index"].get("state_data", pd.DataFrame())

    # Financial data
    consolidated_data["financial_impact"] = data_sources["mckinsey"].get(
        "financial_impact", pd.DataFrame()
    )
    consolidated_data["ai_investment_data"] = data_sources["ai_index"].get(
        "investment_trends", pd.DataFrame()
    )

    # Add all other data sources
    for source_name, source_data in data_sources.items():
        if isinstance(source_data, dict):
            consolidated_data.update(source_data)

    return consolidated_data


# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    defaults = {
        "first_visit": True,
        "selected_persona": "General",
        "show_changelog": False,
        "selected_theme": "default",
        "accessibility_mode": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


# Main application
def main():
    """Main application entry point."""
    init_session_state()

    # Apply theme
    theme_manager.apply_theme(st.session_state.selected_theme)

    # Load data
    with st.spinner("Loading dashboard data..."):
        data = load_data()

    if not data:
        error_handler.display_error(
            "Unable to load dashboard data",
            "Please check your internet connection and try again.",
            recovery_action="reload",
        )
        return

    # Title and description
    st.title("🤖 AI Adoption Dashboard: 2018-2025")
    st.markdown(
        "**Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)**"
    )

    # Accessibility toolbar
    a11y.render_accessibility_toolbar()

    # Main navigation
    st.markdown('<nav role="navigation" aria-label="Dashboard navigation">', unsafe_allow_html=True)

    # Sidebar controls
    with st.sidebar:
        st.markdown(
            '<aside role="complementary" aria-label="Dashboard controls">', unsafe_allow_html=True
        )
        st.header("📊 Dashboard Controls")

        # Persona selector
        persona = a11y.create_accessible_form_field(
            field_type="select",
            label="Select Your Role",
            field_id="persona-selector",
            options=["General", "Business Leader", "Policymaker", "Researcher"],
            index=["General", "Business Leader", "Policymaker", "Researcher"].index(
                st.session_state.selected_persona
            ),
            key="persona-selector",
        )
        st.session_state.selected_persona = persona

        # View selector
        view_names = list(VIEW_REGISTRY.keys())
        selected_view = a11y.create_accessible_form_field(
            field_type="select",
            label="Analysis View",
            field_id="view-selector",
            options=view_names,
            key="view-selector",
        )

        # Theme selector
        theme = st.selectbox(
            "Theme",
            options=["default", "executive", "dark", "accessible"],
            index=["default", "executive", "dark", "accessible"].index(
                st.session_state.selected_theme
            ),
        )
        if theme != st.session_state.selected_theme:
            st.session_state.selected_theme = theme
            st.rerun()

        # Performance metrics
        with st.expander("⚡ Performance Metrics"):
            metrics = get_metrics()
            if metrics:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Load Time", f"{metrics.get('load_time', 0):.2f}s")
                    st.metric("Memory", f"{metrics.get('memory_mb', 0):.1f} MB")
                with col2:
                    st.metric("CPU", f"{metrics.get('cpu_percent', 0):.1f}%")
                    cache = get_cache()
                    if cache:
                        stats = cache.get_stats()
                        st.metric("Cache Hit Rate", f"{stats.get('hit_rate', 0):.1%}")

        st.markdown("</aside>", unsafe_allow_html=True)

    # Key metrics
    st.markdown('<section role="region" aria-labelledby="key-metrics">', unsafe_allow_html=True)
    st.markdown('<h2 id="key-metrics">📈 Key Metrics</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            label="AI Adoption",
            value="78%",
            delta="+23pp from 2023",
            insight="Includes any AI use",
            mode="compact",
        )

    with col2:
        render_metric_card(
            label="GenAI Adoption",
            value="71%",
            delta="+38pp from 2023",
            insight="More than doubled",
            mode="compact",
        )

    with col3:
        render_metric_card(
            label="2024 Investment",
            value="$252.3B",
            delta="+44.5% YoY",
            insight="Record levels",
            mode="compact",
        )

    with col4:
        render_metric_card(
            label="Cost Reduction",
            value="280x",
            delta="Since Nov 2022",
            insight="AI inference costs",
            mode="compact",
        )

    st.markdown("</section>", unsafe_allow_html=True)

    # Main content area
    st.markdown('<main role="main">', unsafe_allow_html=True)
    st.markdown(f"<h2>📊 {selected_view}</h2>", unsafe_allow_html=True)

    # Render selected view with error boundary
    try:
        view_registry.render(selected_view, data)
    except Exception as e:
        error_handler.log_error(e, context={"view": selected_view})
        error_handler.display_error(
            f"Error loading {selected_view}",
            "We encountered an issue loading this view. Please try another view or refresh the page.",
            recovery_action="change_view",
        )

    st.markdown("</main>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🤖 AI Adoption Dashboard v2.2.0 | 
            Data sources: AI Index Report 2025, McKinsey, Goldman Sachs, OECD | 
            Created by Robert Casanova</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()