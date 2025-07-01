"""
Cross-Persona Comparison Components for AI Adoption Dashboard

This module provides comprehensive comparison capabilities across different personas
(General, Business Leader, Policymaker, Researcher) allowing users to:
- Compare metrics and insights from multiple perspectives
- Analyze overlapping data points with persona-specific interpretations
- Perform strategic cross-reference analysis between user roles
- View comparative ROI analysis across different user perspectives
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math

# Import existing chart components
from .charts import ChartTheme, ChartStyle, MetricCard, TrendChart, ComparisonChart, ROIChart

class PersonaType(Enum):
    """Enumeration of available personas"""
    GENERAL = "General"
    BUSINESS_LEADER = "Business Leader"
    POLICYMAKER = "Policymaker"  
    RESEARCHER = "Researcher"

@dataclass
class PersonaMetrics:
    """Define metrics relevant to each persona"""
    persona: PersonaType
    primary_metrics: List[str]
    secondary_metrics: List[str]
    roi_focus: str
    risk_tolerance: str
    time_horizon: str
    key_insights: List[str]

# Define persona-specific metric configurations
PERSONA_CONFIGS = {
    PersonaType.GENERAL: PersonaMetrics(
        persona=PersonaType.GENERAL,
        primary_metrics=["adoption_rate", "market_growth", "competitive_position"],
        secondary_metrics=["basic_roi", "implementation_ease", "market_trends"],
        roi_focus="General market returns",
        risk_tolerance="Moderate",
        time_horizon="1-2 years",
        key_insights=["Market position", "Growth opportunities", "Competitive advantage"]
    ),
    PersonaType.BUSINESS_LEADER: PersonaMetrics(
        persona=PersonaType.BUSINESS_LEADER,
        primary_metrics=["roi_multiplier", "cost_savings", "revenue_impact", "investment_required"],
        secondary_metrics=["implementation_timeline", "risk_assessment", "skill_requirements"],
        roi_focus="Financial returns and business impact",
        risk_tolerance="Calculated",
        time_horizon="6 months - 3 years",
        key_insights=["Revenue impact", "Cost optimization", "Strategic advantage", "Investment timing"]
    ),
    PersonaType.POLICYMAKER: PersonaMetrics(
        persona=PersonaType.POLICYMAKER,
        primary_metrics=["labor_impact", "geographic_distribution", "regulatory_compliance", "social_benefits"],
        secondary_metrics=["economic_multiplier", "infrastructure_needs", "skill_gap_analysis"],
        roi_focus="Societal and economic returns",
        risk_tolerance="Conservative",
        time_horizon="3-10 years",
        key_insights=["Job market impact", "Regional development", "Policy effectiveness", "Infrastructure needs"]
    ),
    PersonaType.RESEARCHER: PersonaMetrics(
        persona=PersonaType.RESEARCHER,
        primary_metrics=["technology_maturity", "research_impact", "innovation_rate", "data_quality"],
        secondary_metrics=["methodology_robustness", "peer_validation", "reproducibility"],
        roi_focus="Knowledge and innovation returns",
        risk_tolerance="Experimental",
        time_horizon="1-5 years",
        key_insights=["Scientific progress", "Technology evolution", "Research gaps", "Future trends"]
    )
}

class PersonaComparisonFramework:
    """Core framework for cross-persona comparisons and analysis"""
    
    def __init__(self):
        self.personas = list(PersonaType)
        self.configs = PERSONA_CONFIGS
        self.style = ChartStyle.executive_style()
    
    def get_shared_metrics(self, personas: List[PersonaType]) -> List[str]:
        """Identify metrics that are relevant across selected personas"""
        if not personas:
            return []
        
        # Get metrics for each persona
        persona_metrics = []
        for persona in personas:
            config = self.configs[persona]
            all_metrics = config.primary_metrics + config.secondary_metrics
            persona_metrics.append(set(all_metrics))
        
        # Find intersection (shared metrics)
        shared = set.intersection(*persona_metrics) if persona_metrics else set()
        
        # Also identify metrics that appear in most personas (useful for comparison)
        all_metrics = set()
        for metrics in persona_metrics:
            all_metrics.update(metrics)
        
        # Metrics that appear in at least half of selected personas
        threshold = math.ceil(len(personas) / 2)
        frequent_metrics = []
        for metric in all_metrics:
            count = sum(1 for metrics in persona_metrics if metric in metrics)
            if count >= threshold:
                frequent_metrics.append(metric)
        
        return list(shared) + [m for m in frequent_metrics if m not in shared]
    
    def get_persona_perspective(self, persona: PersonaType, metric: str, value: float) -> Dict[str, Any]:
        """Get persona-specific interpretation of a metric value"""
        config = self.configs[persona]
        
        # Define perspective mappings for common metrics
        perspectives = {
            "adoption_rate": {
                PersonaType.GENERAL: self._general_adoption_perspective,
                PersonaType.BUSINESS_LEADER: self._business_adoption_perspective,
                PersonaType.POLICYMAKER: self._policy_adoption_perspective,
                PersonaType.RESEARCHER: self._research_adoption_perspective
            },
            "roi_multiplier": {
                PersonaType.GENERAL: self._general_roi_perspective,
                PersonaType.BUSINESS_LEADER: self._business_roi_perspective,
                PersonaType.POLICYMAKER: self._policy_roi_perspective,
                PersonaType.RESEARCHER: self._research_roi_perspective
            },
            "investment_required": {
                PersonaType.GENERAL: self._general_investment_perspective,
                PersonaType.BUSINESS_LEADER: self._business_investment_perspective,
                PersonaType.POLICYMAKER: self._policy_investment_perspective,
                PersonaType.RESEARCHER: self._research_investment_perspective
            }
        }
        
        if metric in perspectives and persona in perspectives[metric]:
            return perspectives[metric][persona](value)
        else:
            return self._default_perspective(persona, metric, value)
    
    def _general_adoption_perspective(self, value: float) -> Dict[str, Any]:
        """General user perspective on adoption rates"""
        if value >= 70:
            return {"assessment": "Mainstream", "action": "Safe to adopt", "color": "success"}
        elif value >= 40:
            return {"assessment": "Growing", "action": "Consider adoption", "color": "warning"}
        else:
            return {"assessment": "Emerging", "action": "Monitor closely", "color": "info"}
    
    def _business_adoption_perspective(self, value: float) -> Dict[str, Any]:
        """Business leader perspective on adoption rates"""
        if value >= 80:
            return {"assessment": "Market Standard", "action": "Mandatory for competitiveness", "color": "error"}
        elif value >= 60:
            return {"assessment": "Competitive Advantage", "action": "Implement now", "color": "success"}
        elif value >= 30:
            return {"assessment": "Early Opportunity", "action": "Pilot programs", "color": "warning"}
        else:
            return {"assessment": "Innovation Risk", "action": "Research and monitor", "color": "info"}
    
    def _policy_adoption_perspective(self, value: float) -> Dict[str, Any]:
        """Policymaker perspective on adoption rates"""
        if value >= 60:
            return {"assessment": "Policy Action Needed", "action": "Regulation and support frameworks", "color": "warning"}
        elif value >= 30:
            return {"assessment": "Emerging Trend", "action": "Stakeholder engagement", "color": "info"}
        else:
            return {"assessment": "Early Monitoring", "action": "Research and assessment", "color": "success"}
    
    def _research_adoption_perspective(self, value: float) -> Dict[str, Any]:
        """Researcher perspective on adoption rates"""
        if value >= 70:
            return {"assessment": "Mature Technology", "action": "Impact and optimization studies", "color": "success"}
        elif value >= 40:
            return {"assessment": "Scaling Phase", "action": "Implementation research", "color": "warning"}
        else:
            return {"assessment": "Innovation Phase", "action": "Fundamental research", "color": "info"}
    
    def _general_roi_perspective(self, value: float) -> Dict[str, Any]:
        """General ROI perspective"""
        if value >= 3.0:
            return {"assessment": "High Return", "action": "Strong investment case", "color": "success"}
        elif value >= 2.0:
            return {"assessment": "Positive Return", "action": "Viable investment", "color": "warning"}
        else:
            return {"assessment": "Uncertain Return", "action": "High risk investment", "color": "error"}
    
    def _business_roi_perspective(self, value: float) -> Dict[str, Any]:
        """Business leader ROI perspective"""
        if value >= 4.0:
            return {"assessment": "Exceptional ROI", "action": "Priority investment", "color": "success"}
        elif value >= 2.5:
            return {"assessment": "Strong ROI", "action": "Approved for investment", "color": "success"}
        elif value >= 1.5:
            return {"assessment": "Acceptable ROI", "action": "Consider with conditions", "color": "warning"}
        else:
            return {"assessment": "Poor ROI", "action": "Reject or redesign", "color": "error"}
    
    def _policy_roi_perspective(self, value: float) -> Dict[str, Any]:
        """Policymaker ROI perspective (societal returns)"""
        if value >= 5.0:
            return {"assessment": "High Social Value", "action": "Public investment priority", "color": "success"}
        elif value >= 2.0:
            return {"assessment": "Positive Social Impact", "action": "Support with incentives", "color": "warning"}
        else:
            return {"assessment": "Limited Social Return", "action": "Require private funding", "color": "info"}
    
    def _research_roi_perspective(self, value: float) -> Dict[str, Any]:
        """Researcher ROI perspective (knowledge returns)"""
        if value >= 3.0:
            return {"assessment": "High Research Value", "action": "Priority research area", "color": "success"}
        elif value >= 1.5:
            return {"assessment": "Research Potential", "action": "Continued investigation", "color": "warning"}
        else:
            return {"assessment": "Limited Research Value", "action": "Low priority", "color": "info"}
    
    def _general_investment_perspective(self, value: float) -> Dict[str, Any]:
        """General investment perspective"""
        if value >= 1000000:
            return {"assessment": "Major Investment", "action": "Requires careful planning", "color": "warning"}
        elif value >= 100000:
            return {"assessment": "Significant Investment", "action": "Business case required", "color": "info"}
        else:
            return {"assessment": "Manageable Investment", "action": "Low barrier to entry", "color": "success"}
    
    def _business_investment_perspective(self, value: float) -> Dict[str, Any]:
        """Business leader investment perspective"""
        if value >= 5000000:
            return {"assessment": "Strategic Investment", "action": "Board approval required", "color": "error"}
        elif value >= 1000000:
            return {"assessment": "Major Investment", "action": "Executive approval required", "color": "warning"}
        elif value >= 100000:
            return {"assessment": "Standard Investment", "action": "Department budget approval", "color": "info"}
        else:
            return {"assessment": "Minor Investment", "action": "Manager approval sufficient", "color": "success"}
    
    def _policy_investment_perspective(self, value: float) -> Dict[str, Any]:
        """Policymaker investment perspective"""
        if value >= 100000000:
            return {"assessment": "National Priority", "action": "Federal funding required", "color": "warning"}
        elif value >= 10000000:
            return {"assessment": "State Initiative", "action": "State funding programs", "color": "info"}
        else:
            return {"assessment": "Local Initiative", "action": "Local grants and support", "color": "success"}
    
    def _research_investment_perspective(self, value: float) -> Dict[str, Any]:
        """Researcher investment perspective"""
        if value >= 10000000:
            return {"assessment": "Major Research Program", "action": "Multi-institutional collaboration", "color": "warning"}
        elif value >= 1000000:
            return {"assessment": "Significant Research", "action": "Grant funding required", "color": "info"}
        else:
            return {"assessment": "Standard Research", "action": "Department funding", "color": "success"}
    
    def _default_perspective(self, persona: PersonaType, metric: str, value: float) -> Dict[str, Any]:
        """Default perspective for unmapped metrics"""
        return {
            "assessment": f"Value: {value}",
            "action": f"Requires {persona.value.lower()} analysis",
            "color": "info"
        }

class PersonaComparisonChart:
    """Advanced chart component for cross-persona comparisons"""
    
    def __init__(self):
        self.framework = PersonaComparisonFramework()
        self.style = ChartStyle.executive_style()
    
    def render_side_by_side_metrics(self, 
                                   data: pd.DataFrame, 
                                   personas: List[PersonaType],
                                   metrics: List[str],
                                   title: str = "Cross-Persona Metric Comparison") -> go.Figure:
        """
        Render side-by-side comparison of metrics across personas
        
        Args:
            data: DataFrame with metric data
            personas: List of personas to compare
            metrics: List of metrics to display
            title: Chart title
        """
        fig = go.Figure()
        
        # Colors for personas
        colors = {
            PersonaType.GENERAL: '#2E86AB',
            PersonaType.BUSINESS_LEADER: '#A23B72', 
            PersonaType.POLICYMAKER: '#F18F01',
            PersonaType.RESEARCHER: '#6A994E'
        }
        
        # Create subplots for each metric
        subplot_titles = []
        for metric in metrics:
            subplot_titles.append(f"{metric.replace('_', ' ').title()}")
        
        # Calculate positions for subplots
        rows = math.ceil(len(metrics) / 2)
        cols = 2 if len(metrics) > 1 else 1
        
        from plotly.subplots import make_subplots
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Add data for each metric and persona
        for i, metric in enumerate(metrics):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            if metric in data.columns:
                persona_values = []
                persona_names = []
                persona_colors = []
                persona_insights = []
                
                for persona in personas:
                    # Get value for this persona (using first row for simplicity)
                    value = data[metric].iloc[0] if len(data) > 0 else 0
                    
                    # Get persona perspective
                    perspective = self.framework.get_persona_perspective(persona, metric, value)
                    
                    persona_values.append(value)
                    persona_names.append(persona.value)
                    persona_colors.append(colors[persona])
                    persona_insights.append(f"{perspective['assessment']}: {perspective['action']}")
                
                # Add bar chart for this metric
                fig.add_trace(
                    go.Bar(
                        x=persona_names,
                        y=persona_values,
                        name=metric,
                        marker_color=persona_colors,
                        text=[f"{val:.1f}" for val in persona_values],
                        textposition='outside',
                        hovertemplate='<b>%{x}</b><br>' +
                                     f'{metric}: %{{y}}<br>' +
                                     '<extra></extra>',
                        showlegend=False
                    ),
                    row=row, col=col
                )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.02,
                font=dict(size=20, color='#2c3e50')
            ),
            height=400 * rows,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family=self.style.font_family)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        return fig
    
    def render_persona_radar_comparison(self, 
                                       data: Dict[PersonaType, Dict[str, float]],
                                       title: str = "Persona Perspective Radar") -> go.Figure:
        """
        Render radar chart comparing persona perspectives on multiple dimensions
        
        Args:
            data: Dict mapping personas to their metric values
            title: Chart title
        """
        fig = go.Figure()
        
        colors = {
            PersonaType.GENERAL: '#2E86AB',
            PersonaType.BUSINESS_LEADER: '#A23B72',
            PersonaType.POLICYMAKER: '#F18F01', 
            PersonaType.RESEARCHER: '#6A994E'
        }
        
        # Get all metrics from data
        all_metrics = set()
        for persona_data in data.values():
            all_metrics.update(persona_data.keys())
        metrics = sorted(list(all_metrics))
        
        # Add trace for each persona
        for persona, persona_data in data.items():
            values = [persona_data.get(metric, 0) for metric in metrics]
            
            # Close the radar chart
            values.append(values[0])
            labels = metrics + [metrics[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=labels,
                fill='toself',
                name=persona.value,
                line_color=colors[persona],
                fillcolor=self._hex_to_rgba(colors[persona], 0.2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([max(pd.values()) for pd in data.values() if pd.values()])]
                )
            ),
            title=dict(
                text=f"<b>{title}</b>",
                x=0.5,
                font=dict(size=18, color='#2c3e50')
            ),
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        return fig
    
    def render_roi_comparison_matrix(self, 
                                    data: pd.DataFrame,
                                    personas: List[PersonaType],
                                    scenarios: List[str],
                                    title: str = "ROI Comparison Matrix") -> go.Figure:
        """
        Render matrix showing ROI values across personas and scenarios
        
        Args:
            data: DataFrame with ROI data
            personas: List of personas
            scenarios: List of scenarios/use cases
            title: Chart title
        """
        # Create matrix data
        matrix_data = []
        hover_text = []
        
        for scenario in scenarios:
            row_data = []
            row_hover = []
            for persona in personas:
                # Get ROI value for this persona/scenario combination
                roi_value = self._get_roi_value(data, persona, scenario)
                perspective = self.framework.get_persona_perspective(persona, 'roi_multiplier', roi_value)
                
                row_data.append(roi_value)
                row_hover.append(f"<b>{persona.value}</b><br>" +
                               f"Scenario: {scenario}<br>" +
                               f"ROI: {roi_value:.1f}x<br>" +
                               f"Assessment: {perspective['assessment']}")
            
            matrix_data.append(row_data)
            hover_text.append(row_hover)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=[p.value for p in personas],
            y=scenarios,
            colorscale='RdYlGn',
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_text,
            colorbar=dict(title="ROI Multiplier")
        ))
        
        # Add text annotations
        for i, scenario in enumerate(scenarios):
            for j, persona in enumerate(personas):
                fig.add_annotation(
                    x=j, y=i,
                    text=f"{matrix_data[i][j]:.1f}x",
                    showarrow=False,
                    font=dict(color="white" if matrix_data[i][j] < 2.5 else "black", size=12)
                )
        
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.02,
                font=dict(size=18, color='#2c3e50')
            ),
            xaxis_title="Persona",
            yaxis_title="Scenario",
            height=400,
            font=dict(family=self.style.font_family)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        return fig
    
    def _get_roi_value(self, data: pd.DataFrame, persona: PersonaType, scenario: str) -> float:
        """Get ROI value for persona/scenario combination"""
        # This is a simplified implementation - in practice, you'd have
        # more sophisticated logic to map personas and scenarios to ROI values
        base_roi = data.get('avg_roi', pd.Series([3.0])).iloc[0] if len(data) > 0 else 3.0
        
        # Adjust ROI based on persona perspective
        multipliers = {
            PersonaType.GENERAL: 1.0,
            PersonaType.BUSINESS_LEADER: 1.2,  # Business leaders focus on higher ROI
            PersonaType.POLICYMAKER: 0.8,      # Policy ROI includes social factors
            PersonaType.RESEARCHER: 0.9        # Research ROI includes knowledge value
        }
        
        return base_roi * multipliers.get(persona, 1.0)
    
    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        """Convert hex color to rgba format"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return f'rgba({r},{g},{b},{alpha})'

