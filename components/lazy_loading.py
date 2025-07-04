"""Lazy loading components for improved UI performance."""

import streamlit as st
from typing import Any, Callable, Dict, List, Optional, Union
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import plotly.graph_objects as go

from performance.monitor import track_performance, PerformanceContext
from performance.cache_manager import cache_result, get_cache


class LazyLoadContainer:
    """Container that loads content only when visible."""
    
    def __init__(self, 
                 loader_func: Callable,
                 placeholder_text: str = "Loading...",
                 show_spinner: bool = True,
                 cache_key: Optional[str] = None,
                 cache_ttl: int = 300):
        """Initialize lazy load container.
        
        Args:
            loader_func: Function that loads and returns content
            placeholder_text: Text to show while loading
            show_spinner: Show loading spinner
            cache_key: Optional cache key
            cache_ttl: Cache TTL in seconds
        """
        self.loader_func = loader_func
        self.placeholder_text = placeholder_text
        self.show_spinner = show_spinner
        self.cache_key = cache_key
        self.cache_ttl = cache_ttl
        self._loaded = False
        self._content = None
    
    def render(self):
        """Render the lazy loaded content."""
        # Check if already loaded
        if self._loaded and self._content is not None:
            return self._content
        
        # Check cache
        if self.cache_key:
            cache = get_cache()
            cached_content = cache.get(self.cache_key)
            if cached_content is not None:
                self._content = cached_content
                self._loaded = True
                return cached_content
        
        # Create placeholder
        placeholder = st.empty()
        
        # Show loading state
        if self.show_spinner:
            with placeholder.container():
                with st.spinner(self.placeholder_text):
                    self._load_content()
        else:
            placeholder.info(self.placeholder_text)
            self._load_content()
            placeholder.empty()
        
        # Render loaded content
        return self._content
    
    def _load_content(self):
        """Load content using the loader function."""
        with PerformanceContext('lazy_load_content'):
            try:
                self._content = self.loader_func()
                self._loaded = True
                
                # Cache if key provided
                if self.cache_key and self._content is not None:
                    cache = get_cache()
                    cache.set(self.cache_key, self._content, memory_ttl=self.cache_ttl)
                    
            except Exception as e:
                st.error(f"Error loading content: {e}")
                self._content = None


class LazyChart:
    """Lazy loading chart component."""
    
    def __init__(self,
                 chart_func: Callable[[], go.Figure],
                 height: int = 400,
                 use_container_width: bool = True):
        """Initialize lazy chart.
        
        Args:
            chart_func: Function that creates and returns a Plotly figure
            height: Chart height
            use_container_width: Use full container width
        """
        self.chart_func = chart_func
        self.height = height
        self.use_container_width = use_container_width
        self._figure = None
        self._rendered = False
    
    @track_performance('lazy_chart_render', threshold=0.5)
    def render(self):
        """Render the chart lazily."""
        # Check if already rendered
        if self._rendered and self._figure is not None:
            st.plotly_chart(
                self._figure,
                use_container_width=self.use_container_width,
                height=self.height
            )
            return
        
        # Create placeholder
        placeholder = st.empty()
        
        # Check if chart is in viewport (simplified check)
        # In production, use intersection observer
        if st.session_state.get('render_all_charts', True):
            with placeholder.container():
                with st.spinner("Rendering chart..."):
                    self._figure = self.chart_func()
                    self._rendered = True
                
                st.plotly_chart(
                    self._figure,
                    use_container_width=self.use_container_width,
                    height=self.height
                )
        else:
            # Show placeholder
            placeholder.info("📊 Chart will load when scrolled into view")


