"""Progressive disclosure system for managing information complexity."""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from components.accessibility import AccessibilityManager


class DisclosureLevel(Enum):
    """Information disclosure levels."""
    EXECUTIVE = "executive"  # High-level summary only
    STANDARD = "standard"    # Key metrics and insights
    DETAILED = "detailed"    # Full analysis with all data


class ProgressiveDisclosure:
    """Manages progressive disclosure of information based on user needs."""
    
    def __init__(self):
        """Initialize progressive disclosure system."""
        # Initialize session state
        if 'disclosure_level' not in st.session_state:
            st.session_state.disclosure_level = DisclosureLevel.STANDARD
        
        if 'expanded_sections' not in st.session_state:
            st.session_state.expanded_sections = set()
    
    def set_level(self, level: DisclosureLevel):
        """Set the global disclosure level."""
        st.session_state.disclosure_level = level
    
    def get_level(self) -> DisclosureLevel:
        """Get current disclosure level."""
        return st.session_state.disclosure_level
    
    def render_level_selector(self):
        """Render the disclosure level selector in the sidebar."""
        st.sidebar.markdown("### 📊 Information Detail Level")
        
        level_descriptions = {
            DisclosureLevel.EXECUTIVE: "Executive Summary - Key insights only",
            DisclosureLevel.STANDARD: "Standard View - Balanced detail",
            DisclosureLevel.DETAILED: "Deep Dive - All available data"
        }
        
        # Create radio buttons with descriptions
        current_level = st.session_state.disclosure_level
        
        # Add ARIA label for screen readers
        st.sidebar.markdown(
            '<div role="group" aria-label="Information detail level selector">',
            unsafe_allow_html=True
        )
        
        for level in DisclosureLevel:
            button_label = level_descriptions[level]
            is_selected = level == current_level
            
            if st.sidebar.button(
                button_label,
                key=f"level_{level.value}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                help=f"{'Currently selected' if is_selected else 'Click to select'} {level.value} view"
            ):
                self.set_level(level)
                # Announce change to screen readers
                AccessibilityManager.announce_to_screen_reader(
                    f"View changed to {level.value} level"
                )
                st.rerun()
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Add visual indicator with ARIA label
        st.sidebar.info(f"Currently viewing: **{current_level.value.title()} Level**")
    
    def progressive_container(
        self,
        title: str,
        content_levels: Dict[DisclosureLevel, Callable],
        key: str,
        expanded_by_default: bool = False,
        show_always: bool = False
    ):
        """Create a progressive disclosure container.
        
        Args:
            title: Section title
            content_levels: Dict mapping disclosure levels to content rendering functions
            key: Unique key for this section
            expanded_by_default: Whether to expand by default
            show_always: Whether to show regardless of level
        """
        current_level = self.get_level()
        
        # Determine if this section should be shown
        if not show_always and current_level == DisclosureLevel.EXECUTIVE:
            # In executive mode, only show if content is provided for executive level
            if DisclosureLevel.EXECUTIVE not in content_levels:
                return
        
        # Determine if section is expanded
        is_expanded = key in st.session_state.expanded_sections or expanded_by_default
        
        # Create expandable section
        col1, col2 = st.columns([20, 1])
        
        with col1:
            if st.button(
                f"{'▼' if is_expanded else '▶'} {title}",
                key=f"toggle_{key}",
                use_container_width=True,
                type="secondary"
            ):
                if is_expanded:
                    st.session_state.expanded_sections.discard(key)
                else:
                    st.session_state.expanded_sections.add(key)
                st.rerun()
        
        with col2:
            # Level indicator
            if current_level == DisclosureLevel.EXECUTIVE:
                st.markdown("🎯")
            elif current_level == DisclosureLevel.STANDARD:
                st.markdown("📊")
            else:
                st.markdown("🔍")
        
        # Render content if expanded
        if is_expanded:
            with st.container():
                # Get appropriate content function
                if current_level in content_levels:
                    content_levels[current_level]()
                else:
                    # Fallback to nearest available level
                    for level in [DisclosureLevel.STANDARD, DisclosureLevel.DETAILED, DisclosureLevel.EXECUTIVE]:
                        if level in content_levels:
                            content_levels[level]()
                            break
    
    def auto_disclosure(
        self,
        executive_content: Optional[Callable] = None,
        standard_content: Optional[Callable] = None,
        detailed_content: Optional[Callable] = None
    ):
        """Automatically render content based on current disclosure level.
        
        Args:
            executive_content: Function to render executive summary
            standard_content: Function to render standard view
            detailed_content: Function to render detailed view
        """
        current_level = self.get_level()
        
        content_map = {
            DisclosureLevel.EXECUTIVE: executive_content,
            DisclosureLevel.STANDARD: standard_content,
            DisclosureLevel.DETAILED: detailed_content
        }
        
        # Render appropriate content
        content_func = content_map.get(current_level)
        if content_func:
            content_func()
        else:
            # Fallback logic
            if current_level == DisclosureLevel.EXECUTIVE and standard_content:
                standard_content()
            elif current_level == DisclosureLevel.STANDARD and detailed_content:
                detailed_content()
            else:
                st.warning("No content available for this detail level")
    
    @staticmethod
    def create_summary_card(
        title: str,
        metric: str,
        delta: Optional[str] = None,
        description: Optional[str] = None,
        color: str = "blue"
    ):
        """Create a summary card for executive level display.
        
        Args:
            title: Card title
            metric: Main metric value
            delta: Change indicator
            description: Brief description
            color: Card accent color
        """
        color_map = {
            "blue": "#1f77b4",
            "green": "#28a745",
            "red": "#dc3545",
            "yellow": "#ffc107",
            "gray": "#6c757d"
        }
        
        accent_color = color_map.get(color, color_map["blue"])
        
        st.markdown(f"""
        <div style='background-color: #f8f9fa; border-left: 4px solid {accent_color}; 
                    padding: 20px; margin: 10px 0; border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0; color: #495057;'>{title}</h4>
            <h2 style='margin: 10px 0; color: {accent_color};'>{metric}</h2>
            {f"<p style='margin: 5px 0; color: #6c757d;'>{delta}</p>" if delta else ""}
            {f"<p style='margin: 5px 0; font-size: 14px; color: #6c757d;'>{description}</p>" if description else ""}
        </div>
        """, unsafe_allow_html=True)
    
    def render_key_metrics(self, metrics: List[Dict[str, Any]], columns: int = 3):
        """Render key metrics in a grid layout.
        
        Args:
            metrics: List of metric dictionaries with keys: title, value, delta, color
            columns: Number of columns for layout
        """
        cols = st.columns(columns)
        
        for idx, metric in enumerate(metrics):
            with cols[idx % columns]:
                if self.get_level() == DisclosureLevel.EXECUTIVE:
                    # Simplified view for executives
                    self.create_summary_card(
                        title=metric.get('title', ''),
                        metric=metric.get('value', ''),
                        delta=metric.get('delta'),
                        description=metric.get('description'),
                        color=metric.get('color', 'blue')
                    )
                else:
                    # Standard metric display
                    st.metric(
                        label=metric.get('title', ''),
                        value=metric.get('value', ''),
                        delta=metric.get('delta'),
                        help=metric.get('help')
                    )
    
    def should_show_details(self) -> bool:
        """Check if detailed information should be shown."""
        return self.get_level() in [DisclosureLevel.STANDARD, DisclosureLevel.DETAILED]
    
    def should_show_advanced(self) -> bool:
        """Check if advanced/technical information should be shown."""
        return self.get_level() == DisclosureLevel.DETAILED


