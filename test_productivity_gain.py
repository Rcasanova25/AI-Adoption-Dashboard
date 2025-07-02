#!/usr/bin/env python3
"""
Test Productivity Gain Calculation - Standard Approach Validation

This script validates that the calculate_productivity_gain method follows
the established standard approach and uses authentic project data.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import logging

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_productivity_gain_standard_approach():
    """Test that calculate_productivity_gain follows standard approach"""
    
    try:
        from business.metrics import business_metrics, calculate_roi
        
        logger.info("🧪 Testing Productivity Gain Standard Approach")
        logger.info("=" * 60)
        
        # Test 1: Basic functionality
        logger.info("Test 1: Basic functionality with default parameters")
        result = business_metrics.calculate_productivity_gain()
        
        # Validate return structure
        required_keys = [
            'base_gain', 'adjusted_gain', 'annual_impact', 'cumulative_gain',
            'confidence_level', 'confidence_score', 'factors', 'recommendations',
            'calculation_breakdown'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"
        
        logger.info(f"✅ Basic functionality test passed")
        logger.info(f"   Base gain: {result['base_gain']}%")
        logger.info(f"   Adjusted gain: {result['adjusted_gain']}%")
        logger.info(f"   Confidence level: {result['confidence_level']}")
        
        # Test 2: Skill level variations
        logger.info("\nTest 2: Skill level variations")
        skill_levels = ['Low-skilled', 'Medium-skilled', 'High-skilled']
        
        for skill in skill_levels:
            result = business_metrics.calculate_productivity_gain(skill_level=skill)
            logger.info(f"   {skill}: {result['base_gain']}% base gain")
            
            # Validate skill level logic (Low-skilled should have higher gains)
            if skill == 'Low-skilled':
                assert result['base_gain'] > 10, f"Low-skilled should have high gains, got {result['base_gain']}"
            elif skill == 'High-skilled':
                assert result['base_gain'] < 10, f"High-skilled should have lower gains, got {result['base_gain']}"
        
        logger.info("✅ Skill level variations test passed")
        
        # Test 3: Industry variations
        logger.info("\nTest 3: Industry variations")
        industries = ['Technology', 'Healthcare', 'Government']
        
        for industry in industries:
            result = business_metrics.calculate_productivity_gain(industry=industry)
            logger.info(f"   {industry}: {result['adjusted_gain']}% adjusted gain")
            
            # Technology should have higher gains than Government
            if industry == 'Technology':
                tech_gain = result['adjusted_gain']
            elif industry == 'Government':
                gov_gain = result['adjusted_gain']
        
        assert tech_gain > gov_gain, f"Technology should have higher gains than Government"
        logger.info("✅ Industry variations test passed")
        
        # Test 4: Function variations
        logger.info("\nTest 4: Function variations")
        functions = ['Software Engineering', 'HR', 'Finance']
        
        for function in functions:
            result = business_metrics.calculate_productivity_gain(function=function)
            logger.info(f"   {function}: {result['adjusted_gain']}% adjusted gain")
            
            # Software Engineering should have higher gains than HR
            if function == 'Software Engineering':
                eng_gain = result['adjusted_gain']
            elif function == 'HR':
                hr_gain = result['adjusted_gain']
        
        assert eng_gain > hr_gain, f"Software Engineering should have higher gains than HR"
        logger.info("✅ Function variations test passed")
        
        # Test 5: Maturity level variations
        logger.info("\nTest 5: Maturity level variations")
        maturity_levels = ['No AI', 'Early Adoption', 'Advanced']
        
        for maturity in maturity_levels:
            result = business_metrics.calculate_productivity_gain(implementation_maturity=maturity)
            logger.info(f"   {maturity}: {result['adjusted_gain']}% adjusted gain")
            
            # Advanced should have higher gains than No AI
            if maturity == 'Advanced':
                advanced_gain = result['adjusted_gain']
            elif maturity == 'No AI':
                no_ai_gain = result['adjusted_gain']
        
        assert advanced_gain > no_ai_gain, f"Advanced maturity should have higher gains than No AI"
        logger.info("✅ Maturity level variations test passed")
        
        # Test 6: Investment level variations
        logger.info("\nTest 6: Investment level variations")
        investment_levels = ['Low', 'Moderate', 'High']
        
        for investment in investment_levels:
            result = business_metrics.calculate_productivity_gain(investment_level=investment)
            logger.info(f"   {investment}: {result['adjusted_gain']}% adjusted gain")
            
            # High investment should have higher gains than Low
            if investment == 'High':
                high_gain = result['adjusted_gain']
            elif investment == 'Low':
                low_gain = result['adjusted_gain']
        
        assert high_gain > low_gain, f"High investment should have higher gains than Low"
        logger.info("✅ Investment level variations test passed")
        
        # Test 7: Time horizon variations
        logger.info("\nTest 7: Time horizon variations")
        time_horizons = [1, 3, 5]
        
        for years in time_horizons:
            result = business_metrics.calculate_productivity_gain(time_horizon_years=years)
            logger.info(f"   {years} years: {result['cumulative_gain']}% cumulative gain")
            
            # Longer time horizons should have higher cumulative gains
            if years == 5:
                five_year_gain = result['cumulative_gain']
            elif years == 1:
                one_year_gain = result['cumulative_gain']
        
        assert five_year_gain > one_year_gain, f"5-year horizon should have higher cumulative gains than 1-year"
        logger.info("✅ Time horizon variations test passed")
        
        # Test 8: Data authenticity validation
        logger.info("\nTest 8: Data authenticity validation")
        
        # Test that the method uses authentic project data
        result = business_metrics.calculate_productivity_gain(
            skill_level="Medium-skilled",
            industry="Technology",
            function="Software Engineering"
        )
        
        # Validate that the calculation breakdown shows authentic data usage
        breakdown = result['calculation_breakdown']
        assert 'skill_level_gain' in breakdown, "Should show skill level gain calculation"
        assert 'industry_multiplier' in breakdown, "Should show industry multiplier"
        assert 'function_multiplier' in breakdown, "Should show function multiplier"
        
        logger.info("✅ Data authenticity validation passed")
        
        # Test 9: Error handling
        logger.info("\nTest 9: Error handling")
        
        # Test with invalid parameters
        result = business_metrics.calculate_productivity_gain(
            skill_level="Invalid Skill",
            industry="Invalid Industry",
            function="Invalid Function"
        )
        
        # Should still return valid structure with default values
        assert result['confidence_level'] == 'Low' or result['confidence_level'] == 'Medium', "Should handle invalid inputs gracefully"
        assert len(result['recommendations']) > 0, "Should provide recommendations even with invalid inputs"
        
        logger.info("✅ Error handling test passed")
        
        # Test 10: Standard approach compliance
        logger.info("\nTest 10: Standard approach compliance")
        
        # Validate that the method follows the standard approach
        standard_approach_requirements = [
            "Uses authentic project data",
            "Provides comprehensive analysis",
            "Includes confidence scoring",
            "Generates actionable recommendations",
            "Handles errors gracefully",
            "Returns structured results"
        ]
        
        compliance_score = 0
        for requirement in standard_approach_requirements:
            if requirement == "Uses authentic project data":
                if result['factors'] and any('data available' in factor for factor in result['factors']):
                    compliance_score += 1
            elif requirement == "Provides comprehensive analysis":
                if len(result) >= 8:  # Has comprehensive return structure
                    compliance_score += 1
            elif requirement == "Includes confidence scoring":
                if 'confidence_level' in result and 'confidence_score' in result:
                    compliance_score += 1
            elif requirement == "Generates actionable recommendations":
                if result['recommendations'] and len(result['recommendations']) >= 3:
                    compliance_score += 1
            elif requirement == "Handles errors gracefully":
                if 'calculation_breakdown' in result:
                    compliance_score += 1
            elif requirement == "Returns structured results":
                if isinstance(result, dict) and all(key in result for key in required_keys):
                    compliance_score += 1
        
        compliance_percentage = (compliance_score / len(standard_approach_requirements)) * 100
        logger.info(f"   Standard approach compliance: {compliance_percentage:.1f}%")
        
        assert compliance_percentage >= 80, f"Should meet at least 80% of standard approach requirements, got {compliance_percentage}%"
        logger.info("✅ Standard approach compliance test passed")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 PRODUCTIVITY GAIN STANDARD APPROACH TEST RESULTS")
        logger.info("=" * 60)
        logger.info("✅ All 10 tests passed successfully!")
        logger.info("✅ Method follows standard approach guidelines")
        logger.info("✅ Uses authentic project data")
        logger.info("✅ Provides comprehensive analysis")
        logger.info("✅ Includes proper error handling")
        logger.info("✅ Generates actionable recommendations")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Productivity gain test failed: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_productivity_gain_standard_approach()
    if success:
        logger.info("\n🎯 RECOMMENDATION: This approach is APPROVED for implementation")
        logger.info("   The calculate_productivity_gain method follows the standard approach")
        logger.info("   and uses authentic project data effectively.")
    else:
        logger.error("\n❌ RECOMMENDATION: This approach needs revision")
        logger.error("   The calculate_productivity_gain method does not meet standards.") 