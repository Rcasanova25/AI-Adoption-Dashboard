"""Integration module to connect new data architecture with Dash app."""

import logging
from typing import Dict, Optional, Tuple
from functools import lru_cache
import time

import pandas as pd

logger = logging.getLogger(__name__)


def get_data_manager():
    """Get data manager instance with error handling."""
    try:
        from .data_manager_dash import DataManagerDash
        return DataManagerDash()
    except Exception as e:
        logger.error(f"Failed to create DataManagerDash: {e}")
        return FallbackDataManager()


class FallbackDataManager:
    """Fallback data manager that provides demo data when real manager fails."""
    
    def __init__(self):
        self.demo_data = self._create_demo_data()
    
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get demo dataset."""
        key = f"{source}_{dataset_name}" if source else dataset_name
        return self.demo_data.get(key, pd.DataFrame())
    
    def get_data(self, source: str) -> Dict[str, pd.DataFrame]:
        """Get demo data for a source."""
        source_data = {}
        for key, df in self.demo_data.items():
            if key.startswith(f"{source}_"):
                dataset_name = key.replace(f"{source}_", "")
                source_data[dataset_name] = df
        return source_data
    
    def _create_demo_data(self) -> Dict[str, pd.DataFrame]:
        """Create comprehensive demo data."""
        return {
            # AI Index data
            "ai_index_adoption_trends": pd.DataFrame({
                "year": [2020, 2021, 2022, 2023, 2024],
                "overall_adoption": [45, 52, 63, 72, 78],
                "genai_adoption": [5, 12, 28, 45, 58]
            }),
            "ai_index_sector_adoption": pd.DataFrame({
                "sector": ["Technology", "Financial Services", "Healthcare", "Manufacturing", "Retail"],
                "adoption_rate": [85, 72, 65, 58, 55],
                "year": [2024] * 5
            }),
            "ai_index_geographic_adoption": pd.DataFrame({
                "location": ["United States", "China", "United Kingdom", "Germany", "Canada"],
                "adoption_rate": [78, 74, 68, 65, 62],
                "year": [2024] * 5
            }),
            "ai_index_firm_size_adoption": pd.DataFrame({
                "firm_size": ["Large (>1000)", "Medium (250-1000)", "Small (<250)"],
                "adoption_rate": [85, 65, 45]
            }),
            "ai_index_ai_maturity": pd.DataFrame({
                "maturity_level": ["Exploring", "Experimenting", "Pilot", "Scaling", "Transforming"],
                "percentage_of_firms": [25, 30, 25, 15, 5]
            }),
            "ai_index_investment_trends": pd.DataFrame({
                "year": [2020, 2021, 2022, 2023, 2024],
                "global_investment_billions": [50, 85, 115, 185, 235]
            }),
            
            # McKinsey data
            "mckinsey_financial_impact": pd.DataFrame({
                "metric": ["Revenue Increase", "Cost Reduction", "Productivity Gain"],
                "value": [15, 25, 35],
                "unit": ["percentage"] * 3,
                "category": ["revenue_gains", "cost_savings", "productivity"]
            }),
            "mckinsey_use_case_adoption": pd.DataFrame({
                "function": ["Marketing", "Sales", "Customer Service", "Operations", "Finance"],
                "adoption_rate": [65, 58, 72, 55, 48],
                "year": [2024] * 5
            }),
            "mckinsey_implementation_barriers": pd.DataFrame({
                "barrier": ["Talent Gap", "Data Quality", "Integration Challenges", "ROI Uncertainty"],
                "percentage": [67, 52, 48, 41],
                "category": ["talent", "data", "technology", "financial"]
            }),
            "mckinsey_talent_metrics": pd.DataFrame({
                "metric": ["Talent Gap", "Hiring Increase", "Training Programs"],
                "value": [65, 45, 78],
                "year": [2024] * 3
            }),
            "mckinsey_productivity_gains": pd.DataFrame({
                "metric": ["productivity_improvement", "efficiency_improvement", "time_saved"],
                "value": [35, 28, 40],
                "unit": ["percentage", "percentage", "hours"],
                "category": ["general_productivity", "efficiency", "time_savings"]
            }),
            "mckinsey_risk_governance": pd.DataFrame({
                "governance_aspect": ["AI Ethics Guidelines", "Risk Assessment", "Bias Detection"],
                "adoption_rate": [72, 65, 38],
                "year": [2024] * 3
            }),
            
            # Strategy data
            "ai_strategy_strategy_pillars": pd.DataFrame({
                "pillar": ["Innovation", "Talent", "Infrastructure", "Governance"],
                "description": ["Drive innovation", "Build talent", "Improve infrastructure", "Ensure governance"],
                "priority": ["High", "High", "Medium", "Medium"],
                "owner": ["CTO", "CHO", "CTO", "CPO"]
            }),
            "ai_strategy_implementation_roadmap": pd.DataFrame({
                "phase": ["Phase 1", "Phase 2", "Phase 3"],
                "milestone": ["Foundation", "Scaling", "Transformation"],
                "timeline": ["Q1 2024", "Q3 2024", "Q1 2025"],
                "responsible_party": ["IT Team", "Business Units", "Executive Team"]
            }),
            "ai_strategy_success_metrics": pd.DataFrame({
                "metric": ["Adoption Rate", "ROI", "User Satisfaction"],
                "target": [80, 150, 85],
                "actual": [65, 120, 78],
                "status": ["In Progress", "On Track", "Achieved"]
            }),
            
            # Use cases data
            "ai_use_cases_use_case_catalog": pd.DataFrame({
                "use_case": ["Customer Service Bot", "Predictive Analytics", "Process Automation"],
                "category": ["Customer Service", "Analytics", "Operations"],
                "industry": ["All", "Finance", "Manufacturing"],
                "impact": ["High", "Medium", "High"],
                "adoption_level": ["Pilot", "Production", "Scaling"]
            }),
            "ai_use_cases_implementation_complexity": pd.DataFrame({
                "use_case": ["Customer Service Bot", "Predictive Analytics", "Process Automation"],
                "complexity_score": [3, 7, 5],
                "barriers": ["Integration", "Data Quality", "Change Management"],
                "resources_required": ["Low", "High", "Medium"]
            }),
            "ai_use_cases_value_impact_matrix": pd.DataFrame({
                "use_case": ["Customer Service Bot", "Predictive Analytics", "Process Automation"],
                "value_score": [7, 8, 6],
                "impact_area": ["Customer Experience", "Business Intelligence", "Efficiency"],
                "roi_estimate": [150, 200, 125]
            }),
            
            # Public sector data
            "public_sector_public_sector_adoption": pd.DataFrame({
                "government_level": ["Federal", "State", "Local"],
                "adoption_rate": [45, 35, 25],
                "primary_use_cases": ["Security", "Services", "Operations"],
                "budget_allocated_millions": [500, 200, 50],
                "citizen_satisfaction_improvement": [15, 12, 8],
                "efficiency_gain_percent": [20, 18, 15]
            }),
            "public_sector_implementation_barriers": pd.DataFrame({
                "barrier": ["Budget Constraints", "Regulatory Compliance", "Public Trust"],
                "severity_score": [8, 7, 6],
                "organizations_affected_percent": [75, 65, 45],
                "mitigation_strategies_available": [True, True, False]
            }),
            "public_sector_success_factors": pd.DataFrame({
                "success_factor": ["Leadership Support", "Citizen Engagement", "Technical Expertise"],
                "importance_score": [9, 8, 7],
                "implementation_rate": [65, 45, 55],
                "impact_on_success": [85, 70, 75]
            })
        }


# Cache implementation for Dash
_cache = {}
_cache_timestamps = {}
CACHE_TTL = 3600  # 1 hour in seconds


def load_data() -> Tuple:
    """Load all data for the dashboard using the new modular system with fallbacks."""
    
    # Check cache first
    cache_key = "all_data"
    current_time = time.time()
    
    if cache_key in _cache and cache_key in _cache_timestamps:
        cache_age = current_time - _cache_timestamps[cache_key]
        if cache_age < CACHE_TTL:
            logger.info("Returning cached data")
            return _cache[cache_key]
    
    logger.info("Loading data from modular data sources...")
    
    try:
        # Get data manager instance
        dm = get_data_manager()
        
        # Load all required datasets with fallbacks
        datasets = {}
        
        # Core datasets with fallback data
        dataset_configs = [
            ("historical_data", "ai_index", "adoption_trends"),
            ("sector_data", "ai_index", "sector_adoption"),
            ("geographic_df", "ai_index", "geographic_adoption"),
            ("firm_size_data", "ai_index", "firm_size_adoption"),
            ("ai_maturity_df", "ai_index", "ai_maturity"),
            ("ai_investment_df", "ai_index", "investment_trends"),
            ("financial_impact_data", "mckinsey", "financial_impact"),
            ("use_case_data", "mckinsey", "use_case_adoption"),
            ("barriers_data", "mckinsey", "implementation_barriers"),
            ("talent_data", "mckinsey", "talent_metrics"),
            ("productivity_data", "mckinsey", "productivity_gains"),
            ("governance_data", "mckinsey", "risk_governance"),
        ]
        
        # Load each dataset with error handling
        for var_name, source, dataset in dataset_configs:
            try:
                datasets[var_name] = dm.get_dataset(dataset, source)
                logger.info(f"Successfully loaded {var_name} from {source}.{dataset}")
            except Exception as e:
                logger.warning(f"Failed to load {var_name}: {e}, using fallback data")
                # Use fallback for demo data
                datasets[var_name] = pd.DataFrame()
        
        # Process strategy data specially
        try:
            strategy_data = dm.get_data("ai_strategy")
            use_case_data_full = dm.get_data("ai_use_cases")
            public_sector_data = dm.get_data("public_sector")
            
            # Merge the dictionaries
            datasets.update({
                "strategy_data": strategy_data,
                "use_case_data_full": use_case_data_full,
                "public_sector_data": public_sector_data
            })
        except Exception as e:
            logger.warning(f"Failed to load strategy/use case data: {e}")
            datasets.update({
                "strategy_data": {},
                "use_case_data_full": {},
                "public_sector_data": {}
            })
        
        # Create result tuple in the expected format
        result = (
            datasets.get("historical_data", pd.DataFrame()),
            datasets.get("sector_data", pd.DataFrame()),
            datasets.get("geographic_df", pd.DataFrame()),
            datasets.get("firm_size_data", pd.DataFrame()),
            datasets.get("ai_maturity_df", pd.DataFrame()),
            datasets.get("ai_investment_df", pd.DataFrame()),
            datasets.get("financial_impact_data", pd.DataFrame()),
            datasets.get("use_case_data", pd.DataFrame()),
            datasets.get("barriers_data", pd.DataFrame()),
            datasets.get("talent_data", pd.DataFrame()),
            datasets.get("productivity_data", pd.DataFrame()),
            datasets.get("governance_data", pd.DataFrame()),
            datasets.get("strategy_data", {}),
            datasets.get("use_case_data_full", {}),
            datasets.get("public_sector_data", {})
        )
        
        # Cache the result
        _cache[cache_key] = result
        _cache_timestamps[cache_key] = current_time
        
        return result
        
    except Exception as e:
        logger.error(f"Critical error in load_data: {e}", exc_info=True)
        # Return empty data structure to prevent app crash
        return tuple([pd.DataFrame()] * 12 + [{}, {}, {}])


def clear_cache():
    """Clear the data cache."""
    global _cache, _cache_timestamps
    _cache.clear()
    _cache_timestamps.clear()
    logger.info("Data integration cache cleared")