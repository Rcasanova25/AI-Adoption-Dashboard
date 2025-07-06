"""API endpoints for financial calculations and analysis.

This module provides RESTful endpoints for accessing the dashboard's
calculation capabilities programmatically.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from functools import wraps
import pandas as pd
import streamlit as st

# Import business logic
from business.financial_calculations_cached import (
    calculate_npv,
    calculate_irr,
    calculate_tco,
    calculate_payback_period,
    calculate_risk_adjusted_return,
    calculate_ai_productivity_roi,
    get_cache_statistics
)
from business.scenario_engine_parallel import (
    monte_carlo_simulation_parallel,
    sensitivity_analysis_parallel,
    ScenarioVariable
)
from business.industry_models import (
    calculate_manufacturing_roi,
    calculate_healthcare_roi,
    calculate_financial_services_roi,
    calculate_retail_roi,
    get_industry_benchmarks,
    select_optimal_ai_strategy
)
from business.roi_analysis import (
    compute_comprehensive_roi,
    analyze_roi_by_company_size
)

logger = logging.getLogger(__name__)


# API Response wrapper
class APIResponse:
    """Standard API response format."""
    
    @staticmethod
    def success(data: Any, message: str = "Success") -> Dict:
        """Create success response."""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
    @staticmethod
    def error(message: str, code: int = 400, details: Optional[Dict] = None) -> Dict:
        """Create error response."""
        return {
            "status": "error",
            "message": message,
            "code": code,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }


# Request validation decorator
def validate_request(required_fields: List[str]):
    """Decorator to validate required fields in request."""
    def decorator(func):
        @wraps(func)
        def wrapper(request_data: Dict, *args, **kwargs):
            missing = [field for field in required_fields if field not in request_data]
            if missing:
                return APIResponse.error(
                    f"Missing required fields: {', '.join(missing)}",
                    code=400,
                    details={"missing_fields": missing}
                )
            return func(request_data, *args, **kwargs)
        return wrapper
    return decorator


# Logging decorator
def log_api_call(endpoint: str):
    """Decorator to log API calls."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"API call to {endpoint}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"API call to {endpoint} successful")
                return result
            except Exception as e:
                logger.error(f"API call to {endpoint} failed: {str(e)}")
                raise
        return wrapper
    return decorator


