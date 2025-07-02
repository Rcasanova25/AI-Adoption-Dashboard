#!/usr/bin/env python3
"""
Accessibility Audit Runner for AI Adoption Dashboard
Run comprehensive accessibility audit and generate report
"""

import sys
import logging
from pathlib import Path
import argparse
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def run_accessibility_audit(save_report: bool = True, show_details: bool = True):
    """Run comprehensive accessibility audit"""
    try:
        from accessibility.accessibility_audit import accessibility_auditor
        
        logger.info("🔍 Starting accessibility audit...")
        
        # Run full audit
        results = accessibility_auditor.run_full_audit()
        
        # Display results
        print("=" * 80)
        print("🛡️  ACCESSIBILITY AUDIT RESULTS")
        print("=" * 80)
        print(f"Overall Score: {results['overall_score']}/100")
        print(f"Accessibility Level: {results['accessibility_level']}")
        print(f"Total Issues: {results['total_issues']}")
        print()
        
        # Show severity breakdown
        print("📊 Issue Breakdown by Severity:")
        for severity, count in results['severity_breakdown'].items():
            if count > 0:
                emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "info": "🔵"}.get(severity, "⚪")
                print(f"  {emoji} {severity.title()}: {count}")
        print()
        
        # Show priority recommendations
        if results['recommendations']:
            print("🎯 Priority Recommendations:")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"{i}. {rec['action']}")
                print(f"   Impact: {rec['impact']}")
                print(f"   Effort: {rec['effort']}")
                print()
        
        # Show detailed issues if requested
        if show_details and results['issues']:
            print("📋 Detailed Issues:")
            print("-" * 40)
            
            for issue in results['issues']:
                severity_emoji = {
                    "critical": "🔴", "high": "🟠", "medium": "🟡", 
                    "low": "🟢", "info": "🔵"
                }.get(issue['severity'], "⚪")
                
                print(f"{severity_emoji} {issue['severity'].upper()}: {issue['description']}")
                print(f"   Location: {issue['location']}")
                print(f"   WCAG: {issue['wcag_criterion']}")
                print(f"   Fix: {issue['recommendation']}")
                
                if issue.get('current_value') and issue.get('required_value'):
                    print(f"   Current: {issue['current_value']} | Required: {issue['required_value']}")
                print()
        
        # Save report if requested
        if save_report:
            report_path = accessibility_auditor.save_audit_report(results)
            print(f"📄 Full report saved to: {report_path}")
        
        return results
        
    except ImportError as e:
        logger.error(f"Failed to import accessibility auditor: {e}")
        return None
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        return None


def generate_accessibility_badge(score: int) -> str:
    """Generate accessibility compliance badge"""
    if score >= 90:
        return "🟢 Excellent (90+)"
    elif score >= 80:
        return "🟡 Good (80-89)"
    elif score >= 70:
        return "🟠 Fair (70-79)"
    else:
        return "🔴 Needs Improvement (<70)"


def run_color_contrast_test():
    """Run specific color contrast tests"""
    try:
        from accessibility.accessibility_audit import ColorContrastAnalyzer
        
        logger.info("🎨 Running color contrast analysis...")
        
        # Test current theme colors
        analyzer = ColorContrastAnalyzer()
        
        # Common color combinations to test
        color_tests = [
            ("#2C3E50", "#FFFFFF", "Primary text on white background"),
            ("#6C757D", "#FFFFFF", "Secondary text on white background"),
            ("#2E86AB", "#FFFFFF", "Primary blue on white background"),
            ("#A23B72", "#FFFFFF", "Secondary purple on white background"),
            ("#F18F01", "#FFFFFF", "Warning orange on white background"),
            ("#C73E1D", "#FFFFFF", "Error red on white background"),
            ("#FFFFFF", "#2C3E50", "White text on dark background"),
        ]
        
        print("🎨 Color Contrast Analysis:")
        print("-" * 50)
        
        for fg, bg, description in color_tests:
            result = analyzer.analyze_contrast(fg, bg)
            
            # Status indicators
            aa_status = "✅" if result.aa_compliant else "❌"
            aaa_status = "✅" if result.aaa_compliant else "❌"
            
            print(f"{description}")
            print(f"  Contrast Ratio: {result.contrast_ratio:.2f}:1")
            print(f"  WCAG AA: {aa_status} | WCAG AAA: {aaa_status}")
            
            if not result.aa_compliant and result.recommended_foreground:
                print(f"  💡 Recommended: {result.recommended_foreground}")
            print()
        
    except ImportError as e:
        logger.error(f"Failed to import color contrast analyzer: {e}")
    except Exception as e:
        logger.error(f"Color contrast test failed: {e}")


def run_colorblind_test():
    """Run colorblind accessibility test"""
    try:
        from accessibility.accessibility_audit import ColorBlindnessAnalyzer
        
        logger.info("👁️ Running colorblind accessibility analysis...")
        
        # Test current chart colors
        analyzer = ColorBlindnessAnalyzer()
        chart_colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        
        results = analyzer.analyze_color_palette(chart_colors)
        
        print("👁️ Colorblind Accessibility Analysis:")
        print("-" * 50)
        
        for blindness_type, result in results.items():
            score = result['accessibility_score']
            status = "✅" if score >= 0.8 else "⚠️" if score >= 0.6 else "❌"
            
            print(f"{blindness_type.title()}: {status} {score:.1%} distinguishable")
            
            if score < 0.8:
                print(f"  Original colors: {len(set(result['original_colors']))} unique")
                print(f"  Simulated colors: {len(set(result['simulated_colors']))} unique")
                print("  💡 Recommendation: Add patterns or textures to charts")
            print()
            
    except ImportError as e:
        logger.error(f"Failed to import colorblind analyzer: {e}")
    except Exception as e:
        logger.error(f"Colorblind test failed: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run accessibility audit for AI Adoption Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_accessibility_audit.py                    # Full audit
  python run_accessibility_audit.py --quick            # Summary only
  python run_accessibility_audit.py --contrast         # Color contrast test
  python run_accessibility_audit.py --colorblind       # Colorblind test
  python run_accessibility_audit.py --no-save          # Don't save report
        """
    )
    
    parser.add_argument('--quick', action='store_true',
                       help='Run quick audit without detailed issue breakdown')
    parser.add_argument('--contrast', action='store_true',
                       help='Run color contrast analysis only')
    parser.add_argument('--colorblind', action='store_true',
                       help='Run colorblind accessibility test only')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save audit report to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.contrast:
            run_color_contrast_test()
            return 0
        
        if args.colorblind:
            run_colorblind_test()
            return 0
        
        # Run full audit
        results = run_accessibility_audit(
            save_report=not args.no_save,
            show_details=not args.quick
        )
        
        if results:
            score = results['overall_score']
            badge = generate_accessibility_badge(score)
            
            print("=" * 80)
            print(f"🏆 Final Score: {badge}")
            
            if score < 80:
                print("\n🚨 Action Required:")
                print("The dashboard needs accessibility improvements to meet standards.")
                print("Focus on high-priority issues first for maximum impact.")
                return 1
            else:
                print("\n🎉 Good Job!")
                print("The dashboard meets basic accessibility standards.")
                return 0
        else:
            logger.error("Audit failed to complete")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\n⚠️ Audit interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)