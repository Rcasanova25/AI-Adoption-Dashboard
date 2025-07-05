"""Mock data generators for testing."""

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

import numpy as np
import pandas as pd


def generate_adoption_data(num_months: int = 36) -> pd.DataFrame:
    """Generate mock adoption rate data."""
    dates = pd.date_range(end=datetime.now(), periods=num_months, freq="M")

    # Create realistic adoption curve
    base_adoption = 30
    growth_rate = 0.02
    adoption_rates = []

    for i in range(num_months):
        noise = np.random.normal(0, 2)
        adoption = base_adoption * (1 + growth_rate) ** i + noise
        adoption = min(95, max(0, adoption))  # Cap between 0-95%
        adoption_rates.append(adoption)

    return pd.DataFrame(
        {
            "date": dates,
            "adoption_rate": adoption_rates,
            "enterprise_rate": [min(95, rate + 5) for rate in adoption_rates],
            "sme_rate": [max(0, rate - 10) for rate in adoption_rates],
            "confidence": np.random.choice(
                ["high", "medium", "low"], num_months, p=[0.6, 0.3, 0.1]
            ),
        }
    )


def generate_industry_data() -> pd.DataFrame:
    """Generate mock industry comparison data."""
    industries = [
        "Technology",
        "Finance",
        "Healthcare",
        "Manufacturing",
        "Retail",
        "Education",
        "Government",
        "Energy",
        "Transportation",
        "Media",
        "Telecommunications",
        "Agriculture",
    ]

    return pd.DataFrame(
        {
            "industry": industries,
            "adoption_rate": np.random.uniform(45, 92, len(industries)),
            "growth_rate": np.random.uniform(8, 25, len(industries)),
            "investment_millions": np.random.uniform(0.5, 10, len(industries)),
            "maturity_score": np.random.uniform(3, 9, len(industries)),
            "top_use_cases": [["Automation", "Analytics", "Customer Service"] for _ in industries],
        }
    )


def generate_geographic_data() -> pd.DataFrame:
    """Generate mock geographic distribution data."""
    regions = [
        ("North America", "United States", 87.5),
        ("North America", "Canada", 82.3),
        ("Europe", "United Kingdom", 78.9),
        ("Europe", "Germany", 81.2),
        ("Europe", "France", 75.6),
        ("Asia Pacific", "China", 89.2),
        ("Asia Pacific", "Japan", 76.5),
        ("Asia Pacific", "Singapore", 88.1),
        ("Asia Pacific", "Australia", 79.8),
        ("Latin America", "Brazil", 65.4),
        ("Middle East", "UAE", 72.3),
        ("Africa", "South Africa", 58.9),
    ]

    data = []
    for region, country, base_rate in regions:
        data.append(
            {
                "region": region,
                "country": country,
                "adoption_rate": base_rate + np.random.uniform(-5, 5),
                "talent_availability": np.random.uniform(5, 9),
                "infrastructure_score": np.random.uniform(6, 10),
                "policy_support": np.random.choice(["Strong", "Moderate", "Weak"]),
                "investment_billions": np.random.uniform(0.1, 5),
            }
        )

    return pd.DataFrame(data)


def generate_roi_scenarios() -> List[Dict[str, Any]]:
    """Generate mock ROI scenarios."""
    scenarios = []

    scenario_types = [("Conservative", 0.8, 24), ("Moderate", 1.0, 18), ("Aggressive", 1.3, 12)]

    for name, multiplier, payback in scenario_types:
        base_investment = 1000000
        scenarios.append(
            {
                "scenario": name,
                "investment": base_investment * multiplier,
                "expected_return": base_investment * multiplier * 2.5,
                "payback_months": payback,
                "risk_level": (
                    "High" if name == "Aggressive" else "Medium" if name == "Moderate" else "Low"
                ),
                "confidence": 0.95 - (0.1 * scenario_types.index((name, multiplier, payback))),
            }
        )

    return scenarios


def generate_labor_impact_data() -> pd.DataFrame:
    """Generate mock labor market impact data."""
    job_categories = [
        ("Administrative", 35, 45, 20),
        ("Customer Service", 42, 38, 20),
        ("Sales", 15, 65, 20),
        ("Technical", 8, 72, 20),
        ("Creative", 12, 68, 20),
        ("Management", 10, 75, 15),
        ("Healthcare", 5, 80, 15),
        ("Education", 8, 70, 22),
        ("Manufacturing", 45, 35, 20),
        ("Transportation", 38, 42, 20),
    ]

    data = []
    for category, displacement, augmentation, neutral in job_categories:
        data.append(
            {
                "job_category": category,
                "displacement_risk": displacement,
                "augmentation_potential": augmentation,
                "neutral_impact": neutral,
                "reskilling_urgency": (
                    "High" if displacement > 30 else "Medium" if displacement > 15 else "Low"
                ),
                "timeline_years": np.random.randint(2, 7),
            }
        )

    return pd.DataFrame(data)


def generate_cost_trend_data() -> pd.DataFrame:
    """Generate mock cost trend data."""
    dates = pd.date_range(start="2020-01-01", end="2024-12-01", freq="Q")

    # Exponentially decreasing costs
    initial_cost = 10000
    decay_rate = 0.15

    costs = []
    for i in range(len(dates)):
        cost = initial_cost * np.exp(-decay_rate * i / 4)  # Quarterly decay
        costs.append(cost)

    return pd.DataFrame(
        {
            "date": dates,
            "cost_per_million_tokens": costs,
            "compute_cost_per_hour": [c / 100 for c in costs],
            "storage_cost_per_tb": [c / 1000 for c in costs],
            "training_cost_reduction": [min(95, i * 5) for i in range(len(dates))],
        }
    )


