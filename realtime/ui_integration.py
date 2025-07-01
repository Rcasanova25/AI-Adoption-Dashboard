"""
Streamlit UI integration for real-time data system
"""

import streamlit as st
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from .core import get_global_manager
from .monitoring import get_global_monitor
from .notifications import get_global_notification_manager, get_global_update_notifier
from .config import get_global_config_manager, ConfigUI
from .data_sources import get_global_integrator
from .caching import get_global_cache
from .models import DataSourceConfig, DataSourceType, AuthenticationType, NotificationType

logger = logging.getLogger(__name__)

class RealtimeUIManager:
    """Manages UI integration for real-time data system"""
    
    def __init__(self):
        self.data_manager = None
        self.monitor = None
        self.notification_manager = None
        self.config_manager = None
        self.integrator = None
        self.cache = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize all real-time components"""
        if self._initialized:
            return
        
        try:
            self.data_manager = await get_global_manager()
            self.monitor = await get_global_monitor()
            self.notification_manager = await get_global_notification_manager()
            self.config_manager = get_global_config_manager()
            self.integrator = await get_global_integrator()
            self.cache = get_global_cache()
            self._initialized = True
            logger.info("Real-time UI manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize real-time UI manager: {e}")
            st.error(f"Failed to initialize real-time system: {e}")
    
    def render_status_indicator(self):
        """Render real-time system status indicator"""
        if not self._initialized:
            st.error("⚠️ Real-time system not initialized")
            return
        
        # Get system status
        try:
            # This would be async in real implementation
            # For demo, we'll use mock data
            status_data = {
                'total_sources': 5,
                'healthy_sources': 4,
                'active_streams': 3,
                'total_alerts': 2
            }
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Data Sources", 
                    status_data['total_sources'],
                    delta=f"{status_data['healthy_sources']} healthy"
                )
            
            with col2:
                st.metric(
                    "Active Streams", 
                    status_data['active_streams']
                )
            
            with col3:
                health_rate = (status_data['healthy_sources'] / status_data['total_sources']) * 100
                st.metric(
                    "Health Rate", 
                    f"{health_rate:.1f}%",
                    delta="Good" if health_rate > 80 else "Needs Attention"
                )
            
            with col4:
                st.metric(
                    "Active Alerts", 
                    status_data['total_alerts'],
                    delta="High" if status_data['total_alerts'] > 5 else "Normal"
                )
                
        except Exception as e:
            st.error(f"Error loading status: {e}")
    
    def render_data_source_manager(self):
        """Render data source management interface"""
        st.subheader("📡 Data Source Management")
        
        # Tabs for different operations
        tab1, tab2, tab3 = st.tabs(["📋 Sources", "➕ Add Source", "⚙️ Configure"])
        
        with tab1:
            self._render_source_list()
        
        with tab2:
            self._render_add_source_form()
        
        with tab3:
            self._render_configuration_manager()
    
    def _render_source_list(self):
        """Render list of data sources"""
        st.write("**Available Data Sources**")
        
        # Get available sources from integrator
        if self.integrator:
            sources = self.integrator.list_available_sources()
            
            # Create DataFrame for display
            source_data = []
            for source_id, info in sources.items():
                source_data.append({
                    'ID': source_id,
                    'Name': info['name'],
                    'Type': info['type'],
                    'Update Interval': info['update_interval'],
                    'Status': '🟢 Active' if source_id in ['ai_research_metrics', 'github_ai_trends'] else '⚪ Inactive'
                })
            
            if source_data:
                df = pd.DataFrame(source_data)
                st.dataframe(df, use_container_width=True)
                
                # Action buttons
                selected_source = st.selectbox("Select source for actions:", options=list(sources.keys()))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("▶️ Start"):
                        st.success(f"Started {selected_source}")
                
                with col2:
                    if st.button("⏸️ Stop"):
                        st.info(f"Stopped {selected_source}")
                
                with col3:
                    if st.button("🔄 Restart"):
                        st.info(f"Restarted {selected_source}")
            else:
                st.info("No data sources configured")
    
    def _render_add_source_form(self):
        """Render form to add new data source"""
        st.write("**Add New Data Source**")
        
        # Source type selection
        source_type = st.selectbox(
            "Source Type",
            options=[DataSourceType.REST_API.value, DataSourceType.WEBSOCKET.value],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if source_type == DataSourceType.REST_API.value:
            self._render_rest_api_form()
    
    def _render_rest_api_form(self):
        """Render REST API configuration form"""
        with st.form("add_rest_api_source"):
            # Basic information
            source_id = st.text_input("Source ID", help="Unique identifier for this source")
            name = st.text_input("Display Name")
            description = st.text_area("Description", height=100)
            
            # Connection settings
            st.subheader("Connection Settings")
            base_url = st.text_input("Base URL", placeholder="https://api.example.com")
            endpoint = st.text_input("Endpoint", placeholder="/v1/data")
            method = st.selectbox("HTTP Method", options=["GET", "POST", "PUT"])
            
            # Authentication
            st.subheader("Authentication")
            auth_type = st.selectbox(
                "Authentication Type",
                options=[e.value for e in AuthenticationType],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            api_key = ""
            bearer_token = ""
            username = ""
            password = ""
            
            if auth_type == AuthenticationType.API_KEY.value:
                api_key = st.text_input("API Key", type="password")
            elif auth_type == AuthenticationType.BEARER_TOKEN.value:
                bearer_token = st.text_input("Bearer Token", type="password")
            elif auth_type == AuthenticationType.BASIC_AUTH.value:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            
            # Rate limiting
            st.subheader("Rate Limiting")
            col1, col2 = st.columns(2)
            with col1:
                requests_per_second = st.number_input("Requests per Second", min_value=0.1, value=1.0, step=0.1)
            with col2:
                requests_per_minute = st.number_input("Requests per Minute", min_value=1, value=60, step=1)
            
            # Update settings
            st.subheader("Update Settings")
            col1, col2 = st.columns(2)
            with col1:
                update_interval = st.number_input("Update Interval (minutes)", min_value=1, value=5, step=1)
            with col2:
                timeout = st.number_input("Timeout (seconds)", min_value=1, value=30, step=1)
            
            # Submit button
            submitted = st.form_submit_button("Add Data Source")
            
            if submitted:
                if not all([source_id, name, base_url]):
                    st.error("Please fill in all required fields")
                    return
                
                try:
                    # Create configuration
                    config = DataSourceConfig(
                        source_id=source_id,
                        name=name,
                        description=description,
                        source_type=DataSourceType.REST_API,
                        base_url=base_url,
                        endpoint=endpoint,
                        method=method,
                        credentials={
                            "auth_type": auth_type,
                            "api_key": api_key if api_key else None,
                            "bearer_token": bearer_token if bearer_token else None,
                            "username": username if username else None,
                            "password": password if password else None
                        },
                        rate_limit={
                            "requests_per_second": requests_per_second,
                            "requests_per_minute": requests_per_minute
                        },
                        update_interval=timedelta(minutes=update_interval),
                        timeout=timeout
                    )
                    
                    # Validate configuration
                    if self.config_manager:
                        errors = await self.config_manager.validate_config(config)
                        if errors:
                            st.error("Configuration errors:")
                            for error in errors:
                                st.error(f"- {error}")
                            return
                    
                    st.success(f"Data source '{name}' added successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Failed to add data source: {e}")
    
    def _render_configuration_manager(self):
        """Render configuration management interface"""
        st.write("**Configuration Management**")
        
        # Load existing configurations
        if st.button("🔄 Reload Configurations"):
            st.info("Configurations reloaded")
        
        # Configuration file upload
        uploaded_file = st.file_uploader(
            "Upload Configuration File",
            type=['yaml', 'yml'],
            help="Upload a YAML configuration file for a data source"
        )
        
        if uploaded_file:
            try:
                import yaml
                config_data = yaml.safe_load(uploaded_file)
                
                st.json(config_data)
                
                if st.button("💾 Save Configuration"):
                    st.success("Configuration saved successfully!")
                    
            except Exception as e:
                st.error(f"Invalid configuration file: {e}")
    
    def render_monitoring_dashboard(self):
        """Render monitoring dashboard"""
        st.subheader("📊 Real-Time Monitoring")
        
        # System overview
        self._render_system_overview()
        
        # Performance metrics
        self._render_performance_metrics()
        
        # Alert management
        self._render_alert_management()
    
    def _render_system_overview(self):
        """Render system overview section"""
        st.write("**System Overview**")
        
        # Mock data for demo
        col1, col2 = st.columns(2)
        
        with col1:
            # System health pie chart
            health_data = pd.DataFrame({
                'Status': ['Healthy', 'Warning', 'Error'],
                'Count': [8, 2, 1]
            })
            
            fig = px.pie(
                health_data, 
                values='Count', 
                names='Status',
                title="Source Health Status",
                color_discrete_map={
                    'Healthy': '#10B981',
                    'Warning': '#F59E0B', 
                    'Error': '#EF4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response time trend
            dates = pd.date_range(start='2024-01-01', periods=24, freq='H')
            response_times = [0.5 + 0.3 * (i % 6) for i in range(24)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=response_times,
                mode='lines+markers',
                name='Response Time',
                line=dict(color='#3B82F6')
            ))
            
            fig.update_layout(
                title="Average Response Time (24h)",
                xaxis_title="Time",
                yaxis_title="Response Time (s)",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_performance_metrics(self):
        """Render performance metrics section"""
        st.write("**Performance Metrics**")
        
        # Metrics selection
        col1, col2 = st.columns(2)
        with col1:
            selected_source = st.selectbox(
                "Select Source",
                options=["All Sources", "ai_research_metrics", "github_ai_trends", "financial_data"]
            )
        with col2:
            time_range = st.selectbox(
                "Time Range",
                options=["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
            )
        
        # Metrics table
        metrics_data = pd.DataFrame({
            'Source': ['ai_research_metrics', 'github_ai_trends', 'financial_data'],
            'Avg Response Time (s)': [0.45, 0.67, 1.23],
            'Success Rate (%)': [99.5, 98.8, 97.2],
            'Requests/Hour': [12, 10, 6],
            'Last Update': ['2 min ago', '5 min ago', '8 min ago']
        })
        
        st.dataframe(metrics_data, use_container_width=True)
    
    def _render_alert_management(self):
        """Render alert management section"""
        st.write("**Active Alerts**")
        
        # Mock alerts data
        alerts_data = [
            {
                'Severity': '🔴 Critical',
                'Source': 'financial_data',
                'Message': 'API rate limit exceeded',
                'Time': '5 min ago'
            },
            {
                'Severity': '🟡 Warning',
                'Source': 'ai_research_metrics',
                'Message': 'High response time detected',
                'Time': '15 min ago'
            }
        ]
        
        if alerts_data:
            for alert in alerts_data:
                with st.expander(f"{alert['Severity']} - {alert['Source']}"):
                    st.write(f"**Message:** {alert['Message']}")
                    st.write(f"**Time:** {alert['Time']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Acknowledge", key=f"ack_{alert['Source']}"):
                            st.success("Alert acknowledged")
                    with col2:
                        if st.button("🔕 Dismiss", key=f"dismiss_{alert['Source']}"):
                            st.info("Alert dismissed")
        else:
            st.success("No active alerts")
    
    def render_notifications_panel(self):
        """Render notifications panel in sidebar"""
        with st.sidebar:
            st.subheader("🔔 Notifications")
            
            # Notification filter
            filter_type = st.selectbox(
                "Filter",
                options=["All", "Data Updates", "Errors", "System Alerts"],
                key="notification_filter"
            )
            
            # Mock notifications
            notifications = [
                {
                    'type': 'data_update',
                    'title': 'AI Research Data Updated',
                    'message': 'New research papers available',
                    'time': '2 min ago',
                    'read': False
                },
                {
                    'type': 'error',
                    'title': 'Financial API Error',
                    'message': 'Connection timeout occurred',
                    'time': '10 min ago',
                    'read': False
                },
                {
                    'type': 'system_alert',
                    'title': 'System Health Check',
                    'message': 'All systems operational',
                    'time': '1 hour ago',
                    'read': True
                }
            ]
            
            # Display notifications
            unread_count = sum(1 for n in notifications if not n['read'])
            if unread_count > 0:
                st.caption(f"{unread_count} unread notifications")
            
            for i, notification in enumerate(notifications):
                icon = "🔴" if not notification['read'] else "⚪"
                
                with st.expander(f"{icon} {notification['title']}"):
                    st.write(notification['message'])
                    st.caption(notification['time'])
                    
                    if not notification['read']:
                        if st.button("Mark as read", key=f"read_{i}"):
                            notification['read'] = True
                            st.rerun()
    
    def render_cache_status(self):
        """Render cache status information"""
        st.subheader("🗄️ Cache Status")
        
        # Mock cache statistics
        cache_stats = {
            'hit_rate_percent': 87.5,
            'memory_usage_mb': 45.2,
            'disk_usage_mb': 234.7,
            'total_entries': 1247,
            'expired_entries': 23
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Hit Rate",
                f"{cache_stats['hit_rate_percent']:.1f}%",
                delta="Good" if cache_stats['hit_rate_percent'] > 80 else "Low"
            )
        
        with col2:
            st.metric(
                "Memory Usage",
                f"{cache_stats['memory_usage_mb']:.1f} MB"
            )
        
        with col3:
            st.metric(
                "Total Entries",
                cache_stats['total_entries']
            )
        
        # Cache actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh Cache"):
                st.success("Cache refreshed")
        
        with col2:
            if st.button("🧹 Clear Expired"):
                st.info(f"Cleared {cache_stats['expired_entries']} expired entries")
        
        with col3:
            if st.button("⚠️ Clear All"):
                if st.session_state.get('confirm_clear_cache', False):
                    st.warning("All cache cleared!")
                    st.session_state.confirm_clear_cache = False
                else:
                    st.session_state.confirm_clear_cache = True
                    st.warning("Click again to confirm")

# Global UI manager instance
_global_ui_manager: Optional[RealtimeUIManager] = None

def get_global_ui_manager() -> RealtimeUIManager:
    """Get the global UI manager instance"""
    global _global_ui_manager
    if _global_ui_manager is None:
        _global_ui_manager = RealtimeUIManager()
    return _global_ui_manager

def render_realtime_dashboard():
    """Render the complete real-time dashboard"""
    ui_manager = get_global_ui_manager()
    
    # Initialize if needed
    if not ui_manager._initialized:
        with st.spinner("Initializing real-time system..."):
            try:
                # For demo purposes, we'll simulate initialization
                import time
                time.sleep(1)  # Simulate initialization time
                ui_manager._initialized = True
            except Exception as e:
                st.error(f"Failed to initialize: {e}")
                return
    
    # Main dashboard layout
    st.title("🚀 Real-Time Data Integration Dashboard")
    
    # Status indicator at the top
    ui_manager.render_status_indicator()
    
    st.divider()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📡 Data Sources", 
        "📊 Monitoring", 
        "🗄️ Cache", 
        "⚙️ Settings"
    ])
    
    with tab1:
        ui_manager.render_data_source_manager()
    
    with tab2:
        ui_manager.render_monitoring_dashboard()
    
    with tab3:
        ui_manager.render_cache_status()
    
    with tab4:
        st.subheader("⚙️ System Settings")
        st.info("System settings will be available in future updates")
    
    # Notifications panel in sidebar
    ui_manager.render_notifications_panel()

if __name__ == "__main__":
    # For testing the UI components
    render_realtime_dashboard()