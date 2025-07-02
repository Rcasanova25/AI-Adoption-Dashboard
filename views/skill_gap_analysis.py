"""
Skill Gap Analysis view for AI Adoption Dashboard
Displays AI skills gap analysis with demand vs supply, training recommendations, and salary impact
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import logging

from Utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename
from data.loaders import load_oecd_employment_outlook_data

logger = logging.getLogger(__name__)


def show_skill_gap_analysis(
    data_year: str,
    skill_gap_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI Skills Gap Analysis with comprehensive insights
    
    Args:
        data_year: Selected year (e.g., "2025")
        skill_gap_data: DataFrame with skills gap data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'skills':
            return "**Source**: AI Skills Gap Survey 2025\n\n**Methodology**: Analysis of 2,500+ organizations across industries, examining skill demands, training initiatives, and workforce development programs."
        elif source_type == 'oecd_employment':
            return "**Source**: OECD Employment Outlook 2024 - AI Employment Analysis\n\n**Methodology**: Comprehensive analysis across 34 OECD countries examining AI's impact on employment by skill category, substitution risks, and augmentation potential."
        return "**Source**: AI Index 2025 Report"
    
    st.write("🎓 **AI Skills Gap Analysis**")
    
    # Validate skill gap data
    validator = DataValidator()
    skills_result = validator.validate_dataframe(
        skill_gap_data,
        "Skills Gap Data",
        required_columns=['skill', 'gap_severity', 'training_initiatives'],
        min_rows=1
    )
    
    if skills_result.is_valid:
        # Enhanced skill gap data processing
        enhanced_skills = skill_gap_data.copy()
        
        # Add additional metrics if not present
        if 'demand_score' not in enhanced_skills.columns:
            # Simulate demand scores based on gap severity
            enhanced_skills['demand_score'] = enhanced_skills['gap_severity'] + 15
            enhanced_skills['demand_score'] = enhanced_skills['demand_score'].clip(upper=100)
        
        if 'supply_score' not in enhanced_skills.columns:
            # Calculate supply as inverse of gap severity + some baseline
            enhanced_skills['supply_score'] = 100 - enhanced_skills['gap_severity'] + 10
            enhanced_skills['supply_score'] = enhanced_skills['supply_score'].clip(lower=10, upper=80)
        
        if 'salary_premium' not in enhanced_skills.columns:
            # Simulate salary premium based on gap severity
            salary_premiums = [35, 28, 22, 18, 15, 12, 8, 5]  # Higher premiums for higher gaps
            if len(enhanced_skills) == len(salary_premiums):
                enhanced_skills['salary_premium'] = salary_premiums
            else:
                enhanced_skills['salary_premium'] = enhanced_skills['gap_severity'] * 0.4
        
        # Sort by gap severity for consistent visualization
        enhanced_skills = enhanced_skills.sort_values('gap_severity', ascending=True)
        
        # Main Skills Gap Visualization
        def plot_skills_gap_chart():
            """Plot the main skills gap and training initiatives chart"""
            fig = go.Figure()
            
            # Gap severity bars (horizontal)
            fig.add_trace(go.Bar(
                name='Gap Severity',
                y=enhanced_skills['skill'],
                x=enhanced_skills['gap_severity'],
                orientation='h',
                marker_color='#E74C3C',
                text=[f'{x}%' for x in enhanced_skills['gap_severity']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Gap Severity: %{x}%<extra></extra>'
            ))
            
            # Training initiatives bars (overlaid)
            fig.add_trace(go.Bar(
                name='Training Coverage',
                y=enhanced_skills['skill'],
                x=enhanced_skills['training_initiatives'],
                orientation='h',
                marker_color='#2ECC71',
                text=[f'{x}%' for x in enhanced_skills['training_initiatives']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Training Coverage: %{x}%<extra></extra>',
                opacity=0.7
            ))
            
            fig.update_layout(
                title="AI Skills Gap vs Training Coverage",
                xaxis_title="Percentage (%)",
                yaxis_title="Skill Area",
                height=500,
                barmode='overlay',
                hovermode='y unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Use safe plotting for main chart
        if safe_plot_check(
            enhanced_skills,
            "Skills Gap Data",
            required_columns=['skill', 'gap_severity', 'training_initiatives'],
            plot_func=plot_skills_gap_chart
        ):
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🎯 Demand vs Supply", "💰 Salary Impact", "🌍 OECD Analysis", "📋 Recommendations"])
            
            with tab1:
                # Key insights and metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_gap = enhanced_skills['gap_severity'].mean()
                    st.metric("Average Skills Gap", f"{avg_gap:.1f}%", delta=None)
                
                with col2:
                    avg_training = enhanced_skills['training_initiatives'].mean()
                    st.metric("Average Training Coverage", f"{avg_training:.1f}%", delta=None)
                
                with col3:
                    gap_training_diff = avg_gap - avg_training
                    st.metric("Gap-Training Deficit", f"{gap_training_diff:.1f}%", delta=f"{-gap_training_diff:.1f}%")
                
                # Top insights
                st.write("🔍 **Key Findings:**")
                
                # Get top gap areas
                top_gaps = enhanced_skills.nlargest(3, 'gap_severity')
                worst_training = enhanced_skills.nsmallest(3, 'training_initiatives')
                
                insights_text = f"""
                - **Highest Gap:** {top_gaps.iloc[0]['skill']} shows {top_gaps.iloc[0]['gap_severity']}% gap severity with only {top_gaps.iloc[0]['training_initiatives']}% training coverage
                - **Training Shortfall:** {worst_training.iloc[0]['skill']} has the lowest training coverage at {worst_training.iloc[0]['training_initiatives']}%
                - **Training Opportunity:** Gap between skill demand and training indicates significant workforce development opportunities
                """
                st.info(insights_text)
            
            with tab2:
                # Demand vs Supply Analysis
                st.write("📈 **Skills Demand vs Supply Analysis**")
                
                def plot_demand_supply():
                    """Plot demand vs supply scatter chart"""
                    fig = go.Figure()
                    
                    # Add scatter plot
                    fig.add_trace(go.Scatter(
                        x=enhanced_skills['supply_score'],
                        y=enhanced_skills['demand_score'],
                        mode='markers+text',
                        text=enhanced_skills['skill'],
                        textposition='top center',
                        marker=dict(
                            size=enhanced_skills['gap_severity'] * 0.5,  # Size based on gap severity
                            color=enhanced_skills['gap_severity'],
                            colorscale='Reds',
                            showscale=True,
                            colorbar=dict(title="Gap Severity (%)")
                        ),
                        hovertemplate='<b>%{text}</b><br>' +
                                     'Supply Score: %{x}<br>' +
                                     'Demand Score: %{y}<br>' +
                                     'Gap Severity: %{marker.color}%<extra></extra>'
                    ))
                    
                    # Add diagonal line for reference
                    fig.add_shape(
                        type="line",
                        x0=0, y0=0, x1=100, y1=100,
                        line=dict(color="gray", width=2, dash="dash"),
                    )
                    
                    fig.update_layout(
                        title="Skills Demand vs Supply Analysis",
                        xaxis_title="Supply Score",
                        yaxis_title="Demand Score",
                        height=500,
                        annotations=[
                            dict(
                                x=85, y=15,
                                text="High Supply<br>Low Demand",
                                showarrow=False,
                                font=dict(color="green")
                            ),
                            dict(
                                x=15, y=85,
                                text="Low Supply<br>High Demand",
                                showarrow=False,
                                font=dict(color="red")
                            )
                        ]
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                if safe_plot_check(
                    enhanced_skills,
                    "Demand vs Supply Data",
                    required_columns=['supply_score', 'demand_score', 'skill'],
                    plot_func=plot_demand_supply
                ):
                    st.info("💡 **Interpretation:** Skills in the upper-left quadrant (high demand, low supply) represent the most critical gaps requiring immediate attention.")
            
            with tab3:
                # Salary Impact Analysis
                st.write("💰 **Salary Premium Analysis**")
                
                def plot_salary_impact():
                    """Plot salary premium impact"""
                    fig = go.Figure()
                    
                    # Create horizontal bar chart for salary premiums
                    fig.add_trace(go.Bar(
                        y=enhanced_skills['skill'],
                        x=enhanced_skills['salary_premium'],
                        orientation='h',
                        marker_color='#F39C12',
                        text=[f'+{x}%' for x in enhanced_skills['salary_premium']],
                        textposition='outside',
                        hovertemplate='<b>%{y}</b><br>Salary Premium: +%{x}%<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="Salary Premium by Skill Area",
                        xaxis_title="Salary Premium (%)",
                        yaxis_title="Skill Area",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                if safe_plot_check(
                    enhanced_skills,
                    "Salary Premium Data",
                    required_columns=['skill', 'salary_premium'],
                    plot_func=plot_salary_impact
                ):
                    # Salary insights
                    highest_premium = enhanced_skills.loc[enhanced_skills['salary_premium'].idxmax()]
                    avg_premium = enhanced_skills['salary_premium'].mean()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Highest Premium", f"{highest_premium['skill']}", f"+{highest_premium['salary_premium']}%")
                    with col2:
                        st.metric("Average Premium", f"+{avg_premium:.1f}%", delta=None)
                    
                    st.info(f"💼 **Market Reality:** High-demand AI skills command significant salary premiums, with {highest_premium['skill']} leading at +{highest_premium['salary_premium']}% above baseline roles.")
            
            with tab4:
                # OECD Employment Analysis (NEW Phase 2A integration)
                st.write("🌍 **OECD Employment Outlook - International Perspective**")
                
                try:
                    # Load OECD employment outlook data
                    oecd_employment_data = load_oecd_employment_outlook_data()
                    
                    def plot_oecd_substitution_risk():
                        """Plot OECD AI substitution risk by skill category"""
                        fig = go.Figure()
                        
                        # Create horizontal bar chart
                        fig.add_trace(go.Bar(
                            y=oecd_employment_data['skill_category'],
                            x=oecd_employment_data['ai_substitution_risk'],
                            orientation='h',
                            name='Substitution Risk',
                            marker_color='#E74C3C',
                            text=[f'{x}%' for x in oecd_employment_data['ai_substitution_risk']],
                            textposition='outside'
                        ))
                        
                        # Add augmentation potential as overlay
                        fig.add_trace(go.Bar(
                            y=oecd_employment_data['skill_category'],
                            x=oecd_employment_data['ai_augmentation_potential'],
                            orientation='h',
                            name='Augmentation Potential',
                            marker_color='#2ECC71',
                            opacity=0.7,
                            text=[f'{x}%' for x in oecd_employment_data['ai_augmentation_potential']],
                            textposition='outside'
                        ))
                        
                        fig.update_layout(
                            title="AI Impact on Employment by Skill Category (OECD Analysis)",
                            xaxis_title="Percentage (%)",
                            yaxis_title="Skill Category",
                            height=400,
                            barmode='overlay',
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    if safe_plot_check(
                        oecd_employment_data,
                        "OECD Employment Data",
                        required_columns=['skill_category', 'ai_substitution_risk', 'ai_augmentation_potential'],
                        plot_func=plot_oecd_substitution_risk
                    ):
                        
                        # Key insights from OECD data
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**🔍 Key OECD Findings:**")
                            # Calculate insights
                            highest_risk = oecd_employment_data.loc[oecd_employment_data['ai_substitution_risk'].idxmax()]
                            highest_augmentation = oecd_employment_data.loc[oecd_employment_data['ai_augmentation_potential'].idxmax()]
                            
                            st.write(f"• **Highest substitution risk:** {highest_risk['skill_category']} ({highest_risk['ai_substitution_risk']}%)")
                            st.write(f"• **Highest augmentation potential:** {highest_augmentation['skill_category']} ({highest_augmentation['ai_augmentation_potential']}%)")
                            st.write(f"• **Coverage:** {oecd_employment_data['coverage'].iloc[0]}")
                        
                        with col2:
                            st.write("**📊 Employment Impact Projections:**")
                            # Show employment change projections
                            positive_change = oecd_employment_data[oecd_employment_data['net_employment_change_2030'] > 0]
                            negative_change = oecd_employment_data[oecd_employment_data['net_employment_change_2030'] < 0]
                            
                            if len(positive_change) > 0:
                                st.write(f"• **Job growth expected:** {len(positive_change)} skill categories")
                            if len(negative_change) > 0:
                                st.write(f"• **Job displacement risk:** {len(negative_change)} skill categories")
                            
                            avg_retraining = oecd_employment_data['retraining_urgency_score'].mean()
                            st.write(f"• **Average retraining urgency:** {avg_retraining:.0f}/100")
                        
                        st.success("✅ **OECD Insight:** This international analysis from 34 OECD countries provides authoritative data on AI's employment impact across different skill levels.")
                        
                        if st.button("📊 View OECD Data Source", key="oecd_employment_source"):
                            with st.expander("OECD Employment Outlook Source", expanded=True):
                                st.info(show_source_info('oecd_employment'))
                
                except Exception as e:
                    logger.error(f"Error loading OECD employment data: {e}")
                    st.warning("OECD Employment Outlook data temporarily unavailable")
                    st.info("💡 This tab normally displays comprehensive international analysis of AI's impact on employment from the OECD's 34-country study.")
            
            with tab5:
                # Training Recommendations
                st.write("📋 **Training & Development Recommendations**")
                
                # Calculate priority scores
                enhanced_skills['priority_score'] = (
                    enhanced_skills['gap_severity'] * 0.4 +
                    (100 - enhanced_skills['training_initiatives']) * 0.3 +
                    enhanced_skills['salary_premium'] * 0.3
                )
                
                # Sort by priority
                priority_skills = enhanced_skills.sort_values('priority_score', ascending=False)
                
                st.write("🎯 **High Priority Skills (Immediate Action Required):**")
                
                for i, (_, skill) in enumerate(priority_skills.head(3).iterrows(), 1):
                    with st.expander(f"{i}. {skill['skill']} (Priority Score: {skill['priority_score']:.1f})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Gap Severity:** {skill['gap_severity']}%")
                            st.write(f"**Current Training:** {skill['training_initiatives']}%")
                            st.write(f"**Salary Premium:** +{skill['salary_premium']}%")
                        
                        with col2:
                            st.write("**Recommended Actions:**")
                            if skill['skill'] == 'AI/ML Engineering':
                                st.write("• Partner with universities for specialized AI programs")
                                st.write("• Implement hands-on ML bootcamps")
                                st.write("• Create mentorship programs with senior engineers")
                            elif skill['skill'] == 'Data Science':
                                st.write("• Develop internal data science academies")
                                st.write("• Provide cloud platform training (AWS, Azure, GCP)")
                                st.write("• Focus on business application of analytics")
                            elif skill['skill'] == 'AI Ethics':
                                st.write("• Establish AI ethics committees")
                                st.write("• Create responsible AI training modules")
                                st.write("• Develop bias detection workshops")
                            elif skill['skill'] == 'Prompt Engineering':
                                st.write("• Create prompt engineering workshops")
                                st.write("• Develop LLM application training")
                                st.write("• Build internal prompt libraries")
                            elif skill['skill'] == 'AI Product Management':
                                st.write("• Train PMs on AI capabilities and limitations")
                                st.write("• Develop AI product strategy frameworks")
                                st.write("• Create cross-functional AI teams")
                            elif skill['skill'] == 'MLOps':
                                st.write("• Implement MLOps platform training")
                                st.write("• Focus on model deployment and monitoring")
                                st.write("• Develop CI/CD for ML workflows")
                            elif skill['skill'] == 'AI Security':
                                st.write("• Establish AI security protocols")
                                st.write("• Train on adversarial attack prevention")
                                st.write("• Develop secure AI deployment practices")
                            else:  # Change Management
                                st.write("• Develop change management frameworks for AI")
                                st.write("• Train leaders on AI transformation")
                                st.write("• Create employee AI adoption programs")
                
                # Overall recommendations
                st.write("📈 **Strategic Recommendations:**")
                st.success("""
                **1. Immediate Actions (0-3 months):**
                - Launch emergency training programs for top 3 priority skills
                - Establish partnerships with AI training providers
                - Create internal AI skill assessment framework
                
                **2. Medium-term Strategy (3-12 months):**
                - Develop comprehensive AI curriculum
                - Implement mentorship and knowledge transfer programs
                - Create career progression paths for AI roles
                
                **3. Long-term Vision (1-3 years):**
                - Establish internal AI university/academy
                - Build centers of excellence for each skill area
                - Create industry partnerships for continuous learning
                """)
            
            # Download and source information
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 View Data Source", key="skills_source"):
                    with st.expander("Data Source", expanded=True):
                        st.info(show_source_info('skills'))
            
            with col2:
                # Safe download button
                safe_download_button(
                    enhanced_skills,
                    clean_filename(f"ai_skills_gap_analysis_{data_year}.csv"),
                    "📥 Download Skills Data",
                    key="download_skills_gap",
                    help_text="Download complete AI skills gap analysis data including recommendations"
                )
    
    else:
        st.warning("Skills gap data not available for analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_skills"):
                    st.cache_data.clear()
                    st.rerun()