def generate_governance_data() -> Dict[str, Any]:
    """Generate mock governance and compliance data."""
    return {
        "governance_maturity": {
            "overall_score": 65,
            "dimensions": {
                "Ethics Framework": 72,
                "Data Privacy": 68,
                "Algorithm Transparency": 58,
                "Risk Management": 70,
                "Compliance": 75,
                "Stakeholder Engagement": 60,
            },
        },
        "compliance_status": {
            "gdpr": "Compliant",
            "ccpa": "Compliant",
            "ai_act": "In Progress",
            "iso_27001": "Certified",
            "soc2": "Type II",
        },
        "risk_areas": [
            {"area": "Bias in algorithms", "severity": "High", "mitigation": "Active"},
            {"area": "Data privacy", "severity": "Medium", "mitigation": "Implemented"},
            {"area": "Model explainability", "severity": "Medium", "mitigation": "Planned"},
            {"area": "Third-party risks", "severity": "Low", "mitigation": "Monitored"},
        ],
    }


def generate_competitive_matrix() -> pd.DataFrame:
    """Generate mock competitive positioning matrix."""
    companies = ["Your Company", "Leader A", "Leader B", "Peer 1", "Peer 2", "Laggard 1"]

    return pd.DataFrame(
        {
            "company": companies,
            "ai_maturity": [7.5, 9.2, 8.8, 7.2, 6.8, 4.5],
            "innovation_score": [8.0, 9.5, 9.0, 7.0, 6.5, 3.5],
            "implementation_speed": [7.0, 8.5, 8.8, 6.5, 6.0, 4.0],
            "roi_achieved": [165, 210, 195, 150, 140, 85],
            "market_position": [
                "Competitive",
                "Leader",
                "Leader",
                "Competitive",
                "Follower",
                "Laggard",
            ],
        }
    )


def generate_skill_gap_data() -> pd.DataFrame:
    """Generate mock skill gap analysis data."""
    skills = [
        "Machine Learning",
        "Data Engineering",
        "AI Ethics",
        "MLOps",
        "Natural Language Processing",
        "Computer Vision",
        "AI Product Management",
        "Prompt Engineering",
        "AI Security",
        "Change Management",
    ]

    return pd.DataFrame(
        {
            "skill": skills,
            "current_level": np.random.uniform(2, 7, len(skills)),
            "required_level": np.random.uniform(6, 9, len(skills)),
            "gap_severity": np.random.choice(["Critical", "High", "Medium", "Low"], len(skills)),
            "time_to_close_months": np.random.randint(3, 18, len(skills)),
            "training_cost_per_person": np.random.randint(1000, 8000, len(skills)),
        }
    )


def generate_investment_data() -> Dict[str, pd.DataFrame]:
    """Generate comprehensive investment analysis data."""
    # Investment by category
    categories = pd.DataFrame(
        {
            "category": ["Infrastructure", "Talent", "Training", "Software", "Consulting"],
            "current_spend": [500000, 800000, 200000, 300000, 150000],
            "recommended_spend": [750000, 1200000, 400000, 450000, 200000],
            "roi_potential": [2.1, 3.5, 4.2, 2.8, 1.9],
        }
    )

    # Investment timeline
    months = pd.date_range(start="2024-01", periods=36, freq="M")
    timeline = pd.DataFrame(
        {
            "month": months,
            "cumulative_investment": np.cumsum(np.random.uniform(50000, 150000, 36)),
            "cumulative_return": np.cumsum(np.random.uniform(0, 200000, 36)),
            "milestone": [""] * 36,
        }
    )

    # Add milestones
    milestones = [6, 12, 18, 24, 30]
    milestone_names = [
        "Pilot Complete",
        "Phase 1 ROI",
        "Scale Achieved",
        "Full Deployment",
        "Optimization",
    ]
    for idx, name in zip(milestones, milestone_names):
        if idx < len(timeline):
            timeline.loc[idx, "milestone"] = name

    return {"by_category": categories, "timeline": timeline}


# Mock PDF extraction results
def generate_mock_pdf_data(source: str) -> Dict[str, Any]:
    """Generate mock data as if extracted from PDFs."""
    source_data = {
        "ai_index": {
            "title": "AI Index Report 2025",
            "key_findings": [
                "Global AI adoption reached 87% in enterprises",
                "AI investment grew 32% year-over-year",
                "Productivity gains averaged 25% across sectors",
            ],
            "metrics": generate_adoption_data(24),
            "charts": ["adoption_trend", "investment_flow", "sector_analysis"],
        },
        "mckinsey": {
            "title": "The State of AI in 2024",
            "key_findings": [
                "AI creates $13 trillion in value by 2030",
                "Leaders capture 5x more value than laggards",
                "70% of companies will adopt AI by 2025",
            ],
            "metrics": generate_competitive_matrix(),
            "charts": ["value_creation", "adoption_curve", "use_cases"],
        },
        "goldman_sachs": {
            "title": "Gen AI: Too Much Spend, Too Little Benefit?",
            "key_findings": [
                "7% GDP growth potential from AI",
                "$1 trillion infrastructure investment needed",
                "Productivity gains will offset job displacement",
            ],
            "metrics": generate_roi_scenarios(),
            "charts": ["gdp_impact", "investment_needs", "sector_disruption"],
        },
    }

    return source_data.get(
        source,
        {
            "title": f"Mock {source} Report",
            "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
            "metrics": generate_adoption_data(12),
            "charts": ["chart1", "chart2"],
        },
    )