class LazyDataFrame:
    """Lazy loading DataFrame with pagination."""
    
    def __init__(self,
                 data_func: Callable[[], pd.DataFrame],
                 page_size: int = 50,
                 show_search: bool = True,
                 show_download: bool = True):
        """Initialize lazy DataFrame.
        
        Args:
            data_func: Function that returns DataFrame
            page_size: Rows per page
            show_search: Show search box
            show_download: Show download button
        """
        self.data_func = data_func
        self.page_size = page_size
        self.show_search = show_search
        self.show_download = show_download
        self._data = None
        self._filtered_data = None
    
    @track_performance('lazy_dataframe_render', threshold=0.3)
    def render(self):
        """Render the DataFrame with lazy loading and pagination."""
        # Load data if not already loaded
        if self._data is None:
            with st.spinner("Loading data..."):
                self._data = self.data_func()
                self._filtered_data = self._data
        
        # Search functionality
        if self.show_search and len(self._data) > 0:
            search_term = st.text_input(
                "🔍 Search data",
                key=f"search_{id(self)}",
                placeholder="Type to search..."
            )
            
            if search_term:
                # Filter data
                mask = self._data.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                self._filtered_data = self._data[mask]
            else:
                self._filtered_data = self._data
        
        # Display info
        total_rows = len(self._filtered_data)
        st.caption(f"Showing {total_rows} rows")
        
        # Pagination
        if total_rows > self.page_size:
            # Calculate pages
            total_pages = (total_rows + self.page_size - 1) // self.page_size
            
            # Page selector
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                page = st.number_input(
                    "Page",
                    min_value=1,
                    max_value=total_pages,
                    value=1,
                    key=f"page_{id(self)}"
                )
            
            # Calculate slice
            start_idx = (page - 1) * self.page_size
            end_idx = min(start_idx + self.page_size, total_rows)
            
            # Display page
            st.dataframe(
                self._filtered_data.iloc[start_idx:end_idx],
                use_container_width=True
            )
            
            # Page info
            st.caption(f"Page {page} of {total_pages} ({start_idx + 1}-{end_idx} of {total_rows})")
        else:
            # Display all data
            st.dataframe(self._filtered_data, use_container_width=True)
        
        # Download button
        if self.show_download:
            csv = self._filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="data_export.csv",
                mime="text/csv",
                key=f"download_{id(self)}"
            )


class LazyMetrics:
    """Lazy loading metrics display."""
    
    def __init__(self, metrics_func: Callable[[], List[Dict[str, Any]]]):
        """Initialize lazy metrics.
        
        Args:
            metrics_func: Function that returns list of metric dicts
        """
        self.metrics_func = metrics_func
        self._metrics = None
    
    def render(self):
        """Render metrics lazily."""
        # Load metrics if needed
        if self._metrics is None:
            with st.spinner("Loading metrics..."):
                self._metrics = self.metrics_func()
        
        # Render metrics in columns
        if self._metrics:
            cols = st.columns(len(self._metrics))
            
            for idx, (col, metric) in enumerate(zip(cols, self._metrics)):
                with col:
                    st.metric(
                        label=metric.get('label', f'Metric {idx + 1}'),
                        value=metric.get('value', 'N/A'),
                        delta=metric.get('delta'),
                        help=metric.get('help')
                    )


class LazyTabs:
    """Lazy loading tab component."""
    
    def __init__(self, 
                 tabs: Dict[str, Callable],
                 default_tab: Optional[str] = None):
        """Initialize lazy tabs.
        
        Args:
            tabs: Dict of tab name to content function
            default_tab: Default tab to show
        """
        self.tabs = tabs
        self.default_tab = default_tab or list(tabs.keys())[0]
        self._rendered_tabs = set()
    
    def render(self):
        """Render tabs with lazy content loading."""
        tab_names = list(self.tabs.keys())
        tabs = st.tabs(tab_names)
        
        for tab, tab_name in zip(tabs, tab_names):
            with tab:
                # Only render if tab is selected or was previously rendered
                if tab_name == self.default_tab or tab_name in self._rendered_tabs:
                    # Mark as rendered
                    self._rendered_tabs.add(tab_name)
                    
                    # Render content
                    content_func = self.tabs[tab_name]
                    with PerformanceContext(f'render_tab_{tab_name}'):
                        content_func()
                else:
                    # Show placeholder
                    st.info(f"Click to load {tab_name} content")