class CollapsibleSection:
    """Helper class for creating collapsible sections."""
    
    @staticmethod
    def render(
        title: str,
        content: Callable,
        key: str,
        expanded: bool = False,
        show_indicator: bool = True
    ):
        """Render a collapsible section.
        
        Args:
            title: Section title
            content: Function that renders the content
            key: Unique key for the section
            expanded: Whether to expand by default
            show_indicator: Whether to show expand/collapse indicator
        """
        # Use session state to track expansion
        state_key = f"collapsed_{key}"
        if state_key not in st.session_state:
            st.session_state[state_key] = expanded
        
        # Create header with toggle
        col1, col2 = st.columns([20, 1]) if show_indicator else [st.columns(1)[0], None]
        
        with col1:
            if st.button(
                f"{'▼' if st.session_state[state_key] else '▶'} {title}",
                key=f"toggle_{key}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state[state_key] = not st.session_state[state_key]
                st.rerun()
        
        # Render content if expanded
        if st.session_state[state_key]:
            with st.container():
                content()


class InformationDensityController:
    """Controls information density based on user preferences."""
    
    @staticmethod
    def filter_dataframe(
        df,
        max_rows_executive: int = 5,
        max_rows_standard: int = 10,
        max_rows_detailed: int = None
    ):
        """Filter dataframe rows based on disclosure level.
        
        Args:
            df: Input dataframe
            max_rows_executive: Max rows for executive view
            max_rows_standard: Max rows for standard view
            max_rows_detailed: Max rows for detailed view (None = all)
        
        Returns:
            Filtered dataframe
        """
        disclosure = ProgressiveDisclosure()
        level = disclosure.get_level()
        
        if level == DisclosureLevel.EXECUTIVE:
            return df.head(max_rows_executive)
        elif level == DisclosureLevel.STANDARD:
            return df.head(max_rows_standard)
        else:
            return df if max_rows_detailed is None else df.head(max_rows_detailed)
    
    @staticmethod
    def simplify_chart(
        fig,
        level: DisclosureLevel,
        simplification_rules: Optional[Dict[str, Any]] = None
    ):
        """Simplify chart based on disclosure level.
        
        Args:
            fig: Plotly figure object
            level: Current disclosure level
            simplification_rules: Custom rules for simplification
        
        Returns:
            Modified figure
        """
        if level == DisclosureLevel.EXECUTIVE:
            # Remove minor gridlines
            fig.update_xaxes(showgrid=False, showticklabels=True)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Simplify annotations
            if hasattr(fig, 'layout') and hasattr(fig.layout, 'annotations'):
                # Keep only major annotations
                pass
            
            # Reduce data points if specified
            if simplification_rules and 'max_points' in simplification_rules:
                # Implement data reduction logic
                pass
        
        return fig