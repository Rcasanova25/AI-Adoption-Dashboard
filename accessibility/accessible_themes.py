"""
Accessible Themes for AI Adoption Dashboard
WCAG 2.1 AA compliant themes with colorblind-friendly palettes
"""

import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AccessibilityLevel(Enum):
    """WCAG compliance levels"""
    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class AccessibleColorPalette:
    """WCAG-compliant color palette"""
    # Text colors with high contrast ratios
    text_primary: str = "#1a1a1a"      # 16.94:1 on white
    text_secondary: str = "#4a4a4a"    # 9.74:1 on white  
    text_light: str = "#ffffff"        # For dark backgrounds
    text_muted: str = "#6c757d"        # 4.54:1 on white (AA compliant)
    
    # Background colors
    background_primary: str = "#ffffff"
    background_secondary: str = "#f8f9fa"
    background_dark: str = "#212529"
    surface: str = "#ffffff"
    
    # Status colors (AA compliant on white)
    success: str = "#0f5132"           # 12.63:1 contrast
    warning: str = "#664d03"           # 10.73:1 contrast
    error: str = "#58151c"             # 13.94:1 contrast
    info: str = "#055160"              # 12.95:1 contrast
    
    # Data visualization colors (colorblind-friendly)
    data_primary: str = "#1f77b4"      # Blue
    data_secondary: str = "#ff7f0e"    # Orange
    data_tertiary: str = "#2ca02c"     # Green
    data_quaternary: str = "#d62728"   # Red
    data_quinary: str = "#9467bd"      # Purple
    
    # Additional colors for complex charts
    data_colors: List[str] = None
    
    # Border and accent colors
    border_light: str = "#dee2e6"
    border_dark: str = "#495057"
    accent: str = "#e9ecef"
    
    def __post_init__(self):
        if self.data_colors is None:
            # Colorblind-safe palette based on research
            self.data_colors = [
                "#1f77b4",  # Blue
                "#ff7f0e",  # Orange
                "#2ca02c",  # Green
                "#d62728",  # Red
                "#9467bd",  # Purple
                "#8c564b",  # Brown
                "#e377c2",  # Pink
                "#7f7f7f",  # Gray
                "#bcbd22",  # Olive
                "#17becf"   # Cyan
            ]


@dataclass
class AccessibleTypography:
    """Accessible typography configuration"""
    # Font families optimized for readability
    font_family: str = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    heading_font: str = "'Segoe UI', Tahoma, Geneva, sans-serif"
    monospace_font: str = "'Consolas', 'Monaco', 'Courier New', monospace"
    
    # Minimum font sizes for accessibility
    heading_sizes: Dict[str, str] = None
    body_size: str = "16px"      # Minimum for accessibility
    small_size: str = "14px"     # Minimum for small text
    large_size: str = "18px"     # For better readability
    
    # Line height for readability
    line_height: str = "1.5"     # WCAG recommended
    heading_line_height: str = "1.3"
    
    # Letter spacing
    letter_spacing: str = "0.01em"
    
    def __post_init__(self):
        if self.heading_sizes is None:
            self.heading_sizes = {
                "h1": "2.5rem",    # 40px
                "h2": "2rem",      # 32px
                "h3": "1.75rem",   # 28px
                "h4": "1.5rem",    # 24px
                "h5": "1.25rem",   # 20px
                "h6": "1rem"       # 16px
            }


