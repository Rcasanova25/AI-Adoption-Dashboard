"""
Business logic and metric calculations for AI Adoption Dashboard
Centralizes all business rules, assessments, and calculations
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)


class CompetitivePosition(Enum):
    """Competitive position categories"""
    LEADER = "LEADER"
    COMPETITIVE = "COMPETITIVE"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"


class InvestmentRecommendation(Enum):
    """Investment recommendation categories"""
    APPROVE = "APPROVE"
    CONDITIONAL = "CONDITIONAL"
    REVIEW_SCOPE = "REVIEW SCOPE"
    REJECT = "REJECT"


class UrgencyLevel(Enum):
    """Urgency level categories"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


@dataclass
class CompetitiveAssessment:
    """Results of competitive position assessment"""
    position: CompetitivePosition
    score: float
    industry_benchmark: float
    size_benchmark: float
    gap_analysis: str
    recommendations: List[str]
    urgency_level: int
    risk_factors: List[str]
    opportunities: List[str]


@dataclass
class InvestmentCase:
    """AI investment business case"""
    investment_amount: float
    timeline_months: int
    expected_roi: float
    total_return: float
    net_benefit: float
    monthly_benefit: float
    payback_months: int
    recommendation: InvestmentRecommendation
    risk_factors: List[str]
    success_factors: List[str]
    market_context: str
    confidence_level: str


@dataclass
class MarketIntelligence:
    """Market intelligence summary"""
    adoption_rate: float
    growth_rate: float
    investment_trend: str
    cost_trend: str
    competitive_intensity: str
    market_maturity: str
    key_insights: List[str]
    risk_level: str
    opportunity_score: float


