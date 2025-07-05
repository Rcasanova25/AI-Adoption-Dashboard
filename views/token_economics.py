"""Token Economics view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the token economics view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        token_economics = data.get("token_economics")
        token_usage_patterns = data.get("token_usage_patterns")
        token_optimization = data.get("token_optimization")
        token_pricing_evolution = data.get("token_pricing_evolution")

        # Data presence checks
        missing = []
        if token_economics is None or token_economics.empty:
            missing.append('token_economics')
        if token_usage_patterns is None or token_usage_patterns.empty:
            missing.append('token_usage_patterns')
        if token_optimization is None or token_optimization.empty:
            missing.append('token_optimization')
        if token_pricing_evolution is None or token_pricing_evolution.empty:
            missing.append('token_pricing_evolution')
        if missing:
            st.error(f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support.")
            st.stop()
        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("🪙 **Token Economics: The Language and Currency of AI**")

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Cost Reduction",
                value="286x",
                delta="Since Nov 2022",
                help="From $20 to $0.07 per million tokens",
            )

        with col2:
            st.metric(
                label="Context Windows",
                value="Up to 1M",
                delta="Tokens",
                help="Gemini 1.5 Flash supports 1M token context",
            )

        with col3:
            st.metric(
                label="Processing Speed",
                value="200 tokens/sec",
                delta="Peak performance",
                help="Latest models process 200+ tokens per second",
            )

        with col4:
            st.metric(
                label="Revenue Impact",
                value="25x",
                delta="In 4 weeks",
                help="NVIDIA case study: 20x cost reduction = 25x revenue",
            )

        # Create comprehensive token economics visualization
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "What Are Tokens?",
                "Token Pricing",
                "Usage Patterns",
                "Optimization",
                "Economic Impact",
            ]
        )

        with tab1:
            _render_what_are_tokens(token_economics, a11y)

        with tab2:
            _render_token_pricing(token_economics, token_pricing_evolution, a11y)

        with tab3:
            _render_usage_patterns(token_usage_patterns, a11y)

        with tab4:
            _render_optimization(token_optimization, a11y)

        with tab5:
            _render_economic_impact()

    except Exception as e:
        st.error(f"Error rendering token economics view: {str(e)}")


def _render_what_are_tokens(token_economics: pd.DataFrame, a11y: AccessibilityManager) -> None:
    """Render the What Are Tokens tab."""
    # Educational content about tokens
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
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
        """
        )

    with col2:
        # Token examples visualization
        st.info(
            """
        **💡 Token Examples:**
        
        **Simple word**: "cat" = 1 token
        
        **Complex word**: "artificial" = 2 tokens
        - "artific" + "ial"
        
        **Sentence**: "Hello world!" = 3 tokens
        - "Hello" + "world" + "!"
        
        **Context matters**: "lie"
        - Resting = Token #123
        - Untruth = Token #456
        """
        )

    # Context window comparison
    st.subheader("Context Window Capabilities")

    context_data = token_economics[["model", "context_window"]].sort_values("context_window")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=context_data["model"],
            y=context_data["context_window"],
            text=[
                f"{x:,}" if x < 1000000 else f"{x/1000000:.1f}M"
                for x in context_data["context_window"]
            ],
            textposition="outside",
            marker_color=[
                "#FF6B6B" if x < 10000 else "#4ECDC4" if x < 100000 else "#45B7D1"
                for x in context_data["context_window"]
            ],
            hovertemplate="<b>%{x}</b><br>Context: %{y:,} tokens<br>Equivalent to: %{customdata}<extra></extra>",
            customdata=[
                "~3 pages",
                "~6 pages",
                "~12 pages",
                "~96 pages",
                "~150 pages",
                "~150 pages",
                "~750 pages",
            ],
        )
    )

    fig.update_layout(
        title="AI Model Context Windows: From Pages to Novels",
        xaxis_title="Model",
        yaxis_title="Context Window (tokens)",
        yaxis_type="log",
        height=400,
        xaxis_tickangle=45,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Model Context Windows: From Pages to Novels",
        description="Bar chart on logarithmic scale showing context window capabilities across AI models. Models range from 3-page equivalents to novel-length capabilities. Gemini 1.5 leads with 1M tokens (750 pages), while smaller models like GPT-3.5 handle 4K tokens (3 pages). Color coding shows progression from red (small context) to blue (large context).",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "**Key Insight:** Larger context windows enable processing entire books, codebases, or hours of video in a single prompt"
    )


