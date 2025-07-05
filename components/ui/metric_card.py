"""Metric card component for displaying key metrics with insights."""

from typing import Optional, Union

import streamlit as st


def render_metric_card(
    label: str,
    value: Union[str, int, float],
    delta: Optional[Union[str, int, float]] = None,
    insight: Optional[str] = None,
    mode: str = "default",
    help_text: Optional[str] = None,
    urgency: str = "medium",
) -> None:
    """Render an enhanced metric card with optional insights and styling.

    Args:
        label: The metric label/title
        value: The main metric value
        delta: Optional change/delta value
        insight: Optional insight text to display below the metric
        mode: Display mode ('default', 'highlight', 'warning', 'success', 'danger')
        help_text: Optional help text for the metric
        urgency: Urgency level for styling ('low', 'medium', 'high', 'critical')
    """
    # Color schemes based on mode and urgency (following patterns from economic_insights.py)
    mode_colors = {
        "default": {
            "background": "rgba(248, 249, 250, 0.8)",
            "border": "#1f77b4",
            "text": "#212529",
        },
        "highlight": {
            "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
            "border": "#1f77b4",
            "text": "#1f77b4",
        },
        "warning": {
            "background": "#fff3cd",
            "border": "#ffc107",
            "text": "#856404",
        },
        "success": {
            "background": "#d4edda",
            "border": "#28a745",
            "text": "#155724",
        },
        "danger": {
            "background": "#f8d7da",
            "border": "#dc3545",
            "text": "#721c24",
        },
    }

    # Urgency colors (following patterns from key_takeaways.py)
    urgency_colors = {
        "low": "#28a745",
        "medium": "#ffc107",
        "high": "#fd7e14",
        "critical": "#dc3545",
    }

    # Get colors based on mode
    colors = mode_colors.get(mode, mode_colors["default"])
    urgency_color = urgency_colors.get(urgency, urgency_colors["medium"])

    # Apply urgency color to border if mode is default
    if mode == "default":
        colors["border"] = urgency_color

    # Create the metric card container
    card_style = f"""
    <div style='
        background: {colors["background"]};
        border-left: 5px solid {colors["border"]};
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
    '>
    """

    # Add help icon if help text provided
    if help_text:
        card_style += f"""
        <div style='
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: help;
            color: #6c757d;
            font-size: 14px;
        ' title='{help_text}'>
            ℹ️
        </div>
        """

    # Add metric label
    card_style += f"""
        <div style='
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 5px;
            font-weight: 600;
        '>
            {label}
        </div>
    """

    # Add metric value and delta
    card_style += f"""
        <div style='
            display: flex;
            align-items: baseline;
            gap: 15px;
            margin-bottom: 10px;
        '>
            <span style='
                font-size: 28px;
                font-weight: bold;
                color: {colors["text"]};
            '>
                {value}
            </span>
    """

    if delta is not None:
        # Determine delta color
        delta_str = str(delta)
        if delta_str.startswith("+") or (isinstance(delta, (int, float)) and delta > 0):
            delta_color = "#28a745"
            delta_arrow = "↑"
        elif delta_str.startswith("-") or (isinstance(delta, (int, float)) and delta < 0):
            delta_color = "#dc3545"
            delta_arrow = "↓"
        else:
            delta_color = "#6c757d"
            delta_arrow = "→"

        card_style += f"""
            <span style='
                font-size: 16px;
                color: {delta_color};
                font-weight: 500;
            '>
                {delta_arrow} {delta}
            </span>
        """

    card_style += "</div>"

    # Add insight if provided
    if insight:
        card_style += f"""
        <div style='
            font-size: 13px;
            color: #6c757d;
            line-height: 1.4;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
        '>
            💡 {insight}
        </div>
        """

    card_style += "</div>"

    # Render the card
    st.markdown(card_style, unsafe_allow_html=True)

    # Alternative: Use native st.metric when simple display is needed
    if not insight and not help_text and mode == "default":
        # Provide option to fall back to native streamlit metric
        with st.container():
            st.metric(label=label, value=value, delta=delta, help=help_text)
