"""Economic scenario analysis for AI adoption and impact."""

from typing import Dict, List

from data.models.adoption import AdoptionMetrics
from data.models.economics import EconomicImpact


def project_adoption_scenarios(
    base: AdoptionMetrics, years: List[int], growth_rates: Dict[str, float]
) -> Dict[str, List[AdoptionMetrics]]:
    """
    Project AI adoption under different scenarios.
    Args:
        base: Baseline adoption metrics for the starting year
        years: List of years to project
        growth_rates: Dict of scenario name to annual growth rate (e.g., {'baseline': 0.05, 'optimistic': 0.08, 'pessimistic': 0.02})
    Returns:
        Dict mapping scenario name to list of projected AdoptionMetrics
    """
    scenarios = {}
    for scenario, rate in growth_rates.items():
        projections = []
        last = base
        for year in years:
            if year == base.year:
                projections.append(base)
                continue
            next_metrics = AdoptionMetrics(
                year=year,
                overall_adoption=min(100, last.overall_adoption * (1 + rate)),
                genai_adoption=min(100, last.genai_adoption * (1 + rate)),
                predictive_adoption=min(100, last.predictive_adoption * (1 + rate)),
                nlp_adoption=min(100, last.nlp_adoption * (1 + rate)),
                computer_vision_adoption=min(100, last.computer_vision_adoption * (1 + rate)),
                robotics_adoption=min(100, last.robotics_adoption * (1 + rate)),
            )
            projections.append(next_metrics)
            last = next_metrics
        scenarios[scenario] = projections
    return scenarios


def project_economic_impact_scenarios(
    base: EconomicImpact, years: List[int], growth_rates: Dict[str, float]
) -> Dict[str, List[EconomicImpact]]:
    """
    Project economic impact under different scenarios.
    Args:
        base: Baseline economic impact for the starting year
        years: List of years to project
        growth_rates: Dict of scenario name to annual growth rate
    Returns:
        Dict mapping scenario name to list of projected EconomicImpact
    """
    scenarios = {}
    for scenario, rate in growth_rates.items():
        projections = []
        last = base
        for year in years:
            if year == base.year:
                projections.append(base)
                continue
            next_impact = EconomicImpact(
                metric=base.metric,
                value=last.value * (1 + rate),
                unit=base.unit,
                year=year,
                confidence_interval_low=last.confidence_interval_low,
                confidence_interval_high=last.confidence_interval_high,
                source=base.source,
            )
            projections.append(next_impact)
            last = next_impact
        scenarios[scenario] = projections
    return scenarios