def _render_token_pricing(
    token_economics: pd.DataFrame, token_pricing_evolution: pd.DataFrame, a11y: AccessibilityManager
) -> None:
    """Render the Token Pricing tab."""
    # Token pricing analysis
    st.subheader("Token Pricing Evolution & Model Comparison")

    # Price evolution over time
    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=token_pricing_evolution["date"],
            y=token_pricing_evolution["avg_price_input"],
            mode="lines+markers",
            name="Input Tokens",
            line=dict(width=3, color="#3498DB"),
            marker=dict(size=8),
            fill="tonexty",
            fillcolor="rgba(52, 152, 219, 0.1)",
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=token_pricing_evolution["date"],
            y=token_pricing_evolution["avg_price_output"],
            mode="lines+markers",
            name="Output Tokens",
            line=dict(width=3, color="#E74C3C"),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(231, 76, 60, 0.1)",
        )
    )

    # Add model availability on secondary axis
    fig1.add_trace(
        go.Scatter(
            x=token_pricing_evolution["date"],
            y=token_pricing_evolution["models_available"],
            mode="lines+markers",
            name="Models Available",
            line=dict(width=2, color="#2ECC71", dash="dash"),
            marker=dict(size=6),
            yaxis="y2",
        )
    )

    fig1.update_layout(
        title="Token Pricing Collapse: Competition Drives Costs Down",
        xaxis_title="Date",
        yaxis=dict(title="Price per Million Tokens ($)", type="log", side="left"),
        yaxis2=dict(title="Number of Models", side="right", overlaying="y"),
        height=450,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig1 = a11y.make_chart_accessible(
        fig1,
        title="Token Pricing Collapse: Competition Drives Costs Down",
        description="Dual-axis line chart showing token pricing evolution and model availability over time. Left axis shows pricing on logarithmic scale with input and output token costs both declining dramatically from $20+ to under $1 per million tokens. Right axis shows increasing number of available models from 1 to 7+, with dashed line indicating growing competition driving prices down.",
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Current model pricing comparison
    col1, col2 = st.columns(2)

    with col1:
        # Input vs Output pricing
        fig2 = go.Figure()

        fig2.add_trace(
            go.Bar(
                name="Input Cost",
                x=token_economics.sort_values("cost_per_million_input")["model"],
                y=token_economics.sort_values("cost_per_million_input")["cost_per_million_input"],
                marker_color="#3498DB",
                text=[
                    f"${x:.2f}"
                    for x in token_economics.sort_values("cost_per_million_input")[
                        "cost_per_million_input"
                    ]
                ],
                textposition="outside",
            )
        )

        fig2.add_trace(
            go.Bar(
                name="Output Cost",
                x=token_economics.sort_values("cost_per_million_input")["model"],
                y=token_economics.sort_values("cost_per_million_input")["cost_per_million_output"],
                marker_color="#E74C3C",
                text=[
                    f"${x:.2f}"
                    for x in token_economics.sort_values("cost_per_million_input")[
                        "cost_per_million_output"
                    ]
                ],
                textposition="outside",
            )
        )

        fig2.update_layout(
            title="Current Model Pricing (per Million Tokens)",
            yaxis_title="Cost ($)",
            barmode="group",
            height=350,
            xaxis_tickangle=45,
            yaxis_type="log",
        )

        fig2 = a11y.make_chart_accessible(
            fig2,
            title="Current Model Pricing (per Million Tokens)",
            description="Grouped bar chart on logarithmic scale comparing input and output token costs across AI models. Models sorted by input cost from lowest to highest. Gemini Flash is most affordable at under $0.10, while GPT-4 commands premium pricing at $15-30. Output tokens consistently cost 2-5x more than input tokens across all models.",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.write("**💰 Pricing Insights:**")
        st.write("• **Output typically costs more** than input (2-5x)")
        st.write("• **Gemini Flash**: Cheapest at $0.07/M tokens")
        st.write("• **GPT-4**: Premium pricing at $15-30/M tokens")
        st.write("• **286x reduction** in 2 years for GPT-3.5")

        st.info(
            """
        **Token Pricing Models:**
        - **Pay-per-use**: Charge by tokens consumed
        - **Token bundles**: Pre-purchase token packages
        - **Rate limits**: Max tokens/minute per user
        - **Tiered pricing**: Volume discounts
        """
        )


def _render_usage_patterns(token_usage_patterns: pd.DataFrame, a11y: AccessibilityManager) -> None:
    """Render the Usage Patterns tab."""
    # Usage patterns analysis
    st.subheader("Token Usage Patterns by Use Case")

    # Create scatter plot of usage patterns
    fig = px.scatter(
        token_usage_patterns,
        x="avg_input_tokens",
        y="avg_output_tokens",
        size="input_output_ratio",
        color="use_case",
        title="Token Usage Patterns: Input vs Output by Use Case",
        labels={
            "avg_input_tokens": "Average Input Tokens",
            "avg_output_tokens": "Average Output Tokens",
            "input_output_ratio": "Input/Output Ratio",
        },
        height=450,
        size_max=50,
    )

    # Add diagonal line for equal input/output
    fig.add_shape(
        type="line", x0=0, y0=0, x1=5000, y1=5000, line=dict(color="gray", width=2, dash="dash")
    )

    fig.add_annotation(
        x=3000, y=3500, text="Equal Input/Output", showarrow=False, font=dict(color="gray")
    )

    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")

    fig = a11y.make_chart_accessible(
        fig,
        title="Token Usage Patterns: Input vs Output by Use Case",
        description="Scatter plot on logarithmic scale showing token usage patterns across different AI use cases. X-axis shows average input tokens, Y-axis shows average output tokens, bubble size indicates input/output ratio. Gray diagonal line shows equal input/output ratio. Use cases vary from input-heavy (document analysis, code review) to output-heavy (content generation, creative writing).",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Usage pattern insights
    col1, col2 = st.columns(2)

    with col1:
        # Input-heavy use cases
        input_heavy = token_usage_patterns[
            token_usage_patterns["input_output_ratio"] > 1
        ].sort_values("input_output_ratio", ascending=False)

        st.write("**📥 Input-Heavy Use Cases:**")
        for _, row in input_heavy.iterrows():
            st.write(f"• **{row['use_case']}**: {row['input_output_ratio']:.1f}x more input")
            st.write(f"  - Input: {row['avg_input_tokens']:,} tokens")
            st.write(f"  - Output: {row['avg_output_tokens']:,} tokens")

    with col2:
        # Output-heavy use cases
        output_heavy = token_usage_patterns[
            token_usage_patterns["input_output_ratio"] < 1
        ].sort_values("input_output_ratio")

        st.write("**📤 Output-Heavy Use Cases:**")
        for _, row in output_heavy.iterrows():
            st.write(f"• **{row['use_case']}**: {1/row['input_output_ratio']:.1f}x more output")
            st.write(f"  - Input: {row['avg_input_tokens']:,} tokens")
            st.write(f"  - Output: {row['avg_output_tokens']:,} tokens")

    # Token metrics explanation
    st.info(
        """
    **⏱️ Key Performance Metrics:**
    - **Time to First Token (TTFT)**: Latency before AI starts responding
    - **Inter-Token Latency**: Speed of subsequent token generation
    - **Tokens Per Second**: Overall generation throughput
    - **Context Utilization**: % of available context window used
    """
    )


def _render_optimization(token_optimization: pd.DataFrame, a11y: AccessibilityManager) -> None:
    """Render the Optimization tab."""
    # Optimization strategies
    st.subheader("Token Optimization Strategies")

    # Strategy effectiveness matrix
    fig = px.scatter(
        token_optimization,
        x="implementation_complexity",
        y="cost_reduction",
        size="time_to_implement",
        color="strategy",
        title="Token Optimization: Cost Reduction vs Implementation Complexity",
        labels={
            "implementation_complexity": "Implementation Complexity (1-5)",
            "cost_reduction": "Cost Reduction Potential (%)",
            "time_to_implement": "Time to Implement (days)",
        },
        height=400,
        size_max=40,
    )

    # Add quadrant markers
    fig.add_hline(y=40, line_dash="dash", line_color="gray")
    fig.add_vline(x=3, line_dash="dash", line_color="gray")

    # Quadrant labels
    fig.add_annotation(
        x=1.5, y=60, text="Quick Wins", showarrow=False, font=dict(color="green", size=14)
    )
    fig.add_annotation(
        x=4, y=60, text="Major Projects", showarrow=False, font=dict(color="blue", size=14)
    )
    fig.add_annotation(
        x=1.5, y=20, text="Easy but Limited", showarrow=False, font=dict(color="orange", size=14)
    )
    fig.add_annotation(
        x=4, y=20, text="Complex & Limited", showarrow=False, font=dict(color="red", size=14)
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Token Optimization: Cost Reduction vs Implementation Complexity",
        description="Scatter plot showing optimization strategies across four quadrants based on implementation complexity (X-axis) and cost reduction potential (Y-axis). Bubble size indicates time to implement. Quick Wins quadrant (low complexity, high impact) includes prompt engineering and context caching. Major Projects quadrant shows model fine-tuning and advanced techniques requiring more effort but offering significant cost savings.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optimization recommendations
    col1, col2 = st.columns(2)

    with col1:
        st.write("**🚀 Quick Win Strategies:**")
        quick_wins = token_optimization[
            (token_optimization["implementation_complexity"] <= 2)
            & (token_optimization["cost_reduction"] >= 20)
        ]

        for _, strategy in quick_wins.iterrows():
            st.write(f"**{strategy['strategy']}**")
            st.write(f"• Cost reduction: {strategy['cost_reduction']}%")
            st.write(f"• Implementation: {strategy['time_to_implement']} days")
            st.write("")

    with col2:
        st.write("**🎯 High-Impact Strategies:**")
        high_impact = token_optimization.nlargest(3, "cost_reduction")

        for _, strategy in high_impact.iterrows():
            st.write(f"**{strategy['strategy']}**")
            st.write(f"• Cost reduction: {strategy['cost_reduction']}%")
            st.write(f"• Complexity: {strategy['implementation_complexity']}/5")
            st.write("")

    # Detailed optimization techniques
    with st.expander("📚 Detailed Optimization Techniques"):
        st.markdown(
            """
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
        """
        )


def _render_economic_impact() -> None:
    """Render the Economic Impact tab."""
    # Economic impact analysis
    st.subheader("Token Economics: From Cost to Value")

    # AI Factory concept
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
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
        """
        )

    with col2:
        # ROI calculator for tokens
        st.write("**🧮 Token ROI Calculator**")

        monthly_tokens = st.number_input(
            "Monthly tokens (millions)", min_value=1, max_value=1000, value=100
        )

        cost_per_million = st.slider(
            "Cost per million tokens ($)", min_value=0.1, max_value=20.0, value=1.0, step=0.1
        )

        revenue_per_request = st.number_input(
            "Revenue per request ($)", min_value=0.01, max_value=10.0, value=0.50, step=0.01
        )

        tokens_per_request = st.slider(
            "Avg tokens per request", min_value=100, max_value=5000, value=500
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
    st.success(
        """
    **📈 Real-World Impact - NVIDIA Case Study:**
    - **20x cost reduction** through optimization
    - **25x revenue increase** in 4 weeks
    - Demonstrates direct link between token efficiency and business value
    - Proves that token optimization directly drives bottom-line results
    """
    )

    # Future projections
    st.subheader("Future of Token Economics")

    future_trends = pd.DataFrame(
        {
            "trend": [
                "Cost per Token",
                "Context Windows",
                "Processing Speed",
                "Model Variety",
                "Use Cases",
            ],
            "current": ["$0.07-$30", "4K-1M", "50-200 tps", "95 models", "Hundreds"],
            "year_2027": ["$0.001-$1", "10M+", "1000+ tps", "500+ models", "Thousands"],
            "growth": [
                "100x reduction",
                "10x increase",
                "5x faster",
                "5x variety",
                "10x expansion",
            ],
        }
    )

    st.dataframe(future_trends, hide_index=True, use_container_width=True)

    st.info(
        """
    **🔮 Key Predictions:**
    - **Sub-penny pricing** becomes standard by 2027
    - **Context windows** expand to process entire databases
    - **Real-time processing** enables new use cases
    - **Specialized models** for every industry and task
    - **Token economics** becomes core business metric
    """
    )
