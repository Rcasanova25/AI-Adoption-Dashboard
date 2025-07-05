"""Theme management for the AI Adoption Dashboard."""

from typing import Dict, Optional
import streamlit as st


class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self):
        """Initialize the theme manager with predefined themes."""
        self.themes = {
            "default": {
                "name": "Default",
                "primary_color": "#1f77b4",
                "background_color": "#ffffff",
                "secondary_background": "#f8f9fa",
                "text_color": "#212529",
                "secondary_text": "#6c757d",
                "success_color": "#28a745",
                "warning_color": "#ffc107",
                "danger_color": "#dc3545",
                "info_color": "#17a2b8",
                "border_color": "#dee2e6",
                "shadow": "0 4px 6px rgba(0,0,0,0.1)",
                "gradient": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
            },
            "executive": {
                "name": "Executive",
                "primary_color": "#1a472a",
                "background_color": "#ffffff",
                "secondary_background": "#f5f5f5",
                "text_color": "#1a1a1a",
                "secondary_text": "#666666",
                "success_color": "#2e7d32",
                "warning_color": "#ed6c02",
                "danger_color": "#d32f2f",
                "info_color": "#0288d1",
                "border_color": "#e0e0e0",
                "shadow": "0 2px 4px rgba(0,0,0,0.15)",
                "gradient": "linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)",
            },
            "dark": {
                "name": "Dark",
                "primary_color": "#4da6ff",
                "background_color": "#1e1e1e",
                "secondary_background": "#2d2d2d",
                "text_color": "#ffffff",
                "secondary_text": "#b0b0b0",
                "success_color": "#4caf50",
                "warning_color": "#ff9800",
                "danger_color": "#f44336",
                "info_color": "#03a9f4",
                "border_color": "#424242",
                "shadow": "0 4px 8px rgba(0,0,0,0.3)",
                "gradient": "linear-gradient(135deg, #2d2d2d 0%, #1e1e1e 100%)",
            },
            "accessible": {
                "name": "High Contrast",
                "primary_color": "#0052cc",
                "background_color": "#ffffff",
                "secondary_background": "#f4f5f7",
                "text_color": "#172b4d",
                "secondary_text": "#5e6c84",
                "success_color": "#006644",
                "warning_color": "#ff8b00",
                "danger_color": "#de350b",
                "info_color": "#0065ff",
                "border_color": "#c1c7d0",
                "shadow": "0 1px 3px rgba(0,0,0,0.2)",
                "gradient": "linear-gradient(135deg, #ffffff 0%, #f4f5f7 100%)",
            },
        }
        
        # Default theme
        self.current_theme = "default"
    
    def apply_theme(self, theme_name: str = "default") -> None:
        """Apply a theme to the application using CSS injection.
        
        Args:
            theme_name: Name of the theme to apply
        """
        if theme_name not in self.themes:
            theme_name = "default"
        
        theme = self.themes[theme_name]
        self.current_theme = theme_name
        
        # Generate CSS based on theme
        css = f"""
        <style>
        /* Base theme variables */
        :root {{
            --primary-color: {theme['primary_color']};
            --background-color: {theme['background_color']};
            --secondary-background: {theme['secondary_background']};
            --text-color: {theme['text_color']};
            --secondary-text: {theme['secondary_text']};
            --success-color: {theme['success_color']};
            --warning-color: {theme['warning_color']};
            --danger-color: {theme['danger_color']};
            --info-color: {theme['info_color']};
            --border-color: {theme['border_color']};
            --shadow: {theme['shadow']};
            --gradient: {theme['gradient']};
        }}
        
        /* Global styles */
        .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--primary-color);
        }}
        
        /* Metrics */
        [data-testid="metric-container"] {{
            background-color: var(--secondary-background);
            border: 1px solid var(--border-color);
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
        }}
        
        .stButton > button:hover {{
            background-color: var(--primary-color);
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        /* Selectbox and inputs */
        .stSelectbox > div > div, .stTextInput > div > div > input {{
            background-color: var(--secondary-background);
            color: var(--text-color);
            border: 1px solid var(--border-color);
        }}
        
        /* Expanders */
        .streamlit-expanderHeader {{
            background-color: var(--secondary-background);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
        }}
        
        /* Info, warning, error boxes */
        .stAlert {{
            background-color: var(--secondary-background);
            border-left: 4px solid var(--info-color);
            color: var(--text-color);
        }}
        
        [data-baseweb="notification"][kind="info"] {{
            background-color: var(--info-color);
            color: white;
        }}
        
        [data-baseweb="notification"][kind="warning"] {{
            background-color: var(--warning-color);
            color: var(--text-color);
        }}
        
        [data-baseweb="notification"][kind="error"] {{
            background-color: var(--danger-color);
            color: white;
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: var(--secondary-background);
        }}
        
        /* Custom containers with gradient */
        .gradient-container {{
            background: var(--gradient);
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            margin: 1rem 0;
        }}
        
        /* Data tables */
        .dataframe {{
            background-color: var(--secondary-background);
            color: var(--text-color);
        }}
        
        .dataframe th {{
            background-color: var(--primary-color);
            color: white;
            padding: 0.5rem;
        }}
        
        .dataframe td {{
            border: 1px solid var(--border-color);
            padding: 0.5rem;
        }}
        
        /* Charts and plots */
        .js-plotly-plot {{
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            box-shadow: var(--shadow);
            margin: 1rem 0;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: var(--secondary-background);
            border-bottom: 2px solid var(--border-color);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: var(--secondary-text);
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: var(--primary-color);
            border-bottom: 2px solid var(--primary-color);
        }}
        
        /* Progress bars */
        .stProgress > div > div > div > div {{
            background-color: var(--primary-color);
        }}
        
        /* Sliders */
        .stSlider > div > div > div > div {{
            background-color: var(--primary-color);
        }}
        
        /* Checkboxes and radio buttons */
        input[type="checkbox"]:checked, input[type="radio"]:checked {{
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }}
        
        /* Custom utility classes */
        .urgent-high {{
            border-left: 4px solid var(--danger-color) !important;
        }}
        
        .urgent-medium {{
            border-left: 4px solid var(--warning-color) !important;
        }}
        
        .urgent-low {{
            border-left: 4px solid var(--success-color) !important;
        }}
        
        /* Accessibility improvements for high contrast theme */
        {'''
        a {{
            text-decoration: underline;
        }}
        
        button:focus, a:focus, input:focus, select:focus {{
            outline: 3px solid var(--primary-color);
            outline-offset: 2px;
        }}
        ''' if theme_name == 'accessible' else ''}
        
        /* Dark theme specific adjustments */
        {'''
        .stMarkdown code {{
            background-color: #3d3d3d;
            color: #e0e0e0;
        }}
        
        .stDataFrame {{
            background-color: var(--secondary-background);
        }}
        ''' if theme_name == 'dark' else ''}
        </style>
        """
        
        # Apply the CSS
        st.markdown(css, unsafe_allow_html=True)
    
    def get_current_theme(self) -> Dict[str, str]:
        """Get the current theme configuration.
        
        Returns:
            Dictionary containing current theme settings
        """
        return self.themes[self.current_theme]
    
    def get_theme_names(self) -> list:
        """Get list of available theme names.
        
        Returns:
            List of theme names
        """
        return list(self.themes.keys())
    
    def add_custom_theme(self, name: str, theme_config: Dict[str, str]) -> None:
        """Add a custom theme to the theme manager.
        
        Args:
            name: Name of the custom theme
            theme_config: Dictionary containing theme configuration
        """
        required_keys = [
            "primary_color", "background_color", "secondary_background",
            "text_color", "secondary_text", "success_color", "warning_color",
            "danger_color", "info_color", "border_color", "shadow", "gradient"
        ]
        
        # Validate theme config
        if all(key in theme_config for key in required_keys):
            theme_config["name"] = name
            self.themes[name] = theme_config
        else:
            raise ValueError(f"Theme config must contain all required keys: {required_keys}")
    
    def create_theme_selector(self, key: str = "theme_selector") -> str:
        """Create a theme selector widget.
        
        Args:
            key: Unique key for the selectbox widget
            
        Returns:
            Selected theme name
        """
        selected_theme = st.selectbox(
            "Select Theme",
            options=self.get_theme_names(),
            format_func=lambda x: self.themes[x]["name"],
            key=key,
            help="Choose a visual theme for the dashboard"
        )
        
        # Apply the selected theme
        self.apply_theme(selected_theme)
        
        return selected_theme