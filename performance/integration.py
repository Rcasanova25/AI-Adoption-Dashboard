# performance/integration.py - Complete Performance Integration System
import streamlit as st
import pandas as pd
import numpy as np
import time
import asyncio
import threading
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
import json
import hashlib

# Import our performance modules
from .caching import AdvancedCache, smart_cache, DataPipeline
from .chart_optimization import ChartOptimizer, OptimizedCharts, ChartConfig
from .memory_management import MemoryMonitor, DataFrameOptimizer, memory_profiler

@dataclass
class PerformanceConfig:
    """Master configuration for all performance optimizations"""
    
    # Caching settings
    cache_ttl: int = 3600
    cache_max_entries: int = 1000
    persist_cache: bool = True
    
    # Chart optimization
    max_chart_points: int = 5000
    enable_webgl: bool = True
    chart_downsampling: str = "lttb"
    
    # Memory management
    max_memory_mb: int = 2048
    cleanup_threshold: float = 0.8
    auto_gc_frequency: int = 10
    
    # Database optimization
    connection_pool_size: int = 5
    query_timeout: int = 30
    enable_query_cache: bool = True
    
    # General performance
    enable_async_loading: bool = True
    show_performance_metrics: bool = True
    profile_slow_operations: bool = True

class DatabaseOptimizer:
    """Database query optimization and connection pooling"""
    
    def __init__(self, config: PerformanceConfig):
        self.config = config
        self.connection_pool = []
        self.query_cache = {}
        self.query_stats = {}
        
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection from pool"""
        if self.connection_pool:
            return self.connection_pool.pop()
        else:
            # Create new connection with optimizations
            conn = sqlite3.connect(':memory:', check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
            conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes
            conn.execute("PRAGMA cache_size=10000")   # Larger cache
            conn.execute("PRAGMA temp_store=memory")   # Memory temp tables
            return conn
    
    def return_connection(self, conn: sqlite3.Connection):
        """Return connection to pool"""
        if len(self.connection_pool) < self.config.connection_pool_size:
            self.connection_pool.append(conn)
        else:
            conn.close()
    
    @smart_cache(ttl=1800)  # 30-minute cache for queries
    def execute_optimized_query(self, 
                               query: str, 
                               params: tuple = None,
                               query_name: str = None) -> pd.DataFrame:
        """Execute optimized database query with caching"""
        
        start_time = time.time()
        query_hash = hashlib.md5(f"{query}{params}".encode()).hexdigest()
        
        # Check query cache
        if self.config.enable_query_cache and query_hash in self.query_cache:
            cached_result, cache_time = self.query_cache[query_hash]
            if time.time() - cache_time < 1800:  # 30-minute cache
                return cached_result
        
        # Execute query
        conn = self.get_connection()
        try:
            if params:
                result = pd.read_sql_query(query, conn, params=params)
            else:
                result = pd.read_sql_query(query, conn)
            
            # Optimize DataFrame
            if len(result) > 1000:
                result, _ = DataFrameOptimizer.optimize_dtypes(result)
            
            # Cache result
            if self.config.enable_query_cache:
                self.query_cache[query_hash] = (result, time.time())
            
            # Record stats
            execution_time = time.time() - start_time
            self.query_stats[query_name or query_hash] = {
                'execution_time': execution_time,
                'rows_returned': len(result),
                'timestamp': datetime.now()
            }
            
            return result
            
        finally:
            self.return_connection(conn)
    
    def create_sample_database(self):
        """Create sample database with AI adoption data"""
        conn = self.get_connection()
        
        try:
            # Create tables
            conn.execute("""
            CREATE TABLE IF NOT EXISTS ai_adoption (
                id INTEGER PRIMARY KEY,
                year INTEGER,
                country TEXT,
                industry TEXT,
                adoption_rate REAL,
                investment_millions REAL,
                roi_multiple REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            conn.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY,
                date DATE,
                metric_name TEXT,
                metric_value REAL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_adoption_year ON ai_adoption(year)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_adoption_industry ON ai_adoption(industry)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_market_date ON market_data(date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_market_metric ON market_data(metric_name)")
            
            # Insert sample data
            self._insert_sample_data(conn)
            
            conn.commit()
            
        finally:
            self.return_connection(conn)
    
    def _insert_sample_data(self, conn: sqlite3.Connection):
        """Insert sample AI adoption data"""
        
        # Sample AI adoption data
        industries = ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 'Retail']
        countries = ['USA', 'China', 'Germany', 'UK', 'Japan', 'Canada', 'France']
        
        adoption_data = []
        for year in range(2018, 2026):
            for industry in industries:
                for country in countries:
                    # Generate realistic data
                    base_adoption = {
                        'Technology': 90, 'Financial Services': 75, 'Healthcare': 65,
                        'Manufacturing': 55, 'Retail': 60
                    }[industry]
                    
                    country_modifier = {
                        'USA': 1.1, 'China': 1.05, 'Germany': 0.95, 'UK': 1.0,
                        'Japan': 0.9, 'Canada': 0.95, 'France': 0.9
                    }[country]
                    
                    year_factor = 1 + (year - 2018) * 0.15  # 15% growth per year
                    
                    adoption_rate = min(95, base_adoption * country_modifier * year_factor + np.random.normal(0, 5))
                    investment = adoption_rate * 10 + np.random.normal(0, 20)
                    roi = 1.5 + (adoption_rate - 50) * 0.03 + np.random.normal(0, 0.3)
                    
                    adoption_data.append((year, country, industry, adoption_rate, investment, roi))
        
        conn.executemany("""
        INSERT INTO ai_adoption (year, country, industry, adoption_rate, investment_millions, roi_multiple)
        VALUES (?, ?, ?, ?, ?, ?)
        """, adoption_data)
        
        # Sample market data
        market_metrics = ['ai_investment_total', 'ai_patents', 'ai_startups', 'ai_jobs']
        market_data = []
        
        for i in range(365 * 3):  # 3 years of daily data
            date = datetime(2023, 1, 1) + timedelta(days=i)
            
            for metric in market_metrics:
                base_values = {
                    'ai_investment_total': 250000,
                    'ai_patents': 15000,
                    'ai_startups': 8000,
                    'ai_jobs': 120000
                }
                
                trend_factor = 1 + i * 0.001  # Gradual growth
                seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 365)  # Seasonal variation
                noise = np.random.normal(1, 0.05)
                
                value = base_values[metric] * trend_factor * seasonal_factor * noise
                
                market_data.append((date.strftime('%Y-%m-%d'), metric, value, 'market'))
        
        conn.executemany("""
        INSERT INTO market_data (date, metric_name, metric_value, category)
        VALUES (?, ?, ?, ?)
        """, market_data)

