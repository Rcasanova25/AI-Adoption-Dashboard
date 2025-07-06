"""Reports module for AI Adoption Dashboard.

This module provides automated report generation capabilities.
"""

from .report_generator import (
    ReportGenerator,
    ReportTemplate,
    ExecutiveSummaryTemplate,
    DetailedAnalysisTemplate,
    IndustryComparisonTemplate,
    report_generator
)

__all__ = [
    'ReportGenerator',
    'ReportTemplate',
    'ExecutiveSummaryTemplate',
    'DetailedAnalysisTemplate',
    'IndustryComparisonTemplate',
    'report_generator'
]