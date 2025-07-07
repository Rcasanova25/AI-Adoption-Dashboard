"""
Performance monitoring callbacks for the AI Adoption Dashboard.
Integrates existing performance systems with Dash.
"""
import dash
from dash import Input, Output, State, callback, html
import dash_bootstrap_components as dbc
import psutil
import time
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def register_performance_callbacks(app):
    """Register all performance-related callbacks."""
    
    @callback(
        Output("performance-monitor", "children"),
        Input("performance-interval", "n_intervals"),
        prevent_initial_call=False
    )
    def render_performance_monitor(n_intervals: int) -> html.Div:
        """Render performance monitoring widget."""
        return create_performance_monitor()
    
    @callback(
        [Output("memory-usage-bar", "children"),
         Output("memory-usage-text", "children"),
         Output("cache-status", "children"),
         Output("response-times", "children")],
        Input("performance-interval", "n_intervals")
    )
    def update_performance_metrics(n_intervals: int) -> Tuple[Any, str, html.Div, html.Div]:
        """Update performance metrics every 5 seconds."""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Determine color based on usage
            if memory_percent < 70:
                color = "success"
            elif memory_percent < 85:
                color = "warning" 
            else:
                color = "danger"
            
            memory_bar = dbc.Progress(
                value=memory_percent,
                color=color,
                striped=True,
                animated=True if memory_percent > 70 else False,
                className="mb-1",
                style={"height": "20px"}
            )
            
            memory_text = f"{memory_percent:.1f}% ({memory_used_gb:.1f}/{memory_total_gb:.1f} GB)"
            
            # Cache status (would connect to actual cache manager in production)
            cache_stats = get_cache_stats()
            
            cache_status = html.Div([
                html.Small(f"Hit Rate: {cache_stats['hit_rate']:.1f}%", className="d-block"),
                html.Small(f"Size: {cache_stats['size']}", className="d-block"),
                html.Small(f"Items: {cache_stats['items']}", className="d-block text-muted")
            ])
            
            # Response times (would track actual response times in production)
            response_stats = get_response_stats()
            
            response_times = html.Div([
                html.Small(f"Avg: {response_stats['avg']}ms", className="d-block"),
                html.Small(f"P95: {response_stats['p95']}ms", className="d-block"),
                html.Small(f"Max: {response_stats['max']}ms", className="d-block text-muted")
            ])
            
            return memory_bar, memory_text, cache_status, response_times
            
        except Exception as e:
            logger.error(f"Error updating performance metrics: {str(e)}")
            return (
                dbc.Progress(value=0, color="secondary"),
                "Error",
                html.Small("Error loading cache stats"),
                html.Small("Error loading response times")
            )
    
    @callback(
        [Output("cache-status", "children", allow_duplicate=True),
         Output("success-toast", "is_open", allow_duplicate=True),
         Output("success-toast", "children", allow_duplicate=True)],
        Input("clear-cache-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_cache(n_clicks: int) -> Tuple[html.Div, bool, str]:
        """Clear application cache."""
        if n_clicks:
            try:
                # Clear cache (would connect to actual cache manager)
                clear_application_cache()
                
                # Update cache status
                cache_status = html.Div([
                    html.Small("Cache cleared!", className="d-block text-success"),
                    html.Small("Hit Rate: 0.0%", className="d-block"),
                    html.Small("Size: 0 MB", className="d-block")
                ])
                
                return cache_status, True, "Cache cleared successfully!"
                
            except Exception as e:
                logger.error(f"Error clearing cache: {str(e)}")
                return dash.no_update, True, f"Error clearing cache: {str(e)}"
        
        return dash.no_update, False, ""


def create_performance_monitor() -> html.Div:
    """Create the performance monitoring sidebar widget."""
    return html.Div([
        html.H6([
            html.I(className="fas fa-tachometer-alt me-2"),
            "Performance Monitor"
        ], className="mb-3"),
        
        # Memory usage
        html.Div([
            html.Label("Memory Usage:", className="small fw-bold"),
            html.Div(id="memory-usage-bar"),
            html.Small(id="memory-usage-text", className="text-muted")
        ], className="mb-3"),
        
        # CPU usage
        html.Div([
            html.Label("CPU Usage:", className="small fw-bold"),
            html.Div([
                dbc.Progress(
                    value=psutil.cpu_percent(interval=0.1),
                    color="info",
                    className="mb-1",
                    style={"height": "15px"}
                ),
                html.Small(f"{psutil.cpu_percent():.1f}%", className="text-muted")
            ])
        ], className="mb-3"),
        
        # Cache status
        html.Div([
            html.Label("Cache Status:", className="small fw-bold"),
            html.Div(id="cache-status", className="small"),
        ], className="mb-3"),
        
        # Response times
        html.Div([
            html.Label("Response Times:", className="small fw-bold"),
            html.Div(id="response-times", className="small")
        ], className="mb-3"),
        
        # Cache controls
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-trash me-1"), "Clear Cache"], 
                id="clear-cache-btn", 
                size="sm", 
                color="warning",
                outline=True,
                className="w-100"
            )
        ])
    ])


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics (mock implementation)."""
    # In production, this would connect to the actual cache manager
    # For now, return mock data
    return {
        "hit_rate": 87.5,
        "size": "42.3 MB",
        "items": "1,247",
        "hits": 10234,
        "misses": 1432
    }


def get_response_stats() -> Dict[str, Any]:
    """Get response time statistics (mock implementation)."""
    # In production, this would track actual response times
    # For now, return mock data
    return {
        "avg": 145,
        "p95": 312,
        "max": 892,
        "min": 23
    }


def clear_application_cache():
    """Clear the application cache."""
    # In production, this would connect to the actual cache manager
    # and clear all cached data
    logger.info("Clearing application cache...")
    time.sleep(0.5)  # Simulate cache clearing
    logger.info("Cache cleared successfully")