# Phase 2: Economic Logic & Model Integration - Implementation Plan

## Overview
Phase 2 focuses on implementing real economic models, scenario analysis, and policy simulation capabilities to transform the dashboard from a data visualization tool into a comprehensive economic analysis platform.

## Current State Analysis

### Existing Assets
1. **Pydantic Models** (data/models/):
   - Strong type validation and documentation
   - Cover adoption, economics, governance, and workforce domains
   - Need enhancement for advanced economic analysis

2. **Business Logic** (business/):
   - Basic calculations for ROI, scenarios, labor impact, and policy
   - Uses Pydantic models properly
   - Lacks sophisticated economic modeling

3. **Data Integration**:
   - Phase 1 established solid data pipeline
   - Real data from PDFs now flows to views
   - Ready for enhanced calculations

### Key Gaps Identified
- No NPV/IRR calculations
- Missing Monte Carlo simulation
- No sensitivity analysis
- Limited scenario modeling (only linear projections)
- No risk-adjusted returns
- Missing TCO modeling
- No industry-specific models

## Implementation Roadmap

### Step 1: Core Financial Calculations Enhancement
**Files to create/modify:**
- `business/financial_calculations.py` (new)
- `business/roi_analysis.py` (enhance)

**Implementation:**
```python
# New calculations to add:
- calculate_npv(cash_flows, discount_rate, initial_investment)
- calculate_irr(cash_flows, initial_investment)
- calculate_tco(initial_cost, annual_costs, maintenance_rate, years)
- calculate_payback_period(initial_investment, annual_savings, consider_time_value)
- calculate_risk_adjusted_return(expected_return, risk_level, risk_free_rate)
```

### Step 2: Advanced Scenario Analysis
**Files to create/modify:**
- `business/scenario_engine.py` (new)
- `business/economic_scenarios.py` (enhance)

**Implementation:**
```python
# Scenario capabilities:
- monte_carlo_simulation(base_case, variables, iterations=10000)
- sensitivity_analysis(model, parameters, range_pct=20)
- adoption_s_curve(current_adoption, max_adoption, rate, time)
- correlation_matrix_modeling(technologies, historical_data)
```

### Step 3: Industry-Specific Models
**Files to create:**
- `business/industry_models/` (new directory)
- `business/industry_models/manufacturing.py`
- `business/industry_models/financial_services.py`
- `business/industry_models/healthcare.py`
- `business/industry_models/retail.py`

**Each industry model will include:**
- Sector-specific ROI calculations
- Industry productivity functions
- Typical implementation timelines
- Risk factors and mitigation strategies

### Step 4: Enhanced Labor Market Analysis
**Files to modify:**
- `business/labor_impact.py`
- `data/models/workforce.py`

**New calculations:**
```python
- calculate_wage_impact(job_category, automation_level, market_data)
- estimate_retraining_costs(skill_gap, worker_count, training_type)
- model_labor_mobility(geographic_data, job_displacement)
- productivity_elasticity(technology_type, industry, adoption_level)
```

### Step 5: Risk Analysis Framework
**Files to create:**
- `business/risk_analysis.py` (new)
- `business/risk_models.py` (new)

**Risk calculations:**
```python
- monte_carlo_risk_assessment(project_parameters, risk_factors)
- implementation_success_probability(company_size, industry, ai_maturity)
- regulatory_compliance_cost(jurisdiction, ai_type, data_volume)
- technical_debt_projection(implementation_age, technology_stack)
```

### Step 6: Policy Simulation Enhancement
**Files to modify:**
- `business/policy_simulation.py`

**Enhanced capabilities:**
- Multi-jurisdiction policy comparison
- Policy cost-benefit analysis
- Regulatory scenario planning
- Compliance cost modeling

### Step 7: Model Integration into Views
**Files to modify:**
- All view files to use new calculations
- `views/roi_analysis.py` - Use enhanced ROI calculations
- `views/scenario_analysis.py` (new) - Advanced scenario view
- `views/risk_dashboard.py` (new) - Risk analysis view

## Data Model Enhancements

### Fix Duplicate Models
1. Remove `ProductivityMetrics` from `economics.py`
2. Keep only the version in `workforce.py`

### Add New Models
```python
# data/models/financial.py (new)
class NPVAnalysis(BaseModel):
    cash_flows: List[float]
    discount_rate: float
    initial_investment: float
    npv: float
    irr: Optional[float]

class TCOAnalysis(BaseModel):
    initial_cost: float
    annual_operating_cost: float
    maintenance_cost: float
    total_years: int
    total_cost: float

# data/models/scenarios.py (new)
class ScenarioParameters(BaseModel):
    name: str
    variables: Dict[str, float]
    probability: float
    confidence_interval: Tuple[float, float]

class MonteCarloResult(BaseModel):
    mean: float
    std_dev: float
    percentile_5: float
    percentile_95: float
    iterations: int
```

## Implementation Priority

### High Priority (Week 1):
1. Core financial calculations (NPV, IRR, TCO)
2. Fix model duplications
3. Enhanced ROI analysis with risk adjustment

### Medium Priority (Week 2):
1. Monte Carlo simulation engine
2. Sensitivity analysis
3. Industry-specific models (start with 2-3 key industries)

### Lower Priority (Week 3):
1. Advanced labor market models
2. Policy cost modeling
3. New visualization views

## Success Criteria
- ✅ All financial calculations use industry-standard formulas
- ✅ Scenario analysis provides probabilistic outcomes
- ✅ Risk is quantified and incorporated into returns
- ✅ Industry-specific nuances are captured
- ✅ Models are validated against real-world data
- ✅ Views display uncertainty and confidence intervals

## Testing Strategy
1. Unit tests for all calculation functions
2. Validation against known financial examples
3. Backtesting with historical data
4. Scenario comparison with industry benchmarks
5. User acceptance testing with finance professionals

## Next Steps
1. Start with core financial calculations
2. Build test cases with known outcomes
3. Integrate calculations into existing views
4. Add new views for advanced analysis
5. Document all formulas and assumptions

This plan transforms the dashboard from displaying data to providing actionable economic insights for AI adoption decisions.