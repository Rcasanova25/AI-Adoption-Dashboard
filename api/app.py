"""FastAPI application for AI Adoption Dashboard API.

This module creates a FastAPI application that exposes the dashboard's
financial calculations and analysis capabilities as RESTful endpoints.
"""

from fastapi import FastAPI, HTTPException, Request, WebSocket, Depends
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
from .auth_endpoints import (
    auth_api,
    get_current_user,
    require_permission,
    LoginRequest,
    UserCreate,
    PasswordReset,
    TokenData
)
from .audit_endpoints import audit_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Adoption Dashboard API",
    description="RESTful API for AI investment analysis and financial calculations with authentication",
    version="1.1.0",
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


# Authentication endpoints
@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """User login endpoint."""
    result = auth_api.login(request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/auth/register")
async def register(request: UserCreate):
    """User registration endpoint."""
    result = auth_api.register(request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/auth/refresh")
async def refresh_token(request: Dict[str, str]):
    """Refresh access token."""
    result = auth_api.refresh_token(request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/auth/profile")
async def get_profile(current_user: TokenData = Depends(get_current_user)):
    """Get current user profile."""
    result = auth_api.get_profile(current_user.username)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/auth/change-password")
async def change_password(
    request: PasswordReset,
    current_user: TokenData = Depends(get_current_user)
):
    """Change user password."""
    result = auth_api.change_password(current_user.username, request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/auth/users")
async def list_users(current_user: TokenData = Depends(require_permission("admin:users"))):
    """List all users (admin only)."""
    result = auth_api.list_users()
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/auth/users")
async def create_user_admin(
    request: UserCreate,
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    """Create new user (admin only)."""
    result = auth_api.create_user_admin(request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.put("/api/auth/users/{username}")
async def update_user(
    username: str,
    request: Dict[str, Any],
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    """Update user information (admin only)."""
    result = auth_api.update_user(username, request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.delete("/api/auth/users/{username}")
async def delete_user(
    username: str,
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    """Delete user (admin only)."""
    result = auth_api.delete_user(username)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/auth/generate-api-key")
async def generate_api_key(
    request: Dict[str, Any],
    current_user: TokenData = Depends(get_current_user)
):
    """Generate API key for programmatic access."""
    result = auth_api.create_api_key(current_user.username, request)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/auth/permissions")
async def get_permissions(current_user: TokenData = Depends(get_current_user)):
    """Get current user permissions."""
    result = auth_api.get_permissions(current_user.username)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


# Financial calculation endpoints (protected)
@app.post("/api/financial/npv")
async def calculate_npv(
    request: NPVRequest,
    current_user: TokenData = Depends(require_permission("read:calculations"))
):
    """Calculate Net Present Value (requires authentication)."""
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
            ],
            "audit": [
                "/api/audit/search",
                "/api/audit/stats",
                "/api/audit/recent",
                "/api/audit/user-activity/{username}",
                "/api/audit/export",
                "/api/audit/calculation-history",
                "/api/audit/security-events"
            ]
        }
    })


# Audit endpoints (protected)
@app.post("/api/audit/search")
async def search_audit_logs(
    request: Dict[str, Any],
    current_user: TokenData = Depends(require_permission("read:all"))
):
    """Search audit logs (admin only)."""
    result = audit_api.search_logs(request, current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/audit/stats")
async def get_audit_stats(
    current_user: TokenData = Depends(require_permission("read:all"))
):
    """Get audit statistics (admin only)."""
    result = audit_api.get_statistics(current_user=current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/audit/recent")
async def get_recent_activity(
    current_user: TokenData = Depends(get_current_user)
):
    """Get recent activity."""
    result = audit_api.get_recent_activity(current_user=current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/audit/user-activity/{username}")
async def get_user_activity(
    username: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get user activity (own activity or admin only)."""
    result = audit_api.get_user_activity(username, current_user=current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.post("/api/audit/export")
async def export_audit_logs(
    request: Dict[str, Any],
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    """Export audit logs (admin only)."""
    result = audit_api.export_logs(request, current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/audit/calculation-history")
async def get_calculation_history(
    current_user: TokenData = Depends(get_current_user)
):
    """Get calculation history with performance metrics."""
    result = audit_api.get_calculation_history(current_user=current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


@app.get("/api/audit/security-events")
async def get_security_events(
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    """Get security events (admin only)."""
    result = audit_api.get_security_events(current_user=current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result


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