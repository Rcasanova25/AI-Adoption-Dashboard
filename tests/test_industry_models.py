"""Unit tests for industry-specific financial models.

Tests ROI calculations and benchmarks for different industries.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from business.industry_models import (
    INDUSTRY_PROFILES,
    calculate_manufacturing_roi,
    calculate_healthcare_roi,
    calculate_financial_services_roi,
    calculate_retail_roi,
    get_industry_benchmarks,
    select_optimal_ai_strategy
)


class TestIndustryModels(unittest.TestCase):
    """Test suite for industry-specific models."""
    
    def test_industry_profiles_completeness(self):
        """Test that all industry profiles have required fields."""
        required_fields = [
            'name', 'typical_margin', 'labor_intensity', 'tech_maturity',
            'regulatory_burden', 'data_availability', 'competitive_pressure',
            'typical_project_size', 'implementation_speed'
        ]
        
        for industry, profile in INDUSTRY_PROFILES.items():
            for field in required_fields:
                self.assertTrue(
                    hasattr(profile, field),
                    f"Industry {industry} missing field {field}"
                )
                
            # Validate ranges
            self.assertGreaterEqual(profile.labor_intensity, 0)
            self.assertLessEqual(profile.labor_intensity, 1)
            self.assertGreaterEqual(profile.tech_maturity, 0)
            self.assertLessEqual(profile.tech_maturity, 1)
            self.assertGreaterEqual(profile.regulatory_burden, 0)
            self.assertLessEqual(profile.regulatory_burden, 1)
            
    def test_manufacturing_roi_basic(self):
        """Test manufacturing ROI calculation."""
        result = calculate_manufacturing_roi(
            investment=1000000,
            production_volume=100000,
            defect_rate_reduction=0.25,
            downtime_reduction=0.20,
            labor_productivity_gain=0.15,
            energy_efficiency_gain=0.10,
            years=5
        )
        
        # Check structure
        self.assertIn('financial_metrics', result)
        self.assertIn('benefit_breakdown', result)
        self.assertIn('industry_factors', result)
        self.assertIn('recommendations', result)
        
        # Financial metrics should exist
        metrics = result['financial_metrics']
        self.assertIn('npv', metrics)
        self.assertIn('irr', metrics)
        self.assertIn('payback_years', metrics)
        
        # Benefits should be positive
        benefits = result['benefit_breakdown']
        self.assertGreater(benefits['quality_improvement'], 0)
        self.assertGreater(benefits['downtime_reduction'], 0)
        self.assertGreater(benefits['productivity_gain'], 0)
        self.assertGreater(benefits['energy_savings'], 0)
        
    def test_manufacturing_roi_edge_cases(self):
        """Test manufacturing ROI with edge cases."""
        # Zero improvements
        result = calculate_manufacturing_roi(
            investment=500000,
            production_volume=50000,
            defect_rate_reduction=0,
            downtime_reduction=0,
            labor_productivity_gain=0,
            energy_efficiency_gain=0
        )
        
        # NPV should be negative (only costs, no benefits)
        self.assertLess(result['financial_metrics']['npv'], 0)
        
        # High improvements
        result = calculate_manufacturing_roi(
            investment=2000000,
            production_volume=200000,
            defect_rate_reduction=0.50,
            downtime_reduction=0.40
        )
        
        # Should have recommendations for high improvements
        self.assertGreater(len(result['recommendations']), 0)
        
    def test_healthcare_roi_basic(self):
        """Test healthcare ROI calculation."""
        result = calculate_healthcare_roi(
            investment=2000000,
            patient_volume=30000,
            diagnostic_accuracy_gain=0.15,
            patient_wait_reduction=0.25,
            admin_efficiency_gain=0.35,
            readmission_reduction=0.10,
            years=5
        )
        
        # Check healthcare-specific benefits
        benefits = result['benefit_breakdown']
        self.assertIn('clinical_outcomes', benefits)
        self.assertIn('operational_efficiency', benefits)
        self.assertIn('compliance_costs', benefits)
        
        # Clinical outcomes should include diagnostic and readmission benefits
        self.assertGreater(benefits['clinical_outcomes'], 0)
        
        # Compliance costs should be present
        self.assertGreater(benefits['compliance_costs'], 0)
        
        # Risk should be high due to regulatory burden
        self.assertEqual(result['risk_level'], "High")
        
    def test_healthcare_roi_regulatory_impact(self):
        """Test healthcare ROI with regulatory considerations."""
        # Large investment with moderate improvements
        result = calculate_healthcare_roi(
            investment=5000000,
            patient_volume=50000,
            diagnostic_accuracy_gain=0.20,
            admin_efficiency_gain=0.40
        )
        
        # Should have regulatory-related insights
        profile = INDUSTRY_PROFILES['healthcare']
        self.assertGreater(profile.regulatory_burden, 0.8)
        
        # Industry factors should reflect high regulatory burden
        self.assertGreater(result['industry_factors']['regulatory_burden'], 0.8)
        self.assertGreater(result['industry_factors']['data_privacy_requirements'], 0.9)
        
    def test_financial_services_roi_basic(self):
        """Test financial services ROI calculation."""
        result = calculate_financial_services_roi(
            investment=3000000,
            transaction_volume=5000000,
            fraud_detection_improvement=0.35,
            processing_time_reduction=0.50,
            compliance_automation=0.45,
            customer_experience_gain=0.25
        )
        
        # Check financial services specific benefits
        benefits = result['benefit_breakdown']
        self.assertIn('fraud_prevention', benefits)
        self.assertIn('operational_efficiency', benefits)
        self.assertIn('compliance_savings', benefits)
        self.assertIn('customer_retention', benefits)
        
        # Fraud prevention should be significant
        self.assertGreater(benefits['fraud_prevention'], 0)
        
        # Risk should be lower due to high tech maturity
        self.assertIn(result['risk_level'], ["Low", "Medium"])
        
    def test_financial_services_high_volume(self):
        """Test financial services with high transaction volume."""
        result = calculate_financial_services_roi(
            investment=10000000,
            transaction_volume=100000000,  # 100M transactions
            fraud_detection_improvement=0.40,
            processing_time_reduction=0.60
        )
        
        # With high volume, benefits should be substantial
        self.assertGreater(result['financial_metrics']['npv'], 0)
        
        # Should have positive recommendations
        self.assertGreater(len(result['recommendations']), 0)
        
    def test_retail_roi_basic(self):
        """Test retail/e-commerce ROI calculation."""
        result = calculate_retail_roi(
            investment=750000,
            annual_revenue=20000000,
            personalization_uplift=0.12,
            inventory_optimization=0.18,
            customer_service_automation=0.40,
            supply_chain_efficiency=0.20
        )
        
        # Check retail-specific benefits
        benefits = result['benefit_breakdown']
        self.assertIn('revenue_growth', benefits)
        self.assertIn('inventory_savings', benefits)
        self.assertIn('service_automation', benefits)
        self.assertIn('supply_chain_savings', benefits)
        
        # Revenue growth from personalization should be significant
        self.assertEqual(benefits['revenue_growth'], 20000000 * 0.12)
        
        # Industry factors should show high competitive pressure
        self.assertGreater(result['industry_factors']['competitive_pressure'], 0.9)
        
    def test_retail_roi_competitive_pressure(self):
        """Test retail ROI with competitive pressure considerations."""
        result = calculate_retail_roi(
            investment=1500000,
            annual_revenue=50000000,
            personalization_uplift=0.20,
            inventory_optimization=0.25
        )
        
        # Should have insights about competitive pressure
        profile = INDUSTRY_PROFILES['retail']
        self.assertGreater(profile.competitive_pressure, 0.9)
        
        # Should recommend AI as essential
        recommendations_text = ' '.join(result['recommendations'])
        self.assertIn('competitive', recommendations_text.lower())
        
    def test_get_industry_benchmarks(self):
        """Test industry benchmark retrieval."""
        benchmarks = get_industry_benchmarks('manufacturing')
        
        # Check structure
        self.assertIn('typical_roi_range', benchmarks)
        self.assertIn('implementation_timeline_months', benchmarks)
        self.assertIn('success_probability', benchmarks)
        self.assertIn('key_success_factors', benchmarks)
        self.assertIn('common_pitfalls', benchmarks)
        self.assertIn('recommended_use_cases', benchmarks)
        
        # ROI range should be tuple of two values
        roi_range = benchmarks['typical_roi_range']
        self.assertEqual(len(roi_range), 2)
        self.assertLess(roi_range[0], roi_range[1])
        
        # Success probability should be between 0 and 1
        self.assertGreaterEqual(benchmarks['success_probability'], 0)
        self.assertLessEqual(benchmarks['success_probability'], 1)
        
        # Should have manufacturing-specific use cases
        self.assertIn('Predictive maintenance', benchmarks['recommended_use_cases'])
        
    def test_get_industry_benchmarks_all_industries(self):
        """Test benchmarks for all industries."""
        for industry in INDUSTRY_PROFILES.keys():
            benchmarks = get_industry_benchmarks(industry)
            
            # Each industry should have valid benchmarks
            self.assertNotIn('error', benchmarks)
            self.assertGreater(len(benchmarks['recommended_use_cases']), 0)
            
            # Timeline should be positive
            self.assertGreater(benchmarks['implementation_timeline_months'], 0)
            
    def test_get_industry_benchmarks_invalid(self):
        """Test benchmark retrieval with invalid industry."""
        benchmarks = get_industry_benchmarks('invalid_industry')
        self.assertIn('error', benchmarks)
        
    def test_select_optimal_strategy_basic(self):
        """Test optimal AI strategy selection."""
        strategy = select_optimal_ai_strategy(
            industry='retail',
            company_size='Medium',
            budget=1000000,
            timeline_months=12,
            strategic_goals=['cost_reduction', 'revenue_growth']
        )
        
        # Check structure
        self.assertIn('feasibility', strategy)
        self.assertIn('recommended_approach', strategy)
        self.assertIn('priority_use_cases', strategy)
        self.assertIn('implementation_phases', strategy)
        self.assertIn('risk_mitigation', strategy)
        
        # Should be feasible with adequate budget
        self.assertIn(strategy['feasibility'], ['High', 'Medium'])
        
        # Should have implementation phases
        self.assertGreater(len(strategy['implementation_phases']), 0)
        
    def test_select_optimal_strategy_budget_constraints(self):
        """Test strategy selection with budget constraints."""
        # Low budget
        strategy = select_optimal_ai_strategy(
            industry='financial_services',
            company_size='Small',
            budget=50000,  # Very low for financial services
            timeline_months=6,
            strategic_goals=['cost_reduction']
        )
        
        # Should indicate limited feasibility
        self.assertEqual(strategy['feasibility'], 'Limited')
        self.assertIn('suggested_budget', strategy)
        
    def test_select_optimal_strategy_by_size(self):
        """Test strategy varies by company size."""
        sizes = ['Small', 'Medium', 'Large', 'Enterprise']
        strategies = []
        
        for size in sizes:
            strategy = select_optimal_ai_strategy(
                industry='technology',
                company_size=size,
                budget=2000000,
                timeline_months=12,
                strategic_goals=['revenue_growth']
            )
            strategies.append(strategy)
            
        # Enterprise should have shortest timeline
        enterprise_phases = strategies[3]['implementation_phases']
        small_phases = strategies[0]['implementation_phases']
        
        # Different risk mitigation for different sizes
        self.assertNotEqual(
            strategies[0]['risk_mitigation'],
            strategies[3]['risk_mitigation']
        )
        
    def test_select_optimal_strategy_goal_alignment(self):
        """Test strategy alignment with strategic goals."""
        # Cost reduction focus
        cost_strategy = select_optimal_ai_strategy(
            industry='manufacturing',
            company_size='Large',
            budget=3000000,
            timeline_months=18,
            strategic_goals=['cost_reduction']
        )
        
        # Revenue growth focus
        revenue_strategy = select_optimal_ai_strategy(
            industry='manufacturing',
            company_size='Large',
            budget=3000000,
            timeline_months=18,
            strategic_goals=['revenue_growth']
        )
        
        # Should have different approaches
        self.assertNotEqual(
            cost_strategy['recommended_approach'],
            revenue_strategy['recommended_approach']
        )
        
        # Cost strategy should mention automation
        self.assertIn('automation', cost_strategy['recommended_approach'].lower())
        
    def test_industry_specific_calculations(self):
        """Test that industry calculations produce different results."""
        investment = 1000000
        
        # Same investment, different industries
        mfg_result = calculate_manufacturing_roi(
            investment=investment,
            production_volume=100000
        )
        
        health_result = calculate_healthcare_roi(
            investment=investment,
            patient_volume=20000
        )
        
        fin_result = calculate_financial_services_roi(
            investment=investment,
            transaction_volume=1000000
        )
        
        retail_result = calculate_retail_roi(
            investment=investment,
            annual_revenue=10000000
        )
        
        # NPVs should all be different
        npvs = [
            mfg_result['financial_metrics']['npv'],
            health_result['financial_metrics']['npv'],
            fin_result['financial_metrics']['npv'],
            retail_result['financial_metrics']['npv']
        ]
        
        # Check that all NPVs are unique
        self.assertEqual(len(npvs), len(set(npvs)))
        
        # Risk levels should vary by industry
        risk_levels = [
            mfg_result['risk_level'],
            health_result['risk_level'],
            fin_result['risk_level'],
            retail_result['risk_level']
        ]
        
        # Healthcare should have highest risk
        self.assertEqual(health_result['risk_level'], 'High')
        
        # Financial services should have lower risk
        self.assertIn(fin_result['risk_level'], ['Low', 'Medium'])


if __name__ == '__main__':
    unittest.main(verbosity=2)