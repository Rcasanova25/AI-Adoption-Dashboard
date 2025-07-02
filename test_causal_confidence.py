#!/usr/bin/env python3
"""
Test script to run causal analysis and check confidence scores
This script will work even without streamlit dependencies
"""

import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    import pandas as pd
    import numpy as np
    from datetime import datetime
    
    print("Basic dependencies available")
    
    # Try to import causal analysis
    try:
        from business.causal_analysis import CausalAnalysisEngine
        print("✅ CausalAnalysisEngine imported successfully")
        
        # Create enhanced sample data for better causal discovery
        print("\nCreating enhanced sample dataset...")
        
        # More comprehensive AI adoption data
        adoption_data = pd.DataFrame({
            'year': list(range(2018, 2025)) * 6,  # More time points
            'sector': ['Technology'] * 7 + ['Finance'] * 7 + ['Healthcare'] * 7 + 
                     ['Manufacturing'] * 7 + ['Retail'] * 7 + ['Education'] * 7,
            'adoption_rate': [
                # Technology sector - high adoption with clear growth
                25, 35, 45, 55, 65, 75, 85,
                # Finance - steady growth  
                15, 25, 35, 45, 55, 65, 75,
                # Healthcare - slower but consistent
                10, 15, 25, 35, 45, 55, 65,
                # Manufacturing - recent acceleration
                8, 12, 18, 25, 40, 55, 70,
                # Retail - volatile but growing
                12, 18, 22, 35, 50, 60, 68,
                # Education - late adopter
                5, 8, 12, 20, 30, 45, 60
            ],
            'investment_amount': [
                # Technology sector
                100, 150, 220, 300, 420, 580, 800,
                # Finance
                80, 120, 180, 250, 350, 480, 650,
                # Healthcare
                60, 90, 140, 200, 280, 380, 500,
                # Manufacturing
                40, 60, 95, 140, 220, 320, 450,
                # Retail
                50, 75, 110, 170, 250, 340, 440,
                # Education
                30, 45, 70, 110, 170, 250, 350
            ]
        })
        
        # More comprehensive productivity data with clear causal relationships
        productivity_data = pd.DataFrame({
            'year': list(range(2018, 2025)) * 6,
            'sector': ['Technology'] * 7 + ['Finance'] * 7 + ['Healthcare'] * 7 + 
                     ['Manufacturing'] * 7 + ['Retail'] * 7 + ['Education'] * 7,
            'revenue_per_employee': [
                # Technology - strong productivity gains following AI adoption
                180000, 185000, 195000, 210000, 230000, 255000, 285000,
                # Finance
                120000, 125000, 135000, 150000, 168000, 185000, 205000,
                # Healthcare
                95000, 98000, 105000, 115000, 128000, 142000, 158000,
                # Manufacturing
                75000, 77000, 82000, 90000, 102000, 118000, 135000,
                # Retail
                65000, 67000, 72000, 80000, 92000, 105000, 118000,
                # Education
                55000, 56000, 59000, 64000, 72000, 82000, 95000
            ],
            'operational_efficiency': [
                # Technology - efficiency follows adoption
                85, 87, 90, 93, 96, 98, 99,
                # Finance
                78, 80, 83, 87, 91, 94, 96,
                # Healthcare
                72, 74, 77, 81, 85, 89, 92,
                # Manufacturing
                68, 70, 73, 78, 84, 89, 93,
                # Retail
                70, 72, 75, 80, 86, 90, 93,
                # Education
                65, 66, 69, 74, 80, 86, 90
            ],
            'innovation_index': [
                # Clear innovation benefits from AI
                90, 92, 95, 97, 98, 99, 100,
                82, 84, 87, 90, 93, 95, 97,
                75, 77, 80, 84, 88, 91, 94,
                68, 70, 74, 79, 85, 90, 94,
                72, 74, 78, 83, 88, 92, 95,
                60, 62, 66, 72, 79, 86, 92
            ]
        })
        
        print(f"Created adoption data: {len(adoption_data)} rows, {len(adoption_data.columns)} columns")
        print(f"Created productivity data: {len(productivity_data)} rows, {len(productivity_data.columns)} columns")
        
        # Initialize causal analysis engine
        engine = CausalAnalysisEngine()
        print("✅ CausalAnalysisEngine initialized")
        
        # Run causal analysis
        print("\nRunning causal analysis...")
        result = engine.establish_ai_productivity_causality(
            adoption_data=adoption_data,
            productivity_data=productivity_data,
            sector="all_sectors",
            use_oecd_enhancement=False  # Test baseline first
        )
        
        print("\n" + "="*50)
        print("CAUSAL ANALYSIS RESULTS")
        print("="*50)
        print(f"Analysis ID: {result.analysis_id}")
        print(f"Confidence Score: {result.confidence_score:.3f} ({result.confidence_score*100:.1f}%)")
        print(f"Relationships Found: {len(result.causal_relationships)}")
        print(f"Productivity Impacts: {len(result.productivity_impacts)}")
        print(f"Data Sources: {result.data_sources}")
        
        if result.causal_relationships:
            print("\nTop Causal Relationships:")
            for i, rel in enumerate(result.causal_relationships[:5], 1):
                print(f"{i}. {rel.cause} → {rel.effect}")
                print(f"   Strength: {rel.strength:.3f}, Confidence: {rel.confidence:.3f}")
                print(f"   Type: {rel.relationship_type.value}, Direction: {rel.impact_direction}")
        
        if result.productivity_impacts:
            print("\nProductivity Impacts:")
            for impact in result.productivity_impacts[:3]:
                print(f"- {impact.metric.value}: {impact.improvement_percentage:.1f}% improvement")
                print(f"  Confidence: {impact.causal_confidence:.3f}")
        
        # Test with OECD enhancement if available
        print("\n" + "-"*50)
        print("Testing OECD Enhancement...")
        
        try:
            result_enhanced = engine.establish_ai_productivity_causality(
                adoption_data=adoption_data,
                productivity_data=productivity_data,
                sector="all_sectors", 
                use_oecd_enhancement=True
            )
            
            print(f"Enhanced Confidence Score: {result_enhanced.confidence_score:.3f} ({result_enhanced.confidence_score*100:.1f}%)")
            print(f"Improvement: {((result_enhanced.confidence_score - result.confidence_score)*100):.1f} percentage points")
            
        except Exception as e:
            print(f"OECD enhancement test failed: {e}")
        
    except ImportError as e:
        print(f"❌ Could not import causal analysis: {e}")
    except Exception as e:
        print(f"❌ Error in causal analysis test: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"❌ Missing basic dependencies: {e}")
    print("Please install: pip install pandas numpy")

print("\nTest complete.")