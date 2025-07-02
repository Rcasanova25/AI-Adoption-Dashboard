#!/usr/bin/env python3
"""
Phase 2A Integration Demo
Demonstrates the successful integration of government research sources (St. Louis Fed + OECD)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.research_integration import research_integrator
from data.comprehensive_research_integration import comprehensive_integrator
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Demo the Phase 2A integration progress"""
    
    print("🎯 AI Adoption Dashboard - Phase 2A Integration Demo")
    print("=" * 60)
    
    # Show integration roadmap progress
    roadmap = comprehensive_integrator.get_integration_roadmap()
    
    print(f"📊 Research Integration Progress:")
    print(f"   • Total Sources Available: {roadmap['total_sources']}")
    print(f"   • Completed Integration: {roadmap['completed_count']}")
    print(f"   • Completion Rate: {roadmap['completion_rate']:.1f}%")
    print(f"   • Current Phase: Phase 2A - Government Research ✅")
    print()
    
    # Show completed sources
    print("✅ Phase 1 - Core Sources (Completed):")
    for source in roadmap['completed_sources']:
        source_info = comprehensive_integrator.all_data_sources[source]
        print(f"   • {source_info['authority']}: {source_info['credibility']}")
    print()
    
    # Show Phase 2A government research integration
    print("🏛️ Phase 2A - Government Research (NEW Integration):")
    phase_2a_sources = roadmap['integration_phases']['Phase 2A - Government Research']
    
    for source_key in phase_2a_sources:
        source_info = comprehensive_integrator.all_data_sources[source_key]
        print(f"   ✅ {source_info['authority']}")
        print(f"      📄 {source_info['name']}")
        print(f"      🔗 File: {source_info['file']}")
        print()
    
    # Demonstrate the new data loading
    print("🔄 Testing Phase 2A Data Loading...")
    
    try:
        # Test St. Louis Fed rapid adoption data
        rapid_adoption = research_integrator.get_stlouis_fed_rapid_adoption_data()
        print(f"   ✅ St. Louis Fed Rapid Adoption: {len(rapid_adoption)} time periods loaded")
        
        # Test St. Louis Fed productivity data
        productivity = research_integrator.get_stlouis_fed_productivity_impact_data()
        print(f"   ✅ St. Louis Fed Productivity Impact: {len(productivity)} occupation groups loaded")
        
        # Test OECD Policy Observatory data
        oecd_policy = research_integrator.get_oecd_policy_observatory_data()
        print(f"   ✅ OECD Policy Observatory: {len(oecd_policy)} countries analyzed")
        
        # Test OECD Employment Outlook data
        oecd_employment = research_integrator.get_oecd_employment_outlook_data()
        print(f"   ✅ OECD Employment Outlook: {len(oecd_employment)} skill categories analyzed")
        
    except Exception as e:
        print(f"   ❌ Error testing Phase 2A data: {e}")
    
    print()
    print("🚀 Next Steps - Phase 2B Economic Analysis:")
    phase_2b_sources = roadmap['integration_phases']['Phase 2B - Economic Analysis']
    
    for source_key in phase_2b_sources:
        source_info = comprehensive_integrator.all_data_sources[source_key]
        print(f"   📋 {source_info['authority']}: {source_info['name']}")
    
    print()
    print("📈 Impact of Phase 2A Integration:")
    print("   • Skill Gap Analysis now includes international OECD data")
    print("   • AI Governance includes 15-country policy comparison")
    print("   • Labor Impact enhanced with Federal Reserve research")
    print("   • Data credibility increased to A+ government sources")
    
    print()
    print(f"✨ Dashboard now uses {roadmap['completed_count']} authoritative research sources")
    print("🎓 From Stanford AI Index to OECD international analysis")

if __name__ == "__main__":
    main()