class ProgressiveImage:
    """Progressive image loading with blur-up effect."""
    
    def __init__(self,
                 image_url: str,
                 thumbnail_url: Optional[str] = None,
                 alt_text: str = "Image",
                 width: Optional[int] = None):
        """Initialize progressive image.
        
        Args:
            image_url: Full resolution image URL
            thumbnail_url: Low resolution thumbnail URL
            alt_text: Alt text for accessibility
            width: Image width
        """
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.alt_text = alt_text
        self.width = width
    
    def render(self):
        """Render image with progressive loading."""
        # For Streamlit, we'll use a simplified approach
        # In production, use JavaScript for true progressive loading
        
        placeholder = st.empty()
        
        # Show thumbnail first if available
        if self.thumbnail_url:
            placeholder.image(
                self.thumbnail_url,
                caption=self.alt_text,
                width=self.width,
                output_format='JPEG'
            )
        else:
            placeholder.info(f"Loading {self.alt_text}...")
        
        # Load full image
        # In production, this would be done asynchronously
        placeholder.image(
            self.image_url,
            caption=self.alt_text,
            width=self.width
        )


class AsyncContentLoader:
    """Load multiple content pieces asynchronously."""
    
    def __init__(self, max_workers: int = 4):
        """Initialize async content loader.
        
        Args:
            max_workers: Maximum concurrent workers
        """
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def load_multiple(self, 
                     loaders: Dict[str, Callable],
                     show_progress: bool = True) -> Dict[str, Any]:
        """Load multiple content pieces in parallel.
        
        Args:
            loaders: Dict of name to loader function
            show_progress: Show progress bar
            
        Returns:
            Dict of loaded content
        """
        results = {}
        total = len(loaders)
        
        if show_progress:
            progress_bar = st.progress(0)
            progress_text = st.empty()
        
        # Submit all tasks
        futures = {
            self._executor.submit(loader): name
            for name, loader in loaders.items()
        }
        
        # Collect results as they complete
        completed = 0
        for future in futures:
            name = futures[future]
            try:
                result = future.result()
                results[name] = result
            except Exception as e:
                st.error(f"Error loading {name}: {e}")
                results[name] = None
            
            # Update progress
            completed += 1
            if show_progress:
                progress = completed / total
                progress_bar.progress(progress)
                progress_text.text(f"Loading... {completed}/{total}")
        
        # Clean up progress indicators
        if show_progress:
            progress_bar.empty()
            progress_text.empty()
        
        return results
    
    def __del__(self):
        """Cleanup executor."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)


# Utility functions

def lazy_load_section(
    section_id: str,
    content_func: Callable,
    title: Optional[str] = None,
    expanded: bool = False
):
    """Create a lazy-loaded expandable section.
    
    Args:
        section_id: Unique section ID
        content_func: Function that renders content
        title: Section title
        expanded: Initially expanded
    """
    # Track which sections have been loaded
    if 'loaded_sections' not in st.session_state:
        st.session_state.loaded_sections = set()
    
    # Create expander
    with st.expander(title or f"Section {section_id}", expanded=expanded):
        # Check if content should be loaded
        if expanded or section_id in st.session_state.loaded_sections:
            st.session_state.loaded_sections.add(section_id)
            content_func()
        else:
            st.info("Click to expand and load content")


@cache_result(prefix='lazy_computation', ttl=600)
def lazy_compute(computation_id: str, compute_func: Callable) -> Any:
    """Perform lazy computation with caching.
    
    Args:
        computation_id: Unique computation ID
        compute_func: Function that performs computation
        
    Returns:
        Computation result
    """
    with PerformanceContext(f'lazy_compute_{computation_id}'):
        return compute_func()