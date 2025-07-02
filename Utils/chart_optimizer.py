"""
Chart Performance Optimization Utilities
Implements optimized chart creation for large datasets with performance monitoring
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class ChartOptimizer:
    """
    Performance-optimized chart creation utilities
    """
    
    # Performance thresholds
    MAX_POINTS_SCATTER = 1000
    MAX_POINTS_LINE = 2000
    MAX_CATEGORIES_BAR = 50
    
    @staticmethod
    def create_optimized_scatter(
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: str = "Scatter Plot",
        max_points: int = None
    ) -> go.Figure:
        """
        Create performance-optimized scatter plot
        
        Args:
            df: DataFrame with data
            x: X-axis column name
            y: Y-axis column name
            color: Color column name
            size: Size column name
            hover_data: Additional columns for hover
            title: Chart title
            max_points: Maximum points to display
            
        Returns:
            Optimized Plotly figure
        """
        max_points = max_points or ChartOptimizer.MAX_POINTS_SCATTER
        
        # Sample data if too large
        df_plot = ChartOptimizer._sample_dataframe(df, max_points)
        
        # Create figure with WebGL for performance
        fig = px.scatter(
            df_plot,
            x=x,
            y=y,
            color=color,
            size=size,
            hover_data=hover_data,
            title=title,
            render_mode='webgl'  # Hardware acceleration
        )
        
        # Optimize layout
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
            hovermode='closest',
            # Performance optimizations
            uirevision='constant'  # Preserve UI state
        )
        
        # Optimize traces
        fig.update_traces(
            marker=dict(
                line=dict(width=0),  # Remove marker borders for performance
                opacity=0.7
            )
        )
        
        return fig
    
    @staticmethod
    def create_optimized_line(
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: str = "Line Chart",
        max_points: int = None
    ) -> go.Figure:
        """
        Create performance-optimized line chart
        
        Args:
            df: DataFrame with data
            x: X-axis column name
            y: Y-axis column name
            color: Color column name for multiple lines
            title: Chart title
            max_points: Maximum points per line
            
        Returns:
            Optimized Plotly figure
        """
        max_points = max_points or ChartOptimizer.MAX_POINTS_LINE
        
        # Sample data if too large
        df_plot = ChartOptimizer._sample_dataframe(df, max_points, preserve_order=True)
        
        # Create figure
        fig = px.line(
            df_plot,
            x=x,
            y=y,
            color=color,
            title=title,
            render_mode='webgl'
        )
        
        # Optimize layout
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
            hovermode='x unified'
        )
        
        # Optimize traces for performance
        fig.update_traces(
            line=dict(width=2),
            mode='lines',
            connectgaps=False  # Better performance
        )
        
        return fig
    
    @staticmethod
    def create_optimized_bar(
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: str = "Bar Chart",
        max_categories: int = None
    ) -> go.Figure:
        """
        Create performance-optimized bar chart
        
        Args:
            df: DataFrame with data
            x: X-axis column name (categories)
            y: Y-axis column name (values)
            color: Color column name
            title: Chart title
            max_categories: Maximum categories to display
            
        Returns:
            Optimized Plotly figure
        """
        max_categories = max_categories or ChartOptimizer.MAX_CATEGORIES_BAR
        
        # Limit categories if too many
        if df[x].nunique() > max_categories:
            # Keep top N categories by sum of y values
            top_categories = df.groupby(x)[y].sum().nlargest(max_categories).index
            df_plot = df[df[x].isin(top_categories)].copy()
            logger.warning(f"Showing top {max_categories} categories out of {df[x].nunique()}")
        else:
            df_plot = df.copy()
        
        # Create figure
        fig = px.bar(
            df_plot,
            x=x,
            y=y,
            color=color,
            title=title
        )
        
        # Optimize layout
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
            xaxis_tickangle=-45 if df_plot[x].nunique() > 10 else 0
        )
        
        # Add text labels for better readability
        if len(df_plot) <= 20:  # Only for small datasets
            fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        return fig
    
    @staticmethod
    def create_optimized_heatmap(
        df: pd.DataFrame,
        x: str,
        y: str,
        z: str,
        title: str = "Heatmap",
        max_cells: int = 10000
    ) -> go.Figure:
        """
        Create performance-optimized heatmap
        
        Args:
            df: DataFrame with data
            x: X-axis column name
            y: Y-axis column name
            z: Values column name
            title: Chart title
            max_cells: Maximum cells in heatmap
            
        Returns:
            Optimized Plotly figure
        """
        # Create pivot table
        pivot_df = df.pivot_table(values=z, index=y, columns=x, aggfunc='mean')
        
        # Limit size if too large
        total_cells = pivot_df.shape[0] * pivot_df.shape[1]
        if total_cells > max_cells:
            # Sample rows and columns
            max_rows = int(np.sqrt(max_cells))
            max_cols = max_cells // max_rows
            
            if len(pivot_df) > max_rows:
                pivot_df = pivot_df.sample(n=max_rows, random_state=42)
            if len(pivot_df.columns) > max_cols:
                pivot_df = pivot_df.sample(n=max_cols, axis=1, random_state=42)
            
            logger.warning(f"Heatmap reduced to {pivot_df.shape} to improve performance")
        
        # Create heatmap
        fig = px.imshow(
            pivot_df,
            title=title,
            aspect='auto',
            color_continuous_scale='Viridis'
        )
        
        # Optimize layout
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig
    
    @staticmethod
    def _sample_dataframe(
        df: pd.DataFrame,
        max_points: int,
        preserve_order: bool = False,
        random_state: int = 42
    ) -> pd.DataFrame:
        """
        Sample DataFrame to reduce size for performance
        
        Args:
            df: DataFrame to sample
            max_points: Maximum points to keep
            preserve_order: Whether to preserve order (for time series)
            random_state: Random state for reproducibility
            
        Returns:
            Sampled DataFrame
        """
        if len(df) <= max_points:
            return df
        
        if preserve_order:
            # For time series, sample evenly across the range
            step = len(df) // max_points
            sampled_df = df.iloc[::step].copy()
            # Ensure we include the last point
            if sampled_df.index[-1] != df.index[-1]:
                sampled_df = pd.concat([sampled_df, df.iloc[[-1]]])
        else:
            # Random sampling
            sampled_df = df.sample(n=max_points, random_state=random_state)
        
        logger.info(f"Sampled {len(df)} points down to {len(sampled_df)} for performance")
        return sampled_df


@contextmanager
def performance_monitor(operation_name: str, warn_threshold: float = 1.0):
    """
    Monitor chart creation performance
    
    Args:
        operation_name: Name of the operation being monitored
        warn_threshold: Threshold in seconds to trigger warning
        
    Yields:
        Performance monitoring context
    """
    start_time = time.time()
    start_memory = _get_memory_usage()
    
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = _get_memory_usage()
        
        duration = end_time - start_time
        memory_diff = end_memory - start_memory if end_memory and start_memory else 0
        
        if duration > warn_threshold:
            logger.warning(f"Slow {operation_name}: {duration:.2f}s (memory: +{memory_diff:.1f}MB)")
        else:
            logger.info(f"Completed {operation_name}: {duration:.2f}s (memory: +{memory_diff:.1f}MB)")


def _get_memory_usage() -> Optional[float]:
    """Get current memory usage in MB"""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        return None


def handle_missing_data_for_charts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing data specifically for visualization
    
    Args:
        df: DataFrame with potential missing data
        
    Returns:
        DataFrame ready for visualization
    """
    df_clean = df.copy()
    
    # Drop rows where all key metrics are missing
    key_metrics = ['adoption_rate', 'genai_adoption', 'roi_multiplier', 'investment_amount']
    available_metrics = [col for col in key_metrics if col in df_clean.columns]
    
    if available_metrics:
        # Drop rows where all available metrics are null
        df_clean = df_clean.dropna(subset=available_metrics, how='all')
    
    # For time series data, interpolate missing values
    if 'year' in df_clean.columns:
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col != 'year':
                df_clean[col] = df_clean.groupby('sector')[col].transform(
                    lambda x: x.interpolate(method='linear')
                ) if 'sector' in df_clean.columns else df_clean[col].interpolate(method='linear')
    
    # Add data quality indicators for visualization
    df_clean['data_quality_score'] = (
        df_clean[available_metrics].notna().sum(axis=1) / len(available_metrics) * 100
    ).round(1) if available_metrics else 100
    
    return df_clean