class PerformanceIntegrator:
    """Integrate all performance optimizations into a unified system"""
    
    def __init__(self, config: PerformanceConfig = None):
        self.config = config or PerformanceConfig()
        
        # Initialize all performance components
        self.cache = AdvancedCache()
        self.memory_monitor = MemoryMonitor()
        self.chart_optimizer = ChartOptimizer(ChartConfig(
            max_points=self.config.max_chart_points,
            enable_webgl=self.config.enable_webgl,
            downsampling_method=self.config.chart_downsampling
        ))
        self.db_optimizer = DatabaseOptimizer(self.config)
        self.charts = OptimizedCharts(self.chart_optimizer)
        
        # Performance tracking
        self.operation_timings = {}
        self.performance_log = []
        
        # Initialize database
        self.db_optimizer.create_sample_database()
    
    @memory_profiler("dashboard_render")
    def render_optimized_dashboard(self, filters: Dict[str, Any] = None):
        """Render complete optimized dashboard"""
        
        # Show performance controls in sidebar
        self._render_performance_controls()
        
        # Load data with optimization
        with st.spinner("Loading optimized data..."):
            datasets = self._load_optimized_datasets(filters)
        
        # Render dashboard sections
        self._render_kpi_section(datasets)
        self._render_chart_section(datasets)
        self._render_insights_section(datasets)
        
        # Show performance metrics if enabled
        if self.config.show_performance_metrics:
            self._render_performance_metrics()
    
    def _render_performance_controls(self):
        """Render performance optimization controls"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ⚡ Performance Controls")
            
            # Memory monitoring
            self.memory_monitor.render_memory_dashboard()
            
            # Performance settings
            with st.expander("🔧 Optimization Settings"):
                new_max_points = st.slider(
                    "Max Chart Points", 
                    1000, 10000, 
                    self.config.max_chart_points
                )
                
                if new_max_points != self.config.max_chart_points:
                    self.config.max_chart_points = new_max_points
                    self.chart_optimizer.config.max_points = new_max_points
                
                enable_cache = st.checkbox("Enable Caching", True)
                enable_webgl = st.checkbox("Enable WebGL", self.config.enable_webgl)
                
                if enable_webgl != self.config.enable_webgl:
                    self.config.enable_webgl = enable_webgl
                    self.chart_optimizer.config.enable_webgl = enable_webgl
            
            # Cache management
            with st.expander("💾 Cache Management"):
                cache_stats = self.cache.get_stats()
                st.metric("Cache Entries", cache_stats['entries'])
                st.metric("Cache Size", f"{cache_stats['total_size_mb']:.1f} MB")
                
                if st.button("Clear All Caches"):
                    self.cache.clear()
                    st.cache_data.clear()
                    st.success("All caches cleared!")
    
    @smart_cache(ttl=1800)
    def _load_optimized_datasets(self, filters: Dict[str, Any] = None) -> Dict[str, pd.DataFrame]:
        """Load all datasets with optimization"""
        
        datasets = {}
        
        # Historical AI adoption data
        query = """
        SELECT year, 
               AVG(adoption_rate) as ai_use,
               AVG(roi_multiple) as avg_roi,
               SUM(investment_millions) as total_investment
        FROM ai_adoption 
        WHERE year >= 2018
        GROUP BY year
        ORDER BY year
        """
        
        datasets['historical_data'] = self.db_optimizer.execute_optimized_query(
            query, query_name="historical_trends"
        )
        
        # Add GenAI data (simulated)
        if not datasets['historical_data'].empty:
            genai_adoption = []
            for _, row in datasets['historical_data'].iterrows():
                year = row['year']
                if year < 2022:
                    genai_rate = 0
                elif year == 2022:
                    genai_rate = 15
                elif year == 2023:
                    genai_rate = 33
                elif year == 2024:
                    genai_rate = 71
                else:
                    genai_rate = 75
                
                genai_adoption.append(genai_rate + np.random.normal(0, 2))
            
            datasets['historical_data']['genai_use'] = genai_adoption
        
        # Industry sector data
        sector_query = """
        SELECT industry as sector,
               AVG(adoption_rate) as adoption_rate,
               AVG(roi_multiple) as avg_roi,
               AVG(investment_millions) as avg_investment
        FROM ai_adoption 
        WHERE year = 2025
        GROUP BY industry
        ORDER BY adoption_rate DESC
        """
        
        datasets['sector_2025'] = self.db_optimizer.execute_optimized_query(
            sector_query, query_name="sector_analysis"
        )
        
        # Investment trends
        investment_query = """
        SELECT year,
               SUM(investment_millions) as total_investment,
               COUNT(*) as num_companies
        FROM ai_adoption
        GROUP BY year
        ORDER BY year
        """
        
        datasets['investment_data'] = self.db_optimizer.execute_optimized_query(
            investment_query, query_name="investment_trends"
        )
        
        # Market data
        market_query = """
        SELECT date,
               metric_name,
               AVG(metric_value) as value
        FROM market_data
        WHERE date >= date('2024-01-01')
        GROUP BY date, metric_name
        ORDER BY date
        """
        
        market_data = self.db_optimizer.execute_optimized_query(
            market_query, query_name="market_trends"
        )
        
        # Pivot market data for easier use
        if not market_data.empty:
            datasets['market_metrics'] = market_data.pivot(
                index='date', columns='metric_name', values='value'
            ).reset_index()
        
        return datasets
    
    def _render_kpi_section(self, datasets: Dict[str, pd.DataFrame]):
        """Render optimized KPI section"""
        st.markdown("### 📊 Strategic Performance Indicators")
        
        # Get latest metrics
        if 'historical_data' in datasets and not datasets['historical_data'].empty:
            latest_data = datasets['historical_data'].iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "AI Adoption Rate",
                    f"{latest_data['ai_use']:.1f}%",
                    f"+{latest_data['ai_use'] - datasets['historical_data'].iloc[-2]['ai_use']:.1f}pp"
                )
            
            with col2:
                st.metric(
                    "GenAI Adoption", 
                    f"{latest_data['genai_use']:.1f}%",
                    f"+{latest_data['genai_use'] - datasets['historical_data'].iloc[-2]['genai_use']:.1f}pp"
                )
            
            with col3:
                st.metric(
                    "Average ROI",
                    f"{latest_data['avg_roi']:.1f}x",
                    f"+{latest_data['avg_roi'] - datasets['historical_data'].iloc[-2]['avg_roi']:.1f}x"
                )
            
            with col4:
                st.metric(
                    "Total Investment",
                    f"${latest_data['total_investment']:.1f}B",
                    f"+${latest_data['total_investment'] - datasets['historical_data'].iloc[-2]['total_investment']:.1f}B"
                )
    
    def _render_chart_section(self, datasets: Dict[str, pd.DataFrame]):
        """Render optimized charts section"""
        st.markdown("### 📈 Market Intelligence Analysis")
        
        # Historical trends with optimization
        if 'historical_data' in datasets and not datasets['historical_data'].empty:
            st.subheader("AI Adoption Trends")
            
            fig = self.charts.create_time_series(
                datasets['historical_data'],
                x_col='year',
                y_cols=['ai_use', 'genai_use'],
                title="AI & GenAI Adoption Over Time"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Industry comparison
        if 'sector_2025' in datasets and not datasets['sector_2025'].empty:
            st.subheader("Industry Performance Analysis")
            
            fig = self.charts.create_scatter_plot(
                datasets['sector_2025'],
                x_col='adoption_rate',
                y_col='avg_roi',
                size_col='avg_investment',
                color_col='adoption_rate',
                title="Industry ROI vs Adoption Rate"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_insights_section(self, datasets: Dict[str, pd.DataFrame]):
        """Render AI-powered insights section"""
        st.markdown("### 🧠 Strategic Insights")
        
        # Generate insights based on data
        insights = self._generate_insights(datasets)
        
        for insight in insights:
            if insight['type'] == 'success':
                st.success(f"**{insight['title']}**: {insight['content']}")
            elif insight['type'] == 'warning':
                st.warning(f"**{insight['title']}**: {insight['content']}")
            elif insight['type'] == 'info':
                st.info(f"**{insight['title']}**: {insight['content']}")
    
    def _generate_insights(self, datasets: Dict[str, pd.DataFrame]) -> List[Dict[str, str]]:
        """Generate AI-powered insights from data"""
        insights = []
        
        if 'historical_data' in datasets and len(datasets['historical_data']) >= 2:
            hist_data = datasets['historical_data']
            
            # Growth rate insight
            latest_growth = hist_data['ai_use'].iloc[-1] - hist_data['ai_use'].iloc[-2]
            if latest_growth > 10:
                insights.append({
                    'type': 'success',
                    'title': 'Accelerating Adoption',
                    'content': f'AI adoption grew {latest_growth:.1f} percentage points this year, indicating strong market momentum.'
                })
            
            # ROI trend insight
            roi_trend = hist_data['avg_roi'].diff().iloc[-1]
            if roi_trend > 0.1:
                insights.append({
                    'type': 'success',
                    'title': 'Improving Returns',
                    'content': f'Average ROI increased by {roi_trend:.1f}x, suggesting better implementation strategies.'
                })
        
        if 'sector_2025' in datasets and not datasets['sector_2025'].empty:
            sector_data = datasets['sector_2025']
            
            # Top performer insight
            top_sector = sector_data.loc[sector_data['avg_roi'].idxmax()]
            insights.append({
                'type': 'info',
                'title': 'Sector Leader',
                'content': f'{top_sector["sector"]} leads with {top_sector["avg_roi"]:.1f}x ROI and {top_sector["adoption_rate"]:.1f}% adoption.'
            })
            
            # Opportunity insight
            low_adoption = sector_data[sector_data['adoption_rate'] < 60]
            if not low_adoption.empty:
                insights.append({
                    'type': 'warning',
                    'title': 'Growth Opportunity',
                    'content': f'{len(low_adoption)} sectors still below 60% adoption, representing significant growth potential.'
                })
        
        return insights
    
    def _render_performance_metrics(self):
        """Render performance metrics dashboard"""
        st.markdown("---")
        st.markdown("### ⚡ Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        # Chart performance
        with col1:
            chart_report = self.chart_optimizer.get_performance_report()
            if chart_report:
                st.metric(
                    "Charts Rendered",
                    chart_report.get('total_charts', 0)
                )
                st.metric(
                    "Avg Render Time",
                    f"{chart_report.get('average_render_time', 0):.3f}s"
                )
        
        # Memory performance
        with col2:
            memory_report = self.memory_monitor.get_memory_report()
            st.metric(
                "Memory Usage",
                f"{memory_report['current_memory']['rss_mb']:.0f}MB"
            )
            st.metric(
                "Memory Growth",
                f"{memory_report['memory_growth_mb']:.0f}MB"
            )
        
        # Database performance
        with col3:
            if self.db_optimizer.query_stats:
                avg_query_time = np.mean([
                    stats['execution_time'] 
                    for stats in self.db_optimizer.query_stats.values()
                ])
                st.metric("Avg Query Time", f"{avg_query_time:.3f}s")
                st.metric("Queries Executed", len(self.db_optimizer.query_stats))
        
        # Detailed performance breakdown
        with st.expander("📈 Detailed Performance Breakdown"):
            
            # Chart performance details
            if hasattr(self.chart_optimizer, 'performance_stats'):
                st.subheader("Chart Performance")
                chart_df = pd.DataFrame.from_dict(
                    self.chart_optimizer.performance_stats, 
                    orient='index'
                )
                if not chart_df.empty:
                    st.dataframe(chart_df)
            
            # Query performance details
            if self.db_optimizer.query_stats:
                st.subheader("Database Performance")
                query_df = pd.DataFrame.from_dict(
                    self.db_optimizer.query_stats,
                    orient='index'
                )
                st.dataframe(query_df)

# Demo function
def demo_complete_performance_system():
    """Demonstrate the complete integrated performance system"""
    
    st.title("🚀 Complete Performance Optimization System")
    
    # Initialize performance integrator
    if 'performance_integrator' not in st.session_state:
        with st.spinner("Initializing performance system..."):
            st.session_state.performance_integrator = PerformanceIntegrator()
    
    integrator = st.session_state.performance_integrator
    
    # Performance configuration
    st.sidebar.markdown("### ⚙️ Performance Configuration")
    
    # Filters for data
    filters = {}
    
    with st.sidebar.expander("📊 Data Filters"):
        year_range = st.slider("Year Range", 2018, 2025, (2020, 2025))
        filters['year_range'] = year_range
        
        industries = st.multiselect(
            "Industries",
            ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 'Retail'],
            default=['Technology', 'Financial Services', 'Healthcare']
        )
        filters['industries'] = industries
    
    # Main dashboard
    st.markdown("""
    This demo showcases the complete performance optimization system integrating:
    - **Advanced Caching** with multi-layer cache strategies
    - **Chart Optimization** with WebGL, downsampling, and lazy loading  
    - **Memory Management** with automatic cleanup and monitoring
    - **Database Optimization** with connection pooling and query caching
    """)
    
    # Render optimized dashboard
    integrator.render_optimized_dashboard(filters)
    
    # Performance comparison
    st.markdown("---")
    st.markdown("### 🏁 Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐌 Load Without Optimization", type="secondary"):
            # Simulate unoptimized loading
            start_time = time.time()
            
            with st.spinner("Loading without optimization..."):
                # Simulate slow data loading
                time.sleep(2)
                
                # Create unoptimized large dataset
                large_data = pd.DataFrame({
                    'year': np.repeat(range(2018, 2026), 5000),
                    'value': np.random.randn(40000),
                    'category': np.random.choice(['A', 'B', 'C', 'D'], 40000)
                })
                
                # Create unoptimized chart
                import plotly.express as px
                fig = px.scatter(large_data, x='year', y='value', color='category')
                st.plotly_chart(fig, use_container_width=True)
            
            load_time = time.time() - start_time
            st.metric("Unoptimized Load Time", f"{load_time:.2f}s")
            st.metric("Data Points", f"{len(large_data):,}")
    
    with col2:
        if st.button("⚡ Load With Full Optimization", type="primary"):
            start_time = time.time()
            
            with st.spinner("Loading with optimization..."):
                # Use optimized loading
                datasets = integrator._load_optimized_datasets({})
                
                if 'historical_data' in datasets:
                    fig = integrator.charts.create_time_series(
                        datasets['historical_data'],
                        x_col='year',
                        y_cols=['ai_use'],
                        title="Optimized Chart"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            load_time = time.time() - start_time
            st.metric("Optimized Load Time", f"{load_time:.2f}s")
            
            # Show optimization benefits
            chart_report = integrator.chart_optimizer.get_performance_report()
            if chart_report:
                latest_stats = list(chart_report.get('performance_breakdown', {}).values())
                if latest_stats:
                    st.metric("Optimized Points", f"{latest_stats[-1]['rendered_points']:,}")

if __name__ == "__main__":
    demo_complete_performance_system() 