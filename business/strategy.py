"""
Strategic Planning Module for AI Adoption Dashboard
Provides comprehensive strategic planning and roadmap generation capabilities
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StrategicPriority(Enum):
    CRITICAL = "Critical"
    HIGH = "High" 
    MEDIUM = "Medium"
    LOW = "Low"

class ImplementationPhase(Enum):
    FOUNDATION = "Foundation (0-6 months)"
    ACCELERATION = "Acceleration (6-18 months)"
    OPTIMIZATION = "Optimization (18-36 months)"
    INNOVATION = "Innovation (36+ months)"

@dataclass
class StrategicInitiative:
    """Strategic initiative with implementation details"""
    name: str
    description: str
    priority: StrategicPriority
    phase: ImplementationPhase
    estimated_cost: float
    expected_roi: float
    timeline_months: int
    dependencies: List[str]
    success_metrics: List[str]
    risk_level: str

@dataclass
class StrategicRoadmap:
    """Complete strategic roadmap for AI adoption"""
    organization_profile: Dict[str, str]
    current_maturity: str
    target_maturity: str
    initiatives: List[StrategicInitiative]
    total_investment: float
    expected_total_roi: float
    implementation_timeline: int
    key_milestones: List[Dict[str, str]]
    success_probability: float

class StrategicPlanner:
    """Advanced strategic planning engine for AI adoption"""
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.best_practices = self._load_best_practices()
    
    def generate_strategic_roadmap(
        self,
        industry: str,
        company_size: str,
        current_maturity: str,
        budget_range: str,
        timeline_preference: str,
        strategic_goals: List[str]
    ) -> StrategicRoadmap:
        """
        Generate comprehensive strategic roadmap for AI adoption
        """
        
        # Analyze current state
        maturity_score = self._assess_maturity_score(current_maturity)
        
        # Generate initiatives based on profile
        initiatives = self._generate_initiatives(
            industry, company_size, maturity_score, budget_range, strategic_goals
        )
        
        # Calculate roadmap metrics
        total_investment = sum(init.estimated_cost for init in initiatives)
        expected_total_roi = sum(init.expected_roi * init.estimated_cost for init in initiatives) / total_investment
        implementation_timeline = max(init.timeline_months for init in initiatives)
        
        # Generate milestones
        milestones = self._generate_milestones(initiatives)
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(
            industry, company_size, maturity_score, len(initiatives)
        )
        
        return StrategicRoadmap(
            organization_profile={
                'industry': industry,
                'company_size': company_size,
                'current_maturity': current_maturity,
                'budget_range': budget_range
            },
            current_maturity=current_maturity,
            target_maturity=self._determine_target_maturity(maturity_score, strategic_goals),
            initiatives=initiatives,
            total_investment=total_investment,
            expected_total_roi=expected_total_roi,
            implementation_timeline=implementation_timeline,
            key_milestones=milestones,
            success_probability=success_probability
        )
    
    def _generate_initiatives(
        self,
        industry: str,
        company_size: str,
        maturity_score: int,
        budget_range: str,
        strategic_goals: List[str]
    ) -> List[StrategicInitiative]:
        """Generate tailored strategic initiatives"""
        
        initiatives = []
        
        # Foundation initiatives (always needed for low maturity)
        if maturity_score < 30:
            initiatives.extend(self._get_foundation_initiatives(company_size, budget_range))
        
        # Goal-specific initiatives
        for goal in strategic_goals:
            initiatives.extend(self._get_goal_specific_initiatives(goal, industry, company_size))
        
        # Industry-specific initiatives
        initiatives.extend(self._get_industry_initiatives(industry, maturity_score))
        
        # Prioritize and filter based on budget
        initiatives = self._prioritize_initiatives(initiatives, budget_range)
        
        return initiatives[:12]  # Limit to top 12 initiatives
    
    def _get_foundation_initiatives(self, company_size: str, budget_range: str) -> List[StrategicInitiative]:
        """Get foundational AI initiatives"""
        
        base_cost = 50000 if "1-50" in company_size else 200000 if "5000+" not in company_size else 500000
        
        return [
            StrategicInitiative(
                name="AI Readiness Assessment",
                description="Comprehensive evaluation of current AI capabilities and gaps",
                priority=StrategicPriority.CRITICAL,
                phase=ImplementationPhase.FOUNDATION,
                estimated_cost=base_cost * 0.1,
                expected_roi=2.5,
                timeline_months=2,
                dependencies=[],
                success_metrics=["Assessment completion", "Gap analysis report", "Roadmap approval"],
                risk_level="Low"
            ),
            StrategicInitiative(
                name="Data Infrastructure Modernization",
                description="Establish robust data pipelines and governance for AI initiatives",
                priority=StrategicPriority.CRITICAL,
                phase=ImplementationPhase.FOUNDATION,
                estimated_cost=base_cost * 0.6,
                expected_roi=3.2,
                timeline_months=6,
                dependencies=["AI Readiness Assessment"],
                success_metrics=["Data quality score >85%", "Pipeline uptime >99%", "Governance framework"],
                risk_level="Medium"
            ),
            StrategicInitiative(
                name="AI Talent Development Program",
                description="Train existing workforce and recruit AI specialists",
                priority=StrategicPriority.HIGH,
                phase=ImplementationPhase.FOUNDATION,
                estimated_cost=base_cost * 0.3,
                expected_roi=4.1,
                timeline_months=4,
                dependencies=[],
                success_metrics=["Training completion rate >90%", "Skill assessment scores", "Retention rate"],
                risk_level="Low"
            )
        ]
    
    def _get_goal_specific_initiatives(self, goal: str, industry: str, company_size: str) -> List[StrategicInitiative]:
        """Get initiatives specific to strategic goals"""
        
        base_cost = 100000 if "1-50" in company_size else 400000 if "5000+" not in company_size else 1000000
        
        goal_initiatives = {
            "Cost Reduction": [
                StrategicInitiative(
                    name="Process Automation with AI",
                    description="Implement AI-driven automation for repetitive tasks",
                    priority=StrategicPriority.HIGH,
                    phase=ImplementationPhase.ACCELERATION,
                    estimated_cost=base_cost * 0.8,
                    expected_roi=5.2,
                    timeline_months=8,
                    dependencies=["Data Infrastructure Modernization"],
                    success_metrics=["Cost savings target met", "Process efficiency +30%", "ROI >400%"],
                    risk_level="Medium"
                )
            ],
            "Revenue Growth": [
                StrategicInitiative(
                    name="AI-Powered Customer Intelligence",
                    description="Deploy AI for customer insights and personalization",
                    priority=StrategicPriority.HIGH,
                    phase=ImplementationPhase.ACCELERATION,
                    estimated_cost=base_cost * 1.2,
                    expected_roi=6.8,
                    timeline_months=10,
                    dependencies=["Data Infrastructure Modernization", "AI Talent Development Program"],
                    success_metrics=["Revenue increase >15%", "Customer satisfaction +20%", "Conversion rate +25%"],
                    risk_level="Medium"
                )
            ],
            "Innovation & New Products": [
                StrategicInitiative(
                    name="AI Innovation Lab",
                    description="Establish dedicated AI research and development center",
                    priority=StrategicPriority.MEDIUM,
                    phase=ImplementationPhase.OPTIMIZATION,
                    estimated_cost=base_cost * 2.0,
                    expected_roi=4.5,
                    timeline_months=18,
                    dependencies=["AI Talent Development Program"],
                    success_metrics=["New products launched", "Patent applications", "Innovation pipeline"],
                    risk_level="High"
                )
            ]
        }
        
        return goal_initiatives.get(goal, [])
    
    def _get_industry_initiatives(self, industry: str, maturity_score: int) -> List[StrategicInitiative]:
        """Get industry-specific AI initiatives"""
        
        industry_initiatives = {
            "Technology": [
                StrategicInitiative(
                    name="Advanced ML Platform Development",
                    description="Build proprietary machine learning platform for competitive advantage",
                    priority=StrategicPriority.HIGH,
                    phase=ImplementationPhase.OPTIMIZATION,
                    estimated_cost=2000000,
                    expected_roi=7.5,
                    timeline_months=24,
                    dependencies=["Data Infrastructure Modernization", "AI Talent Development Program"],
                    success_metrics=["Platform deployment", "Performance benchmarks", "Customer adoption"],
                    risk_level="High"
                )
            ],
            "Healthcare": [
                StrategicInitiative(
                    name="Clinical Decision Support AI",
                    description="Implement AI for diagnostic assistance and treatment recommendations",
                    priority=StrategicPriority.HIGH,
                    phase=ImplementationPhase.ACCELERATION,
                    estimated_cost=1500000,
                    expected_roi=4.8,
                    timeline_months=18,
                    dependencies=["Data Infrastructure Modernization", "Regulatory Compliance Framework"],
                    success_metrics=["Clinical accuracy improvement", "Diagnostic speed +40%", "Patient outcomes"],
                    risk_level="High"
                )
            ],
            "Financial Services": [
                StrategicInitiative(
                    name="AI Risk Management System",
                    description="Deploy AI for fraud detection and risk assessment",
                    priority=StrategicPriority.CRITICAL,
                    phase=ImplementationPhase.ACCELERATION,
                    estimated_cost=1200000,
                    expected_roi=6.2,
                    timeline_months=12,
                    dependencies=["Data Infrastructure Modernization", "Regulatory Compliance Framework"],
                    success_metrics=["Fraud detection rate +60%", "Risk assessment accuracy", "Compliance metrics"],
                    risk_level="Medium"
                )
            ]
        }
        
        return industry_initiatives.get(industry, [])
    
    def _prioritize_initiatives(self, initiatives: List[StrategicInitiative], budget_range: str) -> List[StrategicInitiative]:
        """Prioritize initiatives based on ROI, priority, and budget constraints"""
        
        # Budget constraints
        budget_limits = {
            "Under $100K": 100000,
            "$100K - $500K": 500000,
            "$500K - $2M": 2000000,
            "$2M - $10M": 10000000,
            "Over $10M": float('inf')
        }
        
        budget_limit = budget_limits.get(budget_range, 1000000)
        
        # Score initiatives
        for initiative in initiatives:
            priority_score = {"Critical": 100, "High": 80, "Medium": 60, "Low": 40}[initiative.priority.value]
            roi_score = min(initiative.expected_roi * 10, 100)
            risk_penalty = {"Low": 0, "Medium": -10, "High": -20}[initiative.risk_level]
            
            initiative.total_score = priority_score + roi_score + risk_penalty
        
        # Sort by score and filter by budget
        initiatives.sort(key=lambda x: x.total_score, reverse=True)
        
        # Apply budget constraint
        selected_initiatives = []
        cumulative_cost = 0
        
        for initiative in initiatives:
            if cumulative_cost + initiative.estimated_cost <= budget_limit:
                selected_initiatives.append(initiative)
                cumulative_cost += initiative.estimated_cost
        
        return selected_initiatives
    
    def _generate_milestones(self, initiatives: List[StrategicInitiative]) -> List[Dict[str, str]]:
        """Generate key milestones from initiatives"""
        
        milestones = []
        
        # Sort initiatives by timeline
        sorted_initiatives = sorted(initiatives, key=lambda x: x.timeline_months)
        
        for i, initiative in enumerate(sorted_initiatives[:6]):  # Top 6 initiatives
            milestone_date = datetime.now() + timedelta(days=initiative.timeline_months * 30)
            
            milestones.append({
                'month': str(initiative.timeline_months),
                'milestone': f"Complete {initiative.name}",
                'description': initiative.description[:100] + "...",
                'success_metric': initiative.success_metrics[0] if initiative.success_metrics else "Completion",
                'date': milestone_date.strftime("%B %Y")
            })
        
        return milestones
    
    def _assess_maturity_score(self, maturity_level: str) -> int:
        """Convert maturity level to numeric score"""
        
        maturity_scores = {
            "Exploring (0-10%)": 5,
            "Piloting (10-25%)": 17,
            "Implementing (25-50%)": 37,
            "Scaling (50-80%)": 65,
            "Leading (80%+)": 90
        }
        
        return maturity_scores.get(maturity_level, 25)
    
    def _determine_target_maturity(self, current_score: int, strategic_goals: List[str]) -> str:
        """Determine appropriate target maturity level"""
        
        if current_score < 20:
            return "Implementing (25-50%)"
        elif current_score < 40:
            return "Scaling (50-80%)"
        else:
            return "Leading (80%+)"
    
    def _calculate_success_probability(self, industry: str, company_size: str, maturity_score: int, num_initiatives: int) -> float:
        """Calculate probability of successful implementation"""
        
        # Base probability
        base_prob = 0.7
        
        # Industry factor
        industry_factors = {
            "Technology": 0.15,
            "Financial Services": 0.10,
            "Healthcare": 0.05,
            "Manufacturing": 0.08,
            "Government": -0.05
        }
        
        industry_adjustment = industry_factors.get(industry, 0)
        
        # Size factor (larger companies have more resources)
        size_adjustment = 0.1 if "5000+" in company_size else 0.05 if "1000-4999" in company_size else -0.05
        
        # Maturity factor
        maturity_adjustment = (maturity_score - 50) / 1000
        
        # Complexity penalty
        complexity_penalty = min(num_initiatives * 0.02, 0.15)
        
        final_probability = base_prob + industry_adjustment + size_adjustment + maturity_adjustment - complexity_penalty
        
        return max(0.3, min(0.95, final_probability))
    
    def _load_industry_benchmarks(self) -> Dict:
        """Load industry benchmark data"""
        return {
            "Technology": {"avg_adoption": 92, "avg_roi": 4.2},
            "Financial Services": {"avg_adoption": 85, "avg_roi": 3.8},
            "Healthcare": {"avg_adoption": 78, "avg_roi": 3.2},
            "Manufacturing": {"avg_adoption": 75, "avg_roi": 3.5}
        }
    
    def _load_best_practices(self) -> List[str]:
        """Load AI implementation best practices"""
        return [
            "Start with high-impact, low-risk use cases",
            "Invest in data quality and governance early",
            "Build cross-functional AI teams",
            "Implement robust model monitoring and governance",
            "Prioritize explainable AI for critical decisions",
            "Establish clear AI ethics and bias guidelines",
            "Create feedback loops for continuous improvement",
            "Plan for change management and workforce transition"
        ]

# Global strategic planner instance
strategic_planner = StrategicPlanner()

# Export functions
__all__ = [
    'StrategicPriority',
    'ImplementationPhase', 
    'StrategicInitiative',
    'StrategicRoadmap',
    'StrategicPlanner',
    'strategic_planner'
]