"""
Scenario Planning Engine for AI Adoption Dashboard
Provides comprehensive scenario modeling and what-if analysis capabilities
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ScenarioType(Enum):
    OPTIMISTIC = "Optimistic"
    REALISTIC = "Realistic" 
    PESSIMISTIC = "Pessimistic"
    CUSTOM = "Custom"

class VariableType(Enum):
    ADOPTION_RATE = "Adoption Rate"
    INVESTMENT_COST = "Investment Cost"
    ROI_MULTIPLIER = "ROI Multiplier"
    TIMELINE = "Implementation Timeline"
    MARKET_GROWTH = "Market Growth"
    COMPETITION = "Competitive Pressure"

@dataclass
class ScenarioVariable:
    """Variable definition for scenario modeling"""
    name: str
    variable_type: VariableType
    base_value: float
    min_value: float
    max_value: float
    impact_weight: float  # 0-1, how much this affects outcomes
    description: str

@dataclass
class ScenarioOutcome:
    """Predicted outcomes for a scenario"""
    scenario_name: str
    probability: float
    projected_roi: float
    total_investment: float
    payback_months: int
    competitive_position: str
    risk_level: str
    confidence_interval: Tuple[float, float]
    key_assumptions: List[str]
    critical_success_factors: List[str]

@dataclass
class ScenarioAnalysis:
    """Complete scenario analysis results"""
    base_scenario: ScenarioOutcome
    scenarios: List[ScenarioOutcome]
    sensitivity_analysis: Dict[str, float]
    monte_carlo_results: Dict[str, Any]
    recommendations: List[str]
    contingency_plans: Dict[str, List[str]]

class ScenarioPlanningEngine:
    """Advanced scenario planning and what-if analysis engine"""
    
    def __init__(self):
        self.scenario_variables = self._initialize_variables()
        self.market_conditions = self._load_market_conditions()
        
    def create_comprehensive_scenarios(
        self,
        industry: str,
        company_size: str,
        investment_amount: float,
        timeline_months: int,
        strategic_goals: List[str],
        custom_variables: Optional[Dict[str, float]] = None
    ) -> ScenarioAnalysis:
        """
        Create comprehensive scenario analysis with multiple what-if scenarios
        """
        
        # Generate base scenario (realistic)
        base_scenario = self._generate_scenario(
            ScenarioType.REALISTIC, industry, company_size, 
            investment_amount, timeline_months, strategic_goals
        )
        
        # Generate alternative scenarios
        scenarios = []
        
        # Optimistic scenario
        optimistic = self._generate_scenario(
            ScenarioType.OPTIMISTIC, industry, company_size,
            investment_amount, timeline_months, strategic_goals
        )
        scenarios.append(optimistic)
        
        # Pessimistic scenario
        pessimistic = self._generate_scenario(
            ScenarioType.PESSIMISTIC, industry, company_size,
            investment_amount, timeline_months, strategic_goals
        )
        scenarios.append(pessimistic)
        
        # Custom scenarios based on variable adjustments
        if custom_variables:
            custom_scenario = self._generate_custom_scenario(
                custom_variables, industry, company_size,
                investment_amount, timeline_months, strategic_goals
            )
            scenarios.append(custom_scenario)
        
        # Economic downturn scenario
        downturn_scenario = self._generate_economic_scenario(
            "downturn", industry, company_size,
            investment_amount, timeline_months, strategic_goals
        )
        scenarios.append(downturn_scenario)
        
        # Rapid market adoption scenario
        rapid_adoption = self._generate_market_scenario(
            "rapid_adoption", industry, company_size,
            investment_amount, timeline_months, strategic_goals
        )
        scenarios.append(rapid_adoption)
        
        # Perform sensitivity analysis
        sensitivity_analysis = self._perform_sensitivity_analysis(
            base_scenario, industry, company_size, investment_amount
        )
        
        # Run Monte Carlo simulation
        monte_carlo_results = self._run_monte_carlo_simulation(
            base_scenario, 1000, industry, company_size
        )
        
        # Generate recommendations
        recommendations = self._generate_scenario_recommendations(
            base_scenario, scenarios, sensitivity_analysis
        )
        
        # Create contingency plans
        contingency_plans = self._create_contingency_plans(scenarios)
        
        return ScenarioAnalysis(
            base_scenario=base_scenario,
            scenarios=scenarios,
            sensitivity_analysis=sensitivity_analysis,
            monte_carlo_results=monte_carlo_results,
            recommendations=recommendations,
            contingency_plans=contingency_plans
        )
    
    def perform_what_if_analysis(
        self,
        base_parameters: Dict[str, float],
        variable_adjustments: Dict[str, float],
        industry: str
    ) -> Dict[str, Any]:
        """
        Perform detailed what-if analysis by adjusting specific variables
        """
        
        results = {}
        
        for variable_name, adjustment in variable_adjustments.items():
            # Apply adjustment to base parameters
            adjusted_params = base_parameters.copy()
            if variable_name in adjusted_params:
                adjusted_params[variable_name] *= (1 + adjustment)
            
            # Calculate impact
            base_outcome = self._calculate_outcome_metrics(base_parameters, industry)
            adjusted_outcome = self._calculate_outcome_metrics(adjusted_params, industry)
            
            # Calculate percentage change
            roi_change = (adjusted_outcome['roi'] - base_outcome['roi']) / base_outcome['roi'] * 100
            cost_change = (adjusted_outcome['cost'] - base_outcome['cost']) / base_outcome['cost'] * 100
            timeline_change = (adjusted_outcome['timeline'] - base_outcome['timeline']) / base_outcome['timeline'] * 100
            
            results[variable_name] = {
                'adjustment_percent': adjustment * 100,
                'roi_impact_percent': roi_change,
                'cost_impact_percent': cost_change,
                'timeline_impact_percent': timeline_change,
                'overall_impact': abs(roi_change) + abs(cost_change) + abs(timeline_change),
                'recommendation': self._get_variable_recommendation(variable_name, adjustment, roi_change)
            }
        
        return results
    
    def _generate_scenario(
        self,
        scenario_type: ScenarioType,
        industry: str,
        company_size: str,
        investment_amount: float,
        timeline_months: int,
        strategic_goals: List[str]
    ) -> ScenarioOutcome:
        """Generate specific scenario outcome"""
        
        # Base multipliers for different scenarios
        multipliers = {
            ScenarioType.OPTIMISTIC: {
                'roi_multiplier': 1.3,
                'cost_multiplier': 0.9,
                'timeline_multiplier': 0.8,
                'adoption_multiplier': 1.2,
                'probability': 0.25
            },
            ScenarioType.REALISTIC: {
                'roi_multiplier': 1.0,
                'cost_multiplier': 1.0,
                'timeline_multiplier': 1.0,
                'adoption_multiplier': 1.0,
                'probability': 0.5
            },
            ScenarioType.PESSIMISTIC: {
                'roi_multiplier': 0.7,
                'cost_multiplier': 1.3,
                'timeline_multiplier': 1.4,
                'adoption_multiplier': 0.8,
                'probability': 0.25
            }
        }
        
        scenario_mult = multipliers.get(scenario_type, multipliers[ScenarioType.REALISTIC])
        
        # Calculate industry baseline ROI
        industry_roi_base = {
            "Technology": 4.2,
            "Financial Services": 3.8,
            "Healthcare": 3.2,
            "Manufacturing": 3.5,
            "Government": 2.2
        }.get(industry, 3.0)
        
        # Apply scenario adjustments
        projected_roi = industry_roi_base * scenario_mult['roi_multiplier']
        total_investment = investment_amount * scenario_mult['cost_multiplier']
        adjusted_timeline = int(timeline_months * scenario_mult['timeline_multiplier'])
        
        # Calculate payback period
        monthly_benefit = (projected_roi * total_investment) / adjusted_timeline
        payback_months = int(total_investment / monthly_benefit) if monthly_benefit > 0 else adjusted_timeline
        
        # Determine competitive position
        if projected_roi >= 4.0:
            competitive_position = "Market Leader"
        elif projected_roi >= 3.0:
            competitive_position = "Strong Position"
        elif projected_roi >= 2.0:
            competitive_position = "Competitive"
        else:
            competitive_position = "At Risk"
        
        # Assess risk level
        if scenario_type == ScenarioType.OPTIMISTIC:
            risk_level = "Low"
        elif scenario_type == ScenarioType.PESSIMISTIC:
            risk_level = "High"
        else:
            risk_level = "Medium"
        
        # Calculate confidence interval
        base_variance = 0.15  # 15% variance
        if scenario_type == ScenarioType.PESSIMISTIC:
            base_variance *= 1.5
        
        ci_lower = projected_roi * (1 - base_variance)
        ci_upper = projected_roi * (1 + base_variance)
        
        # Generate key assumptions
        assumptions = self._generate_key_assumptions(scenario_type, industry, strategic_goals)
        
        # Generate critical success factors
        success_factors = self._generate_success_factors(scenario_type, industry, company_size)
        
        return ScenarioOutcome(
            scenario_name=f"{scenario_type.value} Scenario",
            probability=scenario_mult['probability'],
            projected_roi=projected_roi,
            total_investment=total_investment,
            payback_months=payback_months,
            competitive_position=competitive_position,
            risk_level=risk_level,
            confidence_interval=(ci_lower, ci_upper),
            key_assumptions=assumptions,
            critical_success_factors=success_factors
        )
    
    def _generate_custom_scenario(
        self,
        custom_variables: Dict[str, float],
        industry: str,
        company_size: str,
        investment_amount: float,
        timeline_months: int,
        strategic_goals: List[str]
    ) -> ScenarioOutcome:
        """Generate custom scenario based on user-defined variables"""
        
        # Start with realistic scenario as base
        base_scenario = self._generate_scenario(
            ScenarioType.REALISTIC, industry, company_size,
            investment_amount, timeline_months, strategic_goals
        )
        
        # Apply custom adjustments
        custom_roi = base_scenario.projected_roi
        custom_investment = base_scenario.total_investment
        custom_timeline = base_scenario.payback_months
        
        for variable, adjustment in custom_variables.items():
            if variable == "roi_adjustment":
                custom_roi *= (1 + adjustment)
            elif variable == "cost_adjustment":
                custom_investment *= (1 + adjustment)
            elif variable == "timeline_adjustment":
                custom_timeline = int(custom_timeline * (1 + adjustment))
        
        return ScenarioOutcome(
            scenario_name="Custom Scenario",
            probability=0.3,  # Default probability for custom scenarios
            projected_roi=custom_roi,
            total_investment=custom_investment,
            payback_months=custom_timeline,
            competitive_position=base_scenario.competitive_position,
            risk_level="Medium",
            confidence_interval=(custom_roi * 0.85, custom_roi * 1.15),
            key_assumptions=["Custom parameter adjustments applied"] + base_scenario.key_assumptions[:3],
            critical_success_factors=base_scenario.critical_success_factors
        )
    
    def _generate_economic_scenario(
        self,
        economic_condition: str,
        industry: str,
        company_size: str,
        investment_amount: float,
        timeline_months: int,
        strategic_goals: List[str]
    ) -> ScenarioOutcome:
        """Generate scenario based on economic conditions"""
        
        if economic_condition == "downturn":
            return ScenarioOutcome(
                scenario_name="Economic Downturn",
                probability=0.15,
                projected_roi=2.1,  # Reduced ROI due to economic pressures
                total_investment=investment_amount * 1.2,  # Higher costs due to resource constraints
                payback_months=int(timeline_months * 1.6),  # Longer payback
                competitive_position="Defensive",
                risk_level="High",
                confidence_interval=(1.5, 2.8),
                key_assumptions=[
                    "Economic recession impacts market demand",
                    "Reduced budget availability",
                    "Increased implementation challenges",
                    "Slower market adoption"
                ],
                critical_success_factors=[
                    "Focus on cost-reduction use cases",
                    "Maintain cash flow management",
                    "Prioritize quick wins",
                    "Build resilient partnerships"
                ]
            )
        
        return self._generate_scenario(ScenarioType.REALISTIC, industry, company_size,
                                     investment_amount, timeline_months, strategic_goals)
    
    def _generate_market_scenario(
        self,
        market_condition: str,
        industry: str,
        company_size: str,
        investment_amount: float,
        timeline_months: int,
        strategic_goals: List[str]
    ) -> ScenarioOutcome:
        """Generate scenario based on market conditions"""
        
        if market_condition == "rapid_adoption":
            return ScenarioOutcome(
                scenario_name="Rapid Market Adoption",
                probability=0.20,
                projected_roi=5.8,  # Higher ROI due to first-mover advantage
                total_investment=investment_amount * 0.85,  # Lower costs due to market momentum
                payback_months=int(timeline_months * 0.7),  # Faster payback
                competitive_position="Market Leader",
                risk_level="Medium",
                confidence_interval=(4.5, 7.1),
                key_assumptions=[
                    "Market adoption accelerates beyond expectations",
                    "Technology costs decrease rapidly",
                    "Competitive advantage window exists",
                    "Customer demand surges"
                ],
                critical_success_factors=[
                    "Speed to market execution",
                    "Scalable infrastructure",
                    "Strong talent acquisition",
                    "Customer experience focus"
                ]
            )
        
        return self._generate_scenario(ScenarioType.REALISTIC, industry, company_size,
                                     investment_amount, timeline_months, strategic_goals)
    
    def _perform_sensitivity_analysis(
        self,
        base_scenario: ScenarioOutcome,
        industry: str,
        company_size: str,
        investment_amount: float
    ) -> Dict[str, float]:
        """Perform sensitivity analysis on key variables"""
        
        sensitivity_results = {}
        
        # Test key variables with ±20% changes
        test_variables = {
            "adoption_rate": 0.2,
            "implementation_cost": 0.2,
            "market_growth": 0.2,
            "competition_intensity": 0.2,
            "technology_maturity": 0.2
        }
        
        base_roi = base_scenario.projected_roi
        
        for variable, change_percent in test_variables.items():
            # Calculate impact of positive and negative changes
            positive_impact = self._calculate_variable_impact(variable, change_percent, base_roi, industry)
            negative_impact = self._calculate_variable_impact(variable, -change_percent, base_roi, industry)
            
            # Calculate sensitivity (change in outcome / change in input)
            avg_impact = (abs(positive_impact) + abs(negative_impact)) / 2
            sensitivity_results[variable] = avg_impact / change_percent
        
        return sensitivity_results
    
    def _run_monte_carlo_simulation(
        self,
        base_scenario: ScenarioOutcome,
        iterations: int,
        industry: str,
        company_size: str
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation for risk analysis"""
        
        results = []
        
        # Define probability distributions for key variables
        np.random.seed(42)  # For reproducible results
        
        for _ in range(iterations):
            # Generate random variations in key parameters
            roi_variation = np.random.normal(1.0, 0.15)  # 15% standard deviation
            cost_variation = np.random.normal(1.0, 0.10)  # 10% standard deviation
            timeline_variation = np.random.normal(1.0, 0.12)  # 12% standard deviation
            
            # Calculate scenario outcome
            simulated_roi = base_scenario.projected_roi * roi_variation
            simulated_cost = base_scenario.total_investment * cost_variation
            simulated_timeline = base_scenario.payback_months * timeline_variation
            
            results.append({
                'roi': simulated_roi,
                'cost': simulated_cost,
                'timeline': simulated_timeline,
                'net_benefit': (simulated_roi * simulated_cost) - simulated_cost
            })
        
        # Calculate statistics
        results_df = pd.DataFrame(results)
        
        return {
            'mean_roi': results_df['roi'].mean(),
            'std_roi': results_df['roi'].std(),
            'roi_percentiles': {
                '10th': results_df['roi'].quantile(0.1),
                '25th': results_df['roi'].quantile(0.25),
                '50th': results_df['roi'].quantile(0.5),
                '75th': results_df['roi'].quantile(0.75),
                '90th': results_df['roi'].quantile(0.9)
            },
            'probability_positive_roi': (results_df['roi'] > 1.0).mean(),
            'probability_target_roi': (results_df['roi'] > base_scenario.projected_roi).mean(),
            'var_95': results_df['net_benefit'].quantile(0.05),  # Value at Risk (95% confidence)
            'expected_value': results_df['net_benefit'].mean()
        }
    
    def _generate_key_assumptions(
        self,
        scenario_type: ScenarioType,
        industry: str,
        strategic_goals: List[str]
    ) -> List[str]:
        """Generate key assumptions for scenario"""
        
        base_assumptions = [
            "Market conditions remain stable",
            "Technology adoption proceeds as planned",
            "Required talent is available",
            "Regulatory environment supports AI adoption"
        ]
        
        scenario_assumptions = {
            ScenarioType.OPTIMISTIC: [
                "Market adoption accelerates",
                "Cost reductions exceed expectations",
                "Competitive advantages are sustained",
                "Technology performance is superior"
            ],
            ScenarioType.PESSIMISTIC: [
                "Market adoption faces delays",
                "Implementation costs increase",
                "Competitive pressures intensify",
                "Technical challenges emerge"
            ]
        }
        
        assumptions = base_assumptions + scenario_assumptions.get(scenario_type, [])
        
        return assumptions[:5]  # Return top 5 assumptions
    
    def _generate_success_factors(
        self,
        scenario_type: ScenarioType,
        industry: str,
        company_size: str
    ) -> List[str]:
        """Generate critical success factors"""
        
        base_factors = [
            "Executive sponsorship and support",
            "Clear AI strategy and roadmap",
            "Adequate budget and resources",
            "Change management execution"
        ]
        
        industry_factors = {
            "Technology": ["Technical expertise", "Innovation culture"],
            "Healthcare": ["Regulatory compliance", "Clinical validation"],
            "Financial Services": ["Risk management", "Regulatory adherence"],
            "Manufacturing": ["Operational integration", "Safety protocols"]
        }
        
        factors = base_factors + industry_factors.get(industry, ["Domain expertise"])
        
        return factors[:6]  # Return top 6 factors
    
    def _calculate_outcome_metrics(self, parameters: Dict[str, float], industry: str) -> Dict[str, float]:
        """Calculate outcome metrics from parameters"""
        
        base_roi = parameters.get('base_roi', 3.0)
        investment = parameters.get('investment', 500000)
        timeline = parameters.get('timeline', 12)
        
        return {
            'roi': base_roi,
            'cost': investment,
            'timeline': timeline,
            'net_benefit': (base_roi * investment) - investment
        }
    
    def _calculate_variable_impact(
        self,
        variable: str,
        change_percent: float,
        base_roi: float,
        industry: str
    ) -> float:
        """Calculate impact of variable change on ROI"""
        
        # Simplified impact calculation - in practice, this would be more sophisticated
        impact_factors = {
            "adoption_rate": 0.8,
            "implementation_cost": -0.6,
            "market_growth": 0.5,
            "competition_intensity": -0.4,
            "technology_maturity": 0.3
        }
        
        impact_factor = impact_factors.get(variable, 0.2)
        return base_roi * change_percent * impact_factor
    
    def _get_variable_recommendation(
        self,
        variable_name: str,
        adjustment: float,
        roi_impact: float
    ) -> str:
        """Get recommendation based on variable impact"""
        
        if abs(roi_impact) > 10:
            sensitivity = "High"
        elif abs(roi_impact) > 5:
            sensitivity = "Medium"
        else:
            sensitivity = "Low"
        
        return f"{sensitivity} impact variable - monitor closely during implementation"
    
    def _generate_scenario_recommendations(
        self,
        base_scenario: ScenarioOutcome,
        scenarios: List[ScenarioOutcome],
        sensitivity_analysis: Dict[str, float]
    ) -> List[str]:
        """Generate actionable recommendations from scenario analysis"""
        
        recommendations = []
        
        # High-level strategy recommendations
        avg_roi = np.mean([s.projected_roi for s in scenarios])
        if avg_roi > 3.5:
            recommendations.append("Strong ROI potential across scenarios - proceed with confidence")
        elif avg_roi > 2.5:
            recommendations.append("Moderate ROI potential - implement with careful monitoring")
        else:
            recommendations.append("Lower ROI potential - consider alternative approaches or delay")
        
        # Risk management recommendations
        roi_variance = np.std([s.projected_roi for s in scenarios])
        if roi_variance > 1.0:
            recommendations.append("High ROI variance - develop strong contingency plans")
        
        # Sensitivity-based recommendations
        most_sensitive = max(sensitivity_analysis.items(), key=lambda x: x[1])
        recommendations.append(f"Monitor {most_sensitive[0]} closely - highest impact variable")
        
        return recommendations
    
    def _create_contingency_plans(self, scenarios: List[ScenarioOutcome]) -> Dict[str, List[str]]:
        """Create contingency plans for different scenarios"""
        
        plans = {}
        
        for scenario in scenarios:
            if scenario.risk_level == "High":
                plans[scenario.scenario_name] = [
                    "Implement early warning indicators",
                    "Prepare budget contingency reserves",
                    "Identify alternative execution paths",
                    "Establish rapid response protocols"
                ]
            elif scenario.projected_roi < 2.0:
                plans[scenario.scenario_name] = [
                    "Focus on quick wins and cost reduction",
                    "Consider phased implementation approach",
                    "Evaluate alternative technologies",
                    "Reassess business case assumptions"
                ]
        
        return plans
    
    def _initialize_variables(self) -> List[ScenarioVariable]:
        """Initialize scenario variables"""
        
        return [
            ScenarioVariable(
                name="Market Adoption Rate",
                variable_type=VariableType.ADOPTION_RATE,
                base_value=0.78,
                min_value=0.50,
                max_value=0.95,
                impact_weight=0.8,
                description="Overall market adoption of AI technologies"
            ),
            ScenarioVariable(
                name="Implementation Cost",
                variable_type=VariableType.INVESTMENT_COST,
                base_value=500000,
                min_value=250000,
                max_value=2000000,
                impact_weight=0.6,
                description="Total cost of AI implementation"
            ),
            ScenarioVariable(
                name="ROI Multiplier",
                variable_type=VariableType.ROI_MULTIPLIER,
                base_value=3.2,
                min_value=1.5,
                max_value=8.0,
                impact_weight=0.9,
                description="Expected return on investment multiplier"
            )
        ]
    
    def _load_market_conditions(self) -> Dict[str, float]:
        """Load current market conditions"""
        
        return {
            "economic_growth": 0.025,
            "technology_maturity": 0.78,
            "competitive_intensity": 0.65,
            "regulatory_support": 0.72
        }

# Global scenario planning engine instance
scenario_planner = ScenarioPlanningEngine()

# Export functions
__all__ = [
    'ScenarioType',
    'VariableType',
    'ScenarioVariable',
    'ScenarioOutcome',
    'ScenarioAnalysis',
    'ScenarioPlanningEngine',
    'scenario_planner'
]