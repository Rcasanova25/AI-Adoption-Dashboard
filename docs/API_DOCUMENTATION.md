# AI Adoption Dashboard API Documentation

## Overview
The AI Adoption Dashboard provides a comprehensive RESTful API for accessing financial calculations, scenario analysis, and report generation capabilities programmatically.

**Base URL:** `http://localhost:8000/api`

**Documentation:** 
- Interactive docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Authentication

The API uses JWT-based authentication for secure access. Most endpoints require authentication.

### Getting Started

1. **Login** to receive access and refresh tokens:
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

2. **Include the token** in subsequent requests:
```http
GET /api/financial/npv
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

3. **Refresh tokens** when they expire (30 minutes):
```http
POST /api/auth/refresh
Content-Type: application/json

{
    "refresh_token": "your_refresh_token"
}
```

### Default Account
- Username: `admin`
- Password: `admin123`
- ⚠️ Change immediately in production!

### User Roles
- **Admin**: Full system access
- **Analyst**: Read/write calculations and reports
- **Viewer**: Read-only access
- **API User**: Optimized for programmatic access

See [AUTHENTICATION.md](./AUTHENTICATION.md) for complete authentication documentation.

## Response Format
All API responses follow a consistent format:

```json
{
  "status": "success" | "error",
  "message": "Description of the result",
  "data": { ... },  // For successful responses
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Error responses include additional fields:
```json
{
  "status": "error",
  "message": "Error description",
  "code": 400,
  "details": { ... },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Endpoints

### 1. Financial Calculations

#### Calculate NPV
Calculate Net Present Value of an investment.

**POST** `/api/financial/npv`

Request:
```json
{
  "cash_flows": [100000, 120000, 140000, 160000, 180000],
  "discount_rate": 0.10,
  "initial_investment": 500000
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "npv": 68618.17,
    "profitable": true,
    "parameters": {
      "years": 5,
      "discount_rate": 0.10,
      "initial_investment": 500000
    }
  }
}
```

#### Calculate IRR
Calculate Internal Rate of Return.

**POST** `/api/financial/irr`

Request:
```json
{
  "cash_flows": [150000, 150000, 150000, 150000],
  "initial_investment": 400000
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "irr": 0.1896,
    "irr_percentage": 18.96,
    "parameters": {
      "years": 4,
      "initial_investment": 400000
    }
  }
}
```

#### Comprehensive ROI Analysis
Perform comprehensive ROI analysis with multiple metrics.

**POST** `/api/financial/comprehensive-roi`

Request:
```json
{
  "initial_investment": 1000000,
  "annual_cash_flows": [300000, 350000, 400000, 450000, 500000],
  "annual_operating_costs": [50000, 55000, 60000, 65000, 70000],
  "risk_level": "Medium",
  "discount_rate": 0.10,
  "num_employees": 100,
  "avg_salary": 75000,
  "productivity_gain_pct": 0.20
}
```

Response includes:
- Financial metrics (NPV, IRR, ROI, Payback)
- TCO analysis
- Risk-adjusted returns
- Productivity impact
- Investment recommendation

#### Get Cache Statistics
Monitor calculation cache performance.

**GET** `/api/financial/cache-stats`

Response:
```json
{
  "status": "success",
  "data": {
    "npv": {
      "size": 42,
      "max_size": 500,
      "hit_count": 238,
      "miss_count": 42,
      "hit_rate": 0.85
    },
    "irr": { ... },
    "monte_carlo": { ... }
  }
}
```

### 2. Scenario Analysis

#### Monte Carlo Simulation
Run probabilistic analysis with multiple scenarios.

**POST** `/api/scenario/monte-carlo`

Request:
```json
{
  "base_case": {
    "revenue": 1000000,
    "cost": 600000,
    "growth_rate": 0.10
  },
  "variables": [
    {
      "name": "revenue",
      "base_value": 1000000,
      "min_value": 800000,
      "max_value": 1200000,
      "distribution": "normal",
      "std_dev": 50000
    },
    {
      "name": "cost",
      "base_value": 600000,
      "min_value": 500000,
      "max_value": 700000,
      "distribution": "uniform"
    }
  ],
  "model_type": "simple_roi",
  "iterations": 10000,
  "confidence_levels": [0.05, 0.25, 0.50, 0.75, 0.95]
}
```

Model types:
- `simple_roi`: (revenue - cost) / cost
- `npv`: Multi-year NPV calculation
- `payback`: Payback period calculation

Response includes:
- Mean, std deviation, min/max
- Percentiles (P5, P25, P50, P75, P95)
- 90% confidence interval
- Correlation analysis
- Histogram data

#### Sensitivity Analysis
Analyze how changes in variables affect outcomes.

**POST** `/api/scenario/sensitivity`

Request:
```json
{
  "base_case": {
    "investment": 100000,
    "revenue": 50000,
    "cost": 20000
  },
  "variables": ["investment", "revenue", "cost"],
  "model_type": "roi",
  "variation_pct": 0.20,
  "steps": 5
}
```

Response includes:
- Base result
- Sensitivity ranking
- Elasticity for each variable
- Tornado chart data

### 3. Industry-Specific Analysis

#### Manufacturing ROI
**POST** `/api/industry/manufacturing/roi`

Request:
```json
{
  "investment": 2000000,
  "production_volume": 100000,
  "defect_rate_reduction": 0.30,
  "downtime_reduction": 0.25,
  "labor_productivity_gain": 0.20,
  "energy_efficiency_gain": 0.15,
  "years": 5
}
```

#### Healthcare ROI
**POST** `/api/industry/healthcare/roi`

Request:
```json
{
  "investment": 3000000,
  "patient_volume": 50000,
  "diagnostic_accuracy_gain": 0.20,
  "patient_wait_reduction": 0.30,
  "admin_efficiency_gain": 0.40,
  "readmission_reduction": 0.15,
  "years": 5
}
```

#### Financial Services ROI
**POST** `/api/industry/financial-services/roi`

Request:
```json
{
  "investment": 5000000,
  "transaction_volume": 10000000,
  "fraud_detection_improvement": 0.40,
  "processing_time_reduction": 0.60,
  "compliance_automation": 0.50,
  "customer_experience_gain": 0.30,
  "years": 5
}
```

#### Retail ROI
**POST** `/api/industry/retail/roi`

Request:
```json
{
  "investment": 1000000,
  "annual_revenue": 20000000,
  "personalization_uplift": 0.15,
  "inventory_optimization": 0.20,
  "customer_service_automation": 0.50,
  "supply_chain_efficiency": 0.25,
  "years": 5
}
```

#### Get Industry Benchmarks
**GET** `/api/industry/{industry}/benchmarks`

Industries: `manufacturing`, `healthcare`, `financial_services`, `retail`, `technology`, `energy`, `government`, `education`

Response:
```json
{
  "status": "success",
  "data": {
    "typical_roi_range": [150, 350],
    "implementation_timeline_months": 12,
    "success_probability": 0.75,
    "typical_investment_range": [100000, 5000000],
    "key_success_factors": [...],
    "common_pitfalls": [...],
    "recommended_use_cases": [...]
  }
}
```

#### Optimal Strategy Selection
**POST** `/api/industry/optimal-strategy`

Request:
```json
{
  "industry": "manufacturing",
  "company_size": "Medium",
  "budget": 2000000,
  "timeline_months": 18,
  "strategic_goals": ["cost_reduction", "quality_improvement"]
}
```

### 4. Export Functionality

#### Export Financial Results
Export calculation results in various formats.

**POST** `/api/export/financial`

Request:
```json
{
  "results": {
    "financial_metrics": { ... },
    "tco_analysis": { ... },
    "risk_analysis": { ... }
  },
  "format": "excel"
}
```

Formats: `csv`, `excel`, `pdf`, `json`

Response (for downloads):
- Returns file as streaming response with appropriate headers
- Or base64 encoded content if no filename specified

#### Export Monte Carlo Results
**POST** `/api/export/monte-carlo`

Request:
```json
{
  "results": { ... },
  "format": "pdf",
  "include_histogram": true
}
```

#### Batch Export
Export multiple analyses together.

**POST** `/api/export/batch`

Request:
```json
{
  "results_list": [
    { "analysis_1": { ... } },
    { "analysis_2": { ... } }
  ],
  "format": "excel"
}
```

#### Get Export Formats
**GET** `/api/export/formats`

### 5. Report Generation

#### Generate Report
Generate formatted reports using templates.

**POST** `/api/report/generate`

Request:
```json
{
  "template": "executive_summary",
  "data": {
    "company_name": "Acme Corp",
    "investment_amount": 1000000,
    "financial_metrics": { ... }
  },
  "format": "pdf"
}
```

Templates:
- `executive_summary`: 2-3 page high-level overview
- `detailed_analysis`: 10-15 page comprehensive report
- `industry_comparison`: Multi-industry comparison

Formats: `markdown`, `pdf`, `html`

#### Generate Comprehensive Report
Automatically run all analyses and generate report.

**POST** `/api/report/comprehensive`

Request:
```json
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
```

#### Generate Industry Comparison
Compare AI investments across industries.

**POST** `/api/report/industry_comparison`

Request:
```json
{
  "industries": ["manufacturing", "healthcare", "retail", "financial_services"],
  "investment_amount": 1000000,
  "company_size": "Medium",
  "analysis_years": 5,
  "output_format": "pdf"
}
```

#### Get Report Templates
**GET** `/api/report/templates`

## Error Codes

| Code | Description |
|------|------------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Request validation failed |
| 500 | Internal Server Error |

## Rate Limiting
Currently no rate limiting. In production:
- 100 requests per minute for calculations
- 10 requests per minute for report generation

## Examples

### Python Example (with Authentication)
```python
import requests
import json

