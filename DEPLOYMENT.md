# AI Adoption Dashboard - Production Deployment Guide

## 📋 Overview

This comprehensive guide covers production deployment of the AI Adoption Dashboard, a multi-persona Streamlit application providing strategic AI adoption analytics. The dashboard supports executive decision-making, policy analysis, and research insights across various industries and geographies.

## 🎯 Application Architecture

### Core Components
- **Frontend**: Streamlit web application with advanced UI components
- **Backend**: Python-based data processing with performance optimization
- **Data Layer**: 28+ comprehensive datasets with validation
- **Caching**: Multi-layer caching system for high performance
- **Analytics**: Business intelligence for ROI, competitive analysis, and market trends

### Technical Stack
- **Runtime**: Python 3.8+ with Streamlit framework
- **Visualization**: Plotly for interactive charts and dashboards  
- **Data Processing**: Pandas, NumPy with optimized DataFrame operations
- **Performance**: Advanced caching, memory management, async loading
- **Security**: Input validation, dependency scanning, secure deployment

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended for Quick Start)
See [STREAMLIT_CLOUD_SETUP.md](./STREAMLIT_CLOUD_SETUP.md) for detailed instructions.

### 2. Docker Container Deployment
Using the included multi-stage Dockerfile for production environments.

### 3. Azure Web Apps
Enterprise deployment using Azure DevOps pipelines and container registry.

### 4. Local Development
For development and testing environments.

## 🔧 Prerequisites

### System Requirements
- **CPU**: 2+ cores recommended (4+ for production)
- **RAM**: 4GB minimum, 8GB recommended for production
- **Storage**: 2GB available space
- **Network**: Stable internet connection for data loading

### Software Dependencies
- Python 3.8, 3.9, or 3.10
- pip package manager
- Git version control
- Docker (for containerized deployment)
- Azure CLI (for Azure deployment)

### Environment Variables
```bash
# Application Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Performance Configuration
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
STREAMLIT_SERVER_RUN_ON_SAVE=false

# Security Configuration
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false

# Environment Specific
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

## 📦 Container Deployment

### Building the Docker Image

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Adoption-Dashboard.git
cd AI-Adoption-Dashboard

# Build production image
docker build -t ai-adoption-dashboard:latest \
  --target production \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VERSION=2.2.1 \
  .

# Build development image (optional)
docker build -t ai-adoption-dashboard:dev \
  --target development \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VERSION=2.2.1 \
  .
```

### Running the Container

```bash
# Production deployment
docker run -d \
  --name ai-dashboard-prod \
  -p 8501:8501 \
  -p 8502:8502 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=WARNING \
  --restart unless-stopped \
  --memory="2g" \
  --cpus="1.0" \
  ai-adoption-dashboard:latest

# Development deployment
docker run -d \
  --name ai-dashboard-dev \
  -p 8501:8501 \
  -v $(pwd):/app \
  -e ENVIRONMENT=development \
  -e LOG_LEVEL=DEBUG \
  -e RUN_TESTS=true \
  ai-adoption-dashboard:dev
```

### Health Checks

The container includes built-in health monitoring:

```bash
# Check container health
docker ps
docker logs ai-dashboard-prod

# Access health endpoint
curl http://localhost:8502/
curl http://localhost:8501/
```

## ☁️ Azure Web App Deployment

### Using Azure DevOps Pipelines

The repository includes a comprehensive Azure DevOps pipeline (`azure-pipelines.yml`) that provides:

1. **Continuous Integration**
   - Multi-Python version testing (3.8, 3.9, 3.10)
   - Security scanning (Bandit, Safety, Trivy)
   - Code quality checks (Black, isort, flake8)
   - Performance regression testing
   - Docker image building and registry push

2. **Staging Deployment**
   - Infrastructure as Code (Bicep templates)
   - Container deployment to staging environment
   - Health checks and monitoring setup

3. **Production Deployment**
   - Blue-green deployment strategy
   - Staging slot validation
   - Automatic rollback on failure
   - Production health monitoring

### Manual Azure Deployment

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name rg-ai-dashboard-prod \
  --location "East US"

# Create App Service Plan
az appservice plan create \
  --name plan-ai-dashboard \
  --resource-group rg-ai-dashboard-prod \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name ai-adoption-dashboard \
  --resource-group rg-ai-dashboard-prod \
  --plan plan-ai-dashboard \
  --deployment-container-image-name ai-adoption-dashboard:latest

# Configure app settings
az webapp config appsettings set \
  --name ai-adoption-dashboard \
  --resource-group rg-ai-dashboard-prod \
  --settings \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
    WEBSITES_PORT=8501 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    ENVIRONMENT=production
```

## 🔍 Verification and Testing

### Post-Deployment Validation

1. **Application Health Check**
```bash
# Check main application
curl -f https://your-app-url.azurewebsites.net/

# Check health endpoint (if configured)
curl -f https://your-app-url.azurewebsites.net/health

# Verify application loads
curl -I https://your-app-url.azurewebsites.net/
```

2. **Performance Validation**
```bash
# Load testing with Apache Bench
ab -n 100 -c 10 https://your-app-url.azurewebsites.net/

# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-app-url.azurewebsites.net/
```

3. **Functional Testing**
```bash
# Run test suite against deployed application
python scripts/test_runner.py --type integration --url https://your-app-url.azurewebsites.net/

# Check data loading and visualization
python -c "
import requests
response = requests.get('https://your-app-url.azurewebsites.net/')
print('Status:', response.status_code)
print('Content-Type:', response.headers.get('content-type'))
"
```

### Performance Monitoring

The application includes built-in performance monitoring:

1. **Memory Management Dashboard** - Real-time memory usage tracking
2. **Performance Metrics** - Function execution times and optimization recommendations
3. **Cache Hit Rates** - Multi-layer caching effectiveness monitoring
4. **Data Loading Performance** - Async loading and processing benchmarks

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Application Won't Start**
```bash
# Check logs
docker logs ai-dashboard-prod

# Common issues:
# - Missing environment variables
# - Port conflicts
# - Memory constraints
# - Python dependency issues

# Solutions:
docker run --rm -it ai-adoption-dashboard:latest bash
python -c "import streamlit; print('Streamlit OK')"
python -c "import app; print('App imports OK')"
```

2. **Performance Issues**
```bash
# Check resource usage
docker stats ai-dashboard-prod

# Monitor memory usage
docker exec ai-dashboard-prod python -c "
from performance import MemoryMonitor
monitor = MemoryMonitor()
print(f'Memory usage: {monitor.get_memory_usage():.1f}MB')
"

# Check cache performance
docker exec ai-dashboard-prod python -c "
from performance import _global_cache
print(f'Cache stats: {_global_cache.get_stats()}')
"
```

3. **Data Loading Failures**
```bash
# Run diagnostic script
docker exec ai-dashboard-prod python diagnose_data_loading.py

# Check external dependencies
docker exec ai-dashboard-prod python -c "
import requests
try:
    response = requests.get('https://api.example.com/health', timeout=10)
    print('External API:', response.status_code)
except Exception as e:
    print('External API error:', e)
"
```

4. **Security and Access Issues**
```bash
# Check CORS settings
curl -H "Origin: https://example.com" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://your-app-url.azurewebsites.net/

# Verify SSL/TLS
openssl s_client -connect your-app-url.azurewebsites.net:443 -servername your-app-url.azurewebsites.net
```

### Error Diagnosis

1. **Application Errors**
```bash
# Enable debug mode temporarily
docker run -e STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true \
           -e LOG_LEVEL=DEBUG \
           ai-adoption-dashboard:latest

# Check error logs
docker logs ai-dashboard-prod --tail 100 -f
```

2. **Performance Degradation**
```bash
# Run performance regression check
docker exec ai-dashboard-prod python scripts/performance_regression_check.py

# Monitor resource usage
docker exec ai-dashboard-prod python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage(\"/\").percent}%')
"
```

## 🔒 Security Considerations

### Container Security
- Non-root user execution
- Minimal base image (Python slim)
- Security scanning with Trivy
- Dependency vulnerability checks
- Read-only file system where possible

### Application Security
- Input validation with Pydantic models
- CSRF protection enabled
- Secure headers configuration
- Environment variable management
- Secrets management for production

### Network Security
- HTTPS enforcement
- CORS configuration
- Rate limiting (application level)
- Access logging and monitoring

## 📊 Monitoring and Maintenance

### Application Monitoring
1. **Health Endpoints**: Built-in health checks on port 8502
2. **Performance Metrics**: Real-time performance dashboard
3. **Error Tracking**: Comprehensive error logging and reporting
4. **Resource Monitoring**: Memory, CPU, and cache utilization

### Maintenance Tasks
1. **Regular Updates**: Dependencies and security patches
2. **Cache Management**: Periodic cache cleanup and optimization
3. **Log Rotation**: Prevent log file growth
4. **Performance Tuning**: Monitor and optimize based on usage patterns

### Scaling Considerations
1. **Horizontal Scaling**: Multiple container instances behind load balancer
2. **Vertical Scaling**: Increase container resources (CPU/memory)
3. **Database Optimization**: External database for large datasets
4. **CDN Integration**: Static asset caching and delivery

## 📞 Support and Documentation

### Getting Help
- **GitHub Issues**: [Repository Issues](https://github.com/yourusername/AI-Adoption-Dashboard/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/AI-Adoption-Dashboard/wiki)
- **Community**: [GitHub Discussions](https://github.com/yourusername/AI-Adoption-Dashboard/discussions)

### Additional Resources
- [STREAMLIT_CLOUD_SETUP.md](./STREAMLIT_CLOUD_SETUP.md) - Streamlit Cloud deployment
- [VERSION_HISTORY.md](./VERSION_HISTORY.md) - Release notes and changelog
- [PRODUCTION_CHECKLIST.md](./PRODUCTION_CHECKLIST.md) - Pre-deployment checklist
- [README.md](./README.md) - Development setup and features

---

**Document Version**: 1.0  
**Last Updated**: July 2025  
**Compatible with**: AI Adoption Dashboard v2.2.1+

For the most up-to-date deployment information, please refer to the [GitHub repository](https://github.com/yourusername/AI-Adoption-Dashboard) and official documentation.