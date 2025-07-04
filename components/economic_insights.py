"""Economic insights and executive summary components for the Economics of AI Dashboard."""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px


class EconomicInsights:
    """Generate economic insights and executive summaries for dashboard views."""
    
    @staticmethod
    def display_executive_summary(
        title: str,
        key_points: List[str],
        recommendations: List[str],
        urgency: str = "medium"
    ):
        """Display executive summary box with key insights.
        
        Args:
            title: Summary title
            key_points: List of key insight points
            recommendations: List of actionable recommendations
            urgency: Urgency level (low, medium, high, critical)
        """
        urgency_colors = {
            "low": "#d4edda",
            "medium": "#fff3cd", 
            "high": "#f8d7da",
            "critical": "#f5c6cb"
        }
        
        color = urgency_colors.get(urgency, urgency_colors["medium"])
        
        st.markdown(f"""
        <div style='background-color: {color}; border-left: 5px solid #1f77b4; 
                    padding: 20px; margin: 20px 0; border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #1f77b4;'>💡 {title}</h3>
            <div style='margin-bottom: 15px;'>
                <h4 style='color: #495057; font-size: 16px;'>Key Points:</h4>
                <ul style='margin: 5px 0;'>
                    {''.join([f"<li style='margin: 5px 0;'>{point}</li>" for point in key_points])}
                </ul>
            </div>
            <div>
                <h4 style='color: #495057; font-size: 16px;'>Recommendations:</h4>
                <ul style='margin: 5px 0;'>
                    {''.join([f"<li style='margin: 5px 0;'>{rec}</li>" for rec in recommendations])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def generate_adoption_insights(adoption_data: pd.DataFrame) -> Dict[str, List[str]]:
        """Generate insights for adoption rate data."""
        current_rate = adoption_data.iloc[-1]['overall_adoption']
        growth_rate = (adoption_data.iloc[-1]['overall_adoption'] - 
                      adoption_data.iloc[-5]['overall_adoption']) / 5
        
        key_points = [
            f"Overall AI adoption has reached {current_rate:.1f}%",
            f"Annual growth rate averaging {growth_rate:.1f}% over past 5 years",
            "GenAI adoption accelerating 3x faster than traditional AI",
            "Industry leaders show 2x higher adoption than average"
        ]
        
        recommendations = []
        if current_rate < 50:
            recommendations.append("Accelerate adoption to avoid competitive disadvantage")
        if growth_rate < 10:
            recommendations.append("Increase investment to match market growth rates")
        recommendations.extend([
            "Focus on GenAI capabilities for maximum impact",
            "Benchmark against industry leaders, not average"
        ])
        
        return {"key_points": key_points, "recommendations": recommendations}
    
    @staticmethod
    def generate_sector_insights(sector_data: pd.DataFrame, your_sector: str) -> Dict[str, List[str]]:
        """Generate sector-specific insights."""
        sector_info = sector_data[sector_data['sector'] == your_sector].iloc[0]
        avg_adoption = sector_data['adoption_rate'].mean()
        
        position = "leading" if sector_info['adoption_rate'] > avg_adoption else "lagging"
        gap = abs(sector_info['adoption_rate'] - avg_adoption)
        
        key_points = [
            f"{your_sector} is {position} with {sector_info['adoption_rate']:.0f}% adoption",
            f"Gap to average: {gap:.0f} percentage points",
            f"Investment level: ${sector_info['investment_millions']:.0f}M",
            f"GenAI adoption at {sector_info['genai_adoption']:.0f}%"
        ]
        
        recommendations = []
        if position == "lagging":
            recommendations.append(f"Increase investment by {gap*2:.0f}% to reach parity")
            recommendations.append("Prioritize quick wins in high-ROI use cases")
        else:
            recommendations.append("Maintain leadership through innovation")
            recommendations.append("Share best practices across organization")
        
        return {"key_points": key_points, "recommendations": recommendations}
    
    @staticmethod
    def calculate_cost_of_inaction(
        company_size: str,
        industry: str,
        delay_months: int,
        current_adoption: float
    ) -> Dict[str, float]:
        """Calculate the economic cost of delaying AI adoption.
        
        Returns:
            Dictionary with cost metrics
        """
        # Base calculations from economic data
        size_multipliers = {
            "Small": 0.5,
            "Medium": 1.0,
            "Large": 2.0,
            "Enterprise": 5.0
        }
        
        industry_growth = {
            "Technology": 0.15,
            "Financial Services": 0.12,
            "Healthcare": 0.10,
            "Retail": 0.09,
            "Manufacturing": 0.08,
            "Other": 0.07
        }
        
        base_multiplier = size_multipliers.get(company_size, 1.0)
        growth_rate = industry_growth.get(industry, 0.08)
        
        # Calculate various costs
        market_share_loss = delay_months * growth_rate * 0.5
        productivity_loss = delay_months * 2.5  # 2.5% per month
        competitive_cycles = delay_months // 6
        revenue_impact = market_share_loss * base_multiplier * 1000000
        
        # Innovation gap calculation
        innovation_gap = min(100, delay_months * 4)
        
        return {
            "market_share_loss": market_share_loss,
            "productivity_loss": productivity_loss,
            "competitive_cycles": competitive_cycles,
            "revenue_impact": revenue_impact,
            "innovation_gap": innovation_gap,
            "total_cost": revenue_impact + (productivity_loss * 50000 * base_multiplier)
        }
    
    @staticmethod
    def display_cost_of_inaction(costs: Dict[str, float], delay_months: int):
        """Display cost of inaction analysis."""
        st.error(f"""
        ⚠️ **Cost of Inaction Analysis**
        
        Delaying AI adoption by {delay_months} months will result in:
        
        📉 **Market Position Impact**
        - Market Share Loss: **{costs['market_share_loss']:.1f}%**
        - Competitive Cycles Behind: **{costs['competitive_cycles']}**
        - Innovation Gap: **{costs['innovation_gap']:.0f}%**
        
        💰 **Financial Impact**
        - Revenue Loss: **${costs['revenue_impact']:,.0f}**
        - Productivity Loss: **{costs['productivity_loss']:.1f}%**
        - Total Economic Cost: **${costs['total_cost']:,.0f}**
        
        ⏰ **Time is Money**: Every month of delay compounds these losses exponentially.
        """)
    
    @staticmethod
    def create_competitive_position_matrix(
        your_adoption: float,
        your_investment: float,
        sector_data: pd.DataFrame
    ) -> go.Figure:
        """Create competitive position visualization."""
        fig = go.Figure()
        
        # Add sector bubbles
        fig.add_trace(go.Scatter(
            x=sector_data['adoption_rate'],
            y=sector_data['investment_millions'],
            mode='markers+text',
            marker=dict(
                size=sector_data['genai_adoption'],
                color=sector_data['avg_roi'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="ROI %"),
                sizemode='diameter',
                sizeref=2
            ),
            text=sector_data['sector'],
            textposition="top center",
            name='Industries'
        ))
        
        # Add your position
        fig.add_trace(go.Scatter(
            x=[your_adoption],
            y=[your_investment],
            mode='markers+text',
            marker=dict(
                size=30,
                color='red',
                symbol='star',
                line=dict(color='darkred', width=2)
            ),
            text=['Your Position'],
            textposition="bottom center",
            name='You'
        ))
        
        # Add quadrant lines
        avg_adoption = sector_data['adoption_rate'].mean()
        avg_investment = sector_data['investment_millions'].mean()
        
        fig.add_hline(y=avg_investment, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=avg_adoption, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=25, y=avg_investment*2, text="Laggards<br>Over-investing", showarrow=False)
        fig.add_annotation(x=75, y=avg_investment*2, text="Leaders<br>High Investment", showarrow=False)
        fig.add_annotation(x=25, y=avg_investment*0.3, text="Slow Movers<br>Low Priority", showarrow=False)
        fig.add_annotation(x=75, y=avg_investment*0.3, text="Efficient<br>Adopters", showarrow=False)
        
        fig.update_layout(
            title="AI Adoption Competitive Position Matrix",
            xaxis_title="AI Adoption Rate (%)",
            yaxis_title="AI Investment (Millions $)",
            height=600,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def generate_what_if_scenarios(
        base_data: Dict[str, float],
        scenario_type: str
    ) -> pd.DataFrame:
        """Generate what-if scenario projections."""
        scenarios = []
        
        if scenario_type == "adoption_acceleration":
            for acceleration in [1.0, 1.5, 2.0, 3.0]:
                scenario = {
                    "scenario": f"{acceleration}x Acceleration",
                    "time_to_roi": base_data['time_to_roi'] / acceleration,
                    "total_roi": base_data['total_roi'] * (1 + (acceleration - 1) * 0.5),
                    "risk_level": min(10, base_data['risk_level'] * acceleration * 0.8),
                    "implementation_cost": base_data['cost'] * (1 + (acceleration - 1) * 0.3)
                }
                scenarios.append(scenario)
        
        elif scenario_type == "investment_levels":
            for investment_mult in [0.5, 1.0, 1.5, 2.0]:
                scenario = {
                    "scenario": f"{investment_mult}x Investment",
                    "adoption_rate": min(100, base_data['adoption'] * (1 + (investment_mult - 1) * 0.4)),
                    "productivity_gain": base_data['productivity'] * (1 + (investment_mult - 1) * 0.3),
                    "market_share_gain": base_data['market_share'] * investment_mult * 0.7,
                    "payback_period": base_data['payback'] / (investment_mult ** 0.5)
                }
                scenarios.append(scenario)
        
        elif scenario_type == "competitive_response":
            responses = ["No Response", "Match Competition", "Exceed by 25%", "Industry Leader"]
            multipliers = [0.5, 1.0, 1.25, 1.5]
            
            for response, mult in zip(responses, multipliers):
                scenario = {
                    "scenario": response,
                    "market_position": base_data['position'] * mult,
                    "revenue_impact": base_data['revenue'] * (0.8 + mult * 0.2),
                    "talent_retention": max(50, min(95, base_data['talent'] * mult)),
                    "innovation_score": base_data['innovation'] * mult
                }
                scenarios.append(scenario)
        
        return pd.DataFrame(scenarios)
    
    @staticmethod
    def display_action_plan(
        urgency: str,
        timeline: str,
        key_actions: List[str],
        success_metrics: List[str]
    ):
        """Display actionable plan based on insights."""
        urgency_emoji = {
            "low": "📅",
            "medium": "⏰",
            "high": "🚨",
            "critical": "🔥"
        }
        
        emoji = urgency_emoji.get(urgency, "📋")
        
        with st.expander(f"{emoji} **Recommended Action Plan** - {urgency.upper()} Priority", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Timeline**: {timeline}")
                st.markdown("**Key Actions**:")
                for i, action in enumerate(key_actions, 1):
                    st.markdown(f"{i}. {action}")
            
            with col2:
                st.markdown("**Success Metrics**:")
                for metric in success_metrics:
                    st.markdown(f"✓ {metric}")
            
            st.info("""
            💡 **Pro Tip**: Download this action plan and share with your team. 
            Track progress monthly and adjust based on results.
            """)


class CompetitiveIntelligence:
    """Generate competitive intelligence insights."""
    
    @staticmethod
    def assess_competitive_position(
        your_metrics: Dict[str, float],
        industry_data: pd.DataFrame,
        peer_data: pd.DataFrame
    ) -> Dict[str, any]:
        """Comprehensive competitive position assessment."""
        
        # Calculate percentiles
        adoption_percentile = (peer_data['adoption_rate'] < your_metrics['adoption']).sum() / len(peer_data) * 100
        investment_percentile = (peer_data['investment'] < your_metrics['investment']).sum() / len(peer_data) * 100
        
        # Determine position
        if adoption_percentile >= 75 and investment_percentile >= 75:
            position = "Leader"
            risk = "Low"
        elif adoption_percentile >= 50:
            position = "Competitive"
            risk = "Medium"
        elif adoption_percentile >= 25:
            position = "Follower"
            risk = "High"
        else:
            position = "Laggard"
            risk = "Critical"
        
        # Calculate gaps
        leader_adoption = peer_data['adoption_rate'].quantile(0.9)
        adoption_gap = leader_adoption - your_metrics['adoption']
        
        # Time to parity calculation
        if your_metrics['growth_rate'] > 0:
            time_to_parity = adoption_gap / your_metrics['growth_rate']
        else:
            time_to_parity = float('inf')
        
        return {
            "position": position,
            "risk_level": risk,
            "adoption_percentile": adoption_percentile,
            "investment_percentile": investment_percentile,
            "adoption_gap": adoption_gap,
            "time_to_parity_months": time_to_parity * 12,
            "recommended_investment_increase": max(0, (leader_adoption - your_metrics['adoption']) * 0.1)
        }