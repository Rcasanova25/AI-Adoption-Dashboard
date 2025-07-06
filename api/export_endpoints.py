"""Export API endpoints for AI Adoption Dashboard.

This module provides API endpoints for exporting calculation results
in various formats (Excel, CSV, PDF, JSON).
"""

import io
import base64
from typing import Dict, Optional, List
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, FileResponse

from utils.export_manager import export_manager
from .endpoints import APIResponse, log_api_call, validate_request


class ExportAPI:
    """API endpoints for data export functionality."""
    
    @staticmethod
    @log_api_call("export/financial")
    @validate_request(["results", "format"])
    def export_financial_results(request_data: Dict) -> Dict:
        """Export financial calculation results.
        
        Request:
            {
                "results": {
                    "financial_metrics": {...},
                    "tco_analysis": {...},
                    "risk_analysis": {...}
                },
                "format": "excel",  # or "csv", "pdf", "json"
                "filename": "analysis_report"  # optional
            }
        """
        try:
            format = request_data["format"].lower()
            results = request_data["results"]
            filename = request_data.get("filename")
            
            # Add extension if filename provided
            if filename and not filename.endswith(f".{format}"):
                filename = f"{filename}.{format}"
            
            # Export data
            output = export_manager.export_financial_results(
                results=results,
                format=format,
                filename=filename
            )
            
            if filename:
                # File was saved, return success with filename
                return APIResponse.success({
                    "filename": filename,
                    "format": format,
                    "message": f"Results exported to {filename}"
                })
            else:
                # Return base64 encoded data
                if isinstance(output, io.BytesIO):
                    data = base64.b64encode(output.getvalue()).decode('utf-8')
                else:
                    data = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                    
                return APIResponse.success({
                    "data": data,
                    "format": format,
                    "encoding": "base64"
                })
                
        except ValueError as e:
            return APIResponse.error(str(e), 400)
        except Exception as e:
            return APIResponse.error(f"Export failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("export/monte_carlo")
    @validate_request(["results", "format"])
    def export_monte_carlo_results(request_data: Dict) -> Dict:
        """Export Monte Carlo simulation results.
        
        Request:
            {
                "results": {
                    "mean": 1234.56,
                    "std_dev": 234.56,
                    "percentiles": {...}
                },
                "format": "excel",
                "include_histogram": true,
                "filename": "monte_carlo_results"
            }
        """
        try:
            format = request_data["format"].lower()
            results = request_data["results"]
            filename = request_data.get("filename")
            include_histogram = request_data.get("include_histogram", True)
            
            if filename and not filename.endswith(f".{format}"):
                filename = f"{filename}.{format}"
            
            output = export_manager.export_monte_carlo_results(
                results=results,
                format=format,
                filename=filename,
                include_histogram=include_histogram
            )
            
            if filename:
                return APIResponse.success({
                    "filename": filename,
                    "format": format,
                    "message": f"Monte Carlo results exported to {filename}"
                })
            else:
                if isinstance(output, io.BytesIO):
                    data = base64.b64encode(output.getvalue()).decode('utf-8')
                else:
                    data = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                    
                return APIResponse.success({
                    "data": data,
                    "format": format,
                    "encoding": "base64"
                })
                
        except Exception as e:
            return APIResponse.error(f"Export failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("export/batch")
    @validate_request(["results_list", "format"])
    def export_batch_results(request_data: Dict) -> Dict:
        """Export multiple calculation results in batch.
        
        Request:
            {
                "results_list": [
                    {"analysis_1": {...}},
                    {"analysis_2": {...}}
                ],
                "format": "excel",
                "filename": "batch_export"
            }
        """
        try:
            format = request_data["format"].lower()
            results_list = request_data["results_list"]
            filename = request_data.get("filename")
            
            if not isinstance(results_list, list):
                return APIResponse.error("results_list must be a list", 400)
            
            if filename and not filename.endswith(f".{format}"):
                filename = f"{filename}.{format}"
            
            output = export_manager.export_batch_results(
                results_list=results_list,
                format=format,
                filename=filename
            )
            
            if filename:
                return APIResponse.success({
                    "filename": filename,
                    "format": format,
                    "count": len(results_list),
                    "message": f"Batch results exported to {filename}"
                })
            else:
                if isinstance(output, io.BytesIO):
                    data = base64.b64encode(output.getvalue()).decode('utf-8')
                else:
                    data = base64.b64encode(output.encode('utf-8')).decode('utf-8')
                    
                return APIResponse.success({
                    "data": data,
                    "format": format,
                    "encoding": "base64",
                    "count": len(results_list)
                })
                
        except Exception as e:
            return APIResponse.error(f"Batch export failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("export/formats")
    def get_supported_formats(request_data: Dict = None) -> Dict:
        """Get list of supported export formats."""
        try:
            formats = {
                "financial": export_manager.supported_formats,
                "monte_carlo": export_manager.supported_formats,
                "batch": ["excel", "json"] if "excel" in export_manager.supported_formats else ["json"]
            }
            
            format_details = {
                "csv": {
                    "name": "CSV",
                    "description": "Comma-separated values, suitable for spreadsheets",
                    "mime_type": "text/csv"
                },
                "excel": {
                    "name": "Excel",
                    "description": "Microsoft Excel workbook with formatting",
                    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "requires": "xlsxwriter"
                },
                "pdf": {
                    "name": "PDF",
                    "description": "Portable Document Format report",
                    "mime_type": "application/pdf",
                    "requires": "reportlab"
                },
                "json": {
                    "name": "JSON",
                    "description": "JavaScript Object Notation, suitable for APIs",
                    "mime_type": "application/json"
                }
            }
            
            return APIResponse.success({
                "supported_formats": formats,
                "format_details": format_details
            })
            
        except Exception as e:
            return APIResponse.error(f"Failed to get formats: {str(e)}", 500)


# FastAPI integration functions for streaming responses
def create_download_response(data: bytes, filename: str, format: str) -> StreamingResponse:
    """Create a streaming download response for FastAPI.
    
    Args:
        data: File data as bytes
        filename: Filename for download
        format: File format
        
    Returns:
        StreamingResponse configured for file download
    """
    mime_types = {
        'csv': 'text/csv',
        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'pdf': 'application/pdf',
        'json': 'application/json'
    }
    
    mime_type = mime_types.get(format, 'application/octet-stream')
    
    return StreamingResponse(
        io.BytesIO(data),
        media_type=mime_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# Export templates for common use cases
class ExportTemplates:
    """Pre-configured export templates for common scenarios."""
    
    @staticmethod
    def investment_summary_template(
        npv: float,
        irr: float,
        payback_years: float,
        risk_level: str,
        recommendation: bool
    ) -> Dict:
        """Create investment summary template for export.
        
        Args:
            npv: Net Present Value
            irr: Internal Rate of Return
            payback_years: Payback period in years
            risk_level: Risk assessment level
            recommendation: Investment recommendation
            
        Returns:
            Formatted results dictionary ready for export
        """
        return {
            "financial_metrics": {
                "npv": npv,
                "irr": irr,
                "simple_roi_pct": (irr * 100) if irr else 0,
                "payback_years": payback_years
            },
            "risk_analysis": {
                "risk_level": risk_level,
                "meets_threshold": recommendation
            },
            "investment_decision": {
                "recommended": recommendation,
                "npv_positive": npv > 0,
                "irr_exceeds_hurdle": irr and irr > 0.10
            }
        }
    
    @staticmethod
    def monte_carlo_summary_template(simulation_results: Dict) -> Dict:
        """Create Monte Carlo summary template for export.
        
        Args:
            simulation_results: Raw Monte Carlo results
            
        Returns:
            Formatted results for export
        """
        return {
            "iterations": simulation_results.get("iterations", 0),
            "mean": simulation_results.get("mean", 0),
            "std_dev": simulation_results.get("std_dev", 0),
            "min": simulation_results.get("min", 0),
            "max": simulation_results.get("max", 0),
            "percentiles": simulation_results.get("percentiles", {}),
            "confidence_interval_90": simulation_results.get("confidence_interval_90", (0, 0)),
            "coefficient_of_variation": simulation_results.get("coefficient_of_variation", 0)
        }
    
    @staticmethod
    def industry_comparison_template(industry_results: List[Dict]) -> List[Dict]:
        """Create industry comparison template for batch export.
        
        Args:
            industry_results: List of industry-specific ROI results
            
        Returns:
            Formatted results list for batch export
        """
        formatted_results = []
        
        for result in industry_results:
            formatted = {
                "industry": result.get("industry_factors", {}).get("name", "Unknown"),
                "financial_metrics": result.get("financial_metrics", {}),
                "benefit_breakdown": result.get("benefit_breakdown", {}),
                "risk_level": result.get("risk_level", "Unknown"),
                "recommendations": result.get("recommendations", [])
            }
            formatted_results.append(formatted)
            
        return formatted_results


# Initialize export API instance
export_api = ExportAPI()
export_templates = ExportTemplates()