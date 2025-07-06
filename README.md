# AI Adoption Dashboard v4.0.0

## 🚀 Enterprise-Grade AI Investment Analysis Platform

A comprehensive, API-driven analytics platform for AI adoption analysis, investment decision-making, and strategic planning with real-time capabilities, advanced customization, and enterprise security features.

## ✨ What's New in v4.0.0

### 🔌 RESTful API
- 60+ endpoints for all dashboard functionality
- JWT-based authentication with role-based access control
- Comprehensive API documentation with interactive docs

### 📊 Real-Time Capabilities
- WebSocket support for live data updates
- Real-time calculation progress tracking
- Live market data integration
- Instant notifications and alerts

### 🎨 Complete Customization
- Custom themes with brand colors
- Flexible dashboard layouts
- Saved views with filters
- Personal preferences and settings

### 📋 Enterprise Features
- Comprehensive audit logging for compliance
- Multi-format data export (Excel, PDF, CSV, JSON)
- Automated report generation
- Performance optimization with intelligent caching

## 🎯 Key Features

### Core Analytics
- **Financial Calculations**: NPV, IRR, ROI, Payback Period, Break-even Analysis
- **Risk Assessment**: Monte Carlo simulations, sensitivity analysis, risk-adjusted returns
- **Industry Models**: Specialized calculations for Manufacturing, Healthcare, Financial Services, Retail
- **Scenario Planning**: What-if analysis, probabilistic modeling, optimization

### API Capabilities
- **Authentication**: JWT tokens, refresh tokens, API keys
- **Calculations**: All financial metrics via REST endpoints
- **Real-time**: WebSocket connections for live updates
- **Export**: Programmatic access to all export formats
- **Customization**: Theme/layout management via API

### Dashboard Features
- **Multi-Persona Views**: Executive, Analyst, Researcher, General
- **Interactive Widgets**: Charts, metrics, tables, calculators
- **Smart Caching**: 100-1000x performance improvement
- **Parallel Processing**: Multi-core Monte Carlo simulations

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (high-performance async)
- **Language**: Python 3.8+
- **Authentication**: JWT with role-based access
- **Real-time**: WebSocket support
- **Database**: File-based with caching layer

### Analytics Engine
- **Financial**: NumPy, SciPy for calculations
- **ML/Stats**: Scikit-learn, Statsmodels
- **Parallel**: Multiprocessing for simulations
- **Caching**: LRU with TTL support

### Frontend
- **Dashboard**: Streamlit (multi-page app)
- **API Docs**: Swagger/ReDoc
- **Real-time UI**: WebSocket client examples

### Export & Reporting
- **Excel**: XlsxWriter with formatting
- **PDF**: ReportLab with templates
- **Templates**: Jinja2 for reports
- **Formats**: CSV, JSON, Markdown, HTML

## 📊 Data Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Dashboard UI  │────▶│   FastAPI App   │────▶│ Business Logic  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   WebSocket     │     │   Calculation   │
                        │     Server      │     │     Engine      │
                        └─────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   Real-time     │     │     Cache       │
                        │     Updates     │     │     Layer       │
                        └─────────────────┘     └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rcasanova25/AI-Adoption-Dashboard.git
   cd AI-Adoption-Dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API server**:
   ```bash
   python -m api.app
   ```
   The API will be available at http://localhost:8000

4. **Start the dashboard** (in a new terminal):
   ```bash
   streamlit run app.py
   ```
   The dashboard will open at http://localhost:8501

## 🔐 Authentication & Security

### Default Credentials
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately in production!

### User Roles
- **Admin**: Full system access
- **Analyst**: Read/write calculations and reports
- **Viewer**: Read-only access
- **API User**: Programmatic access only

### API Authentication

```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "username": "your_username",
    "password": "your_password"
})
tokens = response.json()["data"]

# Use token for API calls
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
npv_response = requests.post(
    "http://localhost:8000/api/financial/npv",
    json={
        "cash_flows": [100000, 120000, 140000],
        "discount_rate": 0.10,
        "initial_investment": 300000
    },
    headers=headers
)
```

## 📈 Using the API

### Interactive Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Example Calculations

#### NPV Calculation
```bash
curl -X POST "http://localhost:8000/api/financial/npv" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cash_flows": [100000, 120000, 140000],
    "discount_rate": 0.10,
    "initial_investment": 300000
  }'
```

#### Monte Carlo Simulation
```python
data = {
    "base_case": {"revenue": 1000000, "cost": 600000},
    "variables": [{
        "name": "revenue",
        "base_value": 1000000,
        "min_value": 800000,
        "max_value": 1200000,
        "distribution": "normal"
    }],
    "model_type": "simple_roi",
    "iterations": 10000
}

response = requests.post(
    "http://localhost:8000/api/scenario/monte-carlo",
    json=data,
    headers=headers
)
```

## 🎨 Customization

### Create Custom Theme
```javascript
const theme = {
    name: "Corporate Brand",
    colors: {
        primary: "#003366",
        secondary: "#0066CC",
        background: "#FFFFFF",
        text_primary: "#212121"
    }
};

fetch('/api/customization/themes/create', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(theme)
});
```