# First, login to get access token
auth_response = requests.post("http://localhost:8000/api/auth/login", json={
    "username": "your_username",
    "password": "your_password"
})
tokens = auth_response.json()["data"]

# Calculate NPV with authentication
url = "http://localhost:8000/api/financial/npv"
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
data = {
    "cash_flows": [100000, 120000, 140000],
    "discount_rate": 0.10,
    "initial_investment": 300000
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

if result["status"] == "success":
    npv = result["data"]["npv"]
    print(f"NPV: ${npv:,.2f}")
```

### JavaScript Example
```javascript
// Run Monte Carlo simulation
const url = 'http://localhost:8000/api/scenario/monte-carlo';
const data = {
  base_case: {
    revenue: 1000000,
    cost: 600000
  },
  variables: [
    {
      name: 'revenue',
      base_value: 1000000,
      min_value: 800000,
      max_value: 1200000,
      distribution: 'normal'
    }
  ],
  model_type: 'simple_roi',
  iterations: 10000
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
  console.log('Mean outcome:', result.data.mean);
  console.log('90% CI:', result.data.confidence_interval_90);
});
```

### cURL Example
```bash
# Get industry benchmarks
curl -X GET "http://localhost:8000/api/industry/manufacturing/benchmarks" \
  -H "Accept: application/json"

