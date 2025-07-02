#!/usr/bin/env python3
"""
Test script for OECD integration in causal analysis
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mock_data():
    """Create mock AI adoption and productivity data for testing"""
    
    # Create mock AI adoption data
    years = list(range(2020, 2025))
    sectors = ['technology', 'finance', 'healthcare']
    
    adoption_data = []
    for year in years:
        for sector in sectors:
            adoption_data.append({
                'year': year,
                'sector': sector,
                'adoption_rate': np.random.uniform(20, 80),
                'investment_amount': np.random.uniform(50000, 500000),
                'implementation_timeline': np.random.uniform(6, 18)
            })
    
    adoption_df = pd.DataFrame(adoption_data)
    
    # Create mock productivity data
    productivity_data = []
    for year in years:
        for sector in sectors:
            productivity_data.append({
                'year': year,
                'sector': sector,
                'revenue_per_employee': np.random.uniform(80000, 150000),
                'operational_efficiency': np.random.uniform(70, 95),
                'cost_reduction_percentage': np.random.uniform(5, 25)
            })
    
    productivity_df = pd.DataFrame(productivity_data)
    
    return adoption_df, productivity_df

def test_oecd_integration():
    """Test the OECD integration functionality"""
    
    try:
        # Import causal analysis engine
        from business.causal_analysis import CausalAnalysisEngine
        
        logger.info("Starting OECD integration test...")
        
        # Create mock data
        adoption_data, productivity_data = create_mock_data()
        logger.info(f"Created mock data: {len(adoption_data)} adoption records, {len(productivity_data)} productivity records")
        
        # Initialize causal analysis engine
        engine = CausalAnalysisEngine()
        
        # Test with OECD enhancement enabled
        logger.info("Testing causal analysis with OECD enhancement...")
        result_with_oecd = engine.establish_ai_productivity_causality(
            adoption_data=adoption_data,
            productivity_data=productivity_data,
            sector="technology",
            use_oecd_enhancement=True
        )
        
        # Test without OECD enhancement for comparison
        logger.info("Testing causal analysis without OECD enhancement...")
        result_without_oecd = engine.establish_ai_productivity_causality(
            adoption_data=adoption_data,
            productivity_data=productivity_data,
            sector="technology",
            use_oecd_enhancement=False
        )
        
        # Compare results
        logger.info("=== RESULTS COMPARISON ===")
        logger.info(f"Without OECD: Confidence = {result_without_oecd.confidence_score:.3f}, Relationships = {len(result_without_oecd.causal_relationships)}")
        logger.info(f"With OECD:    Confidence = {result_with_oecd.confidence_score:.3f}, Relationships = {len(result_with_oecd.causal_relationships)}")
        
        confidence_improvement = result_with_oecd.confidence_score - result_without_oecd.confidence_score
        logger.info(f"Confidence improvement: {confidence_improvement:.3f} ({confidence_improvement/result_without_oecd.confidence_score*100:.1f}%)")
        
        # Display data sources
        logger.info(f"Data sources without OECD: {result_without_oecd.data_sources}")
        logger.info(f"Data sources with OECD: {result_with_oecd.data_sources}")
        
        # Show enhanced relationships with OECD context
        oecd_enhanced_relationships = [
            rel for rel in result_with_oecd.causal_relationships 
            if "OECD" in str(rel.evidence_sources) or "oecd_" in rel.cause.lower()
        ]
        
        if oecd_enhanced_relationships:
            logger.info(f"Found {len(oecd_enhanced_relationships)} relationships enhanced with OECD context:")
            for rel in oecd_enhanced_relationships[:3]:  # Show top 3
                logger.info(f"  {rel.cause} → {rel.effect} (strength: {rel.strength:.3f}, confidence: {rel.confidence:.3f})")
        
        return True
        
    except Exception as e:
        logger.error(f"OECD integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_oecd_data_fetching():
    """Test OECD data fetching functionality"""
    
    try:
        from data.oecd_realtime import OECDIntegration
        
        logger.info("Testing OECD data fetching...")
        
        # Initialize OECD integration
        oecd = OECDIntegration()
        
        # Test fetching indicator summary
        summary = oecd.client.get_indicator_summary()
        logger.info(f"Available OECD indicators: {len(summary)}")
        
        # Test fetching aligned dataset
        aligned_data = oecd.get_aligned_dataset(
            countries=['USA', 'GBR'], 
            months_back=12
        )
        
        if not aligned_data.empty:
            logger.info(f"Successfully fetched OECD data: {aligned_data.shape}")
            logger.info(f"Indicators: {list(aligned_data.columns)}")
            logger.info(f"Date range: {aligned_data.index.min()} to {aligned_data.index.max()}")
        else:
            logger.warning("No OECD data retrieved")
        
        return True
        
    except Exception as e:
        logger.error(f"OECD data fetching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("Testing OECD Integration for AI Adoption Dashboard")
    
    # Test OECD data fetching
    oecd_fetch_success = test_oecd_data_fetching()
    
    # Test causal analysis integration
    integration_success = test_oecd_integration()
    
    if oecd_fetch_success and integration_success:
        logger.info("✅ All OECD integration tests passed!")
    else:
        logger.error("❌ Some tests failed. Check logs for details.")