# Financial Calculations API
class FinancialAPI:
    """API endpoints for financial calculations."""
    
    @staticmethod
    @log_api_call("financial/npv")
    @validate_request(["cash_flows", "discount_rate", "initial_investment"])
    def calculate_npv(request_data: Dict) -> Dict:
        """Calculate Net Present Value.
        
        Request:
            {
                "cash_flows": [100000, 120000, 140000],
                "discount_rate": 0.10,
                "initial_investment": 300000
            }
        """
        try:
            npv = calculate_npv(
                request_data["cash_flows"],
                request_data["discount_rate"],
                request_data["initial_investment"]
            )
            
            return APIResponse.success({
                "npv": npv,
                "profitable": npv > 0,
                "parameters": {
                    "years": len(request_data["cash_flows"]),
                    "discount_rate": request_data["discount_rate"],
                    "initial_investment": request_data["initial_investment"]
                }
            })
        except Exception as e:
            return APIResponse.error(f"NPV calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("financial/irr")
    @validate_request(["cash_flows", "initial_investment"])
    def calculate_irr(request_data: Dict) -> Dict:
        """Calculate Internal Rate of Return.
        
        Request:
            {
                "cash_flows": [50000, 60000, 70000, 80000],
                "initial_investment": 150000
            }
        """
        try:
            irr = calculate_irr(
                request_data["cash_flows"],
                request_data["initial_investment"]
            )
            
            if irr is None:
                return APIResponse.error(
                    "IRR calculation did not converge",
                    400,
                    {"hint": "Check that cash flows sum to more than initial investment"}
                )
            
            return APIResponse.success({
                "irr": irr,
                "irr_percentage": irr * 100,
                "parameters": {
                    "years": len(request_data["cash_flows"]),
                    "initial_investment": request_data["initial_investment"]
                }
            })
        except Exception as e:
            return APIResponse.error(f"IRR calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("financial/comprehensive_roi")
    @validate_request(["initial_investment", "annual_cash_flows", "annual_operating_costs"])
    def comprehensive_roi(request_data: Dict) -> Dict:
        """Calculate comprehensive ROI metrics.
        
        Request:
            {
                "initial_investment": 500000,
                "annual_cash_flows": [150000, 180000, 200000, 220000, 250000],
                "annual_operating_costs": [30000, 35000, 40000, 45000, 50000],
                "risk_level": "Medium",
                "discount_rate": 0.10,
                "num_employees": 50,
                "avg_salary": 75000,
                "productivity_gain_pct": 0.20
            }
        """
        try:
            results = compute_comprehensive_roi(
                initial_investment=request_data["initial_investment"],
                annual_cash_flows=request_data["annual_cash_flows"],
                annual_operating_costs=request_data["annual_operating_costs"],
                risk_level=request_data.get("risk_level", "Medium"),
                discount_rate=request_data.get("discount_rate", 0.10),
                num_employees=request_data.get("num_employees"),
                avg_salary=request_data.get("avg_salary"),
                productivity_gain_pct=request_data.get("productivity_gain_pct")
            )
            
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Comprehensive ROI calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("financial/cache_stats")
    def get_cache_stats(request_data: Dict = None) -> Dict:
        """Get cache statistics for performance monitoring."""
        try:
            stats = get_cache_statistics()
            return APIResponse.success(stats, "Cache statistics retrieved")
        except Exception as e:
            return APIResponse.error(f"Failed to get cache stats: {str(e)}", 500)


# Scenario Analysis API
class ScenarioAPI:
    """API endpoints for scenario analysis."""
    
    @staticmethod
    @log_api_call("scenario/monte_carlo")
    @validate_request(["base_case", "variables", "model_type"])
    def monte_carlo(request_data: Dict) -> Dict:
        """Run Monte Carlo simulation.
        
        Request:
            {
                "base_case": {"revenue": 1000000, "cost": 600000},
                "variables": [
                    {
                        "name": "revenue",
                        "base_value": 1000000,
                        "min_value": 800000,
                        "max_value": 1200000,
                        "distribution": "normal"
                    }
                ],
                "model_type": "simple_roi",
                "iterations": 10000,
                "confidence_levels": [0.05, 0.95]
            }
        """
        try:
            # Convert variable dicts to ScenarioVariable objects
            variables = [
                ScenarioVariable(**var) for var in request_data["variables"]
            ]
            
            # Select model function based on type
            model_functions = {
                "simple_roi": lambda revenue, cost: (revenue - cost) / cost,
                "npv": lambda revenue, cost, rate=0.1: 
                    sum((revenue - cost) / (1 + rate)**i for i in range(1, 6)),
                "payback": lambda revenue, cost, investment=1000000:
                    investment / (revenue - cost) if revenue > cost else float('inf')
            }
            
            model_func = model_functions.get(
                request_data["model_type"], 
                model_functions["simple_roi"]
            )
            
            # Run simulation
            results = monte_carlo_simulation_parallel(
                base_case=request_data["base_case"],
                variables=variables,
                model_function=model_func,
                iterations=request_data.get("iterations", 10000),
                confidence_levels=request_data.get("confidence_levels", [0.05, 0.25, 0.50, 0.75, 0.95])
            )
            
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Monte Carlo simulation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("scenario/sensitivity")
    @validate_request(["base_case", "variables", "model_type"])
    def sensitivity_analysis(request_data: Dict) -> Dict:
        """Run sensitivity analysis.
        
        Request:
            {
                "base_case": {"investment": 100000, "revenue": 50000, "cost": 20000},
                "variables": ["investment", "revenue", "cost"],
                "model_type": "roi",
                "variation_pct": 0.20,
                "steps": 5
            }
        """
        try:
            # Model functions
            model_functions = {
                "roi": lambda investment, revenue, cost: 
                    ((revenue - cost) * 5 - investment) / investment,
                "npv": lambda investment, revenue, cost, rate=0.1:
                    -investment + sum((revenue - cost) / (1 + rate)**i for i in range(1, 6))
            }
            
            model_func = model_functions.get(
                request_data["model_type"],
                model_functions["roi"]
            )
            
            # Run analysis
            results = sensitivity_analysis_parallel(
                base_case=request_data["base_case"],
                variables=request_data["variables"],
                model_function=model_func,
                variation_pct=request_data.get("variation_pct", 0.20),
                steps=request_data.get("steps", 5)
            )
            
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Sensitivity analysis failed: {str(e)}", 500)


# Industry Models API
class IndustryAPI:
    """API endpoints for industry-specific calculations."""
    
    @staticmethod
    @log_api_call("industry/manufacturing")
    @validate_request(["investment", "production_volume"])
    def manufacturing_roi(request_data: Dict) -> Dict:
        """Calculate manufacturing industry ROI."""
        try:
            results = calculate_manufacturing_roi(
                investment=request_data["investment"],
                production_volume=request_data["production_volume"],
                defect_rate_reduction=request_data.get("defect_rate_reduction", 0.25),
                downtime_reduction=request_data.get("downtime_reduction", 0.20),
                labor_productivity_gain=request_data.get("labor_productivity_gain", 0.15),
                energy_efficiency_gain=request_data.get("energy_efficiency_gain", 0.10),
                years=request_data.get("years", 5)
            )
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Manufacturing ROI calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("industry/healthcare")
    @validate_request(["investment", "patient_volume"])
    def healthcare_roi(request_data: Dict) -> Dict:
        """Calculate healthcare industry ROI."""
        try:
            results = calculate_healthcare_roi(
                investment=request_data["investment"],
                patient_volume=request_data["patient_volume"],
                diagnostic_accuracy_gain=request_data.get("diagnostic_accuracy_gain", 0.20),
                patient_wait_reduction=request_data.get("patient_wait_reduction", 0.30),
                admin_efficiency_gain=request_data.get("admin_efficiency_gain", 0.40),
                readmission_reduction=request_data.get("readmission_reduction", 0.15),
                years=request_data.get("years", 5)
            )
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Healthcare ROI calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("industry/financial_services")
    @validate_request(["investment", "transaction_volume"])
    def financial_services_roi(request_data: Dict) -> Dict:
        """Calculate financial services industry ROI."""
        try:
            results = calculate_financial_services_roi(
                investment=request_data["investment"],
                transaction_volume=request_data["transaction_volume"],
                fraud_detection_improvement=request_data.get("fraud_detection_improvement", 0.40),
                processing_time_reduction=request_data.get("processing_time_reduction", 0.60),
                compliance_automation=request_data.get("compliance_automation", 0.50),
                customer_experience_gain=request_data.get("customer_experience_gain", 0.30),
                years=request_data.get("years", 5)
            )
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Financial services ROI calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("industry/retail")
    @validate_request(["investment", "annual_revenue"])
    def retail_roi(request_data: Dict) -> Dict:
        """Calculate retail industry ROI."""
        try:
            results = calculate_retail_roi(
                investment=request_data["investment"],
                annual_revenue=request_data["annual_revenue"],
                personalization_uplift=request_data.get("personalization_uplift", 0.15),
                inventory_optimization=request_data.get("inventory_optimization", 0.20),
                customer_service_automation=request_data.get("customer_service_automation", 0.50),
                supply_chain_efficiency=request_data.get("supply_chain_efficiency", 0.25),
                years=request_data.get("years", 5)
            )
            return APIResponse.success(results)
        except Exception as e:
            return APIResponse.error(f"Retail ROI calculation failed: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("industry/benchmarks")
    @validate_request(["industry"])
    def get_benchmarks(request_data: Dict) -> Dict:
        """Get industry benchmarks."""
        try:
            benchmarks = get_industry_benchmarks(request_data["industry"])
            if "error" in benchmarks:
                return APIResponse.error(benchmarks["error"], 400)
            return APIResponse.success(benchmarks)
        except Exception as e:
            return APIResponse.error(f"Failed to get benchmarks: {str(e)}", 500)
    
    @staticmethod
    @log_api_call("industry/strategy")
    @validate_request(["industry", "company_size", "budget", "timeline_months", "strategic_goals"])
    def optimal_strategy(request_data: Dict) -> Dict:
        """Get optimal AI strategy for industry."""
        try:
            strategy = select_optimal_ai_strategy(
                industry=request_data["industry"],
                company_size=request_data["company_size"],
                budget=request_data["budget"],
                timeline_months=request_data["timeline_months"],
                strategic_goals=request_data["strategic_goals"]
            )
            if "error" in strategy:
                return APIResponse.error(strategy["error"], 400)
            return APIResponse.success(strategy)
        except Exception as e:
            return APIResponse.error(f"Strategy selection failed: {str(e)}", 500)


# Initialize API instances
financial_api = FinancialAPI()
scenario_api = ScenarioAPI()
industry_api = IndustryAPI()


# Export and Report APIs will be in separate files
class ExportAPI:
    """Placeholder for export functionality."""
    pass


class ReportAPI:
    """Placeholder for report generation."""
    pass


export_api = ExportAPI()
report_api = ReportAPI()