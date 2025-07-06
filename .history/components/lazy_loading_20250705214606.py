"""Lazy loading components for improved UI performance."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from performance.cache_manager import cache_result, get_cache
from performance.monitor import PerformanceContext, track_performance


class LazyLoadContainer:
    """Container that loads content only when visible."""

    def __init__(
        self,
        loader_func: Callable,
        placeholder_text: str = "Loading...",
        show_spinner: bool = True,
        cache_key: Optional[str] = None,
        cache_ttl: int = 300,
    ):
        self.loader_func = loader_func
        self.placeholder_text = placeholder_text
        self.show_spinner = show_spinner
        self.cache_key = cache_key
        self.cache_ttl = cache_ttl
        self._loaded = False
        self._content = None

    def render(self):
        """Render the lazy loaded content."""
        if self._loaded and self._content is not None:
            return self._content

        if self.cache_key:
            cache = get_cache()
            cached_content = cache.get(self.cache_key)
            if cached_content is not None:
                self._content = cached_content
                self._loaded = True
                return cached_content

        placeholder = st.empty()
        if self.show_spinner:
            with placeholder.container():
                with st.spinner(self.placeholder_text):
                    self._load_content()
        else:
            placeholder.info(self.placeholder_text)
            self._load_content()
            placeholder.empty()
        return self._content

    def _load_content(self):
        with PerformanceContext("lazy_load_content"):
            try:
                self._content = self.loader_func()
                self._loaded = True
                if self.cache_key and self._content is not None:
                    cache = get_cache()
                    cache.set(self.cache_key, self._content, memory_ttl=self.cache_ttl)
            except Exception as e:
                st.error(f"Error loading content: {e}")
                self._content = None


class LazyChart:
    """Lazy loading chart component."""

    def __init__(
        self,
        chart_func: Callable[[], go.Figure],
        height: int = 400,
        use_container_width: bool = True,
    ):
        self.chart_func = chart_func
        self.height = height
        self.use_container_width = use_container_width
        self._figure = None
        self._rendered = False

    @track_performance("lazy_chart_render", threshold=0.5)
    def render(self):
        if self._rendered and self._figure is not None:
            st.plotly_chart(
                self._figure, use_container_width=self.use_container_width, height=self.height
            )
            return

        placeholder = st.empty()
        if st.session_state.get("render_all_charts", True):
            with placeholder.container():
                with st.spinner("Rendering chart..."):
                    self._figure = self.chart_func()
                    self._rendered = True
                st.plotly_chart(
                    self._figure, use_container_width=self.use_container_width, height=self.height
                )
        else:
            placeholder.info("📊 Chart will load when scrolled into view")


class LazyDataFrame:
    """Lazy loading DataFrame with pagination."""

    def __init__(
        self,
        data_func: Callable[[], pd.DataFrame],
        page_size: int = 50,
        show_search: bool = True,
        show_download: bool = True,
    ):
        self.data_func = data_func
        self.page_size = page_size
        self.show_search = show_search
        self.show_download = show_download
        self._data = None
        self._filtered_data = None

    @track_performance("lazy_dataframe_render", threshold=0.3)
    def render(self):
        if self._data is None:
            with st.spinner("Loading data..."):
                self._data = self.data_func()
                self._filtered_data = self._data

        if self.show_search and len(self._data) > 0:
            search_term = st.text_input(
                "🔍 Search data", key=f"search_{id(self)}", placeholder="Type to search..."
            )
            if search_term:
                mask = (
                    self._data.astype(str)
                    .apply(lambda x: x.str.contains(search_term, case=False, na=False))
                    .any(axis=1)
                )
                self._filtered_data = self._data[mask]
            else:
                self._filtered_data = self._data

        total_rows = len(self._filtered_data)
        st.caption(f"Showing {total_rows} rows")

        if total_rows > self.page_size:
            total_pages = (total_rows + self.page_size - 1) // self.page_size
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                page = st.number_input(
                    "Page", min_value=1, max_value=total_pages, value=1, key=f"page_{id(self)}"
                )
            start_idx = (page - 1) * self.page_size
            end_idx = min(start_idx + self.page_size, total_rows)
            st.dataframe(self._filtered_data.iloc[start_idx:end_idx], use_container_width=True)
            st.caption(f"Page {page} of {total_pages} ({start_idx + 1}-{end_idx} of {total_rows})")
        else:
            st.dataframe(self._filtered_data, use_container_width=True)

        if self.show_download:
            csv = self._filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="data_export.csv",
                mime="text/csv",
                key=f"download_{id(self)}",
            )


class LazyMetrics:
    """Lazy loading metrics display."""

    def __init__(self, metrics_func: Callable[[], List[Dict[str, Any]]]):
        self.metrics_func = metrics_func
        self._metrics = None

    def render(self):
        if self._metrics is None:
            with st.spinner("Loading metrics..."):
                self._metrics = self.metrics_func()
        if self._metrics:
            cols = st.columns(len(self._metrics))
            for idx, (col, metric) in enumerate(zip(cols, self._metrics)):
                with col:
                    st.metric(
                        label=metric.get("label", f"Metric {idx + 1}"),
                        value=metric.get("value", "N/A"),
                        delta=metric.get("delta"),
                        help=metric.get("help"),
                    )


class LazyTabs:
    """Lazy loading tab component."""

    def __init__(self, tabs: Dict[str, Callable], default_tab: Optional[str] = None):
        self.tabs = tabs
        self.default_tab = default_tab or list(tabs.keys())[0]
        self._rendered_tabs = set()

    def render(self):
        tab_names = list(self.tabs.keys())
        tabs = st.tabs(tab_names)
        for tab, tab_name in zip(tabs, tab_names):
            with tab:
                if tab_name == self.default_tab or tab_name in self._rendered_tabs:
                    self._rendered_tabs.add(tab_name)
                    content_func = self.tabs[tab_name]
                    with PerformanceContext(f"render_tab_{tab_name}"):
                        content_func()
                else:
                    st.info(f"Click to load {tab_name} content")


class ProgressiveImage:
    """Progressive image loading with blur-up effect."""

    def __init__(
        self,
        image_url: str,
        thumbnail_url: Optional[str] = None,
        alt_text: str = "Image",
        width: Optional[int] = None,
    ):
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.alt_text = alt_text
        self.width = width

    def render(self):
        placeholder = st.empty()
        if self.thumbnail_url:
            placeholder.image(
                self.thumbnail_url, caption=self.alt_text, width=self.width, output_format="JPEG"
            )
        else:
            placeholder.info(f"Loading {self.alt_text}...")
        placeholder.image(self.image_url, caption=self.alt_text, width=self.width)


class AsyncContentLoader:
    """Load multiple content pieces asynchronously."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def load_multiple(
        self, loaders: Dict[str, Callable], show_progress: bool = True
    ) -> Dict[str, Any]:
        results = {}
        total = len(loaders)
        if show_progress:
            progress_bar = st.progress(0)
            progress_text = st.empty()
        futures = {self._executor.submit(loader): name for name, loader in loaders.items()}
        completed = 0
        for future in futures:
            name = futures[future]
            try:
                result = future.result()
                results[name] = result
            except Exception as e:
                st.error(f"Error loading {name}: {e}")
                results[name] = None
            completed += 1
            if show_progress:
                progress = completed / total
                progress_bar.progress(progress)
                progress_text.text(f"Loading... {completed}/{total}")
        if show_progress:
            progress_bar.empty()
            progress_text.empty()
        return results

    def __del__(self):
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False)


def lazy_load_section(
    section_id: str, content_func: Callable, title: Optional[str] = None, expanded: bool = False
):
    """Create a lazy-loaded expandable section."""
    if "loaded_sections" not in st.session_state:
        st.session_state.loaded_sections = set()
    with st.expander(title or f"Section {section_id}", expanded=expanded):
        if expanded or section_id in st.session_state.loaded_sections:
            st.session_state.loaded_sections.add(section_id)
            content_func()
        else:
            st.info("Click to expand and load content")


@cache_result(prefix="lazy_computation", ttl=600)
def lazy_compute(computation_id: str, compute_func: Callable) -> Any:
    """Perform lazy computation with caching."""
    with PerformanceContext(f"lazy_compute_{computation_id}"):
        return compute_func()