# Generate executive summary
curl -X POST "http://localhost:8000/api/report/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "executive_summary",
    "data": {
      "company_name": "Acme Corp",
      "investment_amount": 1000000,
      "financial_metrics": {
        "npv": 250000,
        "irr": 0.22
      }
    },
    "format": "pdf"
  }' \
  --output report.pdf
```

## WebSocket Real-Time Updates

The API provides WebSocket support for real-time data streaming and live updates.

**WebSocket URL:** `ws://localhost:8000/ws`

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### Message Types

#### Subscribe to Channel
```json
{
    "type": "subscribe",
    "channel": "market_data"
}
```

Available channels:
- `market_data`: Live market updates
- `calculations`: Calculation progress updates
- `notifications`: System notifications
- `system`: System health and cache statistics

#### Request Calculation
```json
{
    "type": "calculate",
    "calculation_id": "calc_123",
    "calculation_type": "npv",
    "parameters": {
        "cash_flows": [100000, 120000, 140000],
        "discount_rate": 0.10,
        "initial_investment": 300000
    }
}
```

#### Server Messages

**Market Update:**
```json
{
    "type": "market_update",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "discount_rate": 0.095,
        "inflation_rate": 0.024,
        "market_growth": 0.082,
        "tech_index": 102.5,
        "ai_adoption_rate": 0.352
    }
}
```

**Calculation Progress:**
```json
{
    "type": "calculation_update",
    "calculation_id": "calc_123",
    "status": "processing",
    "progress": 50,
    "message": "Processing npv... 50%"
}
```

**Calculation Complete:**
```json
{
    "type": "calculation_complete",
    "calculation_id": "calc_123",
    "status": "completed",
    "result": {
        "npv": 68618.17
    },
    "completed_at": "2024-01-15T10:30:05Z"
}
```

**System Health:**
```json
{
    "type": "system_health",
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "healthy",
    "metrics": {
        "active_connections": 5,
        "cache_hit_rate": 0.85,
        "uptime_seconds": 3600
    }
}
```

### Example: Real-Time Dashboard
See `/examples/realtime_dashboard.html` for a complete example of a real-time monitoring dashboard using WebSocket connections.

## Webhooks (Future)
Planned support for webhooks to notify when:
- Long-running calculations complete
- Scheduled reports are generated
- Significant market changes affect analysis

## SDK Support (Future)
Planned SDK support for:
- Python
- JavaScript/TypeScript
- Java
- C#/.NET

## Support
For API support, please contact:
- Documentation: This document
- Interactive docs: `/api/docs`
- Issues: GitHub repository