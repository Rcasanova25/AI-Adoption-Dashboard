"""Automated report generation for AI Adoption Dashboard.

This module provides functionality to generate comprehensive reports
combining multiple analyses into professional documents.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import json
from pathlib import Path

# Report generation dependencies
try:
    from jinja2 import Environment, FileSystemLoader, Template
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False

from utils.export_manager import export_manager
from business.financial_calculations_cached import (
    calculate_npv,
    calculate_irr,
    calculate_tco,
    calculate_payback_period
)
from business.roi_analysis import compute_comprehensive_roi
from business.scenario_engine_parallel import monte_carlo_simulation_parallel
from business.industry_models import (
    get_industry_benchmarks,
    select_optimal_ai_strategy
)

logger = logging.getLogger(__name__)


class ReportTemplate:
    """Base class for report templates."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.sections = []
        
    def add_section(self, section: Dict[str, Any]):
        """Add a section to the report."""
        self.sections.append(section)
        
    def render(self, data: Dict[str, Any]) -> str:
        """Render the report template with data."""
        raise NotImplementedError


class ExecutiveSummaryTemplate(ReportTemplate):
    """Template for executive summary reports."""
    
    def __init__(self):
        super().__init__(
            "Executive Summary",
            "High-level overview of AI investment analysis"
        )
        
    def render(self, data: Dict[str, Any]) -> str:
        """Render executive summary."""
        summary = []
        summary.append("# AI Investment Analysis - Executive Summary")
        summary.append(f"\n**Date:** {datetime.now().strftime('%B %d, %Y')}")
        summary.append(f"**Prepared for:** {data.get('company_name', 'Your Organization')}\n")
        
        # Investment Overview
        summary.append("## Investment Overview")
        if 'investment_amount' in data:
            summary.append(f"- **Total Investment:** ${data['investment_amount']:,.0f}")
        if 'analysis_period' in data:
            summary.append(f"- **Analysis Period:** {data['analysis_period']} years")
        if 'industry' in data:
            summary.append(f"- **Industry:** {data['industry']}")
        if 'company_size' in data:
            summary.append(f"- **Company Size:** {data['company_size']}")
        
        # Key Findings
        summary.append("\n## Key Findings")
        
        if 'financial_metrics' in data:
            metrics = data['financial_metrics']
            if 'npv' in metrics:
                summary.append(f"- **Net Present Value:** ${metrics['npv']:,.0f}")
            if 'irr' in metrics:
                summary.append(f"- **Internal Rate of Return:** {metrics['irr']*100:.1f}%")
            if 'payback_years' in metrics:
                summary.append(f"- **Payback Period:** {metrics['payback_years']:.1f} years")
        
        # Risk Assessment
        if 'risk_analysis' in data:
            summary.append("\n## Risk Assessment")
            risk = data['risk_analysis']
            summary.append(f"- **Risk Level:** {risk.get('risk_level', 'Medium')}")
            summary.append(f"- **Risk-Adjusted Return:** {risk.get('risk_adjusted_return', 0)*100:.1f}%")
            
        # Recommendation
        summary.append("\n## Recommendation")
        if 'recommendation' in data:
            if data['recommendation']:
                summary.append("### ✅ **PROCEED WITH INVESTMENT**")
                summary.append("\nThe analysis indicates positive returns with acceptable risk levels.")
            else:
                summary.append("### ❌ **RECONSIDER INVESTMENT**")
                summary.append("\nThe analysis suggests the investment may not meet return thresholds.")
        
        # Next Steps
        if 'next_steps' in data:
            summary.append("\n## Recommended Next Steps")
            for step in data['next_steps']:
                summary.append(f"1. {step}")
                
        return "\n".join(summary)