def create_responsive_layout(fig: go.Figure) -> go.Figure:
    """
    Apply responsive layout settings to figure
    
    Args:
        fig: Plotly figure to make responsive
        
    Returns:
        Figure with responsive layout
    """
    fig.update_layout(
        autosize=True,
        margin=dict(l=40, r=40, t=60, b=40, pad=4),
        font=dict(size=12),
        title=dict(
            x=0.5,  # Center title
            xanchor='center',
            font=dict(size=16)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)"
        ),
        # Responsive design
        template="plotly_white",
        # Performance settings
        uirevision='constant'
    )
    
    return fig


# Pre-configured chart templates for common use cases
CHART_TEMPLATES = {
    'adoption_over_time': {
        'type': 'line',
        'config': {
            'x': 'year',
            'y': 'adoption_rate',
            'color': 'sector',
            'title': 'AI Adoption Over Time'
        }
    },
    'sector_comparison': {
        'type': 'bar',
        'config': {
            'x': 'sector',
            'y': 'adoption_rate',
            'title': 'AI Adoption by Sector'
        }
    },
    'roi_vs_adoption': {
        'type': 'scatter',
        'config': {
            'x': 'adoption_rate',
            'y': 'roi_multiplier',
            'color': 'company_size',
            'size': 'investment_amount',
            'title': 'ROI vs Adoption Rate'
        }
    }
}


def create_chart_from_template(
    df: pd.DataFrame,
    template_name: str,
    custom_config: Dict[str, Any] = None
) -> go.Figure:
    """
    Create chart from predefined template
    
    Args:
        df: DataFrame with data
        template_name: Name of the template to use
        custom_config: Custom configuration to override template
        
    Returns:
        Optimized Plotly figure
    """
    if template_name not in CHART_TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found")
    
    template = CHART_TEMPLATES[template_name].copy()
    config = template['config']
    
    # Apply custom configuration
    if custom_config:
        config.update(custom_config)
    
    # Create chart based on type
    chart_type = template['type']
    
    with performance_monitor(f"chart_creation_{template_name}"):
        if chart_type == 'scatter':
            fig = ChartOptimizer.create_optimized_scatter(df, **config)
        elif chart_type == 'line':
            fig = ChartOptimizer.create_optimized_line(df, **config)
        elif chart_type == 'bar':
            fig = ChartOptimizer.create_optimized_bar(df, **config)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    # Apply responsive layout
    fig = create_responsive_layout(fig)
    
    return fig