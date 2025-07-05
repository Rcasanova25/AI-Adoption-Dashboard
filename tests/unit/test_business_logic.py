import pytest
from business.economic_scenarios import project_adoption_scenarios, project_economic_impact_scenarios
from business.roi_analysis import compute_roi
from business.policy_simulation import simulate_policy_impact
from business.labor_impact import compute_net_employment_change, analyze_skill_gaps
from data.models.adoption import AdoptionMetrics
from data.models.economics import EconomicImpact
from data.models.governance import GovernanceMetrics, PolicyFramework
from data.models.workforce import WorkforceImpact, SkillGaps


def test_project_adoption_scenarios():
    base = AdoptionMetrics(
        year=2020,
        overall_adoption=50,
        genai_adoption=10,
        predictive_adoption=20,
        nlp_adoption=15,
        computer_vision_adoption=12,
        robotics_adoption=8,
    )
    years = [2020, 2021, 2022]
    growth_rates = {"baseline": 0.05, "optimistic": 0.1}
    scenarios = project_adoption_scenarios(base, years, growth_rates)
    assert "baseline" in scenarios and "optimistic" in scenarios
    assert len(scenarios["baseline"]) == 3
    assert scenarios["baseline"][1].overall_adoption > base.overall_adoption


def test_project_economic_impact_scenarios():
    base = EconomicImpact(
        metric="GDP Impact",
        value=100.0,
        unit="Billion USD",
        year=2020,
        source="TestSource",
    )
    years = [2020, 2021, 2022]
    growth_rates = {"baseline": 0.05}
    scenarios = project_economic_impact_scenarios(base, years, growth_rates)
    assert "baseline" in scenarios
    assert scenarios["baseline"][1].value > base.value


def test_compute_roi():
    roi = compute_roi(
        initial_investment=100000,
        annual_savings=25000,
        payback_period_months=12,
        risk_level="Medium",
        productivity_gain_percent=10.0,
    )
    assert roi.total_roi_percent > 0
    assert roi.payback_period_months == 12
    assert roi.risk_level == "Medium"


def test_simulate_policy_impact():
    base = GovernanceMetrics(
        governance_area="Ethics",
        implementation_rate_percent=50,
        maturity_score=3.0,
        compliance_status="None",
        regulatory_requirements=["Transparency"],
        best_practices_adopted=2,
    )
    policies = [
        PolicyFramework(
            country_or_region="US",
            policy_name="AI Act",
            policy_type="Regulation",
            implementation_year=2025,
            maturity_level="Implemented",
            scope=["Ethics"],
        )
    ]
    result = simulate_policy_impact(base, policies)
    assert result.maturity_score > base.maturity_score
    assert result.compliance_status in ("Partial", "Full")


def test_compute_net_employment_change():
    impacts = [
        WorkforceImpact(
            job_category="A",
            automation_risk_percent=20,
            augmentation_potential_percent=30,
            jobs_displaced=10,
            jobs_created=25,
            net_employment_change=None,
            reskilling_required="Medium",
            timeline_years=5,
        ),
        WorkforceImpact(
            job_category="B",
            automation_risk_percent=10,
            augmentation_potential_percent=40,
            jobs_displaced=5,
            jobs_created=10,
            net_employment_change=None,
            reskilling_required="Low",
            timeline_years=3,
        ),
    ]
    net_change = compute_net_employment_change(impacts)
    assert net_change == (25 - 10) + (10 - 5)


def test_analyze_skill_gaps():
    gaps = [
        SkillGaps(
            skill_category="AI/ML Engineering",
            demand_index=90,
            supply_index=60,
            gap_severity="High",
            training_time_months=12,
            salary_premium_percent=20.0,
        ),
        SkillGaps(
            skill_category="Data Science",
            demand_index=80,
            supply_index=70,
            gap_severity="Medium",
            training_time_months=8,
            salary_premium_percent=15.0,
        ),
    ]
    summary = analyze_skill_gaps(gaps)
    assert summary in ("Medium", "High") 