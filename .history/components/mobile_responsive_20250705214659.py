"""Mobile responsive UI components and utilities."""

from typing import Any, Dict, List, Optional, Callable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


class ResponsiveUI:
    """Utilities for creating mobile-responsive UI components."""

    @staticmethod
    def get_device_type() -> str:
        """Detect device type based on viewport width."""
        if "device_type" not in st.session_state:
            st.session_state.device_type = "desktop"

        # JavaScript for device detection
        device_detector = """
        <script>
        function detectDevice() {
            const width = window.innerWidth;
            let deviceType = 'desktop';
            if (width <= 768) {
                deviceType = 'mobile';
            } else if (width <= 1024) {
                deviceType = 'tablet';
            }
            const event = new CustomEvent('streamlit:setComponentValue', {detail: deviceType});
            window.parent.document.dispatchEvent(event);
        }
        window.addEventListener('load', detectDevice);
        window.addEventListener('resize', detectDevice);
        detectDevice();
        </script>
        """

        # Use a hidden component for detection
        components.html(
            device_detector + """
            <div id="device-detector" style="display: none;"></div>
            <script>
                const container = window.parent.document.querySelector('.main');
                if (container) {
                    const width = container.offsetWidth;
                    if (width < 640) {
                        window.parent.postMessage({type: 'device', value: 'mobile'}, '*');
                    } else if (width < 1024) {
                        window.parent.postMessage({type: 'device', value: 'tablet'}, '*');
                    } else {
                        window.parent.postMessage({type: 'device', value: 'desktop'}, '*');
                    }
                }
            </script>
            """,
            height=0,
            scrolling=False,
        )

        # Fallback: sidebar collapsed = mobile
        if "sidebar_state" in st.session_state and st.session_state.sidebar_state == "collapsed":
            return "mobile"
        return st.session_state.get("device_type", "desktop")

    @staticmethod
    def responsive_columns(
        desktop_widths: List[int],
        tablet_widths: Optional[List[int]] = None,
        mobile_widths: Optional[List[int]] = None,
    ) -> List:
        """Create responsive columns based on device type."""
        device = ResponsiveUI.get_device_type()
        if device == "mobile" and mobile_widths:
            return [st.container() for _ in mobile_widths]
        elif device == "tablet" and tablet_widths:
            return st.columns(tablet_widths)
        else:
            return st.columns(desktop_widths)

    @staticmethod
    def responsive_metrics(
        metrics: List[Dict[str, Any]],
        desktop_cols: int = 4,
        tablet_cols: int = 2,
        mobile_cols: int = 1,
    ):
        """Render metrics in a responsive grid."""
        device = ResponsiveUI.get_device_type()
        num_cols = mobile_cols if device == "mobile" else tablet_cols if device == "tablet" else desktop_cols
        for i in range(0, len(metrics), num_cols):
            cols = st.columns(num_cols)
            for j, col in enumerate(cols):
                if i + j < len(metrics):
                    with col:
                        metric = metrics[i + j]
                        st.metric(
                            label=metric.get("label", ""),
                            value=metric.get("value", ""),
                            delta=metric.get("delta"),
                            help=metric.get("help"),
                        )

    @staticmethod
    def mobile_friendly_chart(
        fig: go.Figure, desktop_height: int = 500, mobile_height: int = 300
    ) -> go.Figure:
        """Optimize Plotly chart for mobile viewing."""
        device = ResponsiveUI.get_device_type()
        if device == "mobile":
            fig.update_layout(
                height=mobile_height,
                margin=dict(l=20, r=20, t=40, b=20),
                font=dict(size=10),
                showlegend=False,
                xaxis=dict(tickangle=-45),
            )
            fig.update_traces(hovertemplate="%{y}<extra></extra>")
        else:
            fig.update_layout(height=desktop_height, margin=dict(l=50, r=50, t=50, b=50))
        return fig

    @staticmethod
    def responsive_tabs(tab_labels: List[str], max_mobile_tabs: int = 3) -> List:
        """Create responsive tabs that work well on mobile."""
        device = ResponsiveUI.get_device_type()
        if device == "mobile" and len(tab_labels) > max_mobile_tabs:
            selected_tab = st.selectbox("Select View", tab_labels, key="mobile_tab_select")
            return [st.container() for _ in tab_labels]
        else:
            return st.tabs(tab_labels)

    @staticmethod
    def mobile_navigation_menu():
        """Create mobile-friendly navigation menu."""
        with st.expander("☰ Navigation", expanded=False):
            st.markdown(
                """
            ### Quick Links
            - 🏠 [Home](#home)
            - 📊 [Dashboard](#dashboard)
            - 📈 [Analytics](#analytics)
            - ⚙️ [Settings](#settings)
            """
            )

    @staticmethod
    def responsive_sidebar():
        """Create responsive sidebar that works on mobile."""
        if ResponsiveUI.get_device_type() == "mobile":
            if st.button("☰ Menu", key="mobile_menu"):
                st.session_state.sidebar_expanded = not st.session_state.get("sidebar_expanded", False)
        if st.session_state.get("sidebar_expanded", True):
            with st.sidebar:
                yield
        else:
            yield

    @staticmethod
    def swipe_carousel(items: List[Dict[str, Any]], item_renderer: Callable):
        """Create swipeable carousel for mobile (simulated with buttons)."""
        if "carousel_index" not in st.session_state:
            st.session_state.carousel_index = 0
        col1, col2, col3 = st.columns([1, 8, 1])
        with col1:
            if st.button("◀", key="carousel_prev"):
                st.session_state.carousel_index = max(0, st.session_state.carousel_index - 1)
                st.rerun()
        with col2:
            if items and st.session_state.carousel_index < len(items):
                item_renderer(items[st.session_state.carousel_index])
        with col3:
            if st.button("▶", key="carousel_next"):
                st.session_state.carousel_index = min(
                    len(items) - 1, st.session_state.carousel_index + 1
                )
                st.rerun()
        if items:
            st.markdown(
                f"<center>{st.session_state.carousel_index + 1} / {len(items)}</center>",
                unsafe_allow_html=True,
            )

    @staticmethod
    def touch_friendly_slider(
        label: str,
        min_value: float,
        max_value: float,
        value: float,
        step: float = 1.0,
        key: str = None,
    ) -> float:
        """Create touch-friendly slider with larger touch targets."""
        col1, col2 = st.columns([4, 1])
        with col1:
            value = st.slider(
                label, min_value=min_value, max_value=max_value, value=value, step=step, key=key
            )
        with col2:
            st.markdown(f"<h3 style='text-align: center;'>{value}</h3>", unsafe_allow_html=True)
        return value

    @staticmethod
    def floating_action_button(label: str, icon: str = "🚀", action: Callable = None):
        """Create floating action button for mobile."""
        st.markdown(
            """
        <style>
        .floating-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #1f77b4;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            font-size: 24px;
            z-index: 1000;
            cursor: pointer;
        }
        @media (min-width: 768px) {
            .floating-button { display: none; }
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        button_html = f"""
        <div class='floating-button' title='{label}'>
            {icon}
        </div>
        """
        if st.button(label, key="fab_button"):
            if action:
                action()

    @staticmethod
    def responsive_data_table(
        data: pd.DataFrame,
        desktop_cols: Optional[List[str]] = None,
        mobile_cols: Optional[List[str]] = None,
    ):
        """Display responsive data table."""
        device = ResponsiveUI.get_device_type()
        if device == "mobile" and mobile_cols:
            st.dataframe(data[mobile_cols], use_container_width=True, hide_index=True)
        else:
            cols_to_show = desktop_cols if desktop_cols else data.columns
            st.dataframe(data[cols_to_show], use_container_width=True, hide_index=True)


def inject_mobile_css():
    """Inject CSS for mobile responsiveness."""
    st.markdown(
        """
    <style>
    @media (max-width: 768px) {
        .css-1d391kg { padding: 1rem; }
        h1 { font-size: 1.75rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        [data-testid="metric-container"] { padding: 0.5rem; }
        [data-testid="column"] { width: 100% !important; flex: 100% !important; }
        button { min-height: 44px; min-width: 44px; }
        .dataframe { font-size: 12px; }
        .desktop-only { display: none; }
    }
    @media (min-width: 768px) and (max-width: 1024px) {
        [data-testid="column"] { flex: 50% !important; }
    }
    @media (hover: none) {
        button:active { transform: scale(0.95); }
        .stSlider > div > div { height: 44px; }
    }
    body {
        -webkit-text-size-adjust: 100%;
        text-size-adjust: 100%;
    }
    .main { overflow-x: hidden; }
    .js-plotly-plot { max-width: 100%; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_mobile_menu():
    """Create mobile-optimized menu."""
    menu_items = {
        "🏠 Home": "home",
        "📊 Dashboard": "dashboard",
        "📈 Analytics": "analytics",
        "🔍 Search": "search",
        "⚙️ Settings": "settings",
    }
    st.markdown(
        """
    <style>
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
    }
    .mobile-nav-item {
        text-align: center;
        flex: 1;
        padding: 5px;
        text-decoration: none;
        color: #666;
    }
    .mobile-nav-item.active { color: #1f77b4; }
    @media (min-width: 768px) {
        .mobile-nav { display: none; }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    nav_html = '<div class="mobile-nav">'
    for label, page in menu_items.items():
        nav_html += f'<a href="#{page}" class="mobile-nav-item">{label}</a>'
    nav_html += "</div>"
    st.markdown(nav_html, unsafe_allow_html=True)
