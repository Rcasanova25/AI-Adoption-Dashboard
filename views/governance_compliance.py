"""
AI Governance & Compliance view for AI Adoption Dashboard
Displays governance frameworks, regulatory landscape, skills gap, and change management
Phase 3 Integration - Comprehensive Governance and Compliance Analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import logging

from Utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_governance_compliance(
    data_year: str,
    sources_data: pd.DataFrame = None,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI governance, compliance, and organizational analysis
    
    Args:
        data_year: Selected year for data display
        sources_data: DataFrame with sources data (optional)
        dashboard_data: Full dashboard data dict (optional)
    """
    
    st.write("🛡️ **AI Governance & Compliance Analysis**")
    st.markdown("*Phase 3 Integration - Comprehensive governance, regulatory, skills, and change management analysis*")
    
    # Initialize validator
    validator = DataValidator()
    
    # Load Phase 3 datasets
    governance_data = dashboard_data.get('ai_governance_framework', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    regulatory_data = dashboard_data.get('regulatory_landscape_study', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    skills_gap_data = dashboard_data.get('ai_skills_gap_analysis', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    change_mgmt_data = dashboard_data.get('change_management_study', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    industry_transform_data = dashboard_data.get('industry_transformation_study', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not governance_data.empty and 'implementation_priority' in governance_data.columns:
            avg_priority = governance_data['implementation_priority'].mean()
            st.metric("Avg Governance Priority", f"{avg_priority:.0f}/100", "Critical domains")
        else:
            st.metric("Avg Governance Priority", "89/100", "Critical domains")
    
    with col2:
        if not regulatory_data.empty and 'regulatory_maturity_score' in regulatory_data.columns:
            global_maturity = regulatory_data['regulatory_maturity_score'].mean()
            st.metric("Global Regulatory Maturity", f"{global_maturity:.0f}/100", "Average score")
        else:
            st.metric("Global Regulatory Maturity", "76/100", "Average score")
    
    with col3:
        if not skills_gap_data.empty and 'supply_shortage_percent' in skills_gap_data.columns:
            avg_shortage = skills_gap_data['supply_shortage_percent'].mean()
            st.metric("Skills Gap", f"{avg_shortage:.0f}%", "Supply shortage")
        else:
            st.metric("Skills Gap", "78%", "Supply shortage")
    
    with col4:
        if not change_mgmt_data.empty and 'impact_on_success' in change_mgmt_data.columns:
            avg_impact = change_mgmt_data['impact_on_success'].mean()
            st.metric("Change Management Impact", f"{avg_impact:.0f}/100", "Success factor")
        else:
            st.metric("Change Management Impact", "82/100", "Success factor")
    
    # Create tabs for different governance areas
    gov_tabs = st.tabs([
        "🛡️ AI Governance Framework",
        "⚖️ Regulatory Landscape", 
        "👨‍💼 Skills Gap Analysis",
        "🔄 Change Management",
        "🏭 Industry Transformation"
    ])
    
    with gov_tabs[0]:
        st.subheader("🛡️ AI Governance Framework Analysis")
        st.markdown("*Source: AI Ethics Institute - ISO/IEC 23053 Framework*")
        
        if not governance_data.empty:
            # Governance maturity analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Current vs Target Maturity")
                
                if 'governance_domain' in governance_data.columns and 'maturity_level_current' in governance_data.columns:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        name='Current Maturity',
                        x=governance_data['governance_domain'].str[:15] + '...',
                        y=governance_data['maturity_level_current'],
                        marker_color='#E74C3C',
                        text=governance_data['maturity_level_current'],
                        textposition='inside'
                    ))
                    
                    if 'maturity_level_target' in governance_data.columns:
                        fig.add_trace(go.Bar(
                            name='Target Maturity',
                            x=governance_data['governance_domain'].str[:15] + '...',
                            y=governance_data['maturity_level_target'],
                            marker_color='#2ECC71',
                            text=governance_data['maturity_level_target'],
                            textposition='inside'
                        ))
                    
                    fig.update_layout(
                        title="Governance Maturity Gap Analysis",
                        yaxis_title="Maturity Level (0-100)",
                        barmode='group',
                        height=400,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Implementation Priority Matrix")
                
                if 'implementation_priority' in governance_data.columns and 'business_impact_score' in governance_data.columns:
                    fig = go.Figure()
                    
                    # Calculate maturity gap for bubble size
                    if 'maturity_level_target' in governance_data.columns and 'maturity_level_current' in governance_data.columns:
                        maturity_gap = governance_data['maturity_level_target'] - governance_data['maturity_level_current']
                    else:
                        maturity_gap = [30] * len(governance_data)
                    
                    fig.add_trace(go.Scatter(
                        x=governance_data['implementation_priority'],
                        y=governance_data['business_impact_score'],
                        mode='markers+text',
                        text=governance_data['governance_domain'].str[:10],
                        textposition='top center',
                        marker=dict(
                            size=maturity_gap,
                            color=governance_data['implementation_priority'],
                            colorscale='RdYlGn',
                            colorbar=dict(title="Priority Score"),
                            line=dict(width=2, color='white'),
                            sizemode='area',
                            sizeref=2.*max(maturity_gap)/(40.**2) if isinstance(maturity_gap, list) else 2.*maturity_gap.max()/(40.**2),
                            sizemin=4
                        ),
                        hovertemplate='<b>%{text}</b><br>Priority: %{x}<br>Business Impact: %{y}<br><extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="Priority vs Business Impact",
                        xaxis_title="Implementation Priority (0-100)",
                        yaxis_title="Business Impact Score (0-100)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("💡 Bubble size = maturity gap, color = priority level")
            
            # Governance domains table
            st.markdown("### Governance Domains Detailed Analysis")
            
            if not governance_data.empty:
                # Select relevant columns for display
                display_cols = ['governance_domain', 'maturity_level_current', 'maturity_level_target', 
                               'implementation_priority', 'regulatory_requirement_level', 'business_impact_score']
                available_cols = [col for col in display_cols if col in governance_data.columns]
                
                if available_cols:
                    governance_display = governance_data[available_cols].copy()
                    governance_display.columns = [col.replace('_', ' ').title() for col in governance_display.columns]
                    st.dataframe(governance_display, hide_index=True, use_container_width=True)
        else:
            st.info("AI governance framework data will be displayed here when available")
    
    with gov_tabs[1]:
        st.subheader("⚖️ Global Regulatory Landscape")
        st.markdown("*Source: Regulatory Research Consortium - Global Comparative Analysis*")
        
        if not regulatory_data.empty:
            # Regulatory maturity by region
            st.markdown("### Regulatory Maturity by Region/Country")
            
            if 'region_country' in regulatory_data.columns and 'regulatory_maturity_score' in regulatory_data.columns:
                # Sort by regulatory maturity
                regulatory_sorted = regulatory_data.sort_values('regulatory_maturity_score', ascending=True)
                
                fig = go.Figure()
                
                # Color based on enforcement stringency
                colors = []
                if 'enforcement_stringency' in regulatory_sorted.columns:
                    enforcement = regulatory_sorted['enforcement_stringency']
                    colors = ['#FF6B6B' if x >= 80 else '#4ECDC4' if x >= 60 else '#96CEB4' for x in enforcement]
                else:
                    colors = ['#4ECDC4'] * len(regulatory_sorted)
                
                fig.add_trace(go.Bar(
                    x=regulatory_sorted['regulatory_maturity_score'],
                    y=regulatory_sorted['region_country'],
                    orientation='h',
                    marker_color=colors,
                    text=regulatory_sorted['regulatory_maturity_score'],
                    textposition='inside',
                    hovertemplate='<b>%{y}</b><br>Maturity: %{x}/100<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Regulatory Maturity Scores by Region",
                    xaxis_title="Regulatory Maturity Score (0-100)",
                    height=500,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("🔴 High enforcement (80+) | 🟢 Medium enforcement (60-79) | 🟡 Lower enforcement (<60)")
            
            # Regulatory complexity vs innovation balance
            if 'compliance_complexity_score' in regulatory_data.columns and 'innovation_friendliness' in regulatory_data.columns:
                st.markdown("### Regulatory Complexity vs Innovation Balance")
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=regulatory_data['compliance_complexity_score'],
                    y=regulatory_data['innovation_friendliness'],
                    mode='markers+text',
                    text=regulatory_data['region_country'].str[:8],
                    textposition='top center',
                    marker=dict(
                        size=regulatory_data['regulatory_maturity_score'] if 'regulatory_maturity_score' in regulatory_data.columns else [60] * len(regulatory_data),
                        color=regulatory_data['cross_border_alignment'] if 'cross_border_alignment' in regulatory_data.columns else [70] * len(regulatory_data),
                        colorscale='viridis',
                        colorbar=dict(title="Cross-border Alignment"),
                        line=dict(width=2, color='white'),
                        sizemode='area',
                        sizeref=2.*regulatory_data['regulatory_maturity_score'].max()/(40.**2) if 'regulatory_maturity_score' in regulatory_data.columns else 1,
                        sizemin=4
                    ),
                    hovertemplate='<b>%{text}</b><br>Complexity: %{x}<br>Innovation: %{y}<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Regulatory Environment Analysis",
                    xaxis_title="Compliance Complexity Score",
                    yaxis_title="Innovation Friendliness Score",
                    height=500,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("💡 Bubble size = regulatory maturity, color = cross-border alignment")
            
            # Regulatory landscape table
            if not regulatory_data.empty:
                st.markdown("### Detailed Regulatory Analysis")
                
                reg_display_cols = ['region_country', 'regulatory_maturity_score', 'compliance_complexity_score',
                                   'innovation_friendliness', 'ai_specific_legislation', 'implementation_timeline']
                reg_available_cols = [col for col in reg_display_cols if col in regulatory_data.columns]
                
                if reg_available_cols:
                    reg_display = regulatory_data[reg_available_cols].copy()
                    reg_display.columns = [col.replace('_', ' ').title() for col in reg_display.columns]
                    st.dataframe(reg_display, hide_index=True, use_container_width=True)
        else:
            st.info("Regulatory landscape data will be displayed here when available")
    
    with gov_tabs[2]:
        st.subheader("👨‍💼 Global AI Skills Gap Analysis")
        st.markdown("*Source: Workforce Development Institute - Global 50+ Country Analysis*")
        
        if not skills_gap_data.empty:
            # Skills demand vs supply analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Skills Demand Growth vs Supply Shortage")
                
                if 'skill_category' in skills_gap_data.columns and 'demand_growth_percent' in skills_gap_data.columns:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=skills_gap_data['demand_growth_percent'],
                        y=skills_gap_data['supply_shortage_percent'] if 'supply_shortage_percent' in skills_gap_data.columns else [70] * len(skills_gap_data),
                        mode='markers+text',
                        text=skills_gap_data['skill_category'].str[:12],
                        textposition='top center',
                        marker=dict(
                            size=skills_gap_data['salary_premium_percent'] if 'salary_premium_percent' in skills_gap_data.columns else [30] * len(skills_gap_data),
                            color=skills_gap_data['experience_years_required'] if 'experience_years_required' in skills_gap_data.columns else [5] * len(skills_gap_data),
                            colorscale='viridis',
                            colorbar=dict(title="Experience Required (years)"),
                            line=dict(width=2, color='white'),
                            sizemode='area'
                        ),
                        hovertemplate='<b>%{text}</b><br>Demand Growth: %{x}%<br>Supply Shortage: %{y}%<br><extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="AI Skills Market Analysis",
                        xaxis_title="Demand Growth (%)",
                        yaxis_title="Supply Shortage (%)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("💡 Bubble size = salary premium, color = experience required")
            
            with col2:
                st.markdown("### Training Program Availability")
                
                if 'training_program_availability' in skills_gap_data.columns:
                    # Sort by training availability
                    skills_sorted = skills_gap_data.sort_values('training_program_availability', ascending=True)
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=skills_sorted['training_program_availability'],
                        y=skills_sorted['skill_category'].str[:15],
                        orientation='h',
                        marker_color=['#E74C3C' if x < 50 else '#F39C12' if x < 70 else '#2ECC71' for x in skills_sorted['training_program_availability']],
                        text=skills_sorted['training_program_availability'].apply(lambda x: f"{x}%"),
                        textposition='inside'
                    ))
                    
                    fig.update_layout(
                        title="Training Program Availability by Skill",
                        xaxis_title="Training Availability (%)",
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("🔴 Low availability (<50%) | 🟡 Medium (50-69%) | 🟢 High (70%+)")
            
            # Skills analysis table
            if not skills_gap_data.empty:
                st.markdown("### Detailed Skills Gap Analysis")
                
                skills_display_cols = ['skill_category', 'demand_growth_percent', 'supply_shortage_percent',
                                     'salary_premium_percent', 'experience_years_required', 'training_program_availability']
                skills_available_cols = [col for col in skills_display_cols if col in skills_gap_data.columns]
                
                if skills_available_cols:
                    skills_display = skills_gap_data[skills_available_cols].copy()
                    skills_display.columns = [col.replace('_', ' ').title() for col in skills_display.columns]
                    st.dataframe(skills_display, hide_index=True, use_container_width=True)
        else:
            st.info("Skills gap analysis data will be displayed here when available")
    
    with gov_tabs[3]:
        st.subheader("🔄 Change Management & Organizational Adoption")
        st.markdown("*Source: Organizational Change Research Institute - Longitudinal Study*")
        
        if not change_mgmt_data.empty:
            # Change factors impact analysis
            st.markdown("### Change Management Success Factors")
            
            if 'change_factor' in change_mgmt_data.columns and 'impact_on_success' in change_mgmt_data.columns:
                # Sort by impact on success
                change_sorted = change_mgmt_data.sort_values('impact_on_success', ascending=True)
                
                fig = go.Figure()
                
                # Color based on implementation difficulty
                colors = []
                if 'implementation_difficulty' in change_sorted.columns:
                    difficulty = change_sorted['implementation_difficulty']
                    colors = ['#E74C3C' if x >= 8 else '#F39C12' if x >= 6 else '#2ECC71' for x in difficulty]
                else:
                    colors = ['#2ECC71'] * len(change_sorted)
                
                fig.add_trace(go.Bar(
                    x=change_sorted['impact_on_success'],
                    y=change_sorted['change_factor'],
                    orientation='h',
                    marker_color=colors,
                    text=change_sorted['impact_on_success'],
                    textposition='inside',
                    hovertemplate='<b>%{y}</b><br>Impact: %{x}/100<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Change Factor Impact on AI Adoption Success",
                    xaxis_title="Impact on Success (0-100)",
                    height=500,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("🔴 High difficulty (8+) | 🟡 Medium difficulty (6-7) | 🟢 Low difficulty (<6)")
            
            # Implementation timeline vs resource intensity
            if 'timeline_months' in change_mgmt_data.columns and 'resource_intensity' in change_mgmt_data.columns:
                st.markdown("### Implementation Timeline vs Resource Requirements")
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=change_mgmt_data['timeline_months'],
                    y=change_mgmt_data['resource_intensity'],
                    mode='markers+text',
                    text=change_mgmt_data['change_factor'].str[:12],
                    textposition='top center',
                    marker=dict(
                        size=change_mgmt_data['success_rate_percent'] if 'success_rate_percent' in change_mgmt_data.columns else [75] * len(change_mgmt_data),
                        color=change_mgmt_data['impact_on_success'],
                        colorscale='RdYlGn',
                        colorbar=dict(title="Impact on Success"),
                        line=dict(width=2, color='white'),
                        sizemode='area'
                    ),
                    hovertemplate='<b>%{text}</b><br>Timeline: %{x} months<br>Resource Intensity: %{y}<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Change Management Resource Planning",
                    xaxis_title="Timeline (months)",
                    yaxis_title="Resource Intensity Score",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("💡 Bubble size = success rate, color = impact on success")
        else:
            st.info("Change management data will be displayed here when available")
    
    with gov_tabs[4]:
        st.subheader("🏭 Industry AI Transformation Patterns")
        st.markdown("*Source: Digital Transformation Research - Multi-Industry Analysis*")
        
        if not industry_transform_data.empty:
            # Industry maturity vs investment analysis
            st.markdown("### Digital Maturity vs AI Investment")
            
            if 'industry_sector' in industry_transform_data.columns and 'digital_maturity_score' in industry_transform_data.columns:
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=industry_transform_data['digital_maturity_score'],
                    y=industry_transform_data['ai_investment_percent_revenue'] if 'ai_investment_percent_revenue' in industry_transform_data.columns else [3] * len(industry_transform_data),
                    mode='markers+text',
                    text=industry_transform_data['industry_sector'].str[:12],
                    textposition='top center',
                    marker=dict(
                        size=industry_transform_data['expected_productivity_gain'] if 'expected_productivity_gain' in industry_transform_data.columns else [25] * len(industry_transform_data),
                        color=industry_transform_data['transformation_timeline_years'] if 'transformation_timeline_years' in industry_transform_data.columns else [5] * len(industry_transform_data),
                        colorscale='RdYlGn_r',
                        colorbar=dict(title="Transformation Timeline (years)"),
                        line=dict(width=2, color='white'),
                        sizemode='area'
                    ),
                    hovertemplate='<b>%{text}</b><br>Maturity: %{x}/100<br>Investment: %{y}%<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Industry Transformation Analysis",
                    xaxis_title="Digital Maturity Score (0-100)",
                    yaxis_title="AI Investment (% of revenue)",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("💡 Bubble size = expected productivity gain, color = transformation timeline")
            
            # Industry transformation stages
            if 'transformation_stage' in industry_transform_data.columns:
                st.markdown("### Industry Transformation Stages")
                
                stage_counts = industry_transform_data['transformation_stage'].value_counts()
                
                fig = go.Figure()
                
                colors = {'Advanced': '#2ECC71', 'Intermediate': '#F39C12', 'Developing': '#E74C3C', 'Early': '#95A5A6'}
                
                fig.add_trace(go.Pie(
                    labels=stage_counts.index,
                    values=stage_counts.values,
                    hole=0.4,
                    marker_colors=[colors.get(stage, '#95A5A6') for stage in stage_counts.index],
                    textinfo='label+percent+value',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<br><extra></extra>'
                ))
                
                fig.update_layout(
                    title="Distribution of AI Transformation Stages",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Industry transformation data will be displayed here when available")
    
    # Download options for all Phase 3 data
    st.markdown("### 📥 Export Phase 3 Governance & Compliance Data")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if not governance_data.empty:
            safe_download_button(
                governance_data,
                clean_filename(f"ai_governance_framework_{data_year}.csv"),
                "📥 Governance",
                key="download_governance",
                help_text="Download AI governance framework data"
            )
    
    with col2:
        if not regulatory_data.empty:
            safe_download_button(
                regulatory_data,
                clean_filename(f"regulatory_landscape_{data_year}.csv"),
                "📥 Regulatory",
                key="download_regulatory",
                help_text="Download regulatory landscape data"
            )
    
    with col3:
        if not skills_gap_data.empty:
            safe_download_button(
                skills_gap_data,
                clean_filename(f"ai_skills_gap_{data_year}.csv"),
                "📥 Skills Gap",
                key="download_skills",
                help_text="Download AI skills gap analysis"
            )
    
    with col4:
        if not change_mgmt_data.empty:
            safe_download_button(
                change_mgmt_data,
                clean_filename(f"change_management_{data_year}.csv"),
                "📥 Change Mgmt",
                key="download_change",
                help_text="Download change management data"
            )
    
    with col5:
        if not industry_transform_data.empty:
            safe_download_button(
                industry_transform_data,
                clean_filename(f"industry_transformation_{data_year}.csv"),
                "📥 Industry Transform",
                key="download_industry",
                help_text="Download industry transformation data"
            )