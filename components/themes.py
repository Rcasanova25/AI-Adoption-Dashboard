# components/themes.py - Professional Theme System
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ThemeMode(Enum):
    EXECUTIVE = "executive"
    ANALYST = "analyst"
    PRESENTATION = "presentation"
    DARK = "dark"
    LIGHT = "light"

@dataclass
class ColorPalette:
    """Color palette configuration"""
    primary: str
    secondary: str
    success: str
    warning: str
    error: str
    info: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    border: str
    accent: str

@dataclass
class Typography:
    """Typography configuration"""
    font_family: str
    heading_font: str
    heading_sizes: Dict[str, str]
    body_size: str
    small_size: str
    line_height: str
    letter_spacing: str

@dataclass
class Spacing:
    """Spacing configuration"""
    xs: str = "0.25rem"
    sm: str = "0.5rem"
    md: str = "1rem"
    lg: str = "1.5rem"
    xl: str = "2rem"
    xxl: str = "3rem"

class ExecutiveTheme:
    """Professional executive theme with sophisticated styling"""
    
    @staticmethod
    def get_color_palette() -> ColorPalette:
        return ColorPalette(
            primary="#2E86AB",      # Professional blue
            secondary="#A23B72",    # Executive purple
            success="#6A994E",      # Growth green
            warning="#F18F01",      # Attention orange
            error="#C73E1D",        # Alert red
            info="#4ECDC4",         # Info teal
            background="#FAFBFC",   # Clean background
            surface="#FFFFFF",      # Card surface
            text_primary="#2C3E50", # Dark text
            text_secondary="#6C757D", # Muted text
            border="#E9ECEF",       # Subtle borders
            accent="#F8F9FA"        # Accent color
        )
    
    @staticmethod
    def get_typography() -> Typography:
        return Typography(
            font_family="'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            heading_font="'Inter', 'Segoe UI', sans-serif",
            heading_sizes={
                "h1": "2.5rem",
                "h2": "2rem", 
                "h3": "1.75rem",
                "h4": "1.5rem",
                "h5": "1.25rem",
                "h6": "1rem"
            },
            body_size="1rem",
            small_size="0.875rem",
            line_height="1.6",
            letter_spacing="0.01em"
        )
    
    @staticmethod
    def apply_theme():
        """Apply executive theme to Streamlit app"""
        colors = ExecutiveTheme.get_color_palette()
        typography = ExecutiveTheme.get_typography()
        
        st.markdown(f"""
        <style>
        /* Executive Theme Styles */
        
        /* Global Styles */
        .stApp {{
            background: linear-gradient(135deg, {colors.background} 0%, #F8F9FA 100%);
            font-family: {typography.font_family};
            color: {colors.text_primary};
        }}
        
        /* Header Styles */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {typography.heading_font};
            color: {colors.text_primary};
            font-weight: 600;
            letter-spacing: {typography.letter_spacing};
        }}
        
        h1 {{ font-size: {typography.heading_sizes['h1']}; }}
        h2 {{ font-size: {typography.heading_sizes['h2']}; }}
        h3 {{ font-size: {typography.heading_sizes['h3']}; }}
        h4 {{ font-size: {typography.heading_sizes['h4']}; }}
        h5 {{ font-size: {typography.heading_sizes['h5']}; }}
        h6 {{ font-size: {typography.heading_sizes['h6']}; }}
        
        /* Executive Cards */
        .executive-card {{
            background: {colors.surface};
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid {colors.border};
            margin: 1rem 0;
            transition: all 0.3s ease;
        }}
        
        .executive-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), 0 3px 6px rgba(0, 0, 0, 0.05);
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: {colors.surface};
            border-left: 4px solid {colors.primary};
            border-radius: 8px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {colors.primary};
            margin: 0.25rem 0;
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: {colors.text_secondary};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .metric-delta {{
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 0.25rem;
        }}
        
        .metric-delta.positive {{ color: {colors.success}; }}
        .metric-delta.negative {{ color: {colors.error}; }}
        .metric-delta.neutral {{ color: {colors.text_secondary}; }}
        
        /* Sidebar Styling */
        .css-1d391kg {{
            background: linear-gradient(180deg, {colors.surface} 0%, {colors.accent} 100%);
            border-right: 1px solid {colors.border};
        }}
        
        /* Button Styling */
        .stButton > button {{
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {colors.primary} 0%, #1c5f7f 100%);
            color: white;
            box-shadow: 0 2px 4px rgba(46, 134, 171, 0.3);
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #1c5f7f 0%, {colors.primary} 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(46, 134, 171, 0.4);
        }}
        
        .stButton > button[kind="secondary"] {{
            background: {colors.surface};
            color: {colors.primary};
            border: 2px solid {colors.primary};
        }}
        
        .stButton > button[kind="secondary"]:hover {{
            background: {colors.primary};
            color: white;
            transform: translateY(-1px);
        }}
        
        /* Alert Styles */
        .alert-success {{
            background: linear-gradient(135deg, rgba(106, 153, 78, 0.1) 0%, rgba(106, 153, 78, 0.05) 100%);
            border-left: 4px solid {colors.success};
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}
        
        .alert-warning {{
            background: linear-gradient(135deg, rgba(241, 143, 1, 0.1) 0%, rgba(241, 143, 1, 0.05) 100%);
            border-left: 4px solid {colors.warning};
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}
        
        .alert-error {{
            background: linear-gradient(135deg, rgba(199, 62, 29, 0.1) 0%, rgba(199, 62, 29, 0.05) 100%);
            border-left: 4px solid {colors.error};
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}
        
        .alert-info {{
            background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(78, 205, 196, 0.05) 100%);
            border-left: 4px solid {colors.info};
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}
        
        /* Chart Container Styling */
        .plotly-chart {{
            background: {colors.surface};
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border: 1px solid {colors.border};
        }}
        
        /* Data Table Styling */
        .stDataFrame {{
            background: {colors.surface};
            border-radius: 8px;
            border: 1px solid {colors.border};
            overflow: hidden;
        }}
        
        /* Progress Bar Styling */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, {colors.primary} 0%, {colors.secondary} 100%);
            border-radius: 4px;
        }}
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {colors.accent};
            border-radius: 8px;
            padding: 4px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 3rem;
            border-radius: 6px;
            padding-left: 1rem;
            padding-right: 1rem;
            background: transparent;
            border: none;
            color: {colors.text_secondary};
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: {colors.surface};
            color: {colors.primary};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        /* Input Styling */
        .stSelectbox > div > div {{
            background: {colors.surface};
            border: 1px solid {colors.border};
            border-radius: 6px;
        }}
        
        .stMultiSelect > div > div {{
            background: {colors.surface};
            border: 1px solid {colors.border};
            border-radius: 6px;
        }}
        
        .stSlider > div > div > div {{
            background: {colors.primary};
        }}
        
        /* Executive Dashboard Specific */
        .executive-header {{
            background: linear-gradient(135deg, {colors.primary} 0%, {colors.secondary} 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(46, 134, 171, 0.3);
        }}
        
        .executive-kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .executive-insight {{
            background: {colors.surface};
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            border-left: 6px solid {colors.accent};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
            
            .executive-header {{
                padding: 2rem 1rem;
            }}
            
            .metric-value {{
                font-size: 2rem;
            }}
        }}
        
        /* Animation Classes */
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}
        
        .slide-up {{
            animation: slideUp 0.3s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{ 
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{ 
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Loading States */
        .loading-shimmer {{
            background: linear-gradient(90deg, {colors.accent} 25%, rgba(255,255,255,0.5) 50%, {colors.accent} 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)

class AnalystTheme:
    """Data-focused analyst theme with clean, functional styling"""
    
    @staticmethod
    def get_color_palette() -> ColorPalette:
        return ColorPalette(
            primary="#1f77b4",      # Data blue
            secondary="#ff7f0e",    # Orange accent
            success="#2ca02c",      # Green success
            warning="#ff7f0e",      # Orange warning
            error="#d62728",        # Red error
            info="#17becf",         # Cyan info
            background="#FFFFFF",   # Clean white
            surface="#F8F9FA",      # Light surface
            text_primary="#212529", # Dark text
            text_secondary="#6C757D", # Gray text
            border="#DEE2E6",       # Light borders
            accent="#F1F3F4"        # Light accent
        )
    
    @staticmethod
    def get_typography() -> Typography:
        return Typography(
            font_family="'Roboto', 'Helvetica Neue', Arial, sans-serif",
            heading_font="'Roboto', Arial, sans-serif",
            heading_sizes={
                "h1": "2.25rem",
                "h2": "1.875rem",
                "h3": "1.5rem", 
                "h4": "1.25rem",
                "h5": "1.125rem",
                "h6": "1rem"
            },
            body_size="0.95rem",
            small_size="0.8rem",
            line_height="1.5",
            letter_spacing="normal"
        )
    
    @staticmethod
    def apply_theme():
        """Apply analyst theme to Streamlit app"""
        colors = AnalystTheme.get_color_palette()
        typography = AnalystTheme.get_typography()
        
        st.markdown(f"""
        <style>
        /* Analyst Theme Styles */
        
        .stApp {{
            background: {colors.background};
            font-family: {typography.font_family};
            color: {colors.text_primary};
        }}
        
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 1400px;
        }}
        
        /* Clean, functional styling for data analysis */
        .analyst-card {{
            background: {colors.surface};
            border: 1px solid {colors.border};
            border-radius: 6px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .data-table {{
            font-size: {typography.small_size};
            border-collapse: collapse;
            width: 100%;
        }}
        
        .data-table th {{
            background: {colors.accent};
            padding: 0.75rem;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid {colors.border};
        }}
        
        .data-table td {{
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid {colors.border};
        }}
        
        /* Chart specific styling for analysts */
        .plotly-chart {{
            border: 1px solid {colors.border};
            border-radius: 4px;
        }}
        
        /* Functional button styling */
        .stButton > button {{
            border-radius: 4px;
            font-size: 0.9rem;
            padding: 0.5rem 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)

class DarkTheme:
    """Professional dark theme for low-light environments"""
    
    @staticmethod
    def get_color_palette() -> ColorPalette:
        return ColorPalette(
            primary="#4FC3F7",      # Light blue
            secondary="#AB47BC",    # Purple
            success="#66BB6A",      # Green
            warning="#FFB74D",      # Orange
            error="#EF5350",        # Red
            info="#26C6DA",         # Cyan
            background="#0E1117",   # Dark background
            surface="#262730",      # Dark surface
            text_primary="#FAFAFA", # Light text
            text_secondary="#B0BEC5", # Gray text
            border="#333333",       # Dark borders
            accent="#1E1E1E"        # Dark accent
        )
    
    @staticmethod
    def apply_theme():
        """Apply dark theme to Streamlit app"""
        colors = DarkTheme.get_color_palette()
        
        st.markdown(f"""
        <style>
        /* Dark Theme Styles */
        
        .stApp {{
            background: {colors.background};
            color: {colors.text_primary};
        }}
        
        .main .block-container {{
            background: {colors.background};
        }}
        
        /* Dark mode cards */
        .dark-card {{
            background: {colors.surface};
            border: 1px solid {colors.border};
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        /* Dark mode inputs */
        .stSelectbox > div > div {{
            background: {colors.surface};
            border: 1px solid {colors.border};
            color: {colors.text_primary};
        }}
        
        /* Dark mode buttons */
        .stButton > button {{
            background: {colors.surface};
            color: {colors.text_primary};
            border: 1px solid {colors.border};
        }}
        
        .stButton > button[kind="primary"] {{
            background: {colors.primary};
            color: {colors.background};
        }}
        </style>
        """, unsafe_allow_html=True)

class ThemeManager:
    """Centralized theme management system"""
    
    @staticmethod
    def apply_theme(theme_mode: ThemeMode):
        """Apply selected theme to the application"""
        if theme_mode == ThemeMode.EXECUTIVE:
            ExecutiveTheme.apply_theme()
        elif theme_mode == ThemeMode.ANALYST:
            AnalystTheme.apply_theme()
        elif theme_mode == ThemeMode.DARK:
            DarkTheme.apply_theme()
        else:
            ExecutiveTheme.apply_theme()  # Default to executive
    
    @staticmethod
    def get_theme_selector() -> ThemeMode:
        """Render theme selector in sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Theme Settings")
            
            theme_choice = st.selectbox(
                "Select Theme",
                options=[
                    ("Executive", ThemeMode.EXECUTIVE),
                    ("Analyst", ThemeMode.ANALYST), 
                    ("Dark Mode", ThemeMode.DARK)
                ],
                format_func=lambda x: x[0],
                key="theme_selector"
            )
            
            return theme_choice[1]
    
    @staticmethod
    def create_custom_components():
        """Create custom styled components using current theme"""
        
        # Executive Summary Card
        def executive_summary_card(title: str, content: str, status: str = "info"):
            status_colors = {
                "success": "#6A994E",
                "warning": "#F18F01", 
                "error": "#C73E1D",
                "info": "#2E86AB"
            }
            
            color = status_colors.get(status, status_colors["info"])
            
            st.markdown(f"""
            <div class="executive-card" style="border-left: 4px solid {color};">
                <h4 style="color: {color}; margin: 0 0 1rem 0;">{title}</h4>
                <p style="margin: 0; line-height: 1.6;">{content}</p>
            </div>
            """, unsafe_allow_html=True)
        
        return {
            "executive_summary_card": executive_summary_card
        }

def apply_custom_theme(
    primary_color: str = "#2E86AB",
    secondary_color: str = "#A23B72",
    background_color: str = "#FAFBFC",
    text_color: str = "#2C3E50"
):
    """Apply custom theme with specified colors"""
    
    st.markdown(f"""
    <style>
    .stApp {{
        background: {background_color};
        color: {text_color};
    }}
    
    .stButton > button[kind="primary"] {{
        background: {primary_color};
        border: none;
        color: white;
    }}
    
    .metric-card {{
        border-left: 4px solid {primary_color};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {primary_color};
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# Demo function for themes
def demo_themes():
    """Demo function to showcase theme system"""
    st.title("🎨 Professional Theme System")
    
    # Theme selector
    selected_theme = ThemeManager.get_theme_selector()
    ThemeManager.apply_theme(selected_theme)
    
    st.success(f"Current theme: {selected_theme.value.title()}")
    
    # Demo content with current theme
    st.header("Theme Demonstration")
    
    # Metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Revenue Growth</div>
            <div class="metric-value">+24.5%</div>
            <div class="metric-delta positive">↗ +5.2% vs target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Market Share</div>
            <div class="metric-value">18.3%</div>
            <div class="metric-delta neutral">→ Stable</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Risk Score</div>
            <div class="metric-value">Medium</div>
            <div class="metric-delta negative">↘ -2pts improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo alerts
    st.markdown("""
    <div class="alert-success">
        <strong>Success:</strong> Your AI implementation strategy is on track.
    </div>
    
    <div class="alert-warning">
        <strong>Attention:</strong> Resource allocation requires review by Q3.
    </div>
    
    <div class="alert-info">
        <strong>Information:</strong> New market data available for analysis.
    </div>
    """, unsafe_allow_html=True)
    
    # Demo buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Primary Action", type="primary", use_container_width=True)
    
    with col2:
        st.button("Secondary Action", type="secondary", use_container_width=True)
    
    with col3:
        st.button("Default Action", use_container_width=True)
    
    # Custom components
    st.subheader("Custom Components")
    
    components = ThemeManager.create_custom_components()
    
    components["executive_summary_card"](
        title="Strategic Recommendation",
        content="Based on current market analysis, recommend accelerating AI adoption initiatives to maintain competitive advantage.",
        status="success"
    )
    
    components["executive_summary_card"](
        title="Risk Assessment", 
        content="Talent shortage poses medium-term risk to implementation timeline. Consider strategic partnerships.",
        status="warning"
    )

if __name__ == "__main__":
    demo_themes(); 