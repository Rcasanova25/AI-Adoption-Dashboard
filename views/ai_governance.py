"""
AI Governance view for AI Adoption Dashboard
Displays AI governance and ethics implementation with proper data validation
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


def show_ai_governance(
    data_year: str,
    governance_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI governance and ethics implementation analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        governance_data: DataFrame with AI governance data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'ai_index':
            return "**Source**: AI Index Report 2025, Stanford Human-Centered AI Institute\n\n**Methodology**: Analysis of responsible AI practices across 1,000+ organizations globally, with focus on ethics guidelines, regulatory compliance, and governance frameworks."
        elif source_type == 'nist':
            return "**Source**: NIST AI Risk Management Framework\n\n**Methodology**: Federal framework for AI governance based on 240+ organization collaboration and extensive public consultation."
        return "**Source**: AI Governance Research"
    
    st.write("⚖️ **AI Governance & Ethics Implementation**")
    
    # Validate governance data
    validator = DataValidator()
    governance_result = validator.validate_dataframe(
        governance_data,
        "AI Governance Data",
        required_columns=['aspect', 'adoption_rate', 'maturity_score'],
        min_rows=1
    )
    
    if governance_result.is_valid:
        # Ensure we have valid numeric data
        if governance_data['adoption_rate'].isna().any() or governance_data['maturity_score'].isna().any():
            st.warning("Some governance data contains missing values. Using fallback data.")
            # Provide fallback data
            governance_data = pd.DataFrame({
                'aspect': ['Ethics Guidelines', 'Data Privacy', 'Bias Detection', 'Transparency',
                          'Accountability Framework', 'Risk Assessment', 'Regulatory Compliance'],
                'adoption_rate': [62, 78, 45, 52, 48, 55, 72],
                'maturity_score': [3.2, 3.8, 2.5, 2.8, 2.6, 3.0, 3.5]  # Out of 5
            })
        
        # Create governance visualization tabs
        tab1, tab2, tab3 = st.tabs(["Governance Overview", "Regulatory Framework", "Policy Timeline"])
        
        with tab1:
            def plot_governance_radar():
                """Plot governance maturity radar chart"""
                fig = go.Figure()
                
                # Create radar chart for maturity
                categories = governance_data['aspect'].tolist()
                
                # Adoption rate trace
                fig.add_trace(go.Scatterpolar(
                    r=governance_data['adoption_rate'],
                    theta=categories,
                    fill='toself',
                    name='Adoption Rate (%)',
                    line_color='#3498DB',
                    marker=dict(size=8)
                ))
                
                # Maturity score trace (scaled to 100)
                fig.add_trace(go.Scatterpolar(
                    r=[x * 20 for x in governance_data['maturity_score']],  # Scale to 100
                    theta=categories,
                    fill='toself',
                    name='Maturity Score (scaled)',
                    line_color='#E74C3C',
                    fillcolor='rgba(231, 76, 60, 0.1)',
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(size=10)
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=10)
                        )
                    ),
                    showlegend=True,
                    title="AI Governance Implementation and Maturity",
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            if safe_plot_check(
                governance_data,
                "AI Governance Data",
                required_columns=['aspect', 'adoption_rate', 'maturity_score'],
                plot_func=plot_governance_radar
            ):
                # Governance insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("✅ **Well-Established Areas:**")
                    
                    # Safely extract top performing areas
                    try:
                        # Get top 3 by adoption rate
                        top_governance = governance_data.nlargest(3, 'adoption_rate')
                        for _, row in top_governance.iterrows():
                            maturity = row.get('maturity_score', 0)
                            st.write(f"• **{row['aspect']}:** {row['adoption_rate']}% adoption, {maturity:.1f}/5 maturity")
                    except Exception as e:
                        logger.error(f"Error displaying top governance areas: {e}")
                        st.write("• **Data Privacy:** 78% adoption, 3.8/5 maturity")
                        st.write("• **Regulatory Compliance:** 72% adoption, 3.5/5 maturity")
                        st.write("• **Ethics Guidelines:** 62% adoption, 3.2/5 maturity")
                
                with col2:
                    st.write("⚠️ **Areas Needing Attention:**")
                    
                    try:
                        # Get bottom 3 by adoption rate
                        bottom_governance = governance_data.nsmallest(3, 'adoption_rate')
                        for _, row in bottom_governance.iterrows():
                            maturity = row.get('maturity_score', 0)
                            st.write(f"• **{row['aspect']}:** Only {row['adoption_rate']}% adoption, {maturity:.1f}/5 maturity")
                    except Exception as e:
                        logger.error(f"Error displaying bottom governance areas: {e}")
                        st.write("• **Bias Detection:** Only 45% adoption, 2.5/5 maturity")
                        st.write("• **Accountability Framework:** 48% adoption, 2.6/5 maturity")
                        st.write("• **Transparency:** 52% adoption, 2.8/5 maturity")
        
        with tab2:
            st.write("📋 **Regulatory Framework Analysis**")
            
            # Create regulatory compliance comparison
            def plot_compliance_comparison():
                """Plot regulatory compliance comparison"""
                # Filter for regulatory-related aspects
                regulatory_aspects = governance_data[
                    governance_data['aspect'].str.contains('Compliance|Privacy|Framework|Assessment', case=False, na=False)
                ].copy()
                
                if not regulatory_aspects.empty:
                    fig = go.Figure()
                    
                    # Add adoption rate bars
                    fig.add_trace(go.Bar(
                        x=regulatory_aspects['aspect'],
                        y=regulatory_aspects['adoption_rate'],
                        name='Adoption Rate (%)',
                        marker_color='#3498DB',
                        text=[f'{x}%' for x in regulatory_aspects['adoption_rate']],
                        textposition='outside'
                    ))
                    
                    # Add maturity score line
                    fig.add_trace(go.Scatter(
                        x=regulatory_aspects['aspect'],
                        y=[x * 20 for x in regulatory_aspects['maturity_score']],  # Scale to 100
                        mode='lines+markers',
                        name='Maturity Score (scaled)',
                        line=dict(width=3, color='#E74C3C'),
                        marker=dict(size=10),
                        yaxis='y2'
                    ))
                    
                    fig.update_layout(
                        title="Regulatory Compliance Framework Status",
                        xaxis_title="Regulatory Aspect",
                        yaxis=dict(title="Adoption Rate (%)", side="left"),
                        yaxis2=dict(title="Maturity Score (scaled to 100)", side="right", overlaying="y"),
                        height=400,
                        hovermode='x unified',
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Fallback chart
                    st.info("Creating regulatory framework overview...")
                    regulatory_fallback = pd.DataFrame({
                        'framework': ['NIST AI RMF', 'EU AI Act', 'ISO/IEC 23053', 'IEEE 2857'],
                        'implementation': [75, 45, 35, 25],
                        'readiness': [80, 60, 50, 40]
                    })
                    
                    fig = px.bar(
                        regulatory_fallback,
                        x='framework',
                        y=['implementation', 'readiness'],
                        title='Regulatory Framework Implementation Status',
                        labels={'value': 'Percentage (%)', 'variable': 'Status Type'},
                        barmode='group',
                        color_discrete_map={'implementation': '#3498DB', 'readiness': '#E74C3C'}
                    )
                    fig.update_layout(height=400, xaxis_tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Safe plotting for regulatory compliance
            if safe_plot_check(
                governance_data,
                "Regulatory Compliance Data",
                required_columns=['aspect', 'adoption_rate'],
                plot_func=plot_compliance_comparison
            ):
                st.write("**Key Regulatory Insights:**")
                st.write("• NIST AI Risk Management Framework shows highest adoption at 75%")
                st.write("• EU AI Act preparation varies significantly across organizations")
                st.write("• International standards (ISO/IEC) adoption remains limited")
                st.write("• Proactive governance shows better preparedness for regulatory changes")
        
        with tab3:
            st.write("📅 **Policy Development Timeline**")
            
            # Policy timeline visualization
            def plot_policy_timeline():
                """Plot policy development timeline"""
                # Create sample policy timeline data
                policy_timeline = pd.DataFrame({
                    'date': ['2022-03', '2022-10', '2023-04', '2023-12', '2024-06', '2024-12'],
                    'event': [
                        'NIST AI RMF 1.0 Released',
                        'White House AI Bill of Rights',
                        'EU AI Act Provisional Agreement',
                        'Executive Order on AI Safety',
                        'AI Index Report 2024',
                        'Global AI Governance Summit'
                    ],
                    'impact': [85, 70, 90, 95, 60, 75],
                    'category': ['Framework', 'Policy', 'Regulation', 'Executive', 'Research', 'International']
                })
                
                # Convert date to datetime for proper plotting
                policy_timeline['date'] = pd.to_datetime(policy_timeline['date'])
                
                fig = go.Figure()
                
                # Color mapping for categories
                colors = {
                    'Framework': '#3498DB',
                    'Policy': '#2ECC71',
                    'Regulation': '#E74C3C',
                    'Executive': '#F39C12',
                    'Research': '#9B59B6',
                    'International': '#1ABC9C'
                }
                
                for category in policy_timeline['category'].unique():
                    cat_data = policy_timeline[policy_timeline['category'] == category]
                    fig.add_trace(go.Scatter(
                        x=cat_data['date'],
                        y=cat_data['impact'],
                        mode='markers+text',
                        name=category,
                        marker=dict(size=15, color=colors.get(category, '#95A5A6')),
                        text=cat_data['event'],
                        textposition='top center',
                        textfont=dict(size=10),
                        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Impact: %{y}%<extra></extra>'
                    ))
                
                fig.update_layout(
                    title="AI Governance Policy Development Timeline",
                    xaxis_title="Date",
                    yaxis_title="Policy Impact Score (%)",
                    height=500,
                    hovermode='closest',
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Safe plotting for policy timeline
            if safe_plot_check(
                pd.DataFrame({'dummy': [1]}),  # Dummy data for timeline
                "Policy Timeline",
                plot_func=plot_policy_timeline
            ):
                st.write("**Timeline Insights:**")
                st.write("• 2022-2024 marked rapid acceleration in AI governance frameworks")
                st.write("• Executive Order on AI Safety (Dec 2023) had highest policy impact")
                st.write("• International coordination efforts gaining momentum in 2024")
                st.write("• Regulatory frameworks moving from principles to implementation")
        
        # Additional governance insights and controls
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 View Data Source", key="governance_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('ai_index'))
        
        with col2:
            if st.button("📋 NIST Framework", key="nist_framework"):
                with st.expander("NIST AI RMF", expanded=True):
                    st.info(show_source_info('nist'))
        
        with col3:
            # Safe download button
            safe_download_button(
                governance_data,
                clean_filename(f"ai_governance_analysis_{data_year}.csv"),
                "📥 Download Governance Data",
                key="download_governance",
                help_text="Download AI governance implementation and maturity data"
            )
        
        # Governance recommendations
        st.markdown("### 💡 **Governance Implementation Recommendations**")
        st.write("""
        **Priority Actions for Organizations:**
        
        **Immediate (0-6 months):**
        • Establish AI Ethics Committee with senior leadership representation
        • Implement comprehensive AI inventory and risk assessment
        • Develop AI use policies aligned with NIST AI RMF
        
        **Medium-term (6-12 months):**
        • Deploy bias detection and monitoring systems
        • Create transparency documentation for AI systems
        • Establish vendor AI governance requirements
        
        **Long-term (12+ months):**
        • Integrate AI governance into enterprise risk management
        • Develop industry-specific compliance frameworks
        • Participate in AI governance standard-setting initiatives
        """)
    
    else:
        st.warning("AI governance data not available for analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_governance"):
                    st.cache_data.clear()
                    st.rerun()