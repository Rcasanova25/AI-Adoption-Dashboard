"""
Token Economics view for AI Adoption Dashboard
Displays token pricing, usage patterns, and economic impact with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import logging

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_token_economics(
    data_year: str,
    token_economics: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display token economics analysis including pricing, usage patterns, and economic impact
    
    Args:
        data_year: Selected year (e.g., "2025")
        token_economics: DataFrame with token economics data
        dashboard_data: Full dashboard data dict for fallback and additional data
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'nvidia':
            return "**Source**: NVIDIA Corporation AI Infrastructure and Token Economics Case Studies, 2024-2025\n\n**Methodology**: Real-world deployment data from enterprise AI implementations, demonstrating cost optimization and revenue impact through token efficiency improvements."
        elif source_type == 'industry':
            return "**Source**: AI Index 2025 Report & Industry Analysis\n\n**Methodology**: Aggregated pricing data from major AI providers (OpenAI, Google, Anthropic, Meta) and enterprise deployment case studies."
        return "**Source**: AI Index 2025 Report"
    
    st.write("🪙 **Token Economics: The Language and Currency of AI**")
    
    # Validate token economics data
    validator = DataValidator()
    token_result = validator.validate_dataframe(
        token_economics,
        "Token Economics Data",
        required_columns=['model', 'cost_per_million_input', 'cost_per_million_output'],
        min_rows=1
    )
    
    if token_result.is_valid:
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Calculate cost reduction from historical data
            if len(token_economics) >= 2:
                oldest_cost = token_economics['cost_per_million_input'].max()
                newest_cost = token_economics['cost_per_million_input'].min()
                reduction = oldest_cost / newest_cost if newest_cost > 0 else 1
                st.metric(
                    label="Cost Reduction", 
                    value=f"{reduction:.0f}x", 
                    delta="Since Nov 2022",
                    help=f"From ${oldest_cost:.2f} to ${newest_cost:.2f} per million tokens"
                )
            else:
                st.metric(
                    label="Cost Reduction", 
                    value="286x", 
                    delta="Since Nov 2022",
                    help="From $20 to $0.07 per million tokens"
                )
        
        with col2:
            max_context = token_economics['context_window'].max() if 'context_window' in token_economics.columns else 1000000
            context_display = f"{max_context/1000000:.1f}M" if max_context >= 1000000 else f"{max_context:,}"
            st.metric(
                label="Context Windows", 
                value=f"Up to {context_display}", 
                delta="Tokens",
                help="Gemini 1.5 Flash supports 1M token context"
            )
        
        with col3:
            max_speed = token_economics['tokens_per_second'].max() if 'tokens_per_second' in token_economics.columns else 200
            st.metric(
                label="Processing Speed", 
                value=f"{max_speed} tokens/sec", 
                delta="Peak performance",
                help="Latest models process 200+ tokens per second"
            )
        
        with col4:
            st.metric(
                label="Revenue Impact", 
                value="25x", 
                delta="In 4 weeks",
                help="NVIDIA case study: 20x cost reduction = 25x revenue"
            )
        
        # Create comprehensive token economics visualization
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["What Are Tokens?", "Token Pricing", "Usage Patterns", "Optimization", "Economic Impact"])
        
        with tab1:
            # Educational content about tokens
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                ### Understanding AI Tokens
                
                **Tokens are the fundamental units of AI processing** - tiny pieces of data that AI models use to understand and generate information.
                
                #### How Tokenization Works:
                - **Text**: Words are split into smaller units (e.g., "darkness" → "dark" + "ness")
                - **Images**: Pixels mapped to discrete visual tokens
                - **Audio**: Sound waves converted to spectrograms or semantic tokens
                - **Video**: Frames processed as sequences of visual tokens
                
                #### Token Usage Across AI Lifecycle:
                1. **Training**: Models learn from billions/trillions of tokens
                2. **Inference**: User prompts converted to tokens, processed, then output as tokens
                3. **Reasoning**: Complex models generate "thinking tokens" for problem-solving
                """)
                
            with col2:
                # Token examples visualization
                st.info("""
                **💡 Token Examples:**
                
                **Simple word**: "cat" = 1 token
                
                **Complex word**: "artificial" = 2 tokens
                - "artific" + "ial"
                
                **Sentence**: "Hello world!" = 3 tokens
                - "Hello" + "world" + "!"
                
                **Context matters**: "lie"
                - Resting = Token #123
                - Untruth = Token #456
                """)
            
            # Context window comparison
            if 'context_window' in token_economics.columns:
                st.subheader("Context Window Capabilities")
                
                def plot_context_windows():
                    """Plot context window comparison chart"""
                    context_data = token_economics[['model', 'context_window']].sort_values('context_window')
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=context_data['model'],
                        y=context_data['context_window'],
                        text=[f'{x:,}' if x < 1000000 else f'{x/1000000:.1f}M' for x in context_data['context_window']],
                        textposition='outside',
                        marker_color=['#FF6B6B' if x < 10000 else '#4ECDC4' if x < 100000 else '#45B7D1' for x in context_data['context_window']],
                        hovertemplate='<b>%{x}</b><br>Context: %{y:,} tokens<br><extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title="AI Model Context Windows: From Pages to Novels",
                        xaxis_title="Model",
                        yaxis_title="Context Window (tokens)",
                        yaxis_type="log",
                        height=400,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Use safe plotting
                if safe_plot_check(
                    token_economics,
                    "Context Window Data",
                    required_columns=['model', 'context_window'],
                    plot_func=plot_context_windows
                ):
                    st.success("**Key Insight:** Larger context windows enable processing entire books, codebases, or hours of video in a single prompt")
            
            # Download button for token basics
            safe_download_button(
                token_economics,
                clean_filename(f"token_economics_overview_{data_year}.csv"),
                "📥 Download Token Data",
                key="download_token_basics",
                help_text="Download token economics overview data"
            )
        
        with tab2:
            # Token pricing analysis
            st.subheader("Token Pricing Evolution & Model Comparison")
            
            # Get pricing evolution data if available
            token_pricing_evolution = dashboard_data.get('token_pricing_evolution', pd.DataFrame()) if dashboard_data else pd.DataFrame()
            
            if not token_pricing_evolution.empty:
                pricing_result = validator.validate_dataframe(
                    token_pricing_evolution,
                    "Token Pricing Evolution",
                    required_columns=['date'],
                    min_rows=1
                )
                
                if pricing_result.is_valid:
                    def plot_pricing_evolution():
                        """Plot pricing evolution over time"""
                        fig1 = go.Figure()
                        
                        if 'avg_price_input' in token_pricing_evolution.columns:
                            fig1.add_trace(go.Scatter(
                                x=token_pricing_evolution['date'],
                                y=token_pricing_evolution['avg_price_input'],
                                mode='lines+markers',
                                name='Input Tokens',
                                line=dict(width=3, color='#3498DB'),
                                marker=dict(size=8),
                                fill='tonexty',
                                fillcolor='rgba(52, 152, 219, 0.1)'
                            ))
                        
                        if 'avg_price_output' in token_pricing_evolution.columns:
                            fig1.add_trace(go.Scatter(
                                x=token_pricing_evolution['date'],
                                y=token_pricing_evolution['avg_price_output'],
                                mode='lines+markers',
                                name='Output Tokens',
                                line=dict(width=3, color='#E74C3C'),
                                marker=dict(size=8),
                                fill='tozeroy',
                                fillcolor='rgba(231, 76, 60, 0.1)'
                            ))
                        
                        # Add model availability on secondary axis if available
                        if 'models_available' in token_pricing_evolution.columns:
                            fig1.add_trace(go.Scatter(
                                x=token_pricing_evolution['date'],
                                y=token_pricing_evolution['models_available'],
                                mode='lines+markers',
                                name='Models Available',
                                line=dict(width=2, color='#2ECC71', dash='dash'),
                                marker=dict(size=6),
                                yaxis='y2'
                            ))
                        
                        fig1.update_layout(
                            title="Token Pricing Collapse: Competition Drives Costs Down",
                            xaxis_title="Date",
                            yaxis=dict(title="Price per Million Tokens ($)", type="log", side="left"),
                            yaxis2=dict(title="Number of Models", side="right", overlaying="y"),
                            height=450,
                            hovermode='x unified',
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    safe_plot_check(
                        token_pricing_evolution,
                        "Token Pricing Evolution",
                        required_columns=['date'],
                        plot_func=plot_pricing_evolution
                    )
            
            # Current model pricing comparison
            col1, col2 = st.columns(2)
            
            with col1:
                def plot_current_pricing():
                    """Plot current model pricing comparison"""
                    fig2 = go.Figure()
                    
                    sorted_data = token_economics.sort_values('cost_per_million_input')
                    
                    fig2.add_trace(go.Bar(
                        name='Input Cost',
                        x=sorted_data['model'],
                        y=sorted_data['cost_per_million_input'],
                        marker_color='#3498DB',
                        text=[f'${x:.2f}' for x in sorted_data['cost_per_million_input']],
                        textposition='outside'
                    ))
                    
                    fig2.add_trace(go.Bar(
                        name='Output Cost',
                        x=sorted_data['model'],
                        y=sorted_data['cost_per_million_output'],
                        marker_color='#E74C3C',
                        text=[f'${x:.2f}' for x in sorted_data['cost_per_million_output']],
                        textposition='outside'
                    ))
                    
                    fig2.update_layout(
                        title="Current Model Pricing (per Million Tokens)",
                        yaxis_title="Cost ($)",
                        barmode='group',
                        height=350,
                        xaxis_tickangle=45,
                        yaxis_type="log"
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Use safe plotting
                safe_plot_check(
                    token_economics,
                    "Current Model Pricing",
                    required_columns=['model', 'cost_per_million_input', 'cost_per_million_output'],
                    plot_func=plot_current_pricing
                )
            
            with col2:
                st.write("**💰 Pricing Insights:**")
                
                try:
                    # Calculate pricing insights
                    avg_output_cost = token_economics['cost_per_million_output'].mean()
                    avg_input_cost = token_economics['cost_per_million_input'].mean()
                    output_premium = avg_output_cost / avg_input_cost if avg_input_cost > 0 else 1
                    
                    cheapest_model = token_economics.loc[token_economics['cost_per_million_input'].idxmin(), 'model']
                    cheapest_cost = token_economics['cost_per_million_input'].min()
                    
                    most_expensive_model = token_economics.loc[token_economics['cost_per_million_input'].idxmax(), 'model']
                    most_expensive_cost = token_economics['cost_per_million_input'].max()
                    
                    cost_reduction = most_expensive_cost / cheapest_cost if cheapest_cost > 0 else 1
                    
                    st.write(f"• **Output typically costs more** than input ({output_premium:.1f}x)")
                    st.write(f"• **{cheapest_model}**: Cheapest at ${cheapest_cost:.2f}/M tokens")
                    st.write(f"• **{most_expensive_model}**: Premium pricing at ${most_expensive_cost:.2f}/M tokens")
                    st.write(f"• **{cost_reduction:.0f}x reduction** across model range")
                    
                except Exception as e:
                    logger.error(f"Error calculating pricing insights: {e}")
                    st.write("• **Output typically costs more** than input (2-5x)")
                    st.write("• **Gemini Flash**: Cheapest at $0.07/M tokens")
                    st.write("• **GPT-4**: Premium pricing at $15-30/M tokens")
                    st.write("• **286x reduction** in 2 years for GPT-3.5")
                
                st.info("""
                **Token Pricing Models:**
                - **Pay-per-use**: Charge by tokens consumed
                - **Token bundles**: Pre-purchase token packages
                - **Rate limits**: Max tokens/minute per user
                - **Tiered pricing**: Volume discounts
                """)
                
                # Data source button
                if st.button("📊 View Pricing Sources", key="pricing_source"):
                    with st.expander("Data Source", expanded=True):
                        st.info(show_source_info('industry'))
        
        with tab3:
            # Usage patterns analysis
            st.subheader("Token Usage Patterns by Use Case")
            
            # Get usage patterns data if available
            token_usage_patterns = dashboard_data.get('token_usage_patterns', pd.DataFrame()) if dashboard_data else pd.DataFrame()
            
            if not token_usage_patterns.empty:
                usage_result = validator.validate_dataframe(
                    token_usage_patterns,
                    "Token Usage Patterns",
                    required_columns=['use_case'],
                    min_rows=1
                )
                
                if usage_result.is_valid and all(col in token_usage_patterns.columns for col in ['avg_input_tokens', 'avg_output_tokens']):
                    def plot_usage_patterns():
                        """Plot usage patterns scatter plot"""
                        fig = px.scatter(
                            token_usage_patterns,
                            x='avg_input_tokens',
                            y='avg_output_tokens',
                            size='input_output_ratio' if 'input_output_ratio' in token_usage_patterns.columns else None,
                            color='use_case',
                            title='Token Usage Patterns: Input vs Output by Use Case',
                            labels={
                                'avg_input_tokens': 'Average Input Tokens',
                                'avg_output_tokens': 'Average Output Tokens',
                                'input_output_ratio': 'Input/Output Ratio'
                            },
                            height=450,
                            size_max=50
                        )
                        
                        # Add diagonal line for equal input/output
                        max_val = max(token_usage_patterns['avg_input_tokens'].max(), 
                                     token_usage_patterns['avg_output_tokens'].max())
                        fig.add_shape(
                            type="line",
                            x0=0, y0=0,
                            x1=max_val, y1=max_val,
                            line=dict(color="gray", width=2, dash="dash")
                        )
                        
                        fig.add_annotation(
                            x=max_val*0.6, y=max_val*0.7,
                            text="Equal Input/Output",
                            showarrow=False,
                            font=dict(color="gray")
                        )
                        
                        fig.update_xaxes(type="log")
                        fig.update_yaxes(type="log")
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    safe_plot_check(
                        token_usage_patterns,
                        "Token Usage Patterns",
                        required_columns=['avg_input_tokens', 'avg_output_tokens'],
                        plot_func=plot_usage_patterns
                    )
                    
                    # Usage pattern insights
                    if 'input_output_ratio' in token_usage_patterns.columns:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Input-heavy use cases
                            input_heavy = token_usage_patterns[token_usage_patterns['input_output_ratio'] > 1].sort_values('input_output_ratio', ascending=False)
                            
                            st.write("**📥 Input-Heavy Use Cases:**")
                            for _, row in input_heavy.iterrows():
                                st.write(f"• **{row['use_case']}**: {row['input_output_ratio']:.1f}x more input")
                                st.write(f"  - Input: {row['avg_input_tokens']:,} tokens")
                                st.write(f"  - Output: {row['avg_output_tokens']:,} tokens")
                        
                        with col2:
                            # Output-heavy use cases
                            output_heavy = token_usage_patterns[token_usage_patterns['input_output_ratio'] < 1].sort_values('input_output_ratio')
                            
                            st.write("**📤 Output-Heavy Use Cases:**")
                            for _, row in output_heavy.iterrows():
                                st.write(f"• **{row['use_case']}**: {1/row['input_output_ratio']:.1f}x more output")
                                st.write(f"  - Input: {row['avg_input_tokens']:,} tokens")
                                st.write(f"  - Output: {row['avg_output_tokens']:,} tokens")
                
                # Download button for usage patterns
                safe_download_button(
                    token_usage_patterns,
                    clean_filename(f"token_usage_patterns_{data_year}.csv"),
                    "📥 Download Usage Data",
                    key="download_usage_patterns",
                    help_text="Download token usage patterns by use case"
                )
            
            # Token metrics explanation
            st.info("""
            **⏱️ Key Performance Metrics:**
            - **Time to First Token (TTFT)**: Latency before AI starts responding
            - **Inter-Token Latency**: Speed of subsequent token generation
            - **Tokens Per Second**: Overall generation throughput
            - **Context Utilization**: % of available context window used
            """)
        
        with tab4:
            # Optimization strategies
            st.subheader("Token Optimization Strategies")
            
            # Get optimization data if available
            token_optimization = dashboard_data.get('token_optimization', pd.DataFrame()) if dashboard_data else pd.DataFrame()
            
            if not token_optimization.empty:
                opt_result = validator.validate_dataframe(
                    token_optimization,
                    "Token Optimization",
                    required_columns=['strategy'],
                    min_rows=1
                )
                
                if opt_result.is_valid and all(col in token_optimization.columns for col in ['implementation_complexity', 'cost_reduction']):
                    def plot_optimization_matrix():
                        """Plot optimization strategy effectiveness matrix"""
                        fig = px.scatter(
                            token_optimization,
                            x='implementation_complexity',
                            y='cost_reduction',
                            size='time_to_implement' if 'time_to_implement' in token_optimization.columns else None,
                            color='strategy',
                            title='Token Optimization: Cost Reduction vs Implementation Complexity',
                            labels={
                                'implementation_complexity': 'Implementation Complexity (1-5)',
                                'cost_reduction': 'Cost Reduction Potential (%)',
                                'time_to_implement': 'Time to Implement (days)'
                            },
                            height=400,
                            size_max=40
                        )
                        
                        # Add quadrant markers
                        fig.add_hline(y=40, line_dash="dash", line_color="gray")
                        fig.add_vline(x=3, line_dash="dash", line_color="gray")
                        
                        # Quadrant labels
                        fig.add_annotation(x=1.5, y=60, text="Quick Wins", showarrow=False, font=dict(color="green", size=14))
                        fig.add_annotation(x=4, y=60, text="Major Projects", showarrow=False, font=dict(color="blue", size=14))
                        fig.add_annotation(x=1.5, y=20, text="Easy but Limited", showarrow=False, font=dict(color="orange", size=14))
                        fig.add_annotation(x=4, y=20, text="Complex & Limited", showarrow=False, font=dict(color="red", size=14))
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    safe_plot_check(
                        token_optimization,
                        "Token Optimization Strategies",
                        required_columns=['implementation_complexity', 'cost_reduction'],
                        plot_func=plot_optimization_matrix
                    )
                    
                    # Optimization recommendations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**🚀 Quick Win Strategies:**")
                        quick_wins = token_optimization[(token_optimization['implementation_complexity'] <= 2) & 
                                                       (token_optimization['cost_reduction'] >= 20)]
                        
                        for _, strategy in quick_wins.iterrows():
                            st.write(f"**{strategy['strategy']}**")
                            st.write(f"• Cost reduction: {strategy['cost_reduction']}%")
                            if 'time_to_implement' in strategy:
                                st.write(f"• Implementation: {strategy['time_to_implement']} days")
                            st.write("")
                    
                    with col2:
                        st.write("**🎯 High-Impact Strategies:**")
                        high_impact = token_optimization.nlargest(3, 'cost_reduction')
                        
                        for _, strategy in high_impact.iterrows():
                            st.write(f"**{strategy['strategy']}**")
                            st.write(f"• Cost reduction: {strategy['cost_reduction']}%")
                            st.write(f"• Complexity: {strategy['implementation_complexity']}/5")
                            st.write("")
                
                # Download button for optimization data
                safe_download_button(
                    token_optimization,
                    clean_filename(f"token_optimization_strategies_{data_year}.csv"),
                    "📥 Download Optimization Data",
                    key="download_optimization",
                    help_text="Download token optimization strategies and impact data"
                )
            
            # Detailed optimization techniques
            with st.expander("📚 Detailed Optimization Techniques"):
                st.markdown("""
                **1. Prompt Engineering (30% reduction)**
                - Use concise, clear prompts
                - Avoid redundant context
                - Structure prompts efficiently
                
                **2. Context Caching (45% reduction)**
                - Reuse common context across requests
                - Implement conversation memory
                - Cache frequently used data
                
                **3. Batch Processing (60% reduction)**
                - Group similar requests
                - Process multiple inputs simultaneously
                - Optimize for throughput over latency
                
                **4. Model Selection (70% reduction)**
                - Choose right-sized models for tasks
                - Use specialized models when appropriate
                - Balance quality vs cost
                
                **5. Response Streaming (15% reduction)**
                - Stream tokens as generated
                - Reduce perceived latency
                - Enable early processing
                
                **6. Token Pruning (25% reduction)**
                - Remove unnecessary tokens
                - Compress prompts intelligently
                - Optimize response length
                """)
        
        with tab5:
            # Economic impact analysis
            st.subheader("Token Economics: From Cost to Value")
            
            # AI Factory concept
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                ### The AI Factory Model
                
                **AI Factories** are a new class of data centers designed to process tokens at scale, 
                converting the "language of AI" into the "currency of AI" - intelligence.
                
                #### Value Creation Process:
                1. **Input**: Raw data converted to tokens
                2. **Processing**: High-speed token computation
                3. **Output**: Intelligence as a monetizable asset
                4. **Scale**: Efficiency increases with volume
                
                #### Economic Principles:
                - **Token velocity**: Faster processing = more value
                - **Cost efficiency**: Lower cost/token = higher margins
                - **Quality output**: Better tokens = premium pricing
                - **Scale economics**: Volume drives profitability
                """)
            
            with col2:
                # ROI calculator for tokens
                st.write("**🧮 Token ROI Calculator**")
                
                monthly_tokens = st.number_input(
                    "Monthly tokens (millions)",
                    min_value=1,
                    max_value=1000,
                    value=100
                )
                
                cost_per_million = st.slider(
                    "Cost per million tokens ($)",
                    min_value=0.1,
                    max_value=20.0,
                    value=1.0,
                    step=0.1
                )
                
                revenue_per_request = st.number_input(
                    "Revenue per request ($)",
                    min_value=0.01,
                    max_value=10.0,
                    value=0.50,
                    step=0.01
                )
                
                tokens_per_request = st.slider(
                    "Avg tokens per request",
                    min_value=100,
                    max_value=5000,
                    value=500
                )
                
                # Calculate economics
                monthly_cost = monthly_tokens * cost_per_million
                requests = (monthly_tokens * 1_000_000) / tokens_per_request
                monthly_revenue = requests * revenue_per_request
                profit = monthly_revenue - monthly_cost
                margin = (profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
                
                st.metric("Monthly Profit", f"${profit:,.0f}", f"{margin:.1f}% margin")
                st.metric("ROI", f"{(monthly_revenue/monthly_cost):.1f}x", "Revenue/Cost ratio")
            
            # Case study
            st.success("""
            **📈 Real-World Impact - NVIDIA Case Study:**
            - **20x cost reduction** through optimization
            - **25x revenue increase** in 4 weeks
            - Demonstrates direct link between token efficiency and business value
            - Proves that token optimization directly drives bottom-line results
            """)
            
            # Data source for case study
            if st.button("📊 View Case Study Source", key="nvidia_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('nvidia'))
            
            # Future projections
            st.subheader("Future of Token Economics")
            
            future_trends = pd.DataFrame({
                'trend': ['Cost per Token', 'Context Windows', 'Processing Speed', 
                         'Model Variety', 'Use Cases'],
                'current': ['$0.07-$30', '4K-1M', '50-200 tps', '95 models', 'Hundreds'],
                'year_2027': ['$0.001-$1', '10M+', '1000+ tps', '500+ models', 'Thousands'],
                'growth': ['100x reduction', '10x increase', '5x faster', '5x variety', '10x expansion']
            })
            
            st.dataframe(future_trends, hide_index=True, use_container_width=True)
            
            st.info("""
            **🔮 Key Predictions:**
            - **Sub-penny pricing** becomes standard by 2027
            - **Context windows** expand to process entire databases
            - **Real-time processing** enables new use cases
            - **Specialized models** for every industry and task
            - **Token economics** becomes core business metric
            """)
            
            # Download button for future trends
            safe_download_button(
                future_trends,
                clean_filename(f"token_economics_future_trends_{data_year}.csv"),
                "📥 Download Future Trends",
                key="download_future_trends",
                help_text="Download token economics future trend projections"
            )
    
    else:
        st.warning("Token economics data not available for analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_token_economics"):
                    st.cache_data.clear()
                    st.rerun()