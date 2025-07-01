"""
Integrated Cross-Persona Comparison View

This module integrates all persona comparison components into a comprehensive
dashboard view that provides meaningful insights across different user perspectives.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Optional
import numpy as np

# Import our comparison components
from .persona_comparison import (
    PersonaType, PersonaComparisonFramework, PersonaComparisonChart, 
    PersonaInsightGenerator, PERSONA_CONFIGS
)
from .persona_navigation import PersonaNavigationInterface, PersonaComparisonNavigation
from .charts import MetricCard

class IntegratedComparisonView:
    """Main integrated view for cross-persona comparisons"""
    
    def __init__(self):
        self.framework = PersonaComparisonFramework()
        self.comparison_chart = PersonaComparisonChart()
        self.insight_generator = PersonaInsightGenerator()
        self.navigation = PersonaNavigationInterface()
        self.comparison_nav = PersonaComparisonNavigation()
    
    def render_full_comparison_dashboard(self, data_sources: Dict[str, pd.DataFrame]) -> None:
        """
        Render the complete cross-persona comparison dashboard
        
        Args:
            data_sources: Dictionary of available data sources
        """
        # Get navigation state
        nav_state = self.navigation.render_navigation_sidebar()
        
        # Render appropriate view based on navigation mode
        if nav_state["mode"].value == "comparison_mode":
            self._render_comparison_mode(nav_state, data_sources)
        elif nav_state["mode"].value == "analysis_mode":
            self._render_analysis_mode(nav_state, data_sources)
        else:
            self._render_single_persona_mode(nav_state, data_sources)
    
    def _render_comparison_mode(self, nav_state: Dict[str, Any], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render the comparison mode dashboard"""
        personas = nav_state["personas"]
        metrics = nav_state.get("metrics", [])
        
        if len(personas) < 2:
            st.warning("⚠️ Please select at least 2 personas for comparison.")
            return
        
        # Render comparison header
        self.comparison_nav.render_comparison_header(personas)
        self.comparison_nav.render_comparison_summary(personas, metrics)
        
        # Navigation breadcrumbs
        self.navigation.render_breadcrumb_navigation("Cross-Persona Comparison")
        
        # Main comparison content
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Metric Comparison", 
            "💰 ROI Analysis", 
            "🎯 Strategic Insights",
            "📈 Trend Analysis"
        ])
        
        with tab1:
            self._render_metric_comparison_tab(personas, metrics, data_sources)
        
        with tab2:
            self._render_roi_analysis_tab(personas, data_sources)
        
        with tab3:
            self._render_strategic_insights_tab(personas, metrics, data_sources)
        
        with tab4:
            self._render_trend_analysis_tab(personas, data_sources)
    
    def _render_metric_comparison_tab(self, personas: List[PersonaType], metrics: List[str], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render metric comparison tab"""
        st.subheader("📊 Cross-Persona Metric Comparison")
        
        # Prepare sample data for comparison
        comparison_data = self._prepare_comparison_data(data_sources)
        
        if comparison_data.empty:
            st.error("No data available for comparison. Please check data sources.")
            return
        
        # Side-by-side metric comparison
        if metrics:
            self.comparison_chart.render_side_by_side_metrics(
                comparison_data, personas, metrics, 
                "Metric Comparison Across Personas"
            )
        
        # Metric cards for key insights
        st.subheader("🎯 Key Metric Insights")
        
        cols = st.columns(len(personas))
        
        for i, persona in enumerate(personas):
            with cols[i]:
                self._render_persona_metric_card(persona, comparison_data)
        
        # Shared metrics analysis
        shared_metrics = self.framework.get_shared_metrics(personas)
        
        if shared_metrics:
            st.subheader("🔗 Shared Metrics Analysis")
            st.write(f"**Metrics relevant to all selected personas:** {', '.join(shared_metrics)}")
            
            # Create radar chart for shared metrics
            radar_data = self._create_radar_data(personas, shared_metrics, comparison_data)
            self.comparison_chart.render_persona_radar_comparison(
                radar_data, "Shared Metrics Radar Comparison"
            )
    
    def _render_roi_analysis_tab(self, personas: List[PersonaType], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render ROI analysis tab"""
        st.subheader("💰 Cross-Persona ROI Analysis")
        
        # ROI comparison matrix
        scenarios = [
            "Basic AI Implementation",
            "Advanced AI Deployment", 
            "Full AI Transformation",
            "Industry-Specific Solutions"
        ]
        
        comparison_data = self._prepare_comparison_data(data_sources)
        
        self.comparison_chart.render_roi_comparison_matrix(
            comparison_data, personas, scenarios,
            "ROI Expectations Across Personas and Scenarios"
        )
        
        # ROI perspective analysis
        st.subheader("🔍 ROI Perspective Analysis")
        
        # Create sample ROI data
        roi_data = pd.DataFrame({
            'scenario': scenarios,
            'general_roi': [2.1, 3.2, 4.5, 3.8],
            'business_roi': [2.5, 3.8, 5.2, 4.3],
            'policy_roi': [1.8, 2.5, 3.2, 2.9],
            'research_roi': [1.9, 2.8, 3.5, 3.1]
        })
        
        # Display ROI perspectives
        for scenario in scenarios:
            with st.expander(f"📈 {scenario} - ROI Perspectives"):
                cols = st.columns(len(personas))
                
                for i, persona in enumerate(personas):
                    with cols[i]:
                        roi_col = f"{persona.value.lower().replace(' ', '_')}_roi"
                        if roi_col in roi_data.columns:
                            roi_value = roi_data[roi_data['scenario'] == scenario][roi_col].iloc[0]
                            perspective = self.framework.get_persona_perspective(persona, 'roi_multiplier', roi_value)
                            
                            st.metric(
                                label=f"{persona.value} ROI",
                                value=f"{roi_value:.1f}x",
                                delta=perspective['assessment']
                            )
                            st.caption(f"**Action:** {perspective['action']}")
    
    def _render_strategic_insights_tab(self, personas: List[PersonaType], metrics: List[str], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render strategic insights tab"""
        st.subheader("🎯 Strategic Cross-Persona Insights")
        
        comparison_data = self._prepare_comparison_data(data_sources)
        
        # Generate insights
        insights = self.insight_generator.generate_cross_persona_insights(
            comparison_data, personas, metrics if metrics else ['adoption_rate', 'roi_multiplier']
        )
        
        # Display insights in organized sections
        col1, col2 = st.columns(2)
        
        with col1:
            # Convergent findings
            if insights.get("convergent_findings"):
                st.success("🤝 **Convergent Findings**")
                for finding in insights["convergent_findings"]:
                    st.write(f"• {finding}")
            
            # Strategic implications
            if insights.get("strategic_implications"):
                st.info("🎯 **Strategic Implications**")
                for implication in insights["strategic_implications"]:
                    st.write(f"• {implication}")
        
        with col2:
            # Divergent perspectives
            if insights.get("divergent_perspectives"):
                st.warning("🔀 **Divergent Perspectives**")
                for perspective in insights["divergent_perspectives"]:
                    st.write(f"• {perspective}")
            
            # Action recommendations
            if insights.get("action_recommendations"):
                st.success("✅ **Action Recommendations**")
                for recommendation in insights["action_recommendations"]:
                    st.write(f"• {recommendation}")
        
        # Decision matrix
        st.subheader("🎯 Cross-Persona Decision Matrix")
        self._render_decision_matrix(personas, comparison_data)
        
        # Stakeholder alignment analysis
        st.subheader("👥 Stakeholder Alignment Analysis")
        self._render_stakeholder_alignment(personas, insights)
    
    def _render_trend_analysis_tab(self, personas: List[PersonaType], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render trend analysis tab"""
        st.subheader("📈 Cross-Persona Trend Analysis")
        
        # Historical perspective comparison
        if 'historical_data' in data_sources:
            historical_data = data_sources['historical_data']
            
            # Create persona-specific trend interpretations
            fig = go.Figure()
            
            # Add trend lines for each persona perspective
            colors = {
                PersonaType.GENERAL: '#2E86AB',
                PersonaType.BUSINESS_LEADER: '#A23B72',
                PersonaType.POLICYMAKER: '#F18F01', 
                PersonaType.RESEARCHER: '#6A994E'
            }
            
            for persona in personas:
                # Simulate persona-specific trend weighting
                if 'ai_use' in historical_data.columns:
                    y_values = historical_data['ai_use'].values
                    
                    # Apply persona-specific weighting
                    if persona == PersonaType.BUSINESS_LEADER:
                        y_values = y_values * 1.1  # Business leaders see higher adoption
                    elif persona == PersonaType.POLICYMAKER:
                        y_values = y_values * 0.9  # Policy view more conservative
                    elif persona == PersonaType.RESEARCHER:
                        y_values = y_values * 0.95  # Research view slightly conservative
                    
                    fig.add_trace(go.Scatter(
                        x=historical_data['year'],
                        y=y_values,
                        mode='lines+markers',
                        name=f"{persona.value} Perspective",
                        line=dict(color=colors[persona], width=3),
                        marker=dict(size=8)
                    ))
            
            fig.update_layout(
                title="AI Adoption Trends - Persona Perspectives",
                xaxis_title="Year",
                yaxis_title="Adoption Rate (%)",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Future projections
        st.subheader("🔮 Future Projections by Persona")
        self._render_future_projections(personas)
    
    def _render_single_persona_mode(self, nav_state: Dict[str, Any], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render single persona mode with comparison options"""
        persona = nav_state["personas"][0]
        
        # Navigation breadcrumbs
        self.navigation.render_breadcrumb_navigation(f"{persona.value} Dashboard")
        
        # Persona-specific header
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2E86AB 0%, #A23B72 50%, #F18F01 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <h2 style="margin: 0; font-size: 1.8rem;">👤 {persona.value} Dashboard</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                {PERSONA_CONFIGS[persona].roi_focus}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show comparison option
        st.info("💡 **Tip:** Switch to 'Compare Personas' mode to see how other roles view the same data!")
        
        # Render persona-specific view selector
        selected_view = self.navigation.render_view_selector(persona)
        
        if selected_view == "🔄 Cross-Persona Comparison":
            st.session_state.navigation_mode = "comparison_mode"
            st.experimental_rerun()
        
        # Show persona-specific metrics
        self._render_persona_dashboard(persona, data_sources)
    
    def _render_analysis_mode(self, nav_state: Dict[str, Any], data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render analysis mode"""
        st.header("🔍 Advanced Cross-Persona Analysis")
        
        analysis_type = nav_state.get("analysis_type", "Convergence Analysis")
        scenario = nav_state.get("scenario", "Current State")
        
        # Navigation breadcrumbs
        self.navigation.render_breadcrumb_navigation(f"Analysis - {analysis_type}")
        
        st.subheader(f"Analysis: {analysis_type}")
        st.write(f"**Scenario:** {scenario}")
        
        if analysis_type == "Convergence Analysis":
            self._render_convergence_analysis(data_sources)
        elif analysis_type == "Strategic Alignment":
            self._render_strategic_alignment_analysis(data_sources)
        elif analysis_type == "Decision Matrix":
            self._render_decision_matrix_analysis(data_sources)
        else:
            st.info(f"Analysis type '{analysis_type}' will be implemented in future updates.")
    
    def _prepare_comparison_data(self, data_sources: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Prepare data for comparison charts"""
        # Create sample comparison data if no specific data available
        sample_data = pd.DataFrame({
            'adoption_rate': [75.0],
            'roi_multiplier': [3.2],
            'investment_required': [250000],
            'risk_score': [45.0],
            'time_to_value': [8.0],
            'implementation_complexity': [6.5]
        })
        
        # Try to use real data if available
        if 'sector_data' in data_sources:
            sector_data = data_sources['sector_data']
            if not sector_data.empty and 'adoption_rate' in sector_data.columns:
                # Use average values from sector data
                sample_data['adoption_rate'] = [sector_data['adoption_rate'].mean()]
                if 'avg_roi' in sector_data.columns:
                    sample_data['roi_multiplier'] = [sector_data['avg_roi'].mean()]
        
        return sample_data
    
    def _render_persona_metric_card(self, persona: PersonaType, data: pd.DataFrame) -> None:
        """Render metric card for a specific persona"""
        config = PERSONA_CONFIGS[persona]
        
        # Get a key metric for this persona
        if 'adoption_rate' in data.columns:
            value = data['adoption_rate'].iloc[0]
            perspective = self.framework.get_persona_perspective(persona, 'adoption_rate', value)
            
            metric_card = MetricCard()
            metric_card.render(
                title=f"{persona.value} View",
                value=f"{value:.1f}%",
                delta=perspective['assessment'],
                insight=perspective['action'],
                color=perspective['color']
            )
    
    def _create_radar_data(self, personas: List[PersonaType], metrics: List[str], data: pd.DataFrame) -> Dict[PersonaType, Dict[str, float]]:
        """Create radar chart data for personas"""
        radar_data = {}
        
        for persona in personas:
            persona_data = {}
            for metric in metrics:
                if metric in data.columns:
                    # Normalize values to 0-1 scale for radar chart
                    value = data[metric].iloc[0] if len(data) > 0 else 0.5
                    if metric == 'adoption_rate':
                        normalized = value / 100.0
                    elif metric == 'roi_multiplier':
                        normalized = min(value / 5.0, 1.0)  # Cap at 5x ROI
                    else:
                        normalized = min(value / 100.0, 1.0)  # Generic normalization
                    
                    persona_data[metric.replace('_', ' ').title()] = normalized
            
            radar_data[persona] = persona_data
        
        return radar_data
    
    def _render_decision_matrix(self, personas: List[PersonaType], data: pd.DataFrame) -> None:
        """Render decision matrix for personas"""
        # Create decision criteria
        criteria = ["ROI Potential", "Implementation Risk", "Strategic Value", "Time to Value"]
        
        # Create sample decision scores
        decision_data = []
        for persona in personas:
            scores = np.random.uniform(0.3, 0.9, len(criteria))  # Sample scores
            decision_data.append(scores)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=decision_data,
            x=criteria,
            y=[p.value for p in personas],
            colorscale='RdYlGn',
            colorbar=dict(title="Decision Score")
        ))
        
        fig.update_layout(
            title="Cross-Persona Decision Matrix",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_stakeholder_alignment(self, personas: List[PersonaType], insights: Dict[str, List[str]]) -> None:
        """Render stakeholder alignment analysis"""
        # Calculate alignment score based on convergent vs divergent findings
        convergent_count = len(insights.get("convergent_findings", []))
        divergent_count = len(insights.get("divergent_perspectives", []))
        
        total_findings = convergent_count + divergent_count
        alignment_score = (convergent_count / total_findings * 100) if total_findings > 0 else 50
        
        # Display alignment metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Alignment Score", f"{alignment_score:.0f}%")
        
        with col2:
            st.metric("Consensus Areas", convergent_count)
        
        with col3:
            st.metric("Divergent Views", divergent_count)
        
        # Alignment visualization
        if alignment_score >= 70:
            st.success("🤝 High stakeholder alignment - Clear path forward")
        elif alignment_score >= 50:
            st.warning("⚖️ Moderate alignment - Negotiation may be needed")
        else:
            st.error("🔀 Low alignment - Significant stakeholder engagement required")
    
    def _render_future_projections(self, personas: List[PersonaType]) -> None:
        """Render future projections by persona"""
        # Create sample projection data
        years = list(range(2025, 2030))
        
        fig = go.Figure()
        
        colors = {
            PersonaType.GENERAL: '#2E86AB',
            PersonaType.BUSINESS_LEADER: '#A23B72',
            PersonaType.POLICYMAKER: '#F18F01',
            PersonaType.RESEARCHER: '#6A994E'
        }
        
        for persona in personas:
            # Generate persona-specific projections
            base_values = [80, 84, 87, 89, 91]  # Sample adoption projections
            
            # Apply persona-specific modifiers
            if persona == PersonaType.BUSINESS_LEADER:
                projections = [v * 1.05 for v in base_values]  # More optimistic
            elif persona == PersonaType.POLICYMAKER:
                projections = [v * 0.95 for v in base_values]  # More conservative
            elif persona == PersonaType.RESEARCHER:
                projections = [v * 0.98 for v in base_values]  # Slightly conservative
            else:
                projections = base_values
            
            fig.add_trace(go.Scatter(
                x=years,
                y=projections,
                mode='lines+markers',
                name=f"{persona.value} Projection",
                line=dict(color=colors[persona], width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="5-Year AI Adoption Projections by Persona",
            xaxis_title="Year",
            yaxis_title="Projected Adoption Rate (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_persona_dashboard(self, persona: PersonaType, data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render persona-specific dashboard content"""
        config = PERSONA_CONFIGS[persona]
        
        # Show persona-specific metrics
        st.subheader(f"📊 {persona.value} Key Metrics")
        
        cols = st.columns(3)
        
        # Display primary metrics
        for i, metric in enumerate(config.primary_metrics[:3]):
            with cols[i]:
                # Sample metric values
                if metric == "adoption_rate":
                    value = "75%"
                    delta = "+5% vs last quarter"
                elif metric == "roi_multiplier":
                    value = "3.2x"
                    delta = "+0.4x vs baseline"
                elif metric == "investment_required":
                    value = "$250K"
                    delta = "Industry average"
                else:
                    value = "Good"
                    delta = "Improving"
                
                metric_card = MetricCard()
                metric_card.render(
                    title=metric.replace('_', ' ').title(),
                    value=value,
                    delta=delta,
                    color="success"
                )
        
        # Show key insights
        st.subheader(f"💡 {persona.value} Insights")
        for insight in config.key_insights:
            st.write(f"• {insight}")
    
    def _render_convergence_analysis(self, data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render convergence analysis"""
        st.write("**Convergence Analysis** identifies areas where all personas agree and areas of divergence.")
        
        # Sample convergence data
        convergence_metrics = {
            'AI Adoption Necessity': 95,
            'ROI Expectations': 75,
            'Implementation Timeline': 60,
            'Risk Assessment': 45,
            'Investment Priorities': 55
        }
        
        # Create convergence chart
        fig = go.Figure(go.Bar(
            x=list(convergence_metrics.keys()),
            y=list(convergence_metrics.values()),
            marker_color=['green' if v >= 70 else 'orange' if v >= 50 else 'red' for v in convergence_metrics.values()]
        ))
        
        fig.update_layout(
            title="Persona Convergence Analysis",
            yaxis_title="Convergence Score (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        high_convergence = [k for k, v in convergence_metrics.items() if v >= 70]
        low_convergence = [k for k, v in convergence_metrics.items() if v < 50]
        
        if high_convergence:
            st.success(f"**High Convergence Areas:** {', '.join(high_convergence)}")
        
        if low_convergence:
            st.warning(f"**Areas Needing Alignment:** {', '.join(low_convergence)}")
    
    def _render_strategic_alignment_analysis(self, data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render strategic alignment analysis"""
        st.write("**Strategic Alignment Analysis** shows how well different personas align on strategic priorities.")
        
        # Sample alignment matrix
        strategies = ["Cost Reduction", "Revenue Growth", "Innovation", "Risk Management", "Market Position"]
        personas = ["General", "Business Leader", "Policymaker", "Researcher"]
        
        # Sample alignment scores
        alignment_matrix = np.random.uniform(0.3, 0.9, (len(strategies), len(personas)))
        
        fig = go.Figure(data=go.Heatmap(
            z=alignment_matrix,
            x=personas,
            y=strategies,
            colorscale='RdYlGn',
            colorbar=dict(title="Alignment Score")
        ))
        
        fig.update_layout(
            title="Strategic Priority Alignment Matrix",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_decision_matrix_analysis(self, data_sources: Dict[str, pd.DataFrame]) -> None:
        """Render decision matrix analysis"""
        st.write("**Decision Matrix Analysis** provides a structured approach to cross-persona decision making.")
        
        # Sample decision matrix
        options = ["Option A: Quick Implementation", "Option B: Comprehensive Solution", "Option C: Phased Approach"]
        criteria = ["Cost", "Speed", "Risk", "ROI", "Scalability"]
        
        decision_matrix = np.random.uniform(1, 5, (len(options), len(criteria)))
        
        fig = go.Figure(data=go.Heatmap(
            z=decision_matrix,
            x=criteria,
            y=options,
            colorscale='Viridis',
            colorbar=dict(title="Score (1-5)")
        ))
        
        fig.update_layout(
            title="Cross-Persona Decision Matrix",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Demo function
def demo_integrated_view():
    """Demo the integrated comparison view"""
    st.title("🎭 Integrated Cross-Persona Comparison Dashboard")
    
    # Sample data sources
    data_sources = {
        'sector_data': pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare'],
            'adoption_rate': [92, 85, 78],
            'avg_roi': [4.2, 3.8, 3.2]
        }),
        'historical_data': pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'ai_use': [55, 60, 65, 72, 78]
        })
    }
    
    # Initialize and render the integrated view
    integrated_view = IntegratedComparisonView()
    integrated_view.render_full_comparison_dashboard(data_sources)

if __name__ == "__main__":
    demo_integrated_view()