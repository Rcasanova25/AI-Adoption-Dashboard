# ui_integration_example.py - Integration Example for Your AI Dashboard
"""
This file shows how to integrate the advanced UI components into your existing app.py
Replace sections of your current app.py with these enhanced versions.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import your new components
from components.charts import MetricCard, TrendChart, ComparisonChart, ROIChart
from components.layouts import ExecutiveDashboard, ResponsiveGrid, GridConfig
from components.widgets import SmartFilter, ActionButton, ProgressIndicator, AlertBox
from components.themes import ThemeManager, ThemeMode

# Enhanced page configuration with professional settings
st.set_page_config(
    page_title="AI Adoption Dashboard | Strategic Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/your-repo/AI-Adoption-Dashboard/issues",
        'About': """
        # AI Adoption Dashboard v2.3.0
        **Strategic Decision Intelligence Platform**
        
        Transform your AI strategy with data-driven insights and professional analysis tools.
        
        Created with ❤️ by the AI Strategy Team
        """
    }
)

# Apply professional theme
def setup_professional_theme():
    """Setup and apply professional theme"""
    # Get theme preference from sidebar
    selected_theme = ThemeManager.get_theme_selector()
    ThemeManager.apply_theme(selected_theme)
    
    # Store theme in session state
    st.session_state.current_theme = selected_theme
    
    return selected_theme

# Enhanced data loading with better error handling
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_enhanced_data():
    """Load data with enhanced error handling and validation"""
    try:
        # Your existing data loading logic here
        from data.loaders import load_all_datasets
        datasets = load_all_datasets()
        
        if datasets is None:
            raise ValueError("Data loading returned None")
        
        # Validate critical datasets
        required_datasets = ['historical_data', 'sector_2025', 'investment_data']
        missing_datasets = [ds for ds in required_datasets if ds not in datasets or datasets[ds] is None]
        
        if missing_datasets:
            st.warning(f"⚠️ Some datasets are missing: {', '.join(missing_datasets)}")
            # Create fallback data for missing datasets
            datasets = create_fallback_datasets(datasets, missing_datasets)
        
        return datasets
        
    except Exception as e:
        st.error(f"❌ Critical error in data loading: {str(e)}")
        st.info("🔄 Using demonstration data. Please check your data sources.")
        return create_demo_datasets()

def create_demo_datasets():
    """Create demonstration datasets for when real data is unavailable"""
    return {
        'historical_data': pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024, 2025],
            'ai_use': [15, 28, 45, 55, 78, 82],
            'genai_use': [0, 2, 15, 33, 71, 75]
        }),
        'sector_2025': pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 'Retail'],
            'adoption_rate': [92, 85, 78, 75, 72],
            'avg_roi': [4.2, 3.8, 3.1, 2.9, 3.3],
            'genai_adoption': [89, 76, 68, 65, 69]
        }),
        'investment_data': pd.DataFrame({
            'year': [2022, 2023, 2024],
            'total_investment': [174.5, 207.8, 252.3],
            'genai_investment': [5.2, 18.7, 33.9]
        })
    }

def create_fallback_datasets(datasets, missing_datasets):
    """Create fallback data for missing datasets"""
    demo_data = create_demo_datasets()
    
    for dataset_name in missing_datasets:
        if dataset_name in demo_data:
            datasets[dataset_name] = demo_data[dataset_name]
    
    return datasets

# Dynamic metrics calculation function
def get_dynamic_metrics(historical_data, ai_cost_reduction, ai_investment_data, sector_2025):
    """Extract dynamic metrics from loaded data"""
    metrics = {}
    
    # Market acceleration calculation
    if historical_data is not None and len(historical_data) >= 2:
        latest_adoption = historical_data['ai_use'].iloc[-1]
        previous_adoption = historical_data['ai_use'].iloc[-3] if len(historical_data) >= 3 else historical_data['ai_use'].iloc[-2]
        adoption_delta = latest_adoption - previous_adoption
        metrics['market_adoption'] = f"{latest_adoption}%"
        metrics['market_delta'] = f"+{adoption_delta}pp vs 2023"
        
        # GenAI adoption
        latest_genai = historical_data['genai_use'].iloc[-1]
        previous_genai = historical_data['genai_use'].iloc[-3] if len(historical_data) >= 3 else historical_data['genai_use'].iloc[-2]
        genai_delta = latest_genai - previous_genai
        metrics['genai_adoption'] = f"{latest_genai}%"
        metrics['genai_delta'] = f"+{genai_delta}pp from 2023"
    else:
        metrics['market_adoption'] = "78%"
        metrics['market_delta'] = "+23pp vs 2023"
        metrics['genai_adoption'] = "71%"
        metrics['genai_delta'] = "+38pp from 2023"
    
    # Cost reduction calculation
    if ai_cost_reduction is not None and len(ai_cost_reduction) >= 2:
        earliest_cost = ai_cost_reduction['cost_per_million_tokens'].iloc[0]
        latest_cost = ai_cost_reduction['cost_per_million_tokens'].iloc[-1]
        cost_multiplier = earliest_cost / latest_cost
        metrics['cost_reduction'] = f"{cost_multiplier:.0f}x cheaper"
        metrics['cost_period'] = "Since Nov 2022"
    else:
        metrics['cost_reduction'] = "280x cheaper"
        metrics['cost_period'] = "Since Nov 2022"
    
    # Investment growth calculation
    if ai_investment_data is not None and len(ai_investment_data) >= 2:
        latest_investment = ai_investment_data['total_investment'].iloc[-1]
        previous_investment = ai_investment_data['total_investment'].iloc[-2]
        investment_growth = ((latest_investment - previous_investment) / previous_investment) * 100
        metrics['investment_value'] = f"${latest_investment}B"
        metrics['investment_delta'] = f"+{investment_growth:.1f}% YoY"
    else:
        metrics['investment_value'] = "$252.3B"
        metrics['investment_delta'] = "+44.5% YoY"
    
    # Average ROI calculation
    if sector_2025 is not None and 'avg_roi' in sector_2025.columns:
        avg_roi = sector_2025['avg_roi'].mean()
        metrics['avg_roi'] = f"{avg_roi:.1f}x"
        metrics['roi_desc'] = "Across sectors"
    else:
        metrics['avg_roi'] = "3.2x"
        metrics['roi_desc'] = "Across sectors"
    
    return metrics

# Enhanced executive dashboard with new components
def render_enhanced_executive_dashboard(datasets, dynamic_metrics):
    """Render enhanced executive dashboard using new components"""
    
    # Executive Dashboard Layout
    exec_dashboard = ExecutiveDashboard()
    
    # Professional Header
    exec_dashboard.render_header(
        title="🚀 AI Strategic Command Center",
        subtitle="Executive Intelligence Dashboard for Strategic Decision Making"
    )
    
    # Enhanced KPI Section with Professional Metric Cards
    st.markdown("### 📊 Strategic Performance Indicators")
    
    # Create metric cards with enhanced styling
    metric_card = MetricCard()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Get trend data for sparkline
        hist_data = datasets.get('historical_data')
        trend_data = hist_data['ai_use'].tolist() if hist_data is not None else [55, 65, 71, 78]
        
        metric_card.render(
            title="Market Adoption Rate",
            value=dynamic_metrics.get('market_adoption', '78%'),
            delta=dynamic_metrics.get('market_delta', '+23pp vs 2023'),
            trend=trend_data,
            insight="Crossed majority adoption threshold",
            color="success",
            help_text="Percentage of businesses using any AI technology"
        )
    
    with col2:
        genai_trend = hist_data['genai_use'].tolist() if hist_data is not None else [15, 33, 65, 71]
        
        metric_card.render(
            title="GenAI Penetration",
            value=dynamic_metrics.get('genai_adoption', '71%'),
            delta=dynamic_metrics.get('genai_delta', '+38pp from 2023'),
            trend=genai_trend,
            insight="Revolutionary technology adoption",
            color="info",
            help_text="Businesses actively using Generative AI solutions"
        )
    
    with col3:
        metric_card.render(
            title="Average ROI Multiple",
            value=dynamic_metrics.get('avg_roi', '3.2x'),
            delta="Consistent value creation",
            insight="Strong business case validated",
            color="success", 
            help_text="Average return on AI investments across sectors"
        )
    
    with col4:
        metric_card.render(
            title="Global Investment",
            value=dynamic_metrics.get('investment_value', '$252.3B'),
            delta=dynamic_metrics.get('investment_delta', '+44.5% YoY'),
            insight="Record investment levels",
            color="warning",
            help_text="Total global AI investment in 2024"
        )
    
    # Enhanced Strategic Insights Section
    insights = [
        {
            "type": "success",
            "title": "🎯 Competitive Advantage Window Open",
            "content": f"With {dynamic_metrics.get('market_adoption', '78%')} market adoption, AI has reached mainstream status. Organizations moving now can still capture first-mover advantages in implementation quality and specialized applications.",
            "action": "Accelerate pilot-to-production transitions within 90 days"
        },
        {
            "type": "warning",
            "title": "⚠️ Talent Market Tightening",
            "content": "68% of organizations cite talent shortage as primary barrier. The window for building internal capabilities at reasonable cost is narrowing rapidly.",
            "action": "Prioritize AI talent acquisition and development programs immediately"
        },
        {
            "type": "info",
            "title": "💰 Investment Economics Favorable", 
            "content": f"Cost reduction of {dynamic_metrics.get('cost_reduction', '280x')} since 2022 enables mass deployment. Combined with proven {dynamic_metrics.get('avg_roi', '3.2x')} average ROI, business case is compelling.",
            "action": "Scale successful pilots to enterprise-wide deployment"
        }
    ]
    
    exec_dashboard.render_insights_section(insights)
    
    # Enhanced Chart Section with Professional Styling
    st.markdown("### 📈 Market Intelligence Analysis")
    
    # Advanced Trend Chart
    if datasets.get('historical_data') is not None:
        trend_chart = TrendChart()
        
        # Add strategic annotations
        annotations = [
            {
                'x': 2022, 
                'y': 45,
                'text': "<b>ChatGPT Launch</b><br>GenAI Revolution Begins",
                'showarrow': True,
                'arrowhead': 2,
                'arrowcolor': "#F18F01",
                'ax': -50,
                'ay': -40,
                'bgcolor': "rgba(241,143,1,0.1)",
                'bordercolor': "#F18F01",
                'borderwidth': 2
            },
            {
                'x': 2024,
                'y': 78,
                'text': "<b>Mainstream Adoption</b><br>Majority Threshold Crossed",
                'showarrow': True, 
                'arrowhead': 2,
                'arrowcolor': "#6A994E",
                'ax': 50,
                'ay': -30,
                'bgcolor': "rgba(106,153,78,0.1)",
                'bordercolor': "#6A994E",
                'borderwidth': 2
            }
        ]
        
        trend_chart.render(
            data=datasets['historical_data'],
            x_col='year',
            y_cols=['ai_use', 'genai_use'],
            title="AI Adoption Acceleration: The Strategic Inflection Point",
            subtitle="Enterprise adoption trends showing unprecedented technology uptake velocity",
            annotations=annotations,
            height=600,
            show_controls=True,
            enable_zoom=True
        )
    
    # Industry Comparison with Enhanced Styling
    if datasets.get('sector_2025') is not None:
        st.markdown("### 🏭 Competitive Landscape Analysis")
        
        comparison_chart = ComparisonChart()
        comparison_chart.render_industry_comparison(
            data=datasets['sector_2025'],
            category_col='sector',
            value_cols=['adoption_rate', 'avg_roi'],
            title="Industry Adoption vs ROI: Strategic Positioning Matrix",
            benchmark_lines={
                "Market Average": 75,
                "ROI Threshold": 3.0,
                "Leadership Tier": 85
            },
            height=500
        )
    
    # ROI Analysis with Risk Assessment
    if datasets.get('sector_2025') is not None:
        st.markdown("### 💹 Investment Risk-Return Analysis")
        
        roi_chart = ROIChart()
        
        # Add risk score if not present (for demo)
        sector_data = datasets['sector_2025'].copy()
        if 'risk_score' not in sector_data.columns:
            # Generate realistic risk scores inversely correlated with adoption
            sector_data = sector_data.reset_index(drop=True)
            num_sectors = len(sector_data)
            
            # DEBUG: Print detailed information about the data
            st.write("🔍 DEBUG: Risk Score Calculation")
            st.write(f"• sector_data shape: {sector_data.shape}")
            st.write(f"• sector_data columns: {list(sector_data.columns)}")
            st.write(f"• num_sectors: {num_sectors}")
            st.write(f"• adoption_rate column type: {type(sector_data['adoption_rate'])}")
            st.write(f"• adoption_rate values: {sector_data['adoption_rate'].tolist()}")
            
            base_adjustments = np.array([5, -5, 10, 15, 0, -10, 8, -3])
            st.write(f"• base_adjustments: {base_adjustments}")
            st.write(f"• base_adjustments shape: {base_adjustments.shape}")
            
            risk_adjustments = np.resize(base_adjustments, num_sectors)
            st.write(f"• risk_adjustments after resize: {risk_adjustments}")
            st.write(f"• risk_adjustments shape: {risk_adjustments.shape}")
            
            # Additional debug info
            adoption_values = sector_data['adoption_rate'].values
            st.write(f"• adoption_values type: {type(adoption_values)}")
            st.write(f"• adoption_values shape: {adoption_values.shape}")
            st.write(f"• adoption_values: {adoption_values}")
            
            # Check for any NaN or invalid values
            st.write(f"• adoption_values has NaN: {np.isnan(adoption_values).any()}")
            st.write(f"• adoption_values has inf: {np.isinf(adoption_values).any()}")
            
            # Verify array compatibility
            st.write(f"• Can broadcast adoption_values and risk_adjustments: {np.can_cast(adoption_values.dtype, risk_adjustments.dtype)}")
            
            # Try the calculation with explicit error handling
            try:
                # Calculate risk score step by step
                base_risk = 100 - adoption_values
                st.write(f"• base_risk (100 - adoption_values): {base_risk}")
                
                final_risk = base_risk + risk_adjustments
                st.write(f"• final_risk (base_risk + risk_adjustments): {final_risk}")
                
                sector_data['risk_score'] = final_risk
                st.write("✅ Risk score calculation successful!")
                
            except Exception as e:
                st.error(f"❌ Error in risk score calculation: {e}")
                st.write(f"• Error type: {type(e)}")
                st.write(f"• Error details: {str(e)}")
                
                # Fallback calculation
                st.write("🔄 Using fallback calculation...")
                sector_data['risk_score'] = 100 - adoption_values
                st.write(f"• Fallback risk_score: {sector_data['risk_score'].tolist()}")
            
            st.stop()  # Stop execution to show debug info
        
        roi_chart.render_roi_analysis(
            data=sector_data,
            roi_col='avg_roi',
            risk_col='risk_score',
            size_col='adoption_rate',
            category_col='sector',
            title="Strategic Investment Quadrant Analysis",
            height=500
        )

# Enhanced navigation with smart filtering
def render_enhanced_navigation_and_filtering(datasets):
    """Render enhanced navigation with smart filtering capabilities"""
    
    st.sidebar.markdown("## 🎛️ Strategic Controls")
    
    # Smart Filter System
    smart_filter = SmartFilter()
    
    # Time-based filtering
    if datasets.get('historical_data') is not None:
        hist_data = datasets['historical_data']
        min_year = int(hist_data['year'].min())
        max_year = int(hist_data['year'].max())
        
        year_range = smart_filter.add_range_filter(
            key="year_filter",
            label="📅 Analysis Time Period",
            min_value=float(min_year),
            max_value=float(max_year),
            step=1.0,
            format_str="%d"
        )
    
    # Industry filtering
    if datasets.get('sector_2025') is not None:
        available_industries = datasets['sector_2025']['sector'].tolist()
        
        selected_industries = smart_filter.add_multiselect_filter(
            key="industry_filter",
            label="🏭 Industry Focus",
            options=available_industries,
            default=available_industries
        )
    
    # Performance filtering
    roi_range = smart_filter.add_range_filter(
        key="roi_filter", 
        label="💰 ROI Performance Range",
        min_value=1.0,
        max_value=5.0,
        step=0.1,
        format_str="%.1fx"
    )
    
    # Apply filters and return filtered data
    filter_configs = {
        "industry_filter": {"column": "sector", "type": "multiselect"},
        "roi_filter": {"column": "avg_roi", "type": "range"}
    }
    
    filtered_data = {}
    for dataset_name, dataset in datasets.items():
        if dataset is not None and dataset_name == 'sector_2025':
            filtered_data[dataset_name] = smart_filter.get_filtered_data(dataset, filter_configs)
        else:
            filtered_data[dataset_name] = dataset
    
    return filtered_data, smart_filter

# Enhanced action center with professional buttons
def render_enhanced_action_center(datasets, dynamic_metrics):
    """Render enhanced action center with professional interactions"""
    
    st.markdown("---")
    st.markdown("### 🎯 Strategic Action Center")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        def generate_executive_report():
            """Generate comprehensive executive report"""
            import time
            time.sleep(2)  # Simulate processing
            
            # Create report content
            report_content = f"""
