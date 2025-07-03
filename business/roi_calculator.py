"""
ROI calculation utilities for AI investments
Specialized calculations for return on investment analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ROIAnalysis:
    """Comprehensive ROI analysis results"""
    simple_roi: float
    adjusted_roi: float
    payback_months: int
    discounted_payback_months: int
    net_present_value: float
    internal_rate_of_return: float
    risk_adjusted_roi: float
    sensitivity_analysis: Dict[str, float]
    confidence_level: str


@dataclass
class SectorROIRanking:
    """Sector ROI ranking and analysis"""
    sector: str
    roi: float
    rank: int
    percentile: float
    performance_category: str
    risk_level: str
    recommended_action: str


class ROICalculator:
    """Specialized ROI calculation utilities"""
    
    # Risk-free rate (approximate US Treasury rate)
    RISK_FREE_RATE = 0.04
    
    # Market risk premiums by industry
    RISK_PREMIUMS = {
        'Technology': 0.08,
        'Financial Services': 0.06,
        'Healthcare': 0.07,
        'Manufacturing': 0.05,
        'Retail & E-commerce': 0.07,
        'Education': 0.04,
        'Energy & Utilities': 0.05,
        'Government': 0.03
    }
    
    @classmethod
    def calculate_comprehensive_roi(
        cls,
        investment: float,
        annual_benefits: List[float],
        discount_rate: float = 0.08,
        risk_adjustment: float = 0.0
    ) -> ROIAnalysis:
        """
        Calculate comprehensive ROI analysis with multiple metrics
        
        Args:
            investment: Initial investment amount
            annual_benefits: List of annual benefits (can vary by year)
            discount_rate: Discount rate for NPV calculations
            risk_adjustment: Additional risk adjustment factor
        
        Returns:
            ROIAnalysis with comprehensive metrics
        """
        try:
            if not annual_benefits or investment <= 0:
                raise ValueError("Invalid investment or benefits data")
            
            # Simple ROI (first year)
            simple_roi = annual_benefits[0] / investment if annual_benefits else 0
            
            # Adjusted ROI (average over all years)
            avg_annual_benefit = np.mean(annual_benefits)
            adjusted_roi = avg_annual_benefit / investment
            
            # Simple payback period
            cumulative_benefits = np.cumsum(annual_benefits)
            payback_months = cls._calculate_payback_months(investment, annual_benefits)
            
            # NPV calculation
            npv = cls._calculate_npv(investment, annual_benefits, discount_rate)
            
            # IRR calculation (approximate)
            irr = cls._calculate_irr(investment, annual_benefits)
            
            # Discounted payback
            discounted_payback_months = cls._calculate_discounted_payback(
                investment, annual_benefits, discount_rate
            )
            
            # Risk-adjusted ROI
            risk_adjusted_discount = discount_rate + risk_adjustment
            risk_adjusted_roi = adjusted_roi * (1 - risk_adjustment)
            
            # Sensitivity analysis
            sensitivity = cls._perform_sensitivity_analysis(
                investment, annual_benefits, discount_rate
            )
            
            # Confidence level based on risk and variance
            confidence = cls._assess_confidence_level(
                adjusted_roi, risk_adjustment, np.std(annual_benefits)
            )
            
            return ROIAnalysis(
                simple_roi=simple_roi,
                adjusted_roi=adjusted_roi,
                payback_months=payback_months,
                discounted_payback_months=discounted_payback_months,
                net_present_value=npv,
                internal_rate_of_return=irr,
                risk_adjusted_roi=risk_adjusted_roi,
                sensitivity_analysis=sensitivity,
                confidence_level=confidence
            )
            
        except Exception as e:
            logger.error(f"Error in ROI calculation: {e}")
            return ROIAnalysis(
                simple_roi=0.0,
                adjusted_roi=0.0,
                payback_months=999,
                discounted_payback_months=999,
                net_present_value=-investment,
                internal_rate_of_return=0.0,
                risk_adjusted_roi=0.0,
                sensitivity_analysis={},
                confidence_level="Low"
            )
    
    @classmethod
    def calculate_sector_roi_ranking(
        cls, 
        sector_data: pd.DataFrame
    ) -> List[SectorROIRanking]:
        """
        Calculate and rank sectors by ROI with comprehensive analysis
        
        Args:
            sector_data: DataFrame with sector ROI data
            
        Returns:
            List of SectorROIRanking objects
        """
        if sector_data is None or 'avg_roi' not in sector_data.columns:
            return []
        
        try:
            # Create working copy
            df = sector_data.copy()
            
            # Calculate rankings
            df['roi_rank'] = df['avg_roi'].rank(ascending=False, method='min')
            df['roi_percentile'] = df['avg_roi'].rank(pct=True) * 100
            
            # Categorize performance
            df['performance_category'] = pd.cut(
                df['avg_roi'],
                bins=[0, 2.5, 3.5, float('inf')],
                labels=['Below Threshold', 'Good', 'Excellent'],
                include_lowest=True
            )
            
            # Assess risk levels based on adoption rate vs ROI
            df['risk_level'] = df.apply(cls._assess_sector_risk, axis=1)
            
            # Generate recommendations
            df['recommended_action'] = df.apply(cls._generate_sector_recommendation, axis=1)
            
            # Create ranking objects
            rankings = []
            for _, row in df.iterrows():
                rankings.append(SectorROIRanking(
                    sector=row['sector'],
                    roi=row['avg_roi'],
                    rank=int(row['roi_rank']),
                    percentile=row['roi_percentile'],
                    performance_category=str(row['performance_category']),
                    risk_level=row['risk_level'],
                    recommended_action=row['recommended_action']
                ))
            
            # Sort by rank
            rankings.sort(key=lambda x: x.rank)
            
            return rankings
            
        except Exception as e:
            logger.error(f"Error calculating sector rankings: {e}")
            return []
    
    @classmethod
    def calculate_payback_scenarios(
        cls,
        investment: float,
        monthly_benefits: float,
        growth_rate: float = 0.0,
        discount_rate: float = 0.08
    ) -> Dict[str, float]:
        """
        Calculate payback under different scenarios
        
        Args:
            investment: Initial investment
            monthly_benefits: Monthly benefit amount
            growth_rate: Monthly growth rate of benefits
            discount_rate: Annual discount rate
        
        Returns:
            Dictionary with different payback scenarios
        """
        try:
            if monthly_benefits <= 0:
                return {
                    "simple_payback": float('inf'),
                    "growth_adjusted_payback": float('inf'),
                    "discounted_payback": float('inf'),
                    "break_even_month": float('inf')
                }
            
            # Simple payback (no growth, no discounting)
            simple_payback = investment / monthly_benefits
            
            # Payback with growth (no discounting)
            if growth_rate > 0:
                # Solve for when cumulative benefits = investment
                # Sum of growing monthly benefits = investment
                growth_payback = cls._solve_growth_payback(investment, monthly_benefits, growth_rate)
            else:
                growth_payback = simple_payback
            
            # Discounted payback
            monthly_discount_rate = discount_rate / 12
            discounted_payback = cls._calculate_discounted_monthly_payback(
                investment, monthly_benefits, monthly_discount_rate, growth_rate
            )
            
            return {
                "simple_payback": simple_payback,
                "growth_adjusted_payback": growth_payback,
                "discounted_payback": discounted_payback,
                "break_even_month": min(simple_payback, growth_payback, discounted_payback)
            }
            
        except Exception as e:
            logger.error(f"Error calculating payback scenarios: {e}")
            return {
                "simple_payback": float('inf'),
                "growth_adjusted_payback": float('inf'),
                "discounted_payback": float('inf'),
                "break_even_month": float('inf')
            }
    
    @classmethod
    def _calculate_payback_months(
        cls, 
        investment: float, 
        annual_benefits: List[float]
    ) -> int:
        """Calculate simple payback period in months"""
        cumulative = 0
        months = 0
        
        for year, annual_benefit in enumerate(annual_benefits):
            monthly_benefit = annual_benefit / 12
            for month in range(12):
                cumulative += monthly_benefit
                months += 1
                if cumulative >= investment:
                    return months
        
        return 999  # If payback not achieved
    
    @classmethod
    def _calculate_npv(
        cls, 
        investment: float, 
        annual_benefits: List[float], 
        discount_rate: float
    ) -> float:
        """Calculate Net Present Value"""
        npv = -investment  # Initial outflow
        
        for year, benefit in enumerate(annual_benefits):
            present_value = benefit / ((1 + discount_rate) ** (year + 1))
            npv += present_value
        
        return npv
    
    @classmethod
    def _calculate_irr(
        cls, 
        investment: float, 
        annual_benefits: List[float]
    ) -> float:
        """Approximate Internal Rate of Return calculation"""
        try:
            # Simple approximation using binary search
            low_rate, high_rate = 0.0, 1.0
            
            for _ in range(100):  # Max iterations
                mid_rate = (low_rate + high_rate) / 2
                npv = cls._calculate_npv(investment, annual_benefits, mid_rate)
                
                if abs(npv) < 0.01:  # Close enough to zero
                    return mid_rate
                elif npv > 0:
                    low_rate = mid_rate
                else:
                    high_rate = mid_rate
            
            return mid_rate
            
        except:
            # Fallback: simple approximation
            total_benefits = sum(annual_benefits)
            avg_annual_benefit = total_benefits / len(annual_benefits)
            return (avg_annual_benefit / investment) - 1
    
    @classmethod
    def _calculate_discounted_payback(
        cls, 
        investment: float, 
        annual_benefits: List[float], 
        discount_rate: float
    ) -> int:
        """Calculate discounted payback period in months"""
        cumulative_pv = 0
        months = 0
        
        for year, annual_benefit in enumerate(annual_benefits):
            monthly_benefit = annual_benefit / 12
            for month in range(12):
                months += 1
                # Present value of this month's benefit
                pv_benefit = monthly_benefit / ((1 + discount_rate/12) ** months)
                cumulative_pv += pv_benefit
                
                if cumulative_pv >= investment:
                    return months
        
        return 999  # If payback not achieved
    
    @classmethod
    def _perform_sensitivity_analysis(
        cls, 
        investment: float, 
        annual_benefits: List[float], 
        base_discount_rate: float
    ) -> Dict[str, float]:
        """Perform sensitivity analysis on key variables"""
        base_roi = np.mean(annual_benefits) / investment
        
        sensitivity = {}
        
        # Benefit sensitivity (+/- 20%)
        high_benefits = [b * 1.2 for b in annual_benefits]
        low_benefits = [b * 0.8 for b in annual_benefits]
        
        sensitivity['benefits_+20%'] = np.mean(high_benefits) / investment
        sensitivity['benefits_-20%'] = np.mean(low_benefits) / investment
        
        # Discount rate sensitivity
        sensitivity['discount_+2%'] = cls._calculate_npv(investment, annual_benefits, base_discount_rate + 0.02) / investment
        sensitivity['discount_-2%'] = cls._calculate_npv(investment, annual_benefits, base_discount_rate - 0.02) / investment
        
        # Investment sensitivity (+/- 15%)
        sensitivity['investment_+15%'] = np.mean(annual_benefits) / (investment * 1.15)
        sensitivity['investment_-15%'] = np.mean(annual_benefits) / (investment * 0.85)
        
        return sensitivity
    
    @classmethod
    def _assess_confidence_level(
        cls, 
        roi: float, 
        risk_adjustment: float, 
        benefit_variance: float
    ) -> str:
        """Assess confidence level based on risk factors"""
        if roi > 3.0 and risk_adjustment < 0.1 and benefit_variance < 0.5:
            return "High"
        elif roi > 2.0 and risk_adjustment < 0.2:
            return "Medium"
        elif roi > 1.5:
            return "Low"
        else:
            return "Very Low"
    
    @classmethod
    def _assess_sector_risk(cls, row: pd.Series) -> str:
        """Assess risk level for a sector based on adoption and ROI"""
        roi = row.get('avg_roi', 0)
        adoption = row.get('adoption_rate', 0)
        
        # High ROI + High adoption = Low risk
        if roi > 3.5 and adoption > 80:
            return "Low"
        # Good ROI + Good adoption = Medium risk
        elif roi > 2.5 and adoption > 60:
            return "Medium"
        # Low adoption or low ROI = High risk
        elif roi < 2.5 or adoption < 40:
            return "High"
        else:
            return "Medium"
    
    @classmethod
    def _generate_sector_recommendation(cls, row: pd.Series) -> str:
        """Generate recommendation for a sector"""
        roi = row.get('avg_roi', 0)
        adoption = row.get('adoption_rate', 0)
        
        if roi > 3.5:
            return "High priority investment - excellent returns"
        elif roi > 2.5 and adoption > 70:
            return "Recommended investment - good returns with market validation"
        elif roi > 2.5:
            return "Conditional investment - good ROI but monitor adoption trends"
        elif adoption > 80:
            return "Market pressure investment - required for competitiveness"
        else:
            return "Cautious approach - evaluate alternatives"
    
    @classmethod
    def _solve_growth_payback(
        cls, 
        investment: float, 
        initial_monthly_benefit: float, 
        growth_rate: float
    ) -> float:
        """Solve for payback period with growing benefits"""
        # Approximate solution using iteration
        cumulative = 0
        monthly_benefit = initial_monthly_benefit
        month = 0
        
        while cumulative < investment and month < 120:  # Max 10 years
            month += 1
            cumulative += monthly_benefit
            monthly_benefit *= (1 + growth_rate)
            
        return month if cumulative >= investment else float('inf')
    
    @classmethod
    def _calculate_discounted_monthly_payback(
        cls, 
        investment: float, 
        monthly_benefit: float, 
        monthly_discount_rate: float,
        growth_rate: float = 0.0
    ) -> float:
        """Calculate discounted payback with optional growth"""
        cumulative_pv = 0
        current_benefit = monthly_benefit
        month = 0
        
        while cumulative_pv < investment and month < 120:  # Max 10 years
            month += 1
            pv_benefit = current_benefit / ((1 + monthly_discount_rate) ** month)
            cumulative_pv += pv_benefit
            current_benefit *= (1 + growth_rate)
        
        return month if cumulative_pv >= investment else float('inf')


# Create instance for easy import
roi_calculator = ROICalculator()

# Add compatibility method for calculate_roi
def calculate_roi(investment: float, return_amount: float) -> float:
    """Calculate simple ROI as (return_amount - investment) / investment"""
    try:
        if investment == 0:
            return 0.0
        return (return_amount - investment) / investment
    except Exception as e:
        logger.error(f"Error calculating ROI: {e}")
        return 0.0

# Add method to ROI calculator instance
roi_calculator.calculate_roi = calculate_roi