"""Report generation API endpoints for AI Adoption Dashboard.

This module provides API endpoints for generating automated reports.
"""

import io
import base64
from typing import Dict, List, Optional
from datetime import datetime

from reports.report_generator import report_generator
from .endpoints import APIResponse, log_api_call, validate_request


class ReportAPI:
    """API endpoints for report generation."""
    
    @staticmethod
    @log_api_call("report/generate")
    @validate_request(["template", "data"])
    def generate_report(request_data: Dict) -> Dict:
        """Generate a report using specified template.
        
        Request:
            {
                "template": "executive_summary",  # or "detailed_analysis", "industry_comparison"
                "data": {
                    "company_name": "Acme Corp",
                    "investment_amount": 1000000,
                    "financial_metrics": {...}
                },
                "format": "pdf",  # or "markdown", "html"
                "filename": "ai_investment_report"
            }
        """
        try:
            template = request_data["template"]
            data = request_data["data"]
            format = request_data.get("format", "markdown")
            filename = request_data.get("filename")
            
            # Add extension if filename provided
            if filename:
                ext_map = {'markdown': 'md', 'pdf': 'pdf', 'html': 'html'}
                ext = ext_map.get(format, 'txt')
                if not filename.endswith(f".{ext}"):
                    filename = f"{filename}.{ext}"
            
            # Generate report
            output = report_generator.generate_report(
                template_name=template,
                data=data,
                format=format,
                filename=filename
            )
            
            if filename and isinstance(output, str):
                # File was saved
                return APIResponse.success({
                    "filename": filename,
                    "format": format,
                    "template": template,
                    "message": f"Report generated: {filename}"
                })
            else:
                # Return content
                if isinstance(output, io.BytesIO):
                    content = base64.b64encode(output.getvalue()).decode('utf-8')
                elif isinstance(output, bytes):
                    content = base64.b64encode(output).decode('utf-8')
                else:
                    content = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                    
                return APIResponse.success({
                    "content": content,
                    "format": format,
                    "template": template,
                    "encoding": "base64"
                })
                
        except ValueError as e:
            return APIResponse.error(str(e), 400)
        except Exception as e:
            return APIResponse.error(f"Report generation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("report/comprehensive")
    @validate_request(["investment_params"])
    def generate_comprehensive_report(request_data: Dict) -> Dict:
        """Generate a comprehensive report with all analyses.
        
        Request:
            {
                "investment_params": {
                    "company_name": "Acme Corp",
                    "initial_investment": 1000000,
                    "annual_cash_flows": [300000, 350000, 400000, 450000, 500000],
                    "annual_operating_costs": [50000, 55000, 60000, 65000, 70000],
                    "industry": "manufacturing",
                    "company_size": "Medium",
                    "risk_level": "Medium"
                },
                "include_sections": ["financial", "risk", "scenario", "industry"],
                "output_format": "pdf"
            }
        """
        try:
            investment_params = request_data["investment_params"]
            include_sections = request_data.get("include_sections")
            output_format = request_data.get("output_format", "markdown")
            
            # Generate comprehensive report data
            report_data = report_generator.generate_comprehensive_report(
                investment_params=investment_params,
                include_sections=include_sections
            )
            
            # Add timestamp
            report_data['generated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate report using detailed template
            output = report_generator.generate_report(
                template_name='detailed_analysis',
                data=report_data,
                format=output_format
            )
            
            if isinstance(output, io.BytesIO):
                content = base64.b64encode(output.getvalue()).decode('utf-8')
            elif isinstance(output, bytes):
                content = base64.b64encode(output).decode('utf-8')
            else:
                content = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                
            return APIResponse.success({
                "content": content,
                "format": output_format,
                "encoding": "base64",
                "report_data": report_data
            })
            
        except Exception as e:
            return APIResponse.error(f"Comprehensive report generation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("report/industry_comparison")
    @validate_request(["industries", "investment_amount"])
    def generate_industry_comparison(request_data: Dict) -> Dict:
        """Generate industry comparison report.
        
        Request:
            {
                "industries": ["manufacturing", "healthcare", "retail", "financial_services"],
                "investment_amount": 1000000,
                "company_size": "Medium",
                "analysis_years": 5,
                "output_format": "pdf"
            }
        """
        try:
            from business.industry_models import (
                calculate_manufacturing_roi,
                calculate_healthcare_roi,
                calculate_financial_services_roi,
                calculate_retail_roi
            )
            
            industries = request_data["industries"]
            investment = request_data["investment_amount"]
            company_size = request_data.get("company_size", "Medium")
            years = request_data.get("analysis_years", 5)
            output_format = request_data.get("output_format", "markdown")
            
            # Calculate ROI for each industry
            industry_results = []
            
            industry_calculators = {
                'manufacturing': lambda: calculate_manufacturing_roi(
                    investment=investment,
                    production_volume=100000,
                    years=years
                ),
                'healthcare': lambda: calculate_healthcare_roi(
                    investment=investment,
                    patient_volume=20000,
                    years=years
                ),
                'financial_services': lambda: calculate_financial_services_roi(
                    investment=investment,
                    transaction_volume=1000000,
                    years=years
                ),
                'retail': lambda: calculate_retail_roi(
                    investment=investment,
                    annual_revenue=10000000,
                    years=years
                )
            }
            
            for industry in industries:
                if industry in industry_calculators:
                    result = industry_calculators[industry]()
                    result['name'] = industry.replace('_', ' ').title()
                    result['recommended'] = result.get('financial_metrics', {}).get('npv', 0) > 0
                    industry_results.append(result)
            
            # Find best industry
            best_industry = None
            best_npv = float('-inf')
            for result in industry_results:
                npv = result.get('financial_metrics', {}).get('npv', 0)
                if npv > best_npv:
                    best_npv = npv
                    best_industry = result['name']
            
            # Prepare report data
            report_data = {
                'industries': industry_results,
                'best_industry': best_industry,
                'investment_amount': investment,
                'company_size': company_size,
                'analysis_years': years
            }
            
            # Generate report
            output = report_generator.generate_report(
                template_name='industry_comparison',
                data=report_data,
                format=output_format
            )
            
            if isinstance(output, io.BytesIO):
                content = base64.b64encode(output.getvalue()).decode('utf-8')
            elif isinstance(output, bytes):
                content = base64.b64encode(output).decode('utf-8')
            else:
                content = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                
            return APIResponse.success({
                "content": content,
                "format": output_format,
                "encoding": "base64",
                "best_industry": best_industry,
                "industry_count": len(industry_results)
            })
            
        except Exception as e:
            return APIResponse.error(f"Industry comparison report failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("report/templates")
    def get_available_templates(request_data: Dict = None) -> Dict:
        """Get list of available report templates."""
        try:
            templates = {
                "executive_summary": {
                    "name": "Executive Summary",
                    "description": "High-level overview for executives and decision makers",
                    "sections": [
                        "Investment Overview",
                        "Key Findings",
                        "Risk Assessment",
                        "Recommendation",
                        "Next Steps"
                    ],
                    "typical_length": "2-3 pages"
                },
                "detailed_analysis": {
                    "name": "Detailed Analysis",
                    "description": "Comprehensive report with full financial analysis",
                    "sections": [
                        "Executive Summary",
                        "Financial Analysis",
                        "Risk Assessment",
                        "Scenario Analysis",
                        "Industry Benchmarks",
                        "Recommendations",
                        "Appendix"
                    ],
                    "typical_length": "10-15 pages"
                },
                "industry_comparison": {
                    "name": "Industry Comparison",
                    "description": "Compare AI investments across multiple industries",
                    "sections": [
                        "Overview",
                        "Summary Comparison Table",
                        "Detailed Industry Analysis",
                        "Strategic Recommendations"
                    ],
                    "typical_length": "8-12 pages"
                }
            }
            
            formats = {
                "markdown": {
                    "extension": ".md",
                    "description": "Markdown format for easy editing"
                },
                "pdf": {
                    "extension": ".pdf",
                    "description": "Professional PDF report",
                    "requires": "reportlab"
                },
                "html": {
                    "extension": ".html",
                    "description": "Web-viewable HTML format"
                }
            }
            
            return APIResponse.success({
                "templates": templates,
                "formats": formats
            })
            
        except Exception as e:
            return APIResponse.error(f"Failed to get templates: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("report/schedule")
    @validate_request(["report_config", "schedule"])
    def schedule_report(request_data: Dict) -> Dict:
        """Schedule automated report generation.
        
        Request:
            {
                "report_config": {
                    "template": "executive_summary",
                    "investment_params": {...},
                    "format": "pdf"
                },
                "schedule": {
                    "frequency": "weekly",  # or "daily", "monthly"
                    "day_of_week": "monday",  # for weekly
                    "time": "09:00",
                    "email_to": ["executive@company.com"]
                }
            }
        """
        # This is a placeholder for scheduled report functionality
        # In production, this would integrate with a task scheduler
        
        return APIResponse.success({
            "message": "Report scheduling is not yet implemented",
            "status": "pending_implementation"
        })


# Initialize report API instance
report_api = ReportAPI()