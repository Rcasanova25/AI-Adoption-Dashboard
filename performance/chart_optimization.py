# performance/chart_optimization.py - Chart Rendering Performance System
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
import time
import json
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import functools

@dataclass
class ChartConfig:
    """Configuration for chart performance optimization"""
    max_points: int = 5000  # Maximum data points to render
    downsampling_method: str = "lttb"  # "lttb", "random", "every_nth"
    enable_webgl: bool = True  # Use WebGL for better performance
    optimize_layout: bool = True  # Optimize layout for performance
    lazy_loading: bool = True  # Enable lazy loading for large datasets
    cache_charts: bool = True  # Cache chart objects
    compression: bool = True  # Compress chart data

class DataDownsampler:
    """Intelligent data downsampling for chart performance"""
    
    @staticmethod
    def largest_triangle_three_buckets(data: pd.DataFrame, 
                                     x_col: str, 
                                     y_col: str, 
                                     target_points: int) -> pd.DataFrame:
        """
        LTTB (Largest Triangle Three Buckets) downsampling algorithm
        Preserves visual characteristics while reducing data points
        """
        if len(data) <= target_points:
            return data
        
        # Ensure data is sorted by x_col
        data_sorted = data.sort_values(x_col).reset_index(drop=True)
        
        # Convert datetime to numeric for calculations if needed
        if pd.api.types.is_datetime64_any_dtype(data_sorted[x_col]):
            x_values = pd.to_numeric(data_sorted[x_col].astype(np.int64))
        else:
            x_values = data_sorted[x_col].values
            
        y_values = data_sorted[y_col].values
        
        # Always keep first and last points
        bucket_size = (len(data_sorted) - 2) / (target_points - 2)
        
        sampled_indices = [0]  # Always include first point
        
        for i in range(1, target_points - 1):
            # Calculate bucket range
            bucket_start = int(i * bucket_size) + 1
            bucket_end = min(int((i + 1) * bucket_size) + 1, len(data_sorted) - 1)
            
            if bucket_start >= bucket_end:
                continue
            
            # Previous point
            prev_idx = sampled_indices[-1]
            prev_x, prev_y = x_values[prev_idx], y_values[prev_idx]
            
            # Next bucket average (for triangle calculation)
            next_bucket_start = bucket_end
            next_bucket_end = min(int((i + 2) * bucket_size) + 1, len(data_sorted))
            
            if next_bucket_end <= next_bucket_start:
                next_avg_x = x_values[-1]
                next_avg_y = y_values[-1]
            else:
                next_avg_x = np.mean(x_values[next_bucket_start:next_bucket_end])
                next_avg_y = np.mean(y_values[next_bucket_start:next_bucket_end])
            
            # Find point in current bucket that forms largest triangle
            max_area = 0
            max_idx = bucket_start
            
            for j in range(bucket_start, bucket_end):
                curr_x, curr_y = x_values[j], y_values[j]
                
                # Calculate triangle area
                area = abs(prev_x * (curr_y - next_avg_y) + 
                          curr_x * (next_avg_y - prev_y) + 
                          next_avg_x * (prev_y - curr_y)) / 2
                
                if area > max_area:
                    max_area = area
                    max_idx = j
            
            sampled_indices.append(max_idx)
        
        # Always include last point
        sampled_indices.append(len(data_sorted) - 1)
        
        return data_sorted.iloc[sampled_indices].reset_index(drop=True)
    
    @staticmethod
    def random_sampling(data: pd.DataFrame, target_points: int) -> pd.DataFrame:
        """Random sampling with guaranteed first and last points"""
        if len(data) <= target_points:
            return data
        
        # Always keep first and last
        middle_indices = np.random.choice(
            range(1, len(data) - 1), 
            size=target_points - 2, 
            replace=False
        )
        
        all_indices = np.concatenate([[0], sorted(middle_indices), [len(data) - 1]])
        return data.iloc[all_indices].reset_index(drop=True)
    
    @staticmethod
    def every_nth_sampling(data: pd.DataFrame, target_points: int) -> pd.DataFrame:
        """Every nth point sampling"""
        if len(data) <= target_points:
            return data
        
        step = len(data) // target_points
        indices = list(range(0, len(data), step))
        
        # Ensure we include the last point
        if indices[-1] != len(data) - 1:
            indices.append(len(data) - 1)
        
        # Take only the first target_points
        selected_indices = indices[:target_points]
        
        # If we still don't have enough points, add the last one
        if len(selected_indices) < target_points and len(data) - 1 not in selected_indices:
            selected_indices.append(len(data) - 1)
        
        return data.iloc[selected_indices].reset_index(drop=True)
    
    @classmethod
    def downsample(cls, 
                   data: pd.DataFrame, 
                   x_col: str, 
                   y_col: str, 
                   target_points: int, 
                   method: str = "lttb") -> pd.DataFrame:
        """Downsample data using specified method"""
        
        if method == "lttb":
            return cls.largest_triangle_three_buckets(data, x_col, y_col, target_points)
        elif method == "random":
            return cls.random_sampling(data, target_points)
        elif method == "every_nth":
            return cls.every_nth_sampling(data, target_points)
        else:
            raise ValueError(f"Unknown downsampling method: {method}")