AI STRATEGIC INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

EXECUTIVE SUMMARY:
• Market Adoption: {dynamic_metrics.get('market_adoption', '78%')}
• ROI Performance: {dynamic_metrics.get('avg_roi', '3.2x')} average
• Investment Climate: {dynamic_metrics.get('investment_value', '$252.3B')} global
• Strategic Window: Open for 12-18 months

RECOMMENDATIONS:
1. Accelerate pilot-to-production transition
2. Invest in AI talent development
3. Establish governance framework
4. Monitor competitive positioning

Risk Factors: Talent shortage, regulatory changes
Opportunities: Cost reduction, productivity gains
            """
            
            # Offer download
            st.download_button(
                label="📥 Download Executive Report",
                data=report_content,
                file_name=f"AI_Executive_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            
            return "Executive report generated successfully!"
        
        ActionButton.render(
            label="Generate Report",
            callback=generate_executive_report,
            button_type="primary",
            icon="📊",
            help_text="Create comprehensive executive summary report"
        )
    
    with col2:
        def export_dashboard_data():
            """Export filtered dashboard data"""
            import time
            time.sleep(1)
            
            # Combine all datasets for export
            combined_data = {}
            for name, data in datasets.items():
                if data is not None:
                    combined_data[name] = data.to_dict('records')
            
            import json
            export_json = json.dumps(combined_data, indent=2, default=str)
            
            st.download_button(
                label="📥 Download Data Export",
                data=export_json,
                file_name=f"AI_Dashboard_Data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
            return "Data exported successfully!"
        
        ActionButton.render(
            label="Export Data",
            callback=export_dashboard_data,
            button_type="secondary",
            icon="📤",
            help_text="Export all dashboard data in JSON format"
        )
    
    with col3:
        def schedule_review():
            """Schedule strategic review"""
            st.info("📅 Strategic review scheduling would integrate with your calendar system")
            return "Review scheduled successfully!"
        
        ActionButton.render(
            label="Schedule Review",
            callback=schedule_review,
            button_type="secondary",
            icon="📅",
            help_text="Schedule strategic AI review meeting"
        )
    
    with col4:
        ActionButton.render(
            label="Share Dashboard",
            callback=lambda: st.info("🔗 Share functionality would generate secure dashboard links"),
            button_type="secondary",
            icon="🔗",
            help_text="Share dashboard with stakeholders"
        )

# Enhanced progress tracking
def render_progress_tracking():
    """Render enhanced progress tracking section"""
    
    st.markdown("---")
    st.markdown("### 📈 Implementation Progress Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Strategic Objectives Progress")
        
        ProgressIndicator.render_linear(
            value=75,
            max_value=100,
            title="AI Strategy Development", 
            color="#2E86AB",
            height=25
        )
        
        ProgressIndicator.render_linear(
            value=45,
            max_value=100,
            title="Talent Acquisition",
            color="#F18F01",
            height=25
        )
        
        ProgressIndicator.render_linear(
            value=60,
            max_value=100,
            title="Technology Implementation",
            color="#6A994E",
            height=25
        )
    
    with col2:
        st.markdown("#### Competitive Position")
        
        ProgressIndicator.render_circular(
            value=68,
            max_value=100,
            title="Market Position",
            color="#2E86AB",
            size=120
        )

# Main integration function
def main_enhanced_dashboard():
    """Main function integrating all enhanced components"""
    
    # Setup theme
    current_theme = setup_professional_theme()
    
    # Load data with enhancement
    datasets = load_enhanced_data()
    
    # Get dynamic metrics (your existing function)
    dynamic_metrics = get_dynamic_metrics(
        datasets.get('historical_data'),
        datasets.get('ai_cost_reduction'), 
        datasets.get('investment_data'),
        datasets.get('sector_2025')
    )
    
    # Enhanced navigation and filtering
    filtered_datasets, smart_filter = render_enhanced_navigation_and_filtering(datasets)
    
    # Professional alert system
    AlertBox.render_alert(
        title="🚀 Dashboard Enhanced",
        message="Your AI Dashboard has been upgraded with advanced UI components for better strategic decision making.",
        alert_type="success",
        dismissible=True
    )
    
    # Main dashboard content
    render_enhanced_executive_dashboard(filtered_datasets, dynamic_metrics)
    
    # Action center
    render_enhanced_action_center(filtered_datasets, dynamic_metrics)
    
    # Progress tracking
    render_progress_tracking()
    
    # Footer with theme info
    st.markdown("---")
    st.markdown(f"*Dashboard theme: {current_theme.value.title()} | Last updated: {datetime.now().strftime('%I:%M %p')}*")

# Integration instructions
if __name__ == "__main__":
    st.title("🎨 UI Components Integration Example")
    st.markdown("""
    This example shows how to integrate the advanced UI components into your existing dashboard.
    
    **Integration Steps:**
    1. Copy the components folder to your project
    2. Replace sections of your app.py with the enhanced versions above
    3. Update imports to include the new components
    4. Test the enhanced functionality
    
    **Key Benefits:**
    - Professional executive-grade styling
    - Interactive filtering and controls
    - Enhanced data visualization
    - Responsive design
    - Theme management system
    """)
    
    # Run the enhanced dashboard demo
    main_enhanced_dashboard() 