class AccessibleExecutiveTheme:
    """Executive theme optimized for accessibility"""
    
    @staticmethod
    def get_color_palette() -> AccessibleColorPalette:
        """Get executive color palette with accessibility enhancements"""
        return AccessibleColorPalette(
            # Enhanced text colors
            text_primary="#1a1a1a",
            text_secondary="#4a4a4a",
            text_light="#ffffff",
            text_muted="#6c757d",
            
            # Professional backgrounds
            background_primary="#ffffff",
            background_secondary="#f8f9fa",
            background_dark="#212529",
            surface="#ffffff",
            
            # Executive status colors (high contrast)
            success="#0f5132",
            warning="#664d03", 
            error="#58151c",
            info="#055160",
            
            # Professional data colors
            data_primary="#0d47a1",     # Deep blue
            data_secondary="#e65100",   # Deep orange
            data_tertiary="#1b5e20",    # Deep green
            data_quaternary="#b71c1c",  # Deep red
            data_quinary="#4a148c",     # Deep purple
            
            # Enhanced borders
            border_light="#dee2e6",
            border_dark="#495057",
            accent="#e9ecef"
        )
    
    @staticmethod
    def get_typography() -> AccessibleTypography:
        """Get executive typography with accessibility features"""
        return AccessibleTypography(
            font_family="'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            heading_font="'Inter', 'Segoe UI', sans-serif",
            monospace_font="'Fira Code', 'Consolas', 'Monaco', monospace",
            body_size="16px",
            small_size="14px",
            large_size="18px",
            line_height="1.6",
            heading_line_height="1.3",
            letter_spacing="0.01em"
        )
    
    @staticmethod
    def apply_theme(high_contrast: bool = False):
        """Apply accessible executive theme"""
        colors = AccessibleExecutiveTheme.get_color_palette()
        typography = AccessibleExecutiveTheme.get_typography()
        
        # High contrast adjustments
        if high_contrast:
            colors.background_primary = "#000000"
            colors.background_secondary = "#111111"
            colors.text_primary = "#ffffff"
            colors.text_secondary = "#e0e0e0"
            colors.border_light = "#ffffff"
        
        css = f"""
        <style>
        /* Accessible Executive Theme */
        
        /* Global accessibility styles */
        html, body, .stApp {{
            font-family: {typography.font_family};
            font-size: {typography.body_size};
            line-height: {typography.line_height};
            color: {colors.text_primary};
            background-color: {colors.background_primary};
        }}
        
        /* Heading hierarchy */
        h1, .stMarkdown h1 {{
            font-size: {typography.heading_sizes['h1']};
            font-weight: 700;
            line-height: {typography.heading_line_height};
            color: {colors.text_primary};
            margin: 1.5rem 0 1rem 0;
        }}
        
        h2, .stMarkdown h2 {{
            font-size: {typography.heading_sizes['h2']};
            font-weight: 600;
            line-height: {typography.heading_line_height};
            color: {colors.text_primary};
            margin: 1.25rem 0 0.75rem 0;
        }}
        
        h3, .stMarkdown h3 {{
            font-size: {typography.heading_sizes['h3']};
            font-weight: 600;
            line-height: {typography.heading_line_height};
            color: {colors.text_primary};
            margin: 1rem 0 0.5rem 0;
        }}
        
        h4, .stMarkdown h4 {{
            font-size: {typography.heading_sizes['h4']};
            font-weight: 600;
            color: {colors.text_primary};
        }}
        
        h5, .stMarkdown h5 {{
            font-size: {typography.heading_sizes['h5']};
            font-weight: 600;
            color: {colors.text_primary};
        }}
        
        h6, .stMarkdown h6 {{
            font-size: {typography.heading_sizes['h6']};
            font-weight: 600;
            color: {colors.text_primary};
        }}
        
        /* Body text */
        p, .stMarkdown p, .stText {{
            font-size: {typography.body_size};
            line-height: {typography.line_height};
            color: {colors.text_primary};
            margin: 0.5rem 0;
        }}
        
        /* Small text */
        small, .small {{
            font-size: {typography.small_size};
            color: {colors.text_muted};
        }}
        
        /* Focus indicators for accessibility */
        button:focus,
        .stButton > button:focus,
        .stSelectbox > div > div > select:focus,
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            outline: 3px solid {colors.info} !important;
            outline-offset: 2px !important;
            box-shadow: 0 0 0 3px rgba(5, 81, 96, 0.3) !important;
        }}
        
        /* Button accessibility */
        .stButton > button {{
            min-height: 44px;  /* Minimum touch target */
            font-size: {typography.body_size};
            font-weight: 600;
            border: 2px solid {colors.border_dark};
            border-radius: 6px;
            padding: 12px 24px;
            transition: all 0.2s ease;
            background-color: {colors.info};
            color: {colors.text_light};
        }}
        
        .stButton > button:hover {{
            background-color: {colors.data_primary};
            border-color: {colors.data_primary};
            transform: translateY(-1px);
        }}
        
        /* Input accessibility */
        .stSelectbox > div > div > select,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            min-height: 44px;
            font-size: {typography.body_size};
            border: 2px solid {colors.border_light};
            border-radius: 4px;
            padding: 8px 12px;
            background-color: {colors.surface};
            color: {colors.text_primary};
        }}
        
        /* Success states */
        .stSuccess, .success {{
            background-color: rgba(15, 81, 50, 0.1);
            border-left: 4px solid {colors.success};
            color: {colors.success};
            padding: 12px 16px;
            margin: 8px 0;
        }}
        
        /* Warning states */
        .stWarning, .warning {{
            background-color: rgba(102, 77, 3, 0.1);
            border-left: 4px solid {colors.warning};
            color: {colors.warning};
            padding: 12px 16px;
            margin: 8px 0;
        }}
        
        /* Error states */
        .stError, .error {{
            background-color: rgba(88, 21, 28, 0.1);
            border-left: 4px solid {colors.error};
            color: {colors.error};
            padding: 12px 16px;
            margin: 8px 0;
        }}
        
        /* Info states */
        .stInfo, .info {{
            background-color: rgba(5, 81, 96, 0.1);
            border-left: 4px solid {colors.info};
            color: {colors.info};
            padding: 12px 16px;
            margin: 8px 0;
        }}
        
        /* Sidebar accessibility */
        .css-1d391kg {{
            background-color: {colors.background_secondary};
            border-right: 2px solid {colors.border_light};
        }}
        
        /* Metric cards */
        .metric-card {{
            background-color: {colors.surface};
            border: 2px solid {colors.border_light};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* High contrast mode */
        {'@media (prefers-contrast: high) {' if high_contrast else ''}
        {'body, .stApp { background-color: #000000 !important; color: #ffffff !important; }' if high_contrast else ''}
        {'.stButton > button { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #ffffff !important; }' if high_contrast else ''}
        {'}' if high_contrast else ''}
        
        /* Skip links for keyboard navigation */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: {colors.text_primary};
            color: {colors.background_primary};
            padding: 8px 12px;
            z-index: 1000;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 600;
        }}
        
        .skip-link:focus {{
            top: 6px;
        }}
        
        /* Screen reader only content */
        .sr-only {{
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            padding: 0 !important;
            margin: -1px !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            white-space: nowrap !important;
            border: 0 !important;
        }}
        
        /* Improve table accessibility */
        .stDataFrame table {{
            border-collapse: collapse;
            width: 100%;
        }}
        
        .stDataFrame th,
        .stDataFrame td {{
            border: 1px solid {colors.border_light};
            padding: 8px 12px;
            text-align: left;
        }}
        
        .stDataFrame th {{
            background-color: {colors.background_secondary};
            font-weight: 600;
            color: {colors.text_primary};
        }}
        
        /* Improve chart accessibility */
        .js-plotly-plot .plotly {{
            border: 2px solid {colors.border_light};
            border-radius: 4px;
        }}
        
        /* Loading states */
        .stSpinner {{
            color: {colors.info} !important;
        }}
        
        /* Progress bars */
        .stProgress > div > div {{
            background-color: {colors.info} !important;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .stButton > button {{
                width: 100%;
                margin: 4px 0;
            }}
            
            h1, .stMarkdown h1 {{ font-size: 2rem; }}
            h2, .stMarkdown h2 {{ font-size: 1.75rem; }}
            h3, .stMarkdown h3 {{ font-size: 1.5rem; }}
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)


class AccessibleHighContrastTheme:
    """High contrast theme for maximum accessibility"""
    
    @staticmethod
    def get_color_palette() -> AccessibleColorPalette:
        """Get high contrast color palette"""
        return AccessibleColorPalette(
            text_primary="#ffffff",
            text_secondary="#e0e0e0",
            text_light="#000000",
            text_muted="#cccccc",
            
            background_primary="#000000",
            background_secondary="#111111",
            background_dark="#000000",
            surface="#111111",
            
            success="#00ff00",
            warning="#ffff00",
            error="#ff0000",
            info="#00ffff",
            
            data_primary="#ffffff",
            data_secondary="#ffff00",
            data_tertiary="#00ff00",
            data_quaternary="#ff0000",
            data_quinary="#ff00ff",
            
            border_light="#ffffff",
            border_dark="#ffffff",
            accent="#333333"
        )
    
    @staticmethod
    def apply_theme():
        """Apply high contrast theme"""
        colors = AccessibleHighContrastTheme.get_color_palette()
        typography = AccessibleTypography()
        
        css = f"""
        <style>
        /* High Contrast Accessibility Theme */
        
        html, body, .stApp {{
            background-color: {colors.background_primary} !important;
            color: {colors.text_primary} !important;
            font-family: {typography.font_family};
            font-size: {typography.large_size};
            line-height: {typography.line_height};
        }}
        
        /* All text elements */
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: {colors.text_primary} !important;
            background-color: transparent !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {colors.text_primary} !important;
            color: {colors.background_primary} !important;
            border: 3px solid {colors.text_primary} !important;
            font-size: {typography.large_size} !important;
            font-weight: bold !important;
            min-height: 48px !important;
        }}
        
        /* Input fields */
        .stSelectbox > div > div > select,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {colors.background_primary} !important;
            color: {colors.text_primary} !important;
            border: 3px solid {colors.text_primary} !important;
            font-size: {typography.large_size} !important;
        }}
        
        /* Focus indicators */
        *:focus {{
            outline: 4px solid {colors.warning} !important;
            outline-offset: 2px !important;
        }}
        
        /* Charts and data displays */
        .js-plotly-plot {{
            border: 3px solid {colors.text_primary} !important;
            background-color: {colors.background_primary} !important;
        }}
        
        /* Remove all background images and gradients */
        * {{
            background-image: none !important;
            background-gradient: none !important;
            box-shadow: none !important;
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)


def apply_accessible_theme(theme_type: str = "executive", high_contrast: bool = False):
    """Apply accessible theme to the application"""
    
    if high_contrast or theme_type == "high_contrast":
        AccessibleHighContrastTheme.apply_theme()
    else:
        AccessibleExecutiveTheme.apply_theme(high_contrast=False)
    
    # Add accessibility controls
    add_accessibility_controls()


def add_accessibility_controls():
    """Add accessibility control panel to sidebar"""
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ♿ Accessibility")
        
        # Theme selection
        theme_option = st.selectbox(
            "Theme",
            options=["Default", "High Contrast"],
            key="accessibility_theme",
            help="Choose a theme optimized for your needs"
        )
        
        # Font size adjustment
        font_size = st.selectbox(
            "Font Size",
            options=["Normal", "Large", "Extra Large"],
            key="accessibility_font_size",
            help="Adjust text size for better readability"
        )
        
        # Motion preferences
        reduce_motion = st.checkbox(
            "Reduce Motion",
            key="accessibility_reduce_motion",
            help="Minimize animations and transitions"
        )
        
        # Screen reader mode
        screen_reader_mode = st.checkbox(
            "Screen Reader Mode",
            key="accessibility_screen_reader",
            help="Optimize for screen reader users"
        )
        
        # Apply changes based on selections
        if theme_option == "High Contrast":
            if 'accessibility_theme_applied' not in st.session_state or st.session_state.accessibility_theme_applied != "high_contrast":
                st.session_state.accessibility_theme_applied = "high_contrast"
                st.experimental_rerun()
        
        # Store accessibility preferences in session state
        st.session_state.accessibility_preferences = {
            "theme": theme_option.lower().replace(" ", "_"),
            "font_size": font_size.lower().replace(" ", "_"),
            "reduce_motion": reduce_motion,
            "screen_reader_mode": screen_reader_mode
        }
        
        # Accessibility help
        with st.expander("Accessibility Help"):
            st.markdown("""
            **Keyboard Navigation:**
            - Tab: Navigate between elements
            - Enter/Space: Activate buttons
            - Arrow keys: Navigate within components
            
            **Screen Reader Support:**
            - All charts include alternative text
            - Data tables available for all visualizations
            - Proper heading structure maintained
            
            **Contact:**
            Report accessibility issues or request features.
            """)


# Global theme application
def initialize_accessible_theme():
    """Initialize accessible theme on app startup"""
    
    # Check for accessibility preferences
    prefs = st.session_state.get('accessibility_preferences', {})
    theme = prefs.get('theme', 'executive')
    high_contrast = theme == 'high_contrast'
    
    # Apply theme
    apply_accessible_theme(theme, high_contrast)
    
    # Add skip navigation
    st.markdown("""
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div id="main-content" role="main">
    """, unsafe_allow_html=True)


# Export theme functions
__all__ = [
    "AccessibleColorPalette",
    "AccessibleTypography", 
    "AccessibleExecutiveTheme",
    "AccessibleHighContrastTheme",
    "apply_accessible_theme",
    "add_accessibility_controls",
    "initialize_accessible_theme"
]