class DetailedAnalysisTemplate(ReportTemplate):
    """Template for detailed analysis reports."""
    
    def __init__(self):
        super().__init__(
            "Detailed Analysis",
            "Comprehensive AI investment analysis with full calculations"
        )
        
    def render(self, data: Dict[str, Any]) -> str:
        """Render detailed analysis."""
        report = []
        report.append("# AI Investment Analysis - Detailed Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Table of Contents
        report.append("\n## Table of Contents")
        report.append("1. Executive Summary")
        report.append("2. Financial Analysis")
        report.append("3. Risk Assessment")
        report.append("4. Scenario Analysis")
        report.append("5. Industry Benchmarks")
        report.append("6. Recommendations")
        report.append("7. Appendix")
        
        # Executive Summary (brief)
        report.append("\n## 1. Executive Summary")
        report.append(self._render_brief_summary(data))
        
        # Financial Analysis
        report.append("\n## 2. Financial Analysis")
        report.append(self._render_financial_analysis(data))
        
        # Risk Assessment
        report.append("\n## 3. Risk Assessment")
        report.append(self._render_risk_assessment(data))
        
        # Scenario Analysis
        report.append("\n## 4. Scenario Analysis")
        report.append(self._render_scenario_analysis(data))
        
        # Industry Benchmarks
        report.append("\n## 5. Industry Benchmarks")
        report.append(self._render_industry_benchmarks(data))
        
        # Recommendations
        report.append("\n## 6. Recommendations")
        report.append(self._render_recommendations(data))
        
        # Appendix
        report.append("\n## 7. Appendix")
        report.append(self._render_appendix(data))
        
        return "\n".join(report)
    
    def _render_brief_summary(self, data: Dict) -> str:
        """Render brief executive summary section."""
        summary = []
        
        if 'recommendation' in data:
            if data['recommendation']:
                summary.append("**Investment Recommendation:** PROCEED ✅")
            else:
                summary.append("**Investment Recommendation:** RECONSIDER ❌")
                
        if 'financial_metrics' in data:
            metrics = data['financial_metrics']
            summary.append(f"\n**Key Metrics:**")
            summary.append(f"- NPV: ${metrics.get('npv', 0):,.0f}")
            summary.append(f"- IRR: {metrics.get('irr', 0)*100:.1f}%")
            summary.append(f"- Payback: {metrics.get('payback_years', 0):.1f} years")
            
        return "\n".join(summary)
    
    def _render_financial_analysis(self, data: Dict) -> str:
        """Render financial analysis section."""
        analysis = []
        
        analysis.append("### 2.1 Investment Parameters")
        if 'investment_amount' in data:
            analysis.append(f"- Initial Investment: ${data['investment_amount']:,.0f}")
        if 'annual_benefits' in data:
            analysis.append(f"- Expected Annual Benefits: ${data['annual_benefits']:,.0f}")
        if 'annual_costs' in data:
            analysis.append(f"- Annual Operating Costs: ${data['annual_costs']:,.0f}")
            
        analysis.append("\n### 2.2 Financial Metrics")
        if 'financial_metrics' in data:
            metrics = data['financial_metrics']
            analysis.append(f"\n**Net Present Value (NPV)**")
            analysis.append(f"- Value: ${metrics.get('npv', 0):,.0f}")
            analysis.append(f"- Interpretation: {'Positive - Value creating' if metrics.get('npv', 0) > 0 else 'Negative - Value destroying'}")
            
            analysis.append(f"\n**Internal Rate of Return (IRR)**")
            if metrics.get('irr'):
                analysis.append(f"- Rate: {metrics.get('irr', 0)*100:.2f}%")
                analysis.append(f"- Benchmark: Exceeds 10% hurdle rate" if metrics.get('irr', 0) > 0.10 else "Below 10% hurdle rate")
            
        analysis.append("\n### 2.3 Total Cost of Ownership")
        if 'tco_analysis' in data:
            tco = data['tco_analysis']
            analysis.append(f"- Initial Cost: ${tco.get('initial_cost', 0):,.0f}")
            analysis.append(f"- Operating Costs (PV): ${tco.get('operating_costs', 0):,.0f}")
            analysis.append(f"- Maintenance Costs (PV): ${tco.get('maintenance_costs', 0):,.0f}")
            analysis.append(f"- **Total TCO: ${tco.get('total_tco', 0):,.0f}**")
            
        return "\n".join(analysis)
    
    def _render_risk_assessment(self, data: Dict) -> str:
        """Render risk assessment section."""
        risk_text = []
        
        if 'risk_analysis' in data:
            risk = data['risk_analysis']
            
            risk_text.append("### 3.1 Risk Metrics")
            risk_text.append(f"- Risk Level: {risk.get('risk_level', 'Medium')}")
            risk_text.append(f"- Expected Return: {risk.get('expected_return', 0)*100:.1f}%")
            risk_text.append(f"- Risk-Adjusted Return: {risk.get('risk_adjusted_return', 0)*100:.1f}%")
            risk_text.append(f"- Sharpe Ratio: {risk.get('sharpe_ratio', 0):.2f}")
            
        risk_text.append("\n### 3.2 Key Risk Factors")
        if 'risk_factors' in data:
            for factor in data['risk_factors']:
                risk_text.append(f"- {factor}")
        else:
            risk_text.append("- Technology implementation risk")
            risk_text.append("- Organizational change management")
            risk_text.append("- Market uncertainty")
            risk_text.append("- Regulatory compliance")
            
        risk_text.append("\n### 3.3 Mitigation Strategies")
        if 'mitigation_strategies' in data:
            for strategy in data['mitigation_strategies']:
                risk_text.append(f"- {strategy}")
        else:
            risk_text.append("- Phased implementation approach")
            risk_text.append("- Comprehensive training programs")
            risk_text.append("- Regular progress monitoring")
            risk_text.append("- Contingency planning")
            
        return "\n".join(risk_text)
    
    def _render_scenario_analysis(self, data: Dict) -> str:
        """Render scenario analysis section."""
        scenario_text = []
        
        if 'monte_carlo_results' in data:
            mc = data['monte_carlo_results']
            
            scenario_text.append("### 4.1 Monte Carlo Simulation")
            scenario_text.append(f"- Iterations: {mc.get('iterations', 10000):,}")
            scenario_text.append(f"- Mean Outcome: ${mc.get('mean', 0):,.0f}")
            scenario_text.append(f"- Standard Deviation: ${mc.get('std_dev', 0):,.0f}")
            
            scenario_text.append("\n### 4.2 Probability Distribution")
            percentiles = mc.get('percentiles', {})
            scenario_text.append(f"- 5th Percentile: ${percentiles.get('p5', 0):,.0f}")
            scenario_text.append(f"- 25th Percentile: ${percentiles.get('p25', 0):,.0f}")
            scenario_text.append(f"- Median: ${percentiles.get('p50', 0):,.0f}")
            scenario_text.append(f"- 75th Percentile: ${percentiles.get('p75', 0):,.0f}")
            scenario_text.append(f"- 95th Percentile: ${percentiles.get('p95', 0):,.0f}")
            
        scenario_text.append("\n### 4.3 Scenario Outcomes")
        scenario_text.append("- **Best Case (95th percentile):** Strong market adoption, minimal issues")
        scenario_text.append("- **Base Case (50th percentile):** Expected outcome with normal challenges")
        scenario_text.append("- **Worst Case (5th percentile):** Significant implementation challenges")
        
        return "\n".join(scenario_text)
    
    def _render_industry_benchmarks(self, data: Dict) -> str:
        """Render industry benchmarks section."""
        benchmark_text = []
        
        if 'industry_benchmarks' in data:
            benchmarks = data['industry_benchmarks']
            
            benchmark_text.append("### 5.1 Industry Comparison")
            benchmark_text.append(f"- Industry: {data.get('industry', 'General')}")
            benchmark_text.append(f"- Typical ROI Range: {benchmarks.get('typical_roi_range', (0, 0))[0]:.0f}% - {benchmarks.get('typical_roi_range', (0, 0))[1]:.0f}%")
            benchmark_text.append(f"- Success Rate: {benchmarks.get('success_probability', 0)*100:.0f}%")
            benchmark_text.append(f"- Implementation Timeline: {benchmarks.get('implementation_timeline_months', 12)} months")
            
        benchmark_text.append("\n### 5.2 Best Practices")
        if 'key_success_factors' in data.get('industry_benchmarks', {}):
            for factor in data['industry_benchmarks']['key_success_factors']:
                benchmark_text.append(f"- {factor}")
                
        return "\n".join(benchmark_text)
    
    def _render_recommendations(self, data: Dict) -> str:
        """Render recommendations section."""
        rec_text = []
        
        rec_text.append("### 6.1 Investment Decision")
        if data.get('recommendation', False):
            rec_text.append("**✅ RECOMMENDATION: PROCEED WITH INVESTMENT**")
            rec_text.append("\nThe financial analysis indicates positive returns that exceed hurdle rates.")
        else:
            rec_text.append("**❌ RECOMMENDATION: RECONSIDER OR MODIFY INVESTMENT**")
            rec_text.append("\nThe current analysis suggests returns may not justify the investment.")
            
        rec_text.append("\n### 6.2 Implementation Approach")
        if 'implementation_approach' in data:
            for approach in data['implementation_approach']:
                rec_text.append(f"- {approach}")
        else:
            rec_text.append("1. Start with pilot project to validate assumptions")
            rec_text.append("2. Build internal capabilities through training")
            rec_text.append("3. Scale gradually based on pilot results")
            rec_text.append("4. Monitor KPIs and adjust strategy as needed")
            
        rec_text.append("\n### 6.3 Success Criteria")
        rec_text.append("- Achieve positive cash flow within projected timeframe")
        rec_text.append("- Meet or exceed projected efficiency gains")
        rec_text.append("- Successful user adoption (>80% utilization)")
        rec_text.append("- Maintain project timeline and budget")
        
        return "\n".join(rec_text)
    
    def _render_appendix(self, data: Dict) -> str:
        """Render appendix section."""
        appendix = []
        
        appendix.append("### 7.1 Methodology")
        appendix.append("- Financial calculations based on industry-standard formulas")
        appendix.append("- Risk assessment using established frameworks")
        appendix.append("- Monte Carlo simulation with 10,000 iterations")
        appendix.append("- Industry benchmarks from authoritative sources")
        
        appendix.append("\n### 7.2 Assumptions")
        if 'assumptions' in data:
            for assumption in data['assumptions']:
                appendix.append(f"- {assumption}")
        else:
            appendix.append("- Discount rate: 10% (industry standard)")
            appendix.append("- Analysis period: 5 years")
            appendix.append("- Stable economic conditions")
            appendix.append("- No major regulatory changes")
            
        appendix.append("\n### 7.3 Data Sources")
        appendix.append("- Internal financial projections")
        appendix.append("- Industry research reports")
        appendix.append("- Academic studies on AI ROI")
        appendix.append("- Vendor estimates and benchmarks")
        
        return "\n".join(appendix)


class IndustryComparisonTemplate(ReportTemplate):
    """Template for industry comparison reports."""
    
    def __init__(self):
        super().__init__(
            "Industry Comparison",
            "Compare AI investment outcomes across different industries"
        )
        
    def render(self, data: Dict[str, Any]) -> str:
        """Render industry comparison report."""
        report = []
        report.append("# AI Investment Analysis - Industry Comparison")
        report.append(f"\n**Date:** {datetime.now().strftime('%B %d, %Y')}")
        
        # Overview
        report.append("\n## Overview")
        report.append("This report compares AI investment opportunities across multiple industries.")
        
        if 'industries' in data:
            report.append("\n## Industry Analysis")
            
            # Summary table
            report.append("\n### Summary Comparison")
            report.append("\n| Industry | NPV | IRR | Payback | Risk | Recommendation |")
            report.append("|----------|-----|-----|---------|------|----------------|")
            
            for industry in data['industries']:
                name = industry.get('name', 'Unknown')
                npv = industry.get('financial_metrics', {}).get('npv', 0)
                irr = industry.get('financial_metrics', {}).get('irr', 0)
                payback = industry.get('financial_metrics', {}).get('payback_years', 0)
                risk = industry.get('risk_level', 'Medium')
                rec = "✅" if industry.get('recommended', False) else "❌"
                
                report.append(f"| {name} | ${npv:,.0f} | {irr*100:.1f}% | {payback:.1f}y | {risk} | {rec} |")
                
            # Detailed analysis for each industry
            report.append("\n## Detailed Industry Analysis")
            
            for industry in data['industries']:
                report.append(f"\n### {industry.get('name', 'Unknown')}")
                
                # Key metrics
                metrics = industry.get('financial_metrics', {})
                report.append(f"- **NPV:** ${metrics.get('npv', 0):,.0f}")
                report.append(f"- **IRR:** {metrics.get('irr', 0)*100:.1f}%")
                report.append(f"- **Payback Period:** {metrics.get('payback_years', 0):.1f} years")
                
                # Industry-specific factors
                report.append("\n**Industry Characteristics:**")
                factors = industry.get('industry_factors', {})
                report.append(f"- Tech Maturity: {factors.get('tech_maturity', 0)*100:.0f}%")
                report.append(f"- Regulatory Burden: {factors.get('regulatory_burden', 0)*100:.0f}%")
                report.append(f"- Competitive Pressure: {factors.get('competitive_pressure', 0)*100:.0f}%")
                
                # Recommendations
                if 'recommendations' in industry:
                    report.append("\n**Key Insights:**")
                    for rec in industry['recommendations']:
                        report.append(f"- {rec}")
                        
        # Overall recommendations
        report.append("\n## Strategic Recommendations")
        
        if 'best_industry' in data:
            report.append(f"\n**Best Opportunity:** {data['best_industry']}")
            report.append("Based on risk-adjusted returns and implementation feasibility.")
            
        report.append("\n**Portfolio Approach:**")
        report.append("- Consider diversifying across 2-3 industries")
        report.append("- Start with highest ROI/lowest risk combination")
        report.append("- Learn from initial implementations before scaling")
        
        return "\n".join(report)


class ReportGenerator:
    """Main report generator class."""
    
    def __init__(self):
        """Initialize report generator."""
        self.templates = {
            'executive_summary': ExecutiveSummaryTemplate(),
            'detailed_analysis': DetailedAnalysisTemplate(),
            'industry_comparison': IndustryComparisonTemplate()
        }
        
    def generate_report(
        self,
        template_name: str,
        data: Dict[str, Any],
        format: str = 'markdown',
        filename: Optional[str] = None
    ) -> Union[str, bytes]:
        """Generate a report using specified template.
        
        Args:
            template_name: Name of the template to use
            data: Data for the report
            format: Output format (markdown, pdf, html)
            filename: Optional filename to save report
            
        Returns:
            Report content as string or bytes
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
            
        template = self.templates[template_name]
        
        # Render markdown content
        markdown_content = template.render(data)
        
        if format == 'markdown':
            if filename:
                with open(filename, 'w') as f:
                    f.write(markdown_content)
                return filename
            return markdown_content
            
        elif format == 'pdf':
            # Convert markdown to PDF using export manager
            temp_results = {
                'report_content': markdown_content,
                'metadata': data
            }
            return export_manager._export_financial_pdf(temp_results, filename)
            
        elif format == 'html':
            # Convert markdown to HTML
            html_content = self._markdown_to_html(markdown_content, template.name)
            if filename:
                with open(filename, 'w') as f:
                    f.write(html_content)
                return filename
            return html_content
            
        else:
            raise ValueError(f"Unsupported format: {format}")
            
    def _markdown_to_html(self, markdown_content: str, title: str) -> str:
        """Convert markdown to HTML with styling."""
        # Basic markdown to HTML conversion
        html_lines = []
        html_lines.append(f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ color: #1E88E5; }}
        h2 {{ color: #424242; margin-top: 30px; }}
        h3 {{ color: #616161; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #E3F2FD;
            font-weight: bold;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        strong {{ color: #1976D2; }}
        .success {{ color: #4CAF50; }}
        .error {{ color: #F44336; }}
    </style>
</head>
<body>
""")
        
        # Simple markdown parsing
        for line in markdown_content.split('\n'):
            if line.startswith('# '):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith('## '):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith('### '):
                html_lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith('- '):
                html_lines.append(f"<li>{line[2:]}</li>")
            elif line.strip() == '':
                html_lines.append("<br>")
            elif '|' in line and line.count('|') >= 3:
                # Simple table handling
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if all(set(cell) <= {'-', ' '} for cell in cells):
                    continue  # Skip separator lines
                row = "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"
                html_lines.append(row)
            else:
                # Handle inline formatting
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                line = line.replace('✅', '<span class="success">✅</span>')
                line = line.replace('❌', '<span class="error">❌</span>')
                html_lines.append(f"<p>{line}</p>")
                
        html_lines.append("</body></html>")
        
        return "\n".join(html_lines)
    
    def generate_comprehensive_report(
        self,
        investment_params: Dict[str, Any],
        include_sections: List[str] = None
    ) -> Dict[str, Any]:
        """Generate a comprehensive report with all analyses.
        
        Args:
            investment_params: Investment parameters
            include_sections: List of sections to include
            
        Returns:
            Complete report data
        """
        if include_sections is None:
            include_sections = ['financial', 'risk', 'scenario', 'industry', 'recommendation']
            
        report_data = {
            'company_name': investment_params.get('company_name', 'Your Organization'),
            'investment_amount': investment_params.get('initial_investment', 0),
            'analysis_period': investment_params.get('years', 5),
            'industry': investment_params.get('industry', 'General'),
            'company_size': investment_params.get('company_size', 'Medium')
        }
        
        # Financial analysis
        if 'financial' in include_sections:
            roi_results = compute_comprehensive_roi(
                initial_investment=investment_params.get('initial_investment', 1000000),
                annual_cash_flows=investment_params.get('annual_cash_flows', [300000] * 5),
                annual_operating_costs=investment_params.get('annual_operating_costs', [50000] * 5),
                risk_level=investment_params.get('risk_level', 'Medium'),
                discount_rate=investment_params.get('discount_rate', 0.10)
            )
            
            report_data['financial_metrics'] = roi_results.get('financial_metrics', {})
            report_data['tco_analysis'] = roi_results.get('tco_analysis', {})
            report_data['risk_analysis'] = roi_results.get('risk_analysis', {})
            report_data['recommendation'] = roi_results.get('investment_decision', {}).get('recommended', False)
            
        # Industry benchmarks
        if 'industry' in include_sections and 'industry' in investment_params:
            benchmarks = get_industry_benchmarks(investment_params['industry'])
            report_data['industry_benchmarks'] = benchmarks
            
        # Implementation strategy
        if 'recommendation' in include_sections:
            strategy = select_optimal_ai_strategy(
                industry=investment_params.get('industry', 'General'),
                company_size=investment_params.get('company_size', 'Medium'),
                budget=investment_params.get('initial_investment', 1000000),
                timeline_months=investment_params.get('timeline_months', 12),
                strategic_goals=investment_params.get('strategic_goals', ['cost_reduction', 'efficiency'])
            )
            
            report_data['implementation_approach'] = strategy.get('implementation_phases', [])
            report_data['risk_factors'] = strategy.get('risk_mitigation', [])
            
        # Next steps
        report_data['next_steps'] = self._generate_next_steps(report_data)
        
        return report_data
    
    def _generate_next_steps(self, report_data: Dict) -> List[str]:
        """Generate recommended next steps based on analysis."""
        next_steps = []
        
        if report_data.get('recommendation', False):
            next_steps.append("Secure executive approval for AI investment")
            next_steps.append("Establish project governance structure")
            next_steps.append("Identify and engage key stakeholders")
            next_steps.append("Develop detailed implementation roadmap")
            next_steps.append("Begin vendor selection process")
        else:
            next_steps.append("Review and refine investment assumptions")
            next_steps.append("Explore alternative AI solutions with lower costs")
            next_steps.append("Consider phased approach to reduce initial investment")
            next_steps.append("Benchmark against successful implementations")
            next_steps.append("Re-evaluate in 6-12 months as technology matures")
            
        return next_steps


# Global report generator instance
report_generator = ReportGenerator()