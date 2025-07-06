

from data.data_manager import DataManager

import streamlit as st
from typing import Dict, Any, List

class ThemeManager:
    def apply_theme(self) -> None:
        st.markdown(
            """
<style>
    .metric-card {
        background-color: transparent; padding: 1rem; border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    } .stApp > div {
        background-color: transparent;
    } .main .block-container {
        background-color: transparent;
    } .source-info {
        font-size: 0.8em; color: #666; cursor: pointer; text-decoration:
        underline;
    } .insight-box {
        background-color: rgba(31, 119, 180, 0.1); border-left: 4px solid
        #1f77b4; padding: 1rem; margin: 1rem 0; border-radius: 0.25rem;
    }
</style>
""",
            unsafe_allow_html=True,
        )

import importlib

class ViewManager:
    def __init__(self) -> None:
        self.all_views = {
            "Adoption Rates": "views.adoption.adoption_rates",
            "Historical Trends": "views.adoption.historical_trends",
            "Industry Analysis": "views.adoption.industry_analysis",
            "Investment Trends": "views.economic.investment_trends",
            "Regional Growth": "views.geographic.regional_growth",
            "AI Cost Trends": "views.adoption.ai_cost_trends",
            "Token Economics": "views.other.token_economics",
            "Financial Impact": "views.economic.financial_impact",
            "Labor Impact": "views.adoption.labor_impact",
            "Firm Size Analysis": "views.adoption.firm_size_analysis",
            "Technology Stack": "views.adoption.technology_stack",
            "AI Technology Maturity": "views.adoption.ai_technology_maturity",
            "Productivity Research": "views.adoption.productivity_research",
            "Environmental Impact": "views.other.environmental_impact",
            "Geographic Distribution": "views.geographic.geographic_distribution",
            "OECD 2025 Findings": "views.adoption.oecd_2025_findings",
            "Barriers & Support": "views.adoption.barriers_support",
            "ROI Analysis": "views.economic.roi_analysis",
            "Skill Gap Analysis": "views.adoption.skill_gap_analysis",
            "AI Governance": "views.other.ai_governance",
            "Bibliography & Sources": "views.other.bibliography_sources",
        }
        self.persona_views = {
            "Business Leader": [
                "Industry Analysis",
                "Financial Impact",
                "Investment Trends",
                "ROI Analysis",
            ],
            "Policymaker": [
                "Geographic Distribution",
                "OECD 2025 Findings",
                "Regional Growth",
                "AI Governance",
            ],
            "Researcher": [
                "Historical Trends",
                "Productivity Research",
                "Environmental Impact",
                "Skill Gap Analysis",
            ],
            "General": ["Adoption Rates", "Historical Trends", "Investment Trends", "Labor Impact"],
        }

    def render_sidebar(self) -> str:
        st.sidebar.header("📊 Dashboard Controls")
        persona = st.sidebar.selectbox(
            "Select Your Role",
            ["General", "Business Leader", "Policymaker", "Researcher"],
            index=["General", "Business Leader", "Policymaker", "Researcher"].index(
                st.session_state.selected_persona
            ),
        )
        st.session_state.selected_persona = persona

        if persona != "General":
            st.sidebar.info(
                f"💡 **Recommended views for {persona}:**\n"
                + "\n".join([f"• {v}" for v in self.persona_views[persona]])
            )

        view_type = st.sidebar.selectbox(
            "Analysis View",
            list(self.all_views.keys()),
            index=list(self.all_views.keys()).index(self.persona_views[persona][0]) if persona != "General" else 0,
        )
        return view_type

    def render_view(self, view_type: str, data: Dict[str, Any]) -> None:
        st.subheader(f"📊 {view_type}")
        try:
            module_path = self.all_views[view_type]
            view_module = importlib.import_module(module_path)
            view_module.render(data)
        except (ImportError, AttributeError) as e:
            st.error(f"Could not load view: {view_type}\nError: {e}")


class DashboardApp:
    def __init__(self) -> None:
        self.theme_manager = ThemeManager()
        self.data_manager = DataManager()
        self.view_manager = ViewManager()
        self.setup_page()

    def setup_page(self) -> None:
        st.set_page_config(
            page_title="AI Adoption Dashboard | 2018-2025 Analysis",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                "Get Help": "https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki",
                "Report a bug": "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
                "About": "# AI Adoption Dashboard\nVersion 2.2.0\n\nTrack AI adoption trends across industries and geographies.\n\nCreated by Robert Casanova",
            },
        )

    def render(self) -> None:
        self.theme_manager.apply_theme()
        st.title("🤖 AI Adoption Dashboard: 2018-2025")
        st.markdown(
            "**Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)**"
        )
        data = self.data_manager.get_data()
        view_type = self.view_manager.render_sidebar()
        self.view_manager.render_view(view_type, data)

if __name__ == "__main__":
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = 'General'
    app = DashboardApp()
    app.render()