### Save Dashboard View
```python
view_config = {
    "name": "Q4 Analysis",
    "layout_id": "layout-financial",
    "theme_id": "theme-dark",
    "filters": {
        "date_range": "2024-Q4",
        "department": "finance"
    }
}

response = requests.post(
    "http://localhost:8000/api/customization/views/save",
    json=view_config,
    headers=headers
)
```

## 📊 Real-Time Features

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    // Subscribe to channels
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'market_data'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Real-time update:', data);
};
```

### Available Channels
- `market_data`: Live market updates
- `calculations`: Calculation progress
- `notifications`: System notifications
- `system`: Health and performance metrics

## 📋 Audit & Compliance

### Audit Logging
All actions are automatically logged:
- API calls with response times
- Calculations with parameters and results
- Authentication events
- Data exports
- Permission checks

### Search Audit Logs
```python
# Search for failed login attempts
audit_search = {
    "event_type": "authentication",
    "severity": "warning",
    "start_date": "2024-01-01T00:00:00"
}

response = requests.post(
    "http://localhost:8000/api/audit/search",
    json=audit_search,
    headers=admin_headers
)
```

## 📚 Documentation

### Available Documentation
- **[API Documentation](docs/API_DOCUMENTATION.md)**: Complete API reference
- **[Authentication Guide](docs/AUTHENTICATION.md)**: Security and auth details
- **[Customization Guide](docs/CUSTOMIZATION.md)**: Themes and layouts
- **[Real-time Features](docs/REALTIME_FEATURES.md)**: WebSocket usage
- **[Audit Logging](docs/AUDIT_LOGGING.md)**: Compliance and monitoring

### Example Applications
- **[Auth Client](examples/auth_client.py)**: Authentication flow example
- **[WebSocket Client](examples/websocket_client.py)**: Real-time connection
- **[Customization Demo](examples/customization_demo.py)**: Theme/layout creation
- **[Real-time Dashboard](examples/realtime_dashboard.html)**: Live monitoring UI

## 🏗️ Project Structure

```
AI-Adoption-Dashboard/
├── api/                    # FastAPI application
│   ├── app.py             # Main API app
│   ├── auth.py            # Authentication system
│   ├── endpoints.py       # Core API endpoints
│   ├── websocket_server.py # Real-time server
│   └── *.py               # Additional endpoints
├── business/              # Business logic
│   ├── financial_calculations_cached.py
│   ├── scenario_engine_parallel.py
│   ├── roi_analysis.py
│   └── industry_models.py
├── utils/                 # Utilities
│   ├── cache_manager.py   # Caching system
│   ├── audit_logger.py    # Audit logging
│   ├── export_manager.py  # Export functionality
│   └── dashboard_customization.py
├── data/                  # Data management
├── views/                 # Dashboard views
├── components/            # UI components
├── examples/              # Example code
├── docs/                  # Documentation
├── tests/                 # Test suite
└── requirements.txt       # Dependencies
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Categories
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Performance tests
pytest tests/performance/

# API tests
pytest tests/api/
```

### Code Quality
```bash
# Format code
black .

# Check code style
flake8 .

# Type checking
mypy .

# Security scan
bandit -r .
```

## 🚀 Deployment

### Using Docker
```bash
# Build image
docker build -t ai-dashboard .

# Run container
docker run -p 8000:8000 -p 8501:8501 ai-dashboard
```

### Environment Variables
```bash
# Security
JWT_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Performance
CACHE_MAX_SIZE=1000
PARALLEL_WORKERS=4

# Logging
AUDIT_LOG_DIR=/var/log/ai-dashboard
LOG_LEVEL=INFO
```

### Production Checklist
- [ ] Change default admin password
- [ ] Set secure JWT secret key
- [ ] Configure HTTPS/TLS
- [ ] Set up database backups
- [ ] Configure monitoring
- [ ] Set up log rotation
- [ ] Configure firewall rules
- [ ] Set up rate limiting

## 📈 Performance

### Optimization Features
- **Smart Caching**: LRU cache with TTL for calculations
- **Parallel Processing**: Multi-core Monte Carlo simulations
- **Connection Pooling**: Efficient resource management
- **Lazy Loading**: On-demand data loading
- **Memory Management**: Automatic cleanup and limits

### Benchmarks
- NPV Calculation: <10ms (cached), <50ms (uncached)
- Monte Carlo (10k iterations): <2s with parallel processing
- API Response Time: <100ms average
- WebSocket Latency: <50ms
- Cache Hit Rate: >85% typical

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Add docstrings to functions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Robert Casanova** - *Lead Developer*
- GitHub: [@Rcasanova25](https://github.com/Rcasanova25)

## 🙏 Acknowledgments

- Stanford AI Index team for comprehensive data
- McKinsey Global Institute for business insights
- FastAPI team for the excellent framework
- Streamlit team for the dashboard platform
- All contributors and beta testers

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Python**: 3.8+
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)

### Recommended Requirements
- **RAM**: 8GB+ for large simulations
- **CPU**: Multi-core for parallel processing
- **Storage**: SSD for better performance
- **Network**: Stable connection for real-time features

---

**Version**: 4.0.0 "API Evolution"  
**Release Date**: January 2025  
**Status**: Production Ready  
**API Version**: 1.1.0  
**Quality Score**: Enterprise Grade