class ChartOptimizer:
    """Optimize charts for performance while maintaining visual quality"""
    
    def __init__(self, config: ChartConfig = None):
        self.config = config or ChartConfig()
        self.chart_cache = {}
        self.performance_stats = {}
    
    def optimize_layout(self, fig: go.Figure) -> go.Figure:
        """Optimize chart layout for performance"""
        
        optimizations = {
            # Reduce animation time
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            
            # Optimize margins
            'margin': dict(l=50, r=30, t=50, b=50),
            
            # Disable hover for better performance with large datasets
            'hovermode': 'closest' if len(fig.data) > 0 and (fig.data[0].x is None or len(fig.data[0].x) < 1000) else False,
            
            # Optimize grid and axis
            'xaxis': dict(
                showgrid=True,
                gridwidth=1,
                zeroline=False,
                showline=True,
                ticks='outside',
                tickwidth=1,
                ticklen=5
            ),
            'yaxis': dict(
                showgrid=True,
                gridwidth=1,
                zeroline=False,
                showline=True,
                ticks='outside',
                tickwidth=1,
                ticklen=5
            ),
            
            # Performance optimizations
            'dragmode': 'pan',  # Faster than zoom
            'doubleClick': 'reset',
            
            # Reduce memory usage
            'uirevision': 'constant',  # Prevent unnecessary re-renders
        }
        
        fig.update_layout(**optimizations)
        return fig
    
    def optimize_traces(self, fig: go.Figure, data_size: int) -> go.Figure:
        """Optimize individual traces based on data size"""
        
        for trace in fig.data:
            if data_size > 1000:
                # For large datasets, reduce visual complexity
                if hasattr(trace, 'mode') and 'markers' in str(trace.mode):
                    # Reduce marker size and remove outlines for large datasets
                    trace.update(
                        marker=dict(
                            size=max(2, 8 - data_size // 1000),
                            line=dict(width=0) if data_size > 5000 else dict(width=1)
                        )
                    )
                
                # Simplify line rendering
                if hasattr(trace, 'line'):
                    trace.update(
                        line=dict(
                            width=max(1, 3 - data_size // 2000),
                            simplify=True
                        )
                    )
                
                # Disable individual hover for very large datasets
                if data_size > 10000:
                    trace.update(hoverinfo='skip')
        
        return fig
    
    def enable_webgl(self, fig: go.Figure) -> go.Figure:
        """Enable WebGL rendering for better performance"""
        if not self.config.enable_webgl:
            return fig
        
        # Convert appropriate traces to WebGL
        for i, trace in enumerate(fig.data):
            if isinstance(trace, go.Scatter) and len(trace.x or []) > 1000:
                # Convert to Scattergl for better performance
                fig.data = list(fig.data)
                fig.data[i] = go.Scattergl(
                    x=trace.x,
                    y=trace.y,
                    mode=trace.mode,
                    name=trace.name,
                    line=trace.line,
                    marker=trace.marker,
                    hovertemplate=trace.hovertemplate
                )
        
        return fig
    
    def create_optimized_chart(self, 
                             chart_func: callable, 
                             data: pd.DataFrame, 
                             chart_id: str,
                             **kwargs) -> go.Figure:
        """Create optimized chart with caching and performance monitoring"""
        
        start_time = time.time()
        
        # Check cache first
        cache_key = self._generate_cache_key(chart_id, data, kwargs)
        if self.config.cache_charts and cache_key in self.chart_cache:
            cached_fig, cached_time = self.chart_cache[cache_key]
            if time.time() - cached_time < 300:  # 5-minute cache
                return cached_fig
        
        # Downsample data if necessary
        original_size = len(data)
        if original_size > self.config.max_points:
            # Determine columns for downsampling
            x_col = kwargs.get('x_col', data.columns[0])
            y_col = kwargs.get('y_col', data.columns[1] if len(data.columns) > 1 else data.columns[0])
            
            data = DataDownsampler.downsample(
                data, x_col, y_col, 
                self.config.max_points, 
                self.config.downsampling_method
            )
            
            # Show downsampling info
            if original_size > self.config.max_points * 2:
                st.info(f"📊 Optimized chart: showing {len(data)} of {original_size} points for better performance")
        
        # Create chart
        fig = chart_func(data, **kwargs)
        
        # Apply optimizations
        if self.config.optimize_layout:
            fig = self.optimize_layout(fig)
            fig = self.optimize_traces(fig, len(data))
        
        if self.config.enable_webgl:
            fig = self.enable_webgl(fig)
        
        # Cache result
        if self.config.cache_charts:
            self.chart_cache[cache_key] = (fig, time.time())
        
        # Record performance
        execution_time = time.time() - start_time
        self.performance_stats[chart_id] = {
            'execution_time': execution_time,
            'original_points': original_size,
            'rendered_points': len(data),
            'optimization_ratio': len(data) / original_size if original_size > 0 else 1.0,
            'timestamp': datetime.now()
        }
        
        return fig
    
    def _generate_cache_key(self, chart_id: str, data: pd.DataFrame, kwargs: dict) -> str:
        """Generate cache key for chart"""
        data_hash = hash(str(data.values.tobytes()) + str(data.columns.tolist()))
        kwargs_hash = hash(str(sorted(kwargs.items())))
        return f"{chart_id}_{data_hash}_{kwargs_hash}"
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.performance_stats:
            return {}
        
        avg_time = np.mean([stats['execution_time'] for stats in self.performance_stats.values()])
        total_charts = len(self.performance_stats)
        
        return {
            'total_charts': total_charts,
            'average_render_time': avg_time,
            'cache_hits': len(self.chart_cache),
            'performance_breakdown': self.performance_stats
        }

class LazyChartLoader:
    """Lazy loading system for charts"""
    
    def __init__(self):
        self.loaded_charts = set()
        self.chart_queue = {}
    
    def register_chart(self, chart_id: str, chart_func: callable, **kwargs):
        """Register a chart for lazy loading"""
        self.chart_queue[chart_id] = {
            'func': chart_func,
            'kwargs': kwargs,
            'loaded': False
        }
    
    def load_chart_on_demand(self, chart_id: str) -> Optional[go.Figure]:
        """Load chart only when requested"""
        if chart_id not in self.chart_queue:
            return None
        
        chart_info = self.chart_queue[chart_id]
        
        if not chart_info['loaded']:
            # Show loading placeholder
            with st.spinner(f"Loading {chart_id}..."):
                fig = chart_info['func'](**chart_info['kwargs'])
                chart_info['fig'] = fig
                chart_info['loaded'] = True
                self.loaded_charts.add(chart_id)
        
        return chart_info.get('fig')
    
    def render_chart_with_lazy_loading(self, chart_id: str, title: str):
        """Render chart with lazy loading option"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(title)
        
        with col2:
            if chart_id not in self.loaded_charts:
                if st.button(f"Load {chart_id}", key=f"load_{chart_id}"):
                    fig = self.load_chart_on_demand(chart_id)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ Loaded")
                fig = self.chart_queue[chart_id].get('fig')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

# Optimized chart creation functions
class OptimizedCharts:
    """Collection of optimized chart creation functions"""
    
    def __init__(self, optimizer: ChartOptimizer = None):
        self.optimizer = optimizer or ChartOptimizer()
    
    def create_time_series(self, 
                          data: pd.DataFrame, 
                          x_col: str, 
                          y_cols: List[str],
                          title: str = "Time Series",
                          **kwargs) -> go.Figure:
        """Create optimized time series chart"""
        
        def _create_chart(data, **chart_kwargs):
            fig = go.Figure()
            
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            for i, y_col in enumerate(y_cols):
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    mode='lines+markers',
                    name=y_col.replace('_', ' ').title(),
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=4),
                    hovertemplate=f'<b>{y_col}</b><br>%{{x}}: %{{y}}<extra></extra>'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title="Value",
                height=500
            )
            
            return fig
        
        return self.optimizer.create_optimized_chart(
            _create_chart, data, f"timeseries_{title}", 
            x_col=x_col, y_cols=y_cols, **kwargs
        )
    
    def create_bar_chart(self,
                        data: pd.DataFrame,
                        x_col: str,
                        y_col: str,
                        title: str = "Bar Chart",
                        **kwargs) -> go.Figure:
        """Create optimized bar chart"""
        
        def _create_chart(data, **chart_kwargs):
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=data[x_col],
                y=data[y_col],
                marker=dict(
                    color=data[y_col],
                    colorscale='viridis',
                    showscale=True
                ),
                text=data[y_col],
                textposition='outside',
                hovertemplate=f'<b>%{{x}}</b><br>{y_col}: %{{y}}<extra></extra>'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title(),
                height=500
            )
            
            return fig
        
        return self.optimizer.create_optimized_chart(
            _create_chart, data, f"bar_{title}",
            x_col=x_col, y_col=y_col, **kwargs
        )
    
    def create_scatter_plot(self,
                           data: pd.DataFrame,
                           x_col: str,
                           y_col: str,
                           size_col: Optional[str] = None,
                           color_col: Optional[str] = None,
                           title: str = "Scatter Plot",
                           **kwargs) -> go.Figure:
        """Create optimized scatter plot"""
        
        def _create_chart(data, **chart_kwargs):
            fig = go.Figure()
            
            marker_config = dict(size=8, opacity=0.7)
            
            if size_col and size_col in data.columns:
                marker_config['size'] = data[size_col]
                marker_config['sizemode'] = 'area'
                marker_config['sizeref'] = 2. * max(data[size_col]) / (40.**2)
                marker_config['sizemin'] = 4
            
            if color_col and color_col in data.columns:
                marker_config['color'] = data[color_col]
                marker_config['colorscale'] = 'viridis'
                marker_config['showscale'] = True
            
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode='markers',
                marker=marker_config,
                text=data.index,
                hovertemplate=f'<b>Point %{{text}}</b><br>{x_col}: %{{x}}<br>{y_col}: %{{y}}<extra></extra>'
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title(),
                height=500
            )
            
            return fig
        
        return self.optimizer.create_optimized_chart(
            _create_chart, data, f"scatter_{title}",
            x_col=x_col, y_col=y_col, **kwargs
        )

# Demo and testing functions
def demo_chart_optimization():
    """Demonstrate chart optimization features"""
    
    st.title("📊 Chart Rendering Optimization Demo")
    
    # Configuration controls
    st.sidebar.markdown("### ⚙️ Chart Optimization Settings")
    
    max_points = st.sidebar.slider("Max Points to Render", 1000, 10000, 5000)
    downsampling_method = st.sidebar.selectbox(
        "Downsampling Method", 
        ["lttb", "random", "every_nth"]
    )
    enable_webgl = st.sidebar.checkbox("Enable WebGL", True)
    
    config = ChartConfig(
        max_points=max_points,
        downsampling_method=downsampling_method,
        enable_webgl=enable_webgl
    )
    
    optimizer = ChartOptimizer(config)
    charts = OptimizedCharts(optimizer)
    
    # Generate test data
    @st.cache_data
    def generate_large_dataset(size: int):
        dates = pd.date_range('2020-01-01', periods=size, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'value1': np.cumsum(np.random.randn(size)) + 100,
            'value2': np.cumsum(np.random.randn(size)) + 50,
            'category': np.random.choice(['A', 'B', 'C', 'D'], size),
            'size': np.random.randint(10, 100, size)
        })
        return data
    
    # Data size selector
    data_size = st.selectbox(
        "Select Dataset Size",
        [1000, 5000, 10000, 25000, 50000],
        index=2
    )
    
    st.info(f"📊 Generating dataset with {data_size:,} points")
    
    # Generate data
    test_data = generate_large_dataset(data_size)
    
    # Performance comparison
    st.markdown("### Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Standard Chart")
        start_time = time.time()
        
        # Create standard chart
        standard_fig = go.Figure()
        standard_fig.add_trace(go.Scatter(
            x=test_data['date'],
            y=test_data['value1'],
            mode='lines+markers',
            name='Standard'
        ))
        standard_fig.update_layout(title="Standard Chart", height=400)
        
        standard_time = time.time() - start_time
        st.plotly_chart(standard_fig, use_container_width=True)
        st.metric("Render Time", f"{standard_time:.3f}s")
        st.metric("Data Points", f"{len(test_data):,}")
    
    with col2:
        st.markdown("#### Optimized Chart")
        start_time = time.time()
        
        # Create optimized chart
        optimized_fig = charts.create_time_series(
            test_data, 'date', ['value1'], 
            title="Optimized Chart"
        )
        
        optimized_time = time.time() - start_time
        st.plotly_chart(optimized_fig, use_container_width=True)
        st.metric("Render Time", f"{optimized_time:.3f}s")
        
        # Show optimization stats
        perf_report = optimizer.get_performance_report()
        if perf_report:
            latest_stats = list(perf_report['performance_breakdown'].values())[-1]
            st.metric("Optimized Points", f"{latest_stats['rendered_points']:,}")
            
            improvement = ((standard_time - optimized_time) / standard_time) * 100
            st.metric("Performance Improvement", f"{improvement:.1f}%")
    
    # Downsampling comparison
    st.markdown("### Downsampling Method Comparison")
    
    if len(test_data) > 1000:
        methods = ["lttb", "random", "every_nth"]
        method_tabs = st.tabs([method.upper() for method in methods])
        
        for i, method in enumerate(methods):
            with method_tabs[i]:
                downsampled = DataDownsampler.downsample(
                    test_data, 'date', 'value1', 1000, method
                )
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=downsampled['date'],
                    y=downsampled['value1'],
                    mode='lines+markers',
                    name=f'{method.upper()} Sampled'
                ))
                fig.update_layout(title=f"{method.upper()} Downsampling", height=300)
                
                st.plotly_chart(fig, use_container_width=True)
                st.write(f"Reduced from {len(test_data):,} to {len(downsampled):,} points")
    
    # Lazy loading demo
    st.markdown("### Lazy Loading Demo")
    
    lazy_loader = LazyChartLoader()
    
    # Register charts for lazy loading
    lazy_loader.register_chart(
        "chart1", 
        lambda: charts.create_time_series(test_data, 'date', ['value1'], "Lazy Chart 1")
    )
    lazy_loader.register_chart(
        "chart2",
        lambda: charts.create_bar_chart(test_data.head(20), 'category', 'value1', "Lazy Chart 2")
    )
    
    # Render lazy charts
    lazy_loader.render_chart_with_lazy_loading("chart1", "Time Series (Lazy)")
    lazy_loader.render_chart_with_lazy_loading("chart2", "Bar Chart (Lazy)")
    
    # Performance report
    st.markdown("### Optimization Performance Report")
    perf_report = optimizer.get_performance_report()
    if perf_report:
        st.json(perf_report)

if __name__ == "__main__":
    demo_chart_optimization() 