class BusinessMetrics:
    """Core business metrics and calculations"""
    
    # Industry benchmarks (from your data)
    INDUSTRY_BENCHMARKS = {
        'Technology': 92,
        'Financial Services': 85,
        'Healthcare': 78,
        'Manufacturing': 75,
        'Retail & E-commerce': 72,
        'Education': 65,
        'Energy & Utilities': 58,
        'Government': 52
    }
    
    # Company size benchmarks
    SIZE_BENCHMARKS = {
        '1-50': 3,
        '51-250': 12,
        '251-1000': 25,
        '1000-5000': 42,
        '5000+': 58
    }
    
    # ROI multipliers by industry
    INDUSTRY_ROI = {
        'Technology': 4.2,
        'Financial Services': 3.8,
        'Healthcare': 3.2,
        'Manufacturing': 3.5,
        'Retail & E-commerce': 3.0,
        'Education': 2.5,
        'Energy & Utilities': 2.8,
        'Government': 2.2
    }
    
    @staticmethod
    def extract_rate_from_string(text: str) -> float:
        """Extract percentage rate from string like 'Technology (92% adoption)'"""
        match = re.search(r'\((\d+)%', text)
        return float(match.group(1)) if match else 50.0
    
    @staticmethod
    def extract_industry_name(text: str) -> str:
        """Extract clean industry name from selection"""
        return text.split('(')[0].strip()
    
    @staticmethod
    def extract_size_category(text: str) -> str:
        """Extract size category from selection"""
        if '1-50' in text:
            return '1-50'
        elif '51-250' in text:
            return '51-250'
        elif '251-1000' in text:
            return '251-1000'
        elif '1000-5000' in text:
            return '1000-5000'
        elif '5000+' in text:
            return '5000+'
        else:
            return '1-50'  # Default to small
    
    @classmethod
    def assess_competitive_position(
        cls,
        industry: str,
        company_size: str,
        current_maturity: str = "Exploring",
        urgency_factor: int = 5
    ) -> CompetitiveAssessment:
        """
        Comprehensive competitive position assessment
        
        Args:
            industry: Company industry (with or without percentage)
            company_size: Company size category (with or without percentage)
            current_maturity: Current AI maturity level
            urgency_factor: Competitive urgency (1-10)
        
        Returns:
            CompetitiveAssessment with detailed analysis
        """
        try:
            # Extract rates and clean names
            industry_rate = cls.extract_rate_from_string(industry)
            size_rate = cls.extract_rate_from_string(company_size)
            clean_industry = cls.extract_industry_name(industry)
            clean_size = cls.extract_size_category(company_size)
            
            # Calculate composite score
            composite_score = (industry_rate + size_rate) / 2
            
            # Adjust for maturity level
            maturity_multipliers = {
                "No AI": 0.1,
                "Exploring": 0.2,
                "Pilot Stage": 0.4,
                "Piloting": 0.4,
                "Early Adoption": 0.6,
                "Implementing": 0.7,
                "Scaling": 0.8,
                "Advanced": 1.0,
                "Leading": 1.0
            }
            
            # Extract maturity key
            maturity_key = current_maturity.split('(')[0].strip()
            maturity_multiplier = maturity_multipliers.get(maturity_key, 0.5)
            
            adjusted_score = composite_score * maturity_multiplier
            
            # Determine position
            if adjusted_score >= 70:
                position = CompetitivePosition.LEADER
                gap_analysis = "You're in a leading position with strong competitive advantages. Focus on maintaining innovation edge and market leadership."
            elif adjusted_score >= 50:
                position = CompetitivePosition.COMPETITIVE
                gap_analysis = "You're competitive but need to accelerate adoption to maintain position against aggressive competitors."
            elif adjusted_score >= 25:
                position = CompetitivePosition.AT_RISK
                gap_analysis = "You're at risk of falling behind market leaders. Immediate strategic action required to close the gap."
            else:
                position = CompetitivePosition.CRITICAL
                gap_analysis = "Critical competitive gap exists. Emergency transformation initiative required to avoid market displacement."
            
            # Generate specific recommendations
            recommendations = cls._generate_position_recommendations(
                position, urgency_factor, industry_rate, size_rate, clean_industry, clean_size
            )
            
            # Identify risk factors and opportunities
            risk_factors = cls._identify_risk_factors(position, adjusted_score, urgency_factor)
            opportunities = cls._identify_opportunities(position, clean_industry, clean_size)
            
            return CompetitiveAssessment(
                position=position,
                score=adjusted_score,
                industry_benchmark=industry_rate,
                size_benchmark=size_rate,
                gap_analysis=gap_analysis,
                recommendations=recommendations,
                urgency_level=urgency_factor,
                risk_factors=risk_factors,
                opportunities=opportunities
            )
            
        except Exception as e:
            logger.error(f"Error in competitive assessment: {e}")
            return CompetitiveAssessment(
                position=CompetitivePosition.AT_RISK,
                score=0.0,
                industry_benchmark=50.0,
                size_benchmark=25.0,
                gap_analysis="Assessment failed - manual review required",
                recommendations=["Conduct detailed competitive analysis", "Engage AI strategy consultants"],
                urgency_level=urgency_factor,
                risk_factors=["Assessment uncertainty"],
                opportunities=["Opportunity for strategic differentiation"]
            )
    
    @classmethod
    def calculate_investment_case(
        cls,
        investment_amount: float,
        timeline_months: int,
        industry: str,
        primary_goal: str,
        risk_tolerance: str = "Medium"
    ) -> InvestmentCase:
        """
        Calculate comprehensive investment business case
        
        Args:
            investment_amount: Total investment amount in USD
            timeline_months: Investment timeline in months
            industry: Company industry
            primary_goal: Primary investment objective
            risk_tolerance: Risk tolerance level
        
        Returns:
            InvestmentCase with financial projections and recommendations
        """
        try:
            # Goal impact multipliers
            goal_multipliers = {
                "Operational Efficiency": 1.2,
                "Revenue Growth": 1.1,
                "Cost Reduction": 1.3,
                "Innovation & New Products": 1.0,
                "Risk Management": 0.9,
                "Customer Experience": 1.1,
                "Competitive Advantage": 1.15,
                "Process Automation": 1.25
            }
            
            # Extract clean industry name and get base ROI
            clean_industry = cls.extract_industry_name(industry)
            base_roi = cls.INDUSTRY_ROI.get(clean_industry, 3.0)
            adjusted_roi = base_roi * goal_multipliers.get(primary_goal, 1.0)
            
            # Risk adjustments
            risk_adjustments = {"Low": 1.1, "Medium": 1.0, "High": 0.9}
            risk_adjusted_roi = adjusted_roi * risk_adjustments.get(risk_tolerance, 1.0)
            
            # Timeline adjustments (longer timelines can achieve higher ROI)
            if timeline_months >= 24:
                timeline_bonus = 1.1
            elif timeline_months >= 18:
                timeline_bonus = 1.05
            else:
                timeline_bonus = 0.95
            
            final_roi = risk_adjusted_roi * timeline_bonus
            
            # Calculate financial metrics
            total_return = investment_amount * final_roi
            net_benefit = total_return - investment_amount
            monthly_benefit = net_benefit / timeline_months if timeline_months > 0 else 0
            payback_months = max(6, int(timeline_months / final_roi)) if final_roi > 0 else 999
            
            # Determine recommendation
            if final_roi >= 3.5:
                recommendation = InvestmentRecommendation.APPROVE
                confidence = "High"
            elif final_roi >= 2.5:
                recommendation = InvestmentRecommendation.CONDITIONAL
                confidence = "Medium"
            elif final_roi >= 2.0:
                recommendation = InvestmentRecommendation.REVIEW_SCOPE
                confidence = "Low"
            else:
                recommendation = InvestmentRecommendation.REJECT
                confidence = "Very Low"
            
            # Generate risk factors and success factors
            risk_factors = cls._identify_investment_risks(
                investment_amount, timeline_months, clean_industry, final_roi
            )
            success_factors = cls._identify_success_factors(
                primary_goal, clean_industry, timeline_months
            )
            
            # Market context
            market_context = cls._generate_market_context(clean_industry, investment_amount)
            
            return InvestmentCase(
                investment_amount=investment_amount,
                timeline_months=timeline_months,
                expected_roi=final_roi,
                total_return=total_return,
                net_benefit=net_benefit,
                monthly_benefit=monthly_benefit,
                payback_months=payback_months,
                recommendation=recommendation,
                risk_factors=risk_factors,
                success_factors=success_factors,
                market_context=market_context,
                confidence_level=confidence
            )
            
        except Exception as e:
            logger.error(f"Error calculating investment case: {e}")
            return InvestmentCase(
                investment_amount=investment_amount,
                timeline_months=timeline_months,
                expected_roi=2.0,
                total_return=investment_amount * 2.0,
                net_benefit=investment_amount,
                monthly_benefit=investment_amount / max(timeline_months, 1),
                payback_months=max(timeline_months, 12),
                recommendation=InvestmentRecommendation.REVIEW_SCOPE,
                risk_factors=["Calculation error - requires manual review"],
                success_factors=["Proper planning and execution"],
                market_context="Analysis incomplete due to calculation error",
                confidence_level="Low"
            )
    
    @classmethod
    def generate_market_intelligence(
        cls,
        historical_data: Optional[pd.DataFrame] = None,
        investment_data: Optional[pd.DataFrame] = None,
        cost_data: Optional[pd.DataFrame] = None
    ) -> MarketIntelligence:
        """
        Generate comprehensive market intelligence summary
        
        Args:
            historical_data: Historical adoption data
            investment_data: Investment trend data
            cost_data: Cost reduction data
        
        Returns:
            MarketIntelligence summary
        """
        try:
            # Calculate current adoption rate and growth
            current_adoption = 78.0  # Default
            growth_rate = 0.0
            
            if historical_data is not None and len(historical_data) >= 2:
                current_adoption = float(historical_data['ai_use'].iloc[-1])
                previous_adoption = float(historical_data['ai_use'].iloc[-2])
                growth_rate = ((current_adoption - previous_adoption) / previous_adoption) * 100
            
            # Analyze investment trend
            investment_trend = "Strong Growth"
            if investment_data is not None and len(investment_data) >= 2:
                recent_growth = ((investment_data['total_investment'].iloc[-1] - 
                                investment_data['total_investment'].iloc[-2]) / 
                               investment_data['total_investment'].iloc[-2]) * 100
                if recent_growth > 40:
                    investment_trend = "Explosive Growth"
                elif recent_growth > 25:
                    investment_trend = "Very Strong Growth"
                elif recent_growth > 15:
                    investment_trend = "Strong Growth"
                elif recent_growth > 5:
                    investment_trend = "Moderate Growth"
                else:
                    investment_trend = "Stabilizing"
            
            # Analyze cost trend
            cost_trend = "Dramatic Reduction"
            if cost_data is not None and len(cost_data) >= 2:
                cost_reduction_factor = (cost_data['cost_per_million_tokens'].iloc[0] / 
                                       cost_data['cost_per_million_tokens'].iloc[-1])
                if cost_reduction_factor > 200:
                    cost_trend = "Revolutionary Cost Collapse"
                elif cost_reduction_factor > 50:
                    cost_trend = "Dramatic Cost Reduction"
                elif cost_reduction_factor > 10:
                    cost_trend = "Significant Cost Reduction"
                else:
                    cost_trend = "Moderate Cost Improvement"
            
            # Determine market characteristics
            if current_adoption > 75:
                competitive_intensity = "Very High"
                market_maturity = "Mainstream Adoption"
                risk_level = "High - Fast-moving market"
            elif current_adoption > 60:
                competitive_intensity = "High"
                market_maturity = "Early Majority"
                risk_level = "Medium-High"
            elif current_adoption > 40:
                competitive_intensity = "Medium-High"
                market_maturity = "Early Adopters"
                risk_level = "Medium"
            else:
                competitive_intensity = "Medium"
                market_maturity = "Innovators"
                risk_level = "Low-Medium"
            
            # Calculate opportunity score
            opportunity_score = min(100, (100 - current_adoption) + (growth_rate * 2))
            
            # Generate key insights
            key_insights = [
                f"Market has reached {current_adoption:.0f}% adoption - {market_maturity.lower()} phase",
                f"Investment trend: {investment_trend.lower()}",
                f"Cost barriers eliminated: {cost_trend.lower()}",
                f"Competitive intensity: {competitive_intensity.lower()}"
            ]
            
            if growth_rate > 20:
                key_insights.append("Fastest enterprise technology adoption in history")
            
            if current_adoption > 75:
                key_insights.append("Non-adopters becoming minority - urgent action required")
            
            if investment_trend == "Explosive Growth":
                key_insights.append("Record investment levels validate massive market opportunity")
            
            return MarketIntelligence(
                adoption_rate=current_adoption,
                growth_rate=growth_rate,
                investment_trend=investment_trend,
                cost_trend=cost_trend,
                competitive_intensity=competitive_intensity,
                market_maturity=market_maturity,
                key_insights=key_insights,
                risk_level=risk_level,
                opportunity_score=opportunity_score
            )
            
        except Exception as e:
            logger.error(f"Error generating market intelligence: {e}")
            return MarketIntelligence(
                adoption_rate=78.0,
                growth_rate=23.0,
                investment_trend="Strong Growth",
                cost_trend="Dramatic Reduction",
                competitive_intensity="High",
                market_maturity="Mainstream Adoption",
                key_insights=["Market intelligence calculation incomplete"],
                risk_level="Medium",
                opportunity_score=50.0
            )
    
    @classmethod
    def _generate_position_recommendations(
        cls,
        position: CompetitivePosition,
        urgency: int,
        industry_rate: float,
        size_rate: float,
        industry: str,
        size_category: str
    ) -> List[str]:
        """Generate specific recommendations based on competitive position"""
        recommendations = []
        
        if position == CompetitivePosition.LEADER:
            recommendations.extend([
                "Maintain leadership through continuous AI innovation",
                "Focus on advanced capabilities (AI agents, multi-modal AI)",
                "Consider strategic acquisitions to expand AI capabilities",
                "Develop AI governance and ethics frameworks",
                "Share thought leadership to influence industry standards"
            ])
            
            if industry in ['Technology', 'Financial Services']:
                recommendations.append("Explore AI product development opportunities")
                
        elif position == CompetitivePosition.COMPETITIVE:
            recommendations.extend([
                "Accelerate AI deployment to maintain competitive position",
                "Focus on high-ROI use cases for quick wins",
                "Invest heavily in AI talent acquisition and training",
                "Monitor competitor AI strategies closely",
                "Develop AI center of excellence"
            ])
            
            if industry_rate > 80:
                recommendations.append("Industry moving fast - increase investment pace")
                
        elif position == CompetitivePosition.AT_RISK:
            recommendations.extend([
                "Launch immediate AI strategy development initiative",
                "Secure executive sponsorship and dedicated budget",
                "Partner with AI vendors for rapid deployment",
                "Start with pilot projects in highest-impact areas",
                "Hire external AI consultants for acceleration"
            ])
            
            if size_category in ['1-50', '51-250']:
                recommendations.append("Consider AI-as-a-Service solutions for faster deployment")
                
        else:  # CRITICAL
            recommendations.extend([
                "Declare AI transformation as company-wide emergency initiative",
                "Establish AI transformation office with C-level leadership",
                "Consider emergency consulting engagement",
                "Rapid competitive gap analysis and catch-up plan",
                "Evaluate acquisition targets with strong AI capabilities"
            ])
        
        # Add urgency-specific recommendations
        if urgency >= 8:
            recommendations.insert(0, "🚨 URGENT: Competitive threat requires immediate C-level action")
        elif urgency >= 6:
            recommendations.insert(0, "⚡ HIGH PRIORITY: Accelerate all AI initiatives")
        
        return recommendations
    
    @classmethod
    def _identify_risk_factors(
        cls,
        position: CompetitivePosition,
        score: float,
        urgency: int
    ) -> List[str]:
        """Identify key risk factors"""
        risks = []
        
        if position in [CompetitivePosition.AT_RISK, CompetitivePosition.CRITICAL]:
            risks.extend([
                "Competitor advantage acceleration",
                "Market share erosion risk",
                "Talent acquisition challenges"
            ])
        
        if score < 30:
            risks.append("Severe competitive disadvantage")
            
        if urgency >= 8:
            risks.append("Time-critical competitive window closing")
        
        return risks
    
    @classmethod
    def _identify_opportunities(
        cls,
        position: CompetitivePosition,
        industry: str,
        size_category: str
    ) -> List[str]:
        """Identify key opportunities"""
        opportunities = []
        
        if position == CompetitivePosition.LEADER:
            opportunities.extend([
                "Market leadership monetization",
                "AI product development opportunities",
                "Industry standard-setting influence"
            ])
        else:
            opportunities.extend([
                "Fast-follower advantage (learn from leader mistakes)",
                "Technology cost reduction benefits",
                "Leapfrog opportunity with latest AI technologies"
            ])
        
        if industry in ['Healthcare', 'Education', 'Government']:
            opportunities.append("First-mover advantage in conservative industry")
            
        if size_category in ['1-50', '51-250']:
            opportunities.append("Agility advantage over large competitors")
        
        return opportunities
    
    @classmethod
    def _identify_investment_risks(
        cls,
        amount: float,
        timeline: int,
        industry: str,
        roi: float
    ) -> List[str]:
        """Identify investment-specific risk factors"""
        risks = []
        
        if amount > 1000000:
            risks.append("Large investment requires strong governance and phased approach")
        
        if timeline < 12:
            risks.append("Aggressive timeline increases execution risk")
        
        if roi < 2.5:
            risks.append("Below-threshold ROI requires careful monitoring and course correction")
        
        if industry == "Government":
            risks.extend([
                "Regulatory and procurement complexity",
                "Longer approval cycles"
            ])
        elif industry == "Healthcare":
            risks.extend([
                "Regulatory compliance requirements",
                "Data privacy and security concerns"
            ])
        
        return risks
    
    @classmethod
    def _identify_success_factors(
        cls,
        goal: str,
        industry: str,
        timeline: int
    ) -> List[str]:
        """Identify key success factors"""
        factors = [
            "Strong executive leadership and sustained sponsorship",
            "Clear success metrics and governance framework",
            "Adequate AI talent and comprehensive training programs"
        ]
        
        if goal == "Operational Efficiency":
            factors.append("Process automation and workflow integration expertise")
        elif goal == "Revenue Growth":
            factors.append("Customer-facing AI applications and user adoption")
        elif goal == "Innovation & New Products":
            factors.append("R&D partnerships and experimentation culture")
        elif goal == "Cost Reduction":
            factors.append("Process optimization and change management")
        
        if timeline > 18:
            factors.append("Phased implementation approach with early wins")
        
        if industry in ['Technology', 'Financial Services']:
            factors.append("Advanced AI capabilities and technical expertise")
        
        return factors
    
    @classmethod
    def _generate_market_context(
        cls,
        industry: str,
        investment_amount: float
    ) -> str:
        """Generate market context for investment"""
        industry_context = {
            'Technology': "Highly competitive market with rapid AI innovation",
            'Financial Services': "Regulated environment with strong ROI potential",
            'Healthcare': "Conservative adoption but high impact opportunities",
            'Manufacturing': "Process optimization focus with proven ROI",
            'Government': "Slower adoption but significant efficiency gains possible"
        }
        
        base_context = industry_context.get(industry, "Moderate AI adoption with growth potential")
        
        if investment_amount > 2000000:
            return f"{base_context}. Large investment scale enables comprehensive transformation."
        elif investment_amount > 500000:
            return f"{base_context}. Significant investment enables strategic AI capabilities."
        else:
            return f"{base_context}. Focused investment approach recommended."


# Create instance for easy import
business_metrics = BusinessMetrics()