class PersonaInsightGenerator:
    """Generate persona-specific insights and recommendations"""
    
    def __init__(self):
        self.framework = PersonaComparisonFramework()
    
    def generate_cross_persona_insights(self, 
                                       data: pd.DataFrame, 
                                       personas: List[PersonaType],
                                       metrics: List[str]) -> Dict[str, List[str]]:
        """Generate insights comparing personas across metrics"""
        insights = {
            "convergent_findings": [],
            "divergent_perspectives": [],
            "strategic_implications": [],
            "action_recommendations": []
        }
        
        for metric in metrics:
            if metric not in data.columns:
                continue
                
            value = data[metric].iloc[0] if len(data) > 0 else 0
            perspectives = {}
            
            # Get perspective from each persona
            for persona in personas:
                perspectives[persona] = self.framework.get_persona_perspective(persona, metric, value)
            
            # Analyze convergence/divergence
            assessments = [p["assessment"] for p in perspectives.values()]
            actions = [p["action"] for p in perspectives.values()]
            
            # Check for convergent findings
            if len(set(assessments)) <= 2:  # Similar assessments
                insights["convergent_findings"].append(
                    f"All personas agree on {metric}: {assessments[0]} ({value:.1f})"
                )
            else:
                # Divergent perspectives
                persona_views = ", ".join([f"{p.value}: {perspectives[p]['assessment']}" 
                                         for p in personas])
                insights["divergent_perspectives"].append(
                    f"Mixed views on {metric}: {persona_views}"
                )
            
            # Strategic implications
            if any("priority" in action.lower() or "mandatory" in action.lower() 
                   for action in actions):
                insights["strategic_implications"].append(
                    f"{metric} identified as strategic priority by multiple personas"
                )
            
            # Action recommendations
            unique_actions = list(set(actions))
            if len(unique_actions) == 1:
                insights["action_recommendations"].append(
                    f"Unified action for {metric}: {unique_actions[0]}"
                )
            else:
                insights["action_recommendations"].append(
                    f"Multi-track approach for {metric}: {', '.join(unique_actions[:2])}"
                )
        
        return insights

# Usage example and demo
def demo_persona_comparison():
    """Demo function for persona comparison components"""
    st.title("🎯 Cross-Persona Comparison Dashboard")
    
    # Sample data
    sample_data = pd.DataFrame({
        'adoption_rate': [75.0],
        'roi_multiplier': [3.2],
        'investment_required': [250000],
        'risk_score': [45.0],
        'time_to_value': [8.0]
    })
    
    # Initialize components
    comparison_chart = PersonaComparisonChart()
    insight_generator = PersonaInsightGenerator()
    
    # Persona selection
    st.sidebar.subheader("🎭 Select Personas for Comparison")
    selected_personas = []
    
    persona_options = {
        "General User": PersonaType.GENERAL,
        "Business Leader": PersonaType.BUSINESS_LEADER,
        "Policymaker": PersonaType.POLICYMAKER,
        "Researcher": PersonaType.RESEARCHER
    }
    
    for name, persona_type in persona_options.items():
        if st.sidebar.checkbox(name, value=True):
            selected_personas.append(persona_type)
    
    if not selected_personas:
        st.warning("Please select at least one persona for comparison.")
        return
    
    # Metric selection
    available_metrics = ['adoption_rate', 'roi_multiplier', 'investment_required', 'risk_score']
    selected_metrics = st.sidebar.multiselect(
        "📊 Select Metrics for Comparison",
        available_metrics,
        default=available_metrics[:3]
    )
    
    if not selected_metrics:
        st.warning("Please select at least one metric for comparison.")
        return
    
    # Generate insights
    insights = insight_generator.generate_cross_persona_insights(
        sample_data, selected_personas, selected_metrics
    )
    
    # Display insights
    st.subheader("🔍 Cross-Persona Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if insights["convergent_findings"]:
            st.success("**Convergent Findings**")
            for finding in insights["convergent_findings"]:
                st.write(f"• {finding}")
        
        if insights["strategic_implications"]:
            st.info("**Strategic Implications**") 
            for implication in insights["strategic_implications"]:
                st.write(f"• {implication}")
    
    with col2:
        if insights["divergent_perspectives"]:
            st.warning("**Divergent Perspectives**")
            for perspective in insights["divergent_perspectives"]:
                st.write(f"• {perspective}")
        
        if insights["action_recommendations"]:
            st.success("**Action Recommendations**")
            for recommendation in insights["action_recommendations"]:
                st.write(f"• {recommendation}")
    
    # Side-by-side comparison
    st.subheader("📊 Side-by-Side Metric Comparison")
    comparison_chart.render_side_by_side_metrics(
        sample_data, selected_personas, selected_metrics
    )
    
    # ROI Comparison Matrix
    st.subheader("💰 ROI Comparison Matrix")
    scenarios = ["Basic Implementation", "Advanced Implementation", "Full Transformation"]
    comparison_chart.render_roi_comparison_matrix(
        sample_data, selected_personas, scenarios
    )
    
    # Radar comparison
    st.subheader("🎯 Persona Perspective Radar")
    radar_data = {}
    for persona in selected_personas:
        radar_data[persona] = {
            'Innovation Focus': np.random.uniform(0.5, 1.0),
            'Risk Tolerance': np.random.uniform(0.3, 0.9),
            'Time Horizon': np.random.uniform(0.4, 1.0),
            'ROI Expectation': np.random.uniform(0.6, 1.0),
            'Implementation Speed': np.random.uniform(0.3, 0.8)
        }
    
    comparison_chart.render_persona_radar_comparison(radar_data)

if __name__ == "__main__":
    demo_persona_comparison()