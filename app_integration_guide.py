"""Integration guide for updating app.py with real economic calculations.

This file provides the specific code changes needed to integrate the new
economic models into the existing dashboard.
"""

# ============================================================================
# STEP 1: Add imports at the top of app.py (after existing imports)
# ============================================================================

IMPORTS_TO_ADD = """
# Import enhanced economic components
from components.dashboard_integration import DashboardIntegration
from components.competitive_assessor_enhanced import EnhancedCompetitiveAssessor
from components.economic_validation import EconomicValidator
"""

# ============================================================================
# STEP 2: Initialize components after data loading
# ============================================================================

INITIALIZATION_CODE = """
# Initialize enhanced economic components
dashboard_integration = DashboardIntegration()
economic_validator = EconomicValidator()
"""

# ============================================================================
# STEP 3: Replace the ROI Analysis section (around line 4839)
# ============================================================================

ENHANCED_ROI_ANALYSIS = '''
elif view_type == "ROI Analysis":
    st.write("💰 **ROI Analysis: Comprehensive Economic Impact**")
    
    # Display methodology
    dashboard_integration.display_calculation_methodology()
    
    # Create detailed ROI dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["Investment Returns", "Payback Analysis", "Sector ROI", "ROI Calculator"])
    
    with tab1:
        # Enhanced investment returns visualization with real data
        st.subheader("📈 AI Investment Returns by Level")
        
        # Get validated industry list
        valid_industries = economic_validator.constraints.VALID_SECTORS
        selected_industry = st.selectbox(
            "Select Industry for Analysis",
            options=valid_industries,
            index=0
        )
        
        # Investment level analysis
        investment_levels = {
            'Pilot (<$100K)': 100_000,
            'Small ($100K-$500K)': 300_000,
            'Medium ($500K-$2M)': 1_250_000,
            'Large ($2M-$10M)': 6_000_000,
            'Enterprise ($10M+)': 25_000_000
        }
        
        roi_data = []
        for level, amount in investment_levels.items():
            # Calculate real ROI for each level
            roi_result = dashboard_integration.economic_models.calculate_roi_with_real_data(
                investment=amount,
                use_case="Default",
                implementation_years=2,
                company_size="Large" if amount > 2_000_000 else "Medium",
                industry=selected_industry
            )
            
            roi_data.append({
                'investment_level': level,
                'avg_roi': roi_result['total_roi_percentage'] / 100,  # Convert to multiplier
                'npv': roi_result['npv'],
                'payback_months': roi_result['payback_period_years'] * 12,
                'efficiency_gain': roi_result['efficiency_gain_percentage']
            })
        
        roi_df = pd.DataFrame(roi_data)
        
        # Create enhanced visualization
        fig = go.Figure()
        
        # ROI bars with real calculations
        fig.add_trace(go.Bar(
            name='Expected ROI',
            x=roi_df['investment_level'],
            y=roi_df['avg_roi'],
            yaxis='y',
            marker_color='#2ECC71',
            text=[f'{x:.1f}x' for x in roi_df['avg_roi']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}x<br>NPV: $%{customdata:,.0f}<extra></extra>',
            customdata=roi_df['npv']
        ))
        
        # Efficiency gains line
        fig.add_trace(go.Scatter(
            name='Efficiency Gain %',
            x=roi_df['investment_level'],
            y=roi_df['efficiency_gain'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(width=3, color='#3498DB'),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Efficiency: %{y:.0f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'AI ROI by Investment Level - {selected_industry}',
            xaxis_title='Investment Level',
            yaxis=dict(title='Expected ROI (x)', side='left'),
            yaxis2=dict(title='Efficiency Gain (%)', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        fig = a11y.make_chart_accessible(
            fig,
            title=f"AI ROI by Investment Level for {selected_industry}",
            description=f"Chart showing real ROI calculations based on McKinsey data and Goldman Sachs productivity gains for the {selected_industry} industry."
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show confidence intervals
        st.info(f"""
        **📊 Data Confidence:** These calculations use:
        - McKinsey actual ROI data by use case
        - Goldman Sachs sector productivity gains ({selected_industry}: {dashboard_integration.economic_models.params.sector_productivity_gains.get(selected_industry, 30):.0f}%)
        - S-curve adoption models with learning effects
        - 80% confidence intervals apply
        """)
    
    with tab2:
        # Enhanced payback period analysis
        st.subheader("⏱️ Payback Period Analysis")
        
        # Industry selector
        payback_industry = st.selectbox(
            "Select Industry",
            options=valid_industries,
            key="payback_industry"
        )
        
        # Get industry-specific payback data
        payback_months = dashboard_integration.economic_models.params.industry_payback_periods.get(
            payback_industry, 18
        )
        
        # Create payback scenarios with real calculations
        scenarios = []
        for complexity in ["Low", "Medium", "High"]:
            result = dashboard_integration.economic_models.calculate_payback_period(
                investment=1_000_000,
                annual_benefit=2_000_000,
                industry=payback_industry,
                implementation_complexity=complexity
            )
            
            scenarios.append({
                'scenario': f'{complexity} Complexity',
                'months': result['payback_months'],
                'base_months': result['base_payback_months'],
                'ramp_up': result['ramp_up_months'],
                'total_implementation': result['total_implementation_months']
            })
        
        scenarios_df = pd.DataFrame(scenarios)
        
        # Visualize payback periods
        fig = go.Figure()
        
        # Stacked bar chart for time components
        fig.add_trace(go.Bar(
            name='Ramp-up Time',
            x=scenarios_df['scenario'],
            y=scenarios_df['ramp_up'],
            marker_color='#F39C12'
        ))
        
        fig.add_trace(go.Bar(
            name='Full Productivity Time',
            x=scenarios_df['scenario'],
            y=scenarios_df['months'] - scenarios_df['ramp_up'],
            marker_color='#2ECC71'
        ))
        
        fig.update_layout(
            title=f'Payback Period by Implementation Complexity - {payback_industry}',
            xaxis_title='Implementation Complexity',
            yaxis_title='Months',
            barmode='stack',
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Industry Baseline",
                f"{payback_months} months",
                help=f"McKinsey data for {payback_industry}"
            )
        
        with col2:
            st.metric(
                "Typical Ramp-up",
                f"{payback_months * 0.5:.0f} months",
                help="Time to reach full productivity"
            )
        
        # Factors affecting payback
        st.markdown("### Factors Affecting Payback Period")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🚀 Accelerators:**")
            st.write("• Clear use case definition")
            st.write("• Strong change management")
            st.write("• Existing data infrastructure")
            st.write("• Skilled team in place")
            st.write("• Executive sponsorship")
        
        with col2:
            st.write("**🐌 Delays:**")
            st.write("• Poor data quality")
            st.write("• Integration challenges")
            st.write("• Organizational resistance")
            st.write("• Scope creep")
            st.write("• Skills gap")
    
    with tab3:
        # Enhanced sector-specific ROI with real calculations
        st.subheader("🏭 Industry-Specific ROI Analysis")
        
        # Get enhanced sector data
        enhanced_sector_data, sector_insights = dashboard_integration.enhance_sector_roi_display(sector_2025)
        
        # Create comprehensive visualization
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('ROI by Sector', 'Productivity Gains by Sector'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Sort by ROI
        sorted_data = enhanced_sector_data.sort_values('avg_roi')
        
        # ROI bars
        fig.add_trace(
            go.Bar(
                x=sorted_data['sector'],
                y=sorted_data['avg_roi'],
                name='Average ROI',
                marker_color=sorted_data['avg_roi'],
                marker_colorscale='Viridis',
                text=[f'{x}x' for x in sorted_data['avg_roi']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>ROI: %{y}x<br>Adoption: %{customdata}%<extra></extra>',
                customdata=sorted_data['adoption_rate']
            ),
            row=1, col=1
        )
        
        # Productivity gains bars
        fig.add_trace(
            go.Bar(
                x=sorted_data['sector'],
                y=sorted_data['productivity_gain'],
                name='Productivity Gain',
                marker_color=sorted_data['productivity_gain'],
                marker_colorscale='Blues',
                text=[f'{x:.0f}%' for x in sorted_data['productivity_gain']],
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sector insights
        st.markdown("### 🎯 Key Sector Insights")
        
        top_sectors = enhanced_sector_data.nlargest(3, 'avg_roi')
        
        for _, sector in top_sectors.iterrows():
            insight = sector_insights.get(sector['sector'], {})
            
            with st.expander(f"📊 {sector['sector']} - {sector['avg_roi']}x ROI"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Adoption Rate", f"{sector['adoption_rate']}%")
                    st.metric("Productivity Baseline", f"{insight.get('productivity_baseline', 30):.0f}%")
                
                with col2:
                    st.metric("Market Value Impact", f"{sector.get('market_value_impact', 0):.0f}%")
                    st.metric("Growth Multiple", f"{insight.get('growth_multiple', 1.3):.1f}x")
                
                with col3:
                    st.metric("GenAI Adoption", f"{sector.get('genai_adoption', 0):.0f}%")
                    st.metric("Adoption Premium", f"{insight.get('adoption_premium', 0):.0f}%")
    
    with tab4:
        # Enhanced Interactive ROI Calculator with validation
        st.write("**🧮 AI Investment ROI Calculator - Real Economic Models**")
        
        # Add validation helper
        validation_helper = dashboard_integration.validate_and_enhance_input_form(st.container())
        
        col1, col2 = st.columns(2)
        
        with col1:
            investment_amount = st.number_input(
                "Initial Investment ($)",
                min_value=10000,
                max_value=10000000,
                value=250000,
                step=10000,
                help="Total AI project investment"
            )
            
            project_type = st.selectbox(
                "Project Type",
                options=economic_validator.constraints.VALID_PROJECT_TYPES[:8],
                help="Based on McKinsey ROI data"
            )
            
            company_size = st.select_slider(
                "Company Size",
                options=list(economic_validator.constraints.COMPANY_SIZES.keys()),
                value="Medium"
            )
            
            industry_calc = st.selectbox(
                "Industry",
                options=valid_industries,
                key="calc_industry"
            )
        
        with col2:
            implementation_quality = st.slider(
                "Implementation Quality",
                min_value=1,
                max_value=5,
                value=3,
                help="1=Poor, 5=Excellent"
            )
            
            data_readiness = st.slider(
                "Data Readiness",
                min_value=1,
                max_value=5,
                value=3,
                help="1=Poor quality, 5=Excellent quality"
            )
            
            timeline = st.selectbox(
                "Implementation Timeline",
                ["6 months", "12 months", "18 months", "24 months", "36 months"],
                index=1
            )
            
            annual_revenue = st.number_input(
                "Annual Revenue ($)",
                min_value=1000000,
                max_value=1000000000,
                value=100000000,
                step=1000000,
                help="For validation and benchmarking"
            )
        
        # Calculate ROI with real models
        calc_results = dashboard_integration.enhance_roi_calculator(
            investment_amount=investment_amount,
            project_type=project_type,
            company_size=company_size,
            implementation_quality=implementation_quality,
            data_readiness=data_readiness,
            timeline=timeline,
            industry=industry_calc
        )
        
        if calc_results['valid']:
            # Display results
            st.markdown("---")
            st.subheader("📊 Projected Results - Based on Real Data")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Expected ROI", 
                    f"{calc_results['final_roi']:.1f}x",
                    help=f"Methodology: {calc_results['methodology']}"
                )
            
            with col2:
                st.metric(
                    "NPV", 
                    f"${calc_results['npv']:,.0f}",
                    delta=f"{calc_results['irr']:.1f}% IRR"
                )
            
            with col3:
                st.metric(
                    "Net Benefit", 
                    f"${calc_results['net_benefit']:,.0f}",
                    delta=f"{(calc_results['net_benefit']/investment_amount)*100:.0f}%"
                )
            
            with col4:
                st.metric(
                    "Payback Period", 
                    f"{calc_results['payback_months']} months",
                    help="Industry-adjusted payback"
                )
            
            # Show confidence intervals
            confidence = calc_results['confidence_intervals']
            
            st.info(f"""
            **Confidence Intervals (80% confidence):**
            - Pessimistic: {confidence['pessimistic']:.0f}% ROI
            - Expected: {confidence['expected']:.0f}% ROI
            - Optimistic: {confidence['optimistic']:.0f}% ROI
            
            **Data Confidence: {calc_results['data_confidence']*100:.0f}%**
            """)
            
            # Risk assessment
            st.warning(f"""
            **Risk Assessment:** {calc_results['risk_level']}
            - Implementation Quality: {'⭐' * implementation_quality}
            - Data Readiness: {'⭐' * data_readiness}
            - Efficiency Gain Potential: {calc_results['efficiency_gain']:.0f}%
            - Recommendation: {"Proceed with confidence" if calc_results['risk_score'] <= 2 else "Address gaps before proceeding"}
            """)
            
            # Generate executive summary
            if st.checkbox("Show Executive Summary"):
                exec_metrics = dashboard_integration.generate_executive_roi_summary(
                    investment=investment_amount,
                    revenue=annual_revenue,
                    industry=industry_calc,
                    current_adoption=25,  # Default
                    target_adoption=75,   # Default target
                    timeline_years=int(timeline.split()[0]) // 12
                )
                
                st.markdown(dashboard_integration.format_executive_metrics(exec_metrics))
            
            # ROI Timeline visualization
            if st.checkbox("Show ROI Timeline"):
                timeline_fig = dashboard_integration.create_enhanced_roi_timeline_chart(
                    investment=investment_amount,
                    use_case=project_type,
                    years=int(timeline.split()[0]) // 12,
                    company_size=company_size,
                    industry=industry_calc
                )
                st.plotly_chart(timeline_fig, use_container_width=True)
            
            # Export calculation
            if st.button("📥 Export ROI Analysis"):
                analysis_text = f"""
                AI ROI Analysis Report - Real Economic Models
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                
                Investment Details:
                - Amount: ${investment_amount:,}
                - Project Type: {project_type}
                - Company Size: {company_size}
                - Industry: {industry_calc}
                - Timeline: {timeline}
                
                Quality Metrics:
                - Implementation Quality: {implementation_quality}/5
                - Data Readiness: {data_readiness}/5
                - Data Confidence: {calc_results['data_confidence']*100:.0f}%
                
                Projected Results (Based on McKinsey/Goldman Sachs Data):
                - Expected ROI: {calc_results['final_roi']:.1f}x
                - NPV: ${calc_results['npv']:,.0f}
                - IRR: {calc_results['irr']:.1f}%
                - Net Benefit: ${calc_results['net_benefit']:,.0f}
                - Payback Period: {calc_results['payback_months']} months
                - Efficiency Gain: {calc_results['efficiency_gain']:.0f}%
                - Risk Level: {calc_results['risk_level']}
                
                Confidence Intervals (80%):
                - Pessimistic: {confidence['pessimistic']:.0f}% ROI
                - Expected: {confidence['expected']:.0f}% ROI  
                - Optimistic: {confidence['optimistic']:.0f}% ROI
                
                Methodology: {calc_results['methodology']}
                
                Data Sources:
                - McKinsey "State of AI 2024" - ROI by use case
                - Goldman Sachs - Sector productivity gains
                - Industry-specific payback periods
                - S-curve adoption models
                """
                
                st.download_button(
                    label="Download Analysis",
                    data=analysis_text,
                    file_name=f"ai_roi_analysis_real_data_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        else:
            # Show validation errors
            st.error(validation_helper['validator'].format_validation_errors(calc_results['errors']))
'''

