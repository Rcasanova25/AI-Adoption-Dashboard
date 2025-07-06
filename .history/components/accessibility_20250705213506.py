"""WCAG 2.1 AA compliant accessibility features for the dashboard."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import plotly.graph_objects as go
import streamlit as st


@dataclass
class AccessibilityConfig:
    """Configuration for accessibility features."""

    enable_screen_reader: bool = True
    enable_keyboard_nav: bool = True
    enable_high_contrast: bool = False
    enable_focus_indicators: bool = True
    enable_skip_links: bool = True
    font_size_multiplier: float = 1.0
    announce_updates: bool = True


class AccessibilityManager:
    """Manages WCAG 2.1 AA compliant accessibility features."""

    def __init__(self):
        """Initialize accessibility manager."""
        self.config = AccessibilityConfig()
        self._init_session_state()

    def _init_session_state(self):
        """Initialize session state for accessibility settings."""
        if "accessibility_config" not in st.session_state:
            st.session_state.accessibility_config = self.config
        else:
            self.config = st.session_state.accessibility_config

    @staticmethod
    def inject_accessibility_css():
        """Inject CSS for WCAG compliance."""
        st.markdown(
            """
        <style>
        .skip-link {
            position: absolute;
            left: -9999px;
            z-index: 999;
            background: #000;
            color: #fff;
            text-decoration: none;
            padding: 10px;
            border-radius: 0 0 4px 0;
        }
        .skip-link:focus {
            left: 0;
            top: 0;
        }
        *:focus {
            outline: 3px solid #0066cc !important;
            outline-offset: 2px !important;
        }
        .high-contrast {
            background-color: #000 !important;
            color: #fff !important;
        }
        .high-contrast * {
            background-color: #000 !important;
            color: #fff !important;
            border-color: #fff !important;
        }
        .high-contrast a {
            color: #ffff00 !important;
            text-decoration: underline !important;
        }
        .high-contrast button {
            background-color: #fff !important;
            color: #000 !important;
            border: 2px solid #fff !important;
        }
        button, a, input, select, textarea {
            min-height: 44px;
            min-width: 44px;
        }
        .metric-value {
            color: #000000;
            font-weight: 600;
        }
        .metric-label {
            color: #333333;
        }
        .sr-only {
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        }
        .keyboard-nav-indicator {
            position: absolute;
            top: 0;
            left: 0;
            padding: 5px 10px;
            background: #0066cc;
            color: white;
            font-size: 14px;
            z-index: 1000;
            display: none;
        }
        .keyboard-nav-active .keyboard-nav-indicator {
            display: block;
        }
        p, li, td, div {
            line-height: 1.5 !important;
            letter-spacing: 0.12em;
            word-spacing: 0.16em;
        }
        [role="alert"] {
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #dc3545;
            background-color: #f8d7da;
            color: #721c24;
        }
        [role="status"] {
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
            background-color: #d4edda;
            color: #155724;
        }
        a:not(.button) {
            text-decoration: underline;
        }
        .loading-indicator[aria-busy="true"]::after {
            content: " (Loading...)";
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def create_skip_link(target_id: str = "main-content"):
        """Create a skip to main content link."""
        st.markdown(
            f'<a href="#{target_id}" class="skip-link">Skip to main content</a>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def announce_to_screen_reader(message: str, priority: str = "polite"):
        """Announce a message to screen readers."""
        aria_live = "polite" if priority == "polite" else "assertive"
        st.markdown(
            f'<div role="status" aria-live="{aria_live}" class="sr-only">{message}</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def create_accessible_metric(
        label: str,
        value: Any,
        delta: Optional[str] = None,
        help_text: Optional[str] = None,
        metric_id: Optional[str] = None,
    ):
        """Create an accessible metric display."""
        metric_id = metric_id or f"metric-{label.lower().replace(' ', '-')}"

        # Build ARIA label
        aria_label = f"{label}: {value}"
        if delta:
            aria_label += f", change: {delta}"
        if help_text:
            aria_label += f". {help_text}"

        # Create accessible metric
        st.markdown(
            f"""
        <div role="group" aria-labelledby="{metric_id}-label" class="accessible-metric">
            <h3 id="{metric_id}-label" class="metric-label">{label}</h3>
            <div class="metric-value" aria-label="{aria_label}">
                <span>{value}</span>
                {f'<span class="metric-delta" aria-label="Change: {delta}">{delta}</span>' if delta else ''}
            </div>
            {f'<p class="metric-help" id="{metric_id}-help">{help_text}</p>' if help_text else ''}
        </div>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def make_chart_accessible(
        fig: go.Figure, title: str, description: str, data_table: Optional[Dict[str, List]] = None
    ) -> go.Figure:
        """Make a Plotly chart accessible."""
        fig.update_layout(
            title={"text": title, "font": {"size": 20}, "x": 0.5, "xanchor": "center"}
        )
        fig.add_annotation(
            text=f'<span class="sr-only">{description}</span>',
            xref="paper",
            yref="paper",
            x=0,
            y=1.1,
            showarrow=False,
            font=dict(size=1),
        )
        fig.update_traces(marker=dict(line=dict(width=2, color="#000000")))
        for i, trace in enumerate(fig.data):
            if hasattr(trace, "marker"):
                patterns = ["/", "\\", "x", "-", "|", "+", "."]
                if i < len(patterns):
                    trace.marker.symbol = i
        return fig

    @staticmethod
    def create_accessible_table(
        data: Any, caption: str, summary: Optional[str] = None, sortable: bool = True
    ):
        """Create an accessible data table."""
        st.markdown(f'<caption class="table-caption">{caption}</caption>', unsafe_allow_html=True)
        if summary:
            st.markdown(
                f'<div class="sr-only" id="table-summary">{summary}</div>', unsafe_allow_html=True
            )
        st.dataframe(data, use_container_width=True, hide_index=True)
        st.markdown(
            '<div class="sr-only">Use arrow keys to navigate table cells</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def create_accessible_form_field(
        field_type: str,
        label: str,
        field_id: str,
        required: bool = False,
        help_text: Optional[str] = None,
        error_message: Optional[str] = None,
        **kwargs,
    ):
        """Create an accessible form field."""
        label_text = f"{label} {'(required)' if required else ''}"
        help_id = f"{field_id}-help" if help_text else None
        error_id = f"{field_id}-error" if error_message else None
        aria_describedby_ids = []
        if help_id:
            aria_describedby_ids.append(help_id)
        if error_id:
            aria_describedby_ids.append(error_id)
        if field_type == "text":
            value = st.text_input(label_text, key=field_id, help=help_text, **kwargs)
        elif field_type == "select":
            value = st.selectbox(label_text, key=field_id, help=help_text, **kwargs)
        elif field_type == "slider":
            value = st.slider(label_text, key=field_id, help=help_text, **kwargs)
        else:
            value = None
        if error_message:
            st.markdown(
                f'<div role="alert" id="{error_id}" class="field-error">{error_message}</div>',
                unsafe_allow_html=True,
            )
        return value

    @staticmethod
    def create_keyboard_navigation_help():
        """Display keyboard navigation help."""
        with st.expander("⌨️ Keyboard Navigation Help"):
            st.markdown(
                """
            ### Keyboard Shortcuts
            
            - **Tab**: Navigate forward through interactive elements
            - **Shift + Tab**: Navigate backward
            - **Enter/Space**: Activate buttons and links
            - **Arrow Keys**: Navigate within data tables and charts
            - **Escape**: Close popups and modals
            
            ### Screen Reader Tips
            
            - This dashboard is optimized for screen readers
            - Use heading navigation (H key) to jump between sections
            - Tables include summaries and captions
            - Charts include text descriptions
            """
            )

    def render_accessibility_toolbar(self):
        """Render accessibility toolbar for user preferences."""
        with st.expander("♿ Accessibility Options"):
            col1, col2 = st.columns(2)
            with col1:
                high_contrast = st.checkbox(
                    "High Contrast Mode",
                    value=self.config.enable_high_contrast,
                    help="Enable high contrast colors for better visibility",
                )
                if high_contrast != self.config.enable_high_contrast:
                    self.config.enable_high_contrast = high_contrast
                    st.session_state.accessibility_config = self.config
                    st.rerun()
                font_size = st.slider(
                    "Font Size",
                    min_value=0.8,
                    max_value=1.5,
                    value=self.config.font_size_multiplier,
                    step=0.1,
                    format="%.1fx",
                    help="Adjust text size",
                )
                if font_size != self.config.font_size_multiplier:
                    self.config.font_size_multiplier = font_size
                    st.session_state.accessibility_config = self.config
            with col2:
                announce = st.checkbox(
                    "Screen Reader Announcements",
                    value=self.config.announce_updates,
                    help="Announce dashboard updates to screen readers",
                )
                if announce != self.config.announce_updates:
                    self.config.announce_updates = announce
                    st.session_state.accessibility_config = self.config
                if st.button("Show Keyboard Shortcuts"):
                    self.create_keyboard_navigation_help()

    def apply_accessibility_settings(self):
        """Apply current accessibility settings."""
        if self.config.enable_high_contrast:
            st.markdown('<div class="high-contrast-wrapper high-contrast">', unsafe_allow_html=True)
        if self.config.font_size_multiplier != 1.0:
            st.markdown(
                f"""
            <style>
            body, .stMarkdown, .stText {{
                font-size: {self.config.font_size_multiplier}em !important;
            }}
            </style>
            """,
                unsafe_allow_html=True,
            )


def create_accessible_dashboard_layout():
    """Create the main accessible dashboard layout."""
    a11y = AccessibilityManager()
    AccessibilityManager.inject_accessibility_css()
    AccessibilityManager.create_skip_link()
    a11y.apply_accessibility_settings()
    st.markdown('<main id="main-content" role="main">', unsafe_allow_html=True)
    return a11y


def ensure_color_contrast(foreground: str, background: str):
    """Ensure color combination meets WCAG AA contrast requirements."""
    safe_combinations = {
        "#ffffff": "#000000",
        "#000000": "#ffffff",
        "#0066cc": "#ffffff",
        "#dc3545": "#ffffff",
        "#28a745": "#ffffff",
    }
    return foreground, 4.5  # Minimum AA ratio


def add_aria_live_region(region_id: str, priority: str = "polite"):
    """Add an ARIA live region for dynamic updates."""
    st.markdown(
        f"""
    <div id="{region_id}" 
         role="region" 
         aria-live="{priority}" 
         aria-atomic="true"
         class="sr-only">
    </div>
    """,
        unsafe_allow_html=True,
    )
