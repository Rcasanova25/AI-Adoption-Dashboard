"""Labor impact and skill gap analysis for AI adoption."""

from typing import List

from data.models.workforce import SkillGaps, WorkforceImpact


def compute_net_employment_change(impacts: List[WorkforceImpact]) -> int:
    """
    Compute net employment change from a list of workforce impacts.
    Args:
        impacts: List of WorkforceImpact objects
    Returns:
        Net employment change (jobs created - jobs displaced)
    """
    net_change = 0
    for impact in impacts:
        created = impact.jobs_created or 0
        displaced = impact.jobs_displaced or 0
        net_change += created - displaced
    return net_change


def analyze_skill_gaps(gaps: List[SkillGaps]) -> str:
    """
    Analyze skill gap severity across categories.
    Args:
        gaps: List of SkillGaps objects
    Returns:
        String summary of overall skill gap severity
    """
    severity_levels = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    if not gaps:
        return "No data"
    avg_severity = sum(severity_levels.get(g.gap_severity, 0) for g in gaps) / len(gaps)
    if avg_severity < 1.5:
        return "Low"
    elif avg_severity < 2.5:
        return "Medium"
    elif avg_severity < 3.5:
        return "High"
    else:
        return "Critical"
