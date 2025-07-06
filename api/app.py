"""FastAPI application for AI Adoption Dashboard API.

This module creates a FastAPI application that exposes the dashboard's
financial calculations and analysis capabilities as RESTful endpoints.
"""

from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import asyncio

from .endpoints import (
    financial_api,
    scenario_api,
    industry_api,
    APIResponse
)
from .export_endpoints import (
    export_api,
    create_download_response,
    export_templates
)
from .websocket_server import (
    websocket_endpoint,
    start_background_tasks,
    stop_background_tasks
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Adoption Dashboard API",
    description="RESTful API for AI investment analysis and financial calculations",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class NPVRequest(BaseModel):
    cash_flows: List[float] = Field(..., description="Annual cash flows")
    discount_rate: float = Field(..., ge=0, le=1, description="Discount rate (0-1)")
    initial_investment: float = Field(..., gt=0, description="Initial investment amount")


class IRRRequest(BaseModel):
    cash_flows: List[float] = Field(..., description="Annual cash flows")
    initial_investment: float = Field(..., gt=0, description="Initial investment amount")


class ComprehensiveROIRequest(BaseModel):
    initial_investment: float = Field(..., gt=0)
    annual_cash_flows: List[float] = Field(...)
    annual_operating_costs: List[float] = Field(...)
    risk_level: str = Field("Medium", pattern="^(Low|Medium|High|Very High)$")
    discount_rate: float = Field(0.10, ge=0, le=1)
    num_employees: Optional[int] = Field(None, gt=0)
    avg_salary: Optional[float] = Field(None, gt=0)
    productivity_gain_pct: Optional[float] = Field(None, ge=0, le=1)


class MonteCarloRequest(BaseModel):
    base_case: Dict[str, float] = Field(...)
    variables: List[Dict[str, Any]] = Field(...)
    model_type: str = Field(..., pattern="^(simple_roi|npv|payback)$")
    iterations: int = Field(10000, ge=100, le=100000)
    confidence_levels: List[float] = Field([0.05, 0.25, 0.50, 0.75, 0.95])


class SensitivityRequest(BaseModel):
    base_case: Dict[str, float] = Field(...)
    variables: List[str] = Field(...)
    model_type: str = Field(..., pattern="^(roi|npv)$")
    variation_pct: float = Field(0.20, ge=0.05, le=0.50)
    steps: int = Field(5, ge=3, le=10)


class IndustryROIRequest(BaseModel):
    investment: float = Field(..., gt=0)
    years: int = Field(5, ge=1, le=10)


class ManufacturingROIRequest(IndustryROIRequest):
    production_volume: float = Field(..., gt=0)
    defect_rate_reduction: float = Field(0.25, ge=0, le=1)
    downtime_reduction: float = Field(0.20, ge=0, le=1)
    labor_productivity_gain: float = Field(0.15, ge=0, le=1)
    energy_efficiency_gain: float = Field(0.10, ge=0, le=1)


class HealthcareROIRequest(IndustryROIRequest):
    patient_volume: float = Field(..., gt=0)
    diagnostic_accuracy_gain: float = Field(0.20, ge=0, le=1)
    patient_wait_reduction: float = Field(0.30, ge=0, le=1)
    admin_efficiency_gain: float = Field(0.40, ge=0, le=1)
    readmission_reduction: float = Field(0.15, ge=0, le=1)


class FinancialServicesROIRequest(IndustryROIRequest):
    transaction_volume: float = Field(..., gt=0)
    fraud_detection_improvement: float = Field(0.40, ge=0, le=1)
    processing_time_reduction: float = Field(0.60, ge=0, le=1)
    compliance_automation: float = Field(0.50, ge=0, le=1)
    customer_experience_gain: float = Field(0.30, ge=0, le=1)


class RetailROIRequest(IndustryROIRequest):
    annual_revenue: float = Field(..., gt=0)
    personalization_uplift: float = Field(0.15, ge=0, le=1)
    inventory_optimization: float = Field(0.20, ge=0, le=1)
    customer_service_automation: float = Field(0.50, ge=0, le=1)
    supply_chain_efficiency: float = Field(0.25, ge=0, le=1)


class StrategyRequest(BaseModel):
    industry: str = Field(...)
    company_size: str = Field(..., pattern="^(Small|Medium|Large|Enterprise)$")
    budget: float = Field(..., gt=0)
    timeline_months: int = Field(..., ge=1, le=60)
    strategic_goals: List[str] = Field(...)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return APIResponse.success({"status": "healthy"}, "API is running")


# Financial calculation endpoints
@app.post("/api/financial/npv")
async def calculate_npv(request: NPVRequest):
    """Calculate Net Present Value."""
    result = financial_api.calculate_npv(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/financial/irr")
async def calculate_irr(request: IRRRequest):
    """Calculate Internal Rate of Return."""
    result = financial_api.calculate_irr(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/financial/comprehensive-roi")
async def calculate_comprehensive_roi(request: ComprehensiveROIRequest):
    """Calculate comprehensive ROI metrics."""
    result = financial_api.comprehensive_roi(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/financial/cache-stats")
async def get_cache_stats():
    """Get cache statistics."""
    return financial_api.get_cache_stats()


# Scenario analysis endpoints
@app.post("/api/scenario/monte-carlo")
async def run_monte_carlo(request: MonteCarloRequest):
    """Run Monte Carlo simulation."""
    result = scenario_api.monte_carlo(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/scenario/sensitivity")
async def run_sensitivity_analysis(request: SensitivityRequest):
    """Run sensitivity analysis."""
    result = scenario_api.sensitivity_analysis(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


# Industry-specific endpoints
@app.post("/api/industry/manufacturing/roi")
async def calculate_manufacturing_roi(request: ManufacturingROIRequest):
    """Calculate manufacturing industry ROI."""
    result = industry_api.manufacturing_roi(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/industry/healthcare/roi")
async def calculate_healthcare_roi(request: HealthcareROIRequest):
    """Calculate healthcare industry ROI."""
    result = industry_api.healthcare_roi(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/industry/financial-services/roi")
async def calculate_financial_services_roi(request: FinancialServicesROIRequest):
    """Calculate financial services industry ROI."""
    result = industry_api.financial_services_roi(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/industry/retail/roi")
async def calculate_retail_roi(request: RetailROIRequest):
    """Calculate retail industry ROI."""
    result = industry_api.retail_roi(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/industry/{industry}/benchmarks")
async def get_industry_benchmarks(industry: str):
    """Get industry benchmarks."""
    result = industry_api.get_benchmarks({"industry": industry})
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/industry/optimal-strategy")
async def get_optimal_strategy(request: StrategyRequest):
    """Get optimal AI implementation strategy."""
    result = industry_api.optimal_strategy(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


# Export endpoints
class ExportRequest(BaseModel):
    results: Dict[str, Any] = Field(..., description="Calculation results to export")
    format: str = Field(..., pattern="^(csv|excel|pdf|json)$", description="Export format")
    filename: Optional[str] = Field(None, description="Optional filename")


class BatchExportRequest(BaseModel):
    results_list: List[Dict[str, Any]] = Field(..., description="List of results to export")
    format: str = Field(..., pattern="^(excel|json)$", description="Export format")
    filename: Optional[str] = Field(None, description="Optional filename")


@app.post("/api/export/financial")
async def export_financial_results(request: ExportRequest):
    """Export financial calculation results."""
    result = export_api.export_financial_results(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    
    # If data is returned (not saved to file), create download response
    if "data" in result["data"]:
        import base64
        data = base64.b64decode(result["data"]["data"])
        filename = f"financial_analysis.{request.format}"
        return create_download_response(data, filename, request.format)
    
    return result


@app.post("/api/export/monte-carlo")
async def export_monte_carlo_results(request: ExportRequest):
    """Export Monte Carlo simulation results."""
    result = export_api.export_monte_carlo_results(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    
    if "data" in result["data"]:
        import base64
        data = base64.b64decode(result["data"]["data"])
        filename = f"monte_carlo_results.{request.format}"
        return create_download_response(data, filename, request.format)
    
    return result


@app.post("/api/export/batch")
async def export_batch_results(request: BatchExportRequest):
    """Export multiple results in batch."""
    result = export_api.export_batch_results(request.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    
    if "data" in result["data"]:
        import base64
        data = base64.b64decode(result["data"]["data"])
        filename = f"batch_export.{request.format}"
        return create_download_response(data, filename, request.format)
    
    return result


@app.get("/api/export/formats")
async def get_export_formats():
    """Get supported export formats."""
    return export_api.get_supported_formats()


# Error handling
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse.error(
            "An unexpected error occurred",
            500,
            {"error": str(exc)}
        )
    )


# API documentation
@app.get("/api")
async def api_info():
    """Get API information and available endpoints."""
    return APIResponse.success({
        "name": "AI Adoption Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "financial": [
                "/api/financial/npv",
                "/api/financial/irr",
                "/api/financial/comprehensive-roi",
                "/api/financial/cache-stats"
            ],
            "scenario": [
                "/api/scenario/monte-carlo",
                "/api/scenario/sensitivity"
            ],
            "industry": [
                "/api/industry/manufacturing/roi",
                "/api/industry/healthcare/roi",
                "/api/industry/financial-services/roi",
                "/api/industry/retail/roi",
                "/api/industry/{industry}/benchmarks",
                "/api/industry/optimal-strategy"
            ],
            "export": [
                "/api/export/financial",
                "/api/export/monte-carlo",
                "/api/export/batch",
                "/api/export/formats"
            ],
            "documentation": [
                "/api/docs",
                "/api/redoc"
            ],
            "websocket": [
                "/ws"
            ]
        }
    })


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket_endpoint(websocket)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize background tasks on startup."""
    await start_background_tasks()
    logger.info("API server started with WebSocket support")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    stop_background_tasks()
    logger.info("API server shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)