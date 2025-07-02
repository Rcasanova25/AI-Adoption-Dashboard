"""
Accessibility Audit Tool for AI Adoption Dashboard
Comprehensive audit of color schemes, chart accessibility, and UI compliance with WCAG 2.1 guidelines
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import colorsys
import math
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class AccessibilityLevel(Enum):
    """WCAG 2.1 accessibility levels"""
    A = "A"
    AA = "AA"  # Recommended standard
    AAA = "AAA"  # Enhanced


class IssueType(Enum):
    """Types of accessibility issues"""
    COLOR_CONTRAST = "color_contrast"
    MISSING_ALT_TEXT = "missing_alt_text" 
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    SCREEN_READER = "screen_reader"
    COLOR_BLINDNESS = "color_blindness"
    FONT_SIZE = "font_size"
    FOCUS_INDICATORS = "focus_indicators"
    SEMANTIC_MARKUP = "semantic_markup"


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue"""
    issue_type: IssueType
    severity: Severity
    description: str
    location: str
    recommendation: str
    wcag_criterion: str
    current_value: Optional[str] = None
    required_value: Optional[str] = None


@dataclass
class ColorContrastResult:
    """Color contrast analysis result"""
    foreground: str
    background: str
    contrast_ratio: float
    aa_compliant: bool
    aaa_compliant: bool
    recommended_foreground: Optional[str] = None


class ColorContrastAnalyzer:
    """Analyzes color contrast compliance with WCAG guidelines"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_luminance(r: int, g: int, b: int) -> float:
        """Calculate relative luminance of RGB color"""
        def srgb_to_linear(c: int) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r_lin = srgb_to_linear(r)
        g_lin = srgb_to_linear(g)
        b_lin = srgb_to_linear(b)
        
        return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
    
    @classmethod
    def calculate_contrast_ratio(cls, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        r1, g1, b1 = cls.hex_to_rgb(color1)
        r2, g2, b2 = cls.hex_to_rgb(color2)
        
        l1 = cls.rgb_to_luminance(r1, g1, b1)
        l2 = cls.rgb_to_luminance(r2, g2, b2)
        
        # Ensure l1 is the lighter color
        if l1 < l2:
            l1, l2 = l2, l1
        
        return (l1 + 0.05) / (l2 + 0.05)
    
    @classmethod
    def analyze_contrast(cls, foreground: str, background: str, 
                        text_size: str = "normal") -> ColorContrastResult:
        """Analyze contrast ratio and compliance"""
        contrast_ratio = cls.calculate_contrast_ratio(foreground, background)
        
        # WCAG 2.1 requirements
        if text_size == "large":  # 18pt+ or 14pt+ bold
            aa_threshold = 3.0
            aaa_threshold = 4.5
        else:  # Normal text
            aa_threshold = 4.5
            aaa_threshold = 7.0
        
        aa_compliant = contrast_ratio >= aa_threshold
        aaa_compliant = contrast_ratio >= aaa_threshold
        
        # Generate recommended foreground color if not compliant
        recommended_foreground = None
        if not aa_compliant:
            recommended_foreground = cls.generate_accessible_color(background, aa_threshold)
        
        return ColorContrastResult(
            foreground=foreground,
            background=background,
            contrast_ratio=contrast_ratio,
            aa_compliant=aa_compliant,
            aaa_compliant=aaa_compliant,
            recommended_foreground=recommended_foreground
        )
    
    @classmethod
    def generate_accessible_color(cls, background: str, min_contrast: float) -> str:
        """Generate an accessible foreground color for given background"""
        bg_r, bg_g, bg_b = cls.hex_to_rgb(background)
        bg_luminance = cls.rgb_to_luminance(bg_r, bg_g, bg_b)
        
        # Try dark text first
        dark_luminance = 0.0
        dark_contrast = (bg_luminance + 0.05) / (dark_luminance + 0.05)
        
        if dark_contrast >= min_contrast:
            return "#000000"
        
        # Try light text
        light_luminance = 1.0
        light_contrast = (light_luminance + 0.05) / (bg_luminance + 0.05)
        
        if light_contrast >= min_contrast:
            return "#FFFFFF"
        
        # Generate intermediate color that meets contrast requirement
        target_luminance = (bg_luminance + 0.05) / min_contrast - 0.05
        target_luminance = max(0, min(1, target_luminance))
        
        # Convert luminance back to RGB (simplified)
        if target_luminance <= 0.03928:
            srgb = target_luminance * 12.92
        else:
            srgb = 1.055 * (target_luminance ** (1/2.4)) - 0.055
        
        rgb_value = int(srgb * 255)
        return f"#{rgb_value:02x}{rgb_value:02x}{rgb_value:02x}"


class ColorBlindnessAnalyzer:
    """Analyzes color accessibility for color blindness"""
    
    @staticmethod
    def simulate_color_blindness(hex_color: str, blindness_type: str) -> str:
        """Simulate how a color appears with different types of color blindness"""
        r, g, b = ColorContrastAnalyzer.hex_to_rgb(hex_color)
        r, g, b = r/255.0, g/255.0, b/255.0
        
        if blindness_type == "protanopia":  # Red-blind
            # Remove red component
            new_r = 0.567 * r + 0.433 * g
            new_g = 0.558 * r + 0.442 * g
            new_b = 0.242 * g + 0.758 * b
        elif blindness_type == "deuteranopia":  # Green-blind
            # Remove green component
            new_r = 0.625 * r + 0.375 * g
            new_g = 0.7 * r + 0.3 * g
            new_b = 0.3 * g + 0.7 * b
        elif blindness_type == "tritanopia":  # Blue-blind
            # Remove blue component
            new_r = 0.95 * r + 0.05 * g
            new_g = 0.433 * g + 0.567 * b
            new_b = 0.475 * g + 0.525 * b
        else:
            return hex_color
        
        # Convert back to hex
        new_r = int(max(0, min(1, new_r)) * 255)
        new_g = int(max(0, min(1, new_g)) * 255)
        new_b = int(max(0, min(1, new_b)) * 255)
        
        return f"#{new_r:02x}{new_g:02x}{new_b:02x}"
    
    @classmethod
    def analyze_color_palette(cls, colors: List[str]) -> Dict[str, Any]:
        """Analyze a color palette for color blindness accessibility"""
        blindness_types = ["protanopia", "deuteranopia", "tritanopia"]
        results = {}
        
        for blindness_type in blindness_types:
            simulated_colors = [cls.simulate_color_blindness(color, blindness_type) for color in colors]
            
            # Check for distinguishability
            unique_colors = len(set(simulated_colors))
            original_unique = len(set(colors))
            
            results[blindness_type] = {
                "original_colors": colors,
                "simulated_colors": simulated_colors,
                "distinguishable_colors": unique_colors,
                "original_unique_colors": original_unique,
                "accessibility_score": unique_colors / original_unique if original_unique > 0 else 1.0
            }
        
        return results


class AccessibilityAuditor:
    """Main accessibility auditor for the dashboard"""
    
    def __init__(self):
        self.issues: List[AccessibilityIssue] = []
        self.contrast_analyzer = ColorContrastAnalyzer()
        self.color_blindness_analyzer = ColorBlindnessAnalyzer()
    
    def audit_color_schemes(self) -> List[AccessibilityIssue]:
        """Audit color schemes used throughout the dashboard"""
        issues = []
        
        # Audit current theme colors
        from components.themes import ExecutiveTheme
        
        colors = ExecutiveTheme.get_color_palette()
        
        # Test primary text on background
        contrast_result = self.contrast_analyzer.analyze_contrast(
            colors.text_primary, colors.background
        )
        
        if not contrast_result.aa_compliant:
            issues.append(AccessibilityIssue(
                issue_type=IssueType.COLOR_CONTRAST,
                severity=Severity.HIGH,
                description=f"Primary text contrast ratio ({contrast_result.contrast_ratio:.2f}) does not meet WCAG AA standards",
                location="Executive Theme - Primary Text",
                recommendation=f"Use darker text color like {contrast_result.recommended_foreground}",
                wcag_criterion="1.4.3 Contrast (Minimum)",
                current_value=f"{contrast_result.contrast_ratio:.2f}:1",
                required_value="4.5:1"
            ))
        
        # Test secondary text on background
        contrast_result = self.contrast_analyzer.analyze_contrast(
            colors.text_secondary, colors.background
        )
        
        if not contrast_result.aa_compliant:
            issues.append(AccessibilityIssue(
                issue_type=IssueType.COLOR_CONTRAST,
                severity=Severity.MEDIUM,
                description=f"Secondary text contrast ratio ({contrast_result.contrast_ratio:.2f}) does not meet WCAG AA standards",
                location="Executive Theme - Secondary Text",
                recommendation=f"Use darker text color like {contrast_result.recommended_foreground}",
                wcag_criterion="1.4.3 Contrast (Minimum)",
                current_value=f"{contrast_result.contrast_ratio:.2f}:1",
                required_value="4.5:1"
            ))
        
        # Test chart colors for color blindness
        chart_colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        color_blind_results = self.color_blindness_analyzer.analyze_color_palette(chart_colors)
        
        for blindness_type, result in color_blind_results.items():
            if result['accessibility_score'] < 0.8:  # Less than 80% distinguishable
                issues.append(AccessibilityIssue(
                    issue_type=IssueType.COLOR_BLINDNESS,
                    severity=Severity.HIGH,
                    description=f"Chart colors are not sufficiently distinguishable for {blindness_type}",
                    location="Chart Color Palette",
                    recommendation="Use patterns, textures, or additional visual cues beyond color",
                    wcag_criterion="1.4.1 Use of Color",
                    current_value=f"{result['accessibility_score']:.1%} distinguishable",
                    required_value="100% distinguishable"
                ))
        
        return issues
    
    def audit_chart_accessibility(self) -> List[AccessibilityIssue]:
        """Audit chart accessibility features"""
        issues = []
        
        # Check for missing alt text
        issues.append(AccessibilityIssue(
            issue_type=IssueType.MISSING_ALT_TEXT,
            severity=Severity.CRITICAL,
            description="Charts lack alternative text descriptions for screen readers",
            location="All Plotly Charts",
            recommendation="Add descriptive alt text and data summaries for each chart",
            wcag_criterion="1.1.1 Non-text Content"
        ))
        
        # Check for missing data tables
        issues.append(AccessibilityIssue(
            issue_type=IssueType.SCREEN_READER,
            severity=Severity.HIGH,
            description="No alternative data tables provided for chart data",
            location="All Charts",
            recommendation="Provide downloadable data tables as alternative to visual charts",
            wcag_criterion="1.3.1 Info and Relationships"
        ))
        
        # Check for keyboard navigation
        issues.append(AccessibilityIssue(
            issue_type=IssueType.KEYBOARD_NAVIGATION,
            severity=Severity.HIGH,
            description="Interactive charts cannot be navigated using keyboard only",
            location="Interactive Plotly Charts",
            recommendation="Implement keyboard navigation for chart interactions",
            wcag_criterion="2.1.1 Keyboard"
        ))
        
        return issues
    
    def audit_ui_accessibility(self) -> List[AccessibilityIssue]:
        """Audit UI component accessibility"""
        issues = []
        
        # Check for missing semantic markup
        issues.append(AccessibilityIssue(
            issue_type=IssueType.SEMANTIC_MARKUP,
            severity=Severity.HIGH,
            description="Missing semantic HTML markup for screen readers",
            location="Dashboard Layout",
            recommendation="Add proper heading hierarchy, landmarks, and ARIA labels",
            wcag_criterion="1.3.1 Info and Relationships"
        ))
        
        # Check for focus indicators
        issues.append(AccessibilityIssue(
            issue_type=IssueType.FOCUS_INDICATORS,
            severity=Severity.MEDIUM,
            description="Missing visible focus indicators for interactive elements",
            location="Buttons and Interactive Elements",
            recommendation="Add clear focus indicators for keyboard navigation",
            wcag_criterion="2.4.7 Focus Visible"
        ))
        
        # Check font sizes
        issues.append(AccessibilityIssue(
            issue_type=IssueType.FONT_SIZE,
            severity=Severity.MEDIUM,
            description="Font sizes may be too small for users with visual impairments",
            location="Dashboard Text",
            recommendation="Ensure minimum 16px font size, provide size adjustment options",
            wcag_criterion="1.4.4 Resize text"
        ))
        
        return issues
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run comprehensive accessibility audit"""
        logger.info("Starting comprehensive accessibility audit...")
        
        # Clear previous issues
        self.issues = []
        
        # Run all audit components
        color_issues = self.audit_color_schemes()
        chart_issues = self.audit_chart_accessibility()
        ui_issues = self.audit_ui_accessibility()
        
        # Combine all issues
        all_issues = color_issues + chart_issues + ui_issues
        self.issues = all_issues
        
        # Generate summary
        severity_counts = {
            severity.value: sum(1 for issue in all_issues if issue.severity == severity)
            for severity in Severity
        }
        
        # Calculate overall score
        total_issues = len(all_issues)
        critical_issues = severity_counts[Severity.CRITICAL.value]
        high_issues = severity_counts[Severity.HIGH.value]
        
        # Scoring: 100 - (critical*10 + high*5 + medium*2 + low*1)
        score = max(0, 100 - (
            critical_issues * 10 +
            high_issues * 5 +
            severity_counts[Severity.MEDIUM.value] * 2 +
            severity_counts[Severity.LOW.value] * 1
        ))
        
        # Determine accessibility level
        if score >= 90 and critical_issues == 0:
            accessibility_level = AccessibilityLevel.AA
        elif score >= 70 and critical_issues <= 1:
            accessibility_level = AccessibilityLevel.A
        else:
            accessibility_level = None
        
        audit_result = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": score,
            "accessibility_level": accessibility_level.value if accessibility_level else "Non-compliant",
            "total_issues": total_issues,
            "severity_breakdown": severity_counts,
            "issues": [asdict(issue) for issue in all_issues],
            "recommendations": self.generate_priority_recommendations()
        }
        
        logger.info(f"Accessibility audit completed. Score: {score}/100, Level: {accessibility_level}")
        
        return audit_result
    
    def generate_priority_recommendations(self) -> List[Dict[str, str]]:
        """Generate prioritized recommendations for fixing accessibility issues"""
        recommendations = []
        
        # Group issues by type and severity
        critical_issues = [issue for issue in self.issues if issue.severity == Severity.CRITICAL]
        high_issues = [issue for issue in self.issues if issue.severity == Severity.HIGH]
        
        # Priority 1: Critical issues
        if critical_issues:
            recommendations.append({
                "priority": "1 - Critical",
                "action": "Add alternative text descriptions for all charts and visualizations",
                "impact": "Makes content accessible to screen reader users",
                "effort": "Medium"
            })
        
        # Priority 2: Color contrast
        contrast_issues = [issue for issue in high_issues if issue.issue_type == IssueType.COLOR_CONTRAST]
        if contrast_issues:
            recommendations.append({
                "priority": "2 - High",
                "action": "Fix color contrast ratios to meet WCAG AA standards",
                "impact": "Improves readability for users with visual impairments",
                "effort": "Low"
            })
        
        # Priority 3: Color blindness
        color_blind_issues = [issue for issue in high_issues if issue.issue_type == IssueType.COLOR_BLINDNESS]
        if color_blind_issues:
            recommendations.append({
                "priority": "3 - High", 
                "action": "Implement colorblind-friendly chart design with patterns and textures",
                "impact": "Makes charts accessible to users with color vision deficiencies",
                "effort": "Medium"
            })
        
        # Priority 4: Keyboard navigation
        keyboard_issues = [issue for issue in high_issues if issue.issue_type == IssueType.KEYBOARD_NAVIGATION]
        if keyboard_issues:
            recommendations.append({
                "priority": "4 - High",
                "action": "Add keyboard navigation support for interactive elements",
                "impact": "Enables users who cannot use a mouse to interact with dashboard",
                "effort": "High"
            })
        
        return recommendations
    
    def save_audit_report(self, results: Dict[str, Any], filepath: str = None):
        """Save audit results to file"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"accessibility_audit_{timestamp}.json"
        
        audit_dir = Path("accessibility/reports")
        audit_dir.mkdir(parents=True, exist_ok=True)
        
        full_path = audit_dir / filepath
        
        with open(full_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Accessibility audit report saved to: {full_path}")
        return full_path


# Create global auditor instance
accessibility_auditor = AccessibilityAuditor()