# ============================================================================
# STEP 4: Replace the Competitive Assessment initialization
# ============================================================================

ENHANCED_COMPETITIVE_ASSESSMENT = """
# Replace the existing CompetitiveAssessor initialization with:
comp_assessor = EnhancedCompetitiveAssessor(
    sector_data=sector_2025,
    firm_size_data=firm_size_data,
    adoption_trends=adoption_trends,
    investment_data=investment_gdp
)

# The render() method will now use real economic calculations
"""

# ============================================================================
# STEP 5: Add validation to forms throughout the app
# ============================================================================

FORM_VALIDATION_EXAMPLE = """
# Example of adding validation to any input form:

# Before accepting inputs
is_valid, errors, confidence = economic_validator.validate_economic_inputs(
    revenue=revenue_input,
    employees=employee_input,
    ai_investment=investment_input,
    sector=industry_input
)

if not is_valid:
    st.error(economic_validator.format_validation_errors(errors))
else:
    # Proceed with calculations
    confidence_info = economic_validator.get_confidence_interpretation(confidence['overall'])
    st.info(f"{confidence_info['icon']} Data Confidence: {confidence_info['level']}")
"""

# ============================================================================
# INSTRUCTIONS FOR INTEGRATION
# ============================================================================

def print_integration_instructions():
    """Print step-by-step integration instructions."""
    
    print("""
    ==========================================
    INTEGRATION INSTRUCTIONS FOR app.py
    ==========================================
    
    1. BACKUP app.py first!
       cp app.py app_backup.py
    
    2. Add imports (after line 20):
       - from components.dashboard_integration import DashboardIntegration
       - from components.competitive_assessor_enhanced import EnhancedCompetitiveAssessor
       - from components.economic_validation import EconomicValidator
    
    3. Initialize components (after data loading, around line 300):
       - dashboard_integration = DashboardIntegration()
       - economic_validator = EconomicValidator()
    
    4. Replace ROI Analysis section (starting at line 4839):
       - Copy the ENHANCED_ROI_ANALYSIS code above
       - This integrates real economic models
    
    5. Replace CompetitiveAssessor with EnhancedCompetitiveAssessor:
       - Update the initialization to use enhanced version
       - No other changes needed - it's backward compatible
    
    6. Add validation to input forms:
       - Use economic_validator.validate_economic_inputs()
       - Display confidence scores
       - Show helpful error messages
    
    7. Test thoroughly:
       - Check ROI calculations show real data
       - Verify validation works properly
       - Confirm competitive assessor uses economic models
       - Test export functionality
    
    BENEFITS:
    - Real economic calculations based on Goldman Sachs & McKinsey
    - Comprehensive input validation with business logic
    - Confidence scoring for all calculations
    - Better error handling and user guidance
    - Data source citations and methodology transparency
    """)

if __name__ == "__main__":
    print_integration_instructions()