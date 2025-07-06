# Audit Logging Documentation

## Overview

The AI Adoption Dashboard includes comprehensive audit logging to track all system activities, calculations, API calls, and security events. This provides compliance, debugging capabilities, and security monitoring.

## Features

### 1. Automatic Logging
- All API calls are automatically logged
- Calculation requests and results are tracked
- User authentication events are recorded
- Permission checks are audited
- Data exports are monitored

### 2. Event Types
- **CALCULATION**: Financial calculations (NPV, IRR, ROI, etc.)
- **API_CALL**: All API endpoint invocations
- **USER_ACTION**: User-initiated actions
- **AUTHENTICATION**: Login attempts, token refreshes
- **DATA_EXPORT**: Export operations
- **REPORT_GENERATION**: Report creation
- **PERMISSION_CHECK**: Access control checks
- **ERROR**: System errors and exceptions
- **SYSTEM**: System-level events

### 3. Severity Levels
- **INFO**: Normal operations
- **WARNING**: Notable events (failed logins, permission denials)
- **ERROR**: Errors and exceptions
- **CRITICAL**: Critical system issues

## Architecture

### Storage
- **In-Memory Buffer**: Recent 1000 entries for fast access
- **File Storage**: JSON logs with automatic rotation
- **Log Rotation**: Files rotate at 100MB

### Performance
- Asynchronous logging to minimize impact
- Efficient search with indexing
- Configurable retention policies

## API Endpoints

### Search Audit Logs
`POST /api/audit/search`

Search logs with filters:
```json
{
    "event_type": "calculation",
    "user": "analyst1",
    "severity": "error",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59",
    "limit": 100
}
```

### Get Statistics
`GET /api/audit/stats`

Returns summary statistics:
- Total entries by type
- Entries by severity
- User activity summary

### Recent Activity
`GET /api/audit/recent`

Get activity from last 24 hours grouped by event type.

### User Activity
`GET /api/audit/user-activity/{username}`

Get specific user's activity:
- Total actions
- Actions by type
- Recent actions

### Export Logs
`POST /api/audit/export`

Export logs in JSON or CSV format:
```json
{
    "format": "csv",
    "filters": {
        "event_type": "calculation",
        "start_date": "2024-01-01T00:00:00"
    }
}
```

### Calculation History
`GET /api/audit/calculation-history`

Performance metrics for calculations:
- Average duration by type
- Cache hit rates
- Recent calculations

### Security Events
`GET /api/audit/security-events`

Monitor security-related events:
- Failed login attempts
- Permission denials
- Suspicious patterns

## Logged Information

### Calculation Logs
```json
{
    "event_type": "calculation",
    "action": "calculate_npv",
    "user": "analyst1",
    "details": {
        "calculation_type": "npv",
        "parameters": {
            "cash_flows_count": 5,
            "discount_rate": 0.1,
            "initial_investment": 1000000
        },
        "result_summary": {
            "npv": 250000,
            "profitable": true
        },
        "duration_ms": 45.2,
        "cache_hit": false
    }
}
```

### API Call Logs
```json
{
    "event_type": "api_call",
    "action": "POST /api/financial/npv",
    "user": "analyst1",
    "details": {
        "endpoint": "/api/financial/npv",
        "method": "POST",
        "status_code": 200,
        "duration_ms": 52.3,
        "ip_address": "192.168.1.100"
    }
}
```

### Authentication Logs
```json
{
    "event_type": "authentication",
    "action": "login",
    "user": "admin",
    "details": {
        "action": "login",
        "success": true,
        "ip_address": "192.168.1.100",
        "method": "password"
    }
}
```

## Security Features

### Sensitive Data Protection
- Passwords and tokens are never logged
- Sensitive parameters are hashed
- PII is redacted automatically

### Access Control
- Admin-only access to full logs
- Users can view their own activity
- Role-based filtering

### Compliance
- Immutable audit trail
- Timestamped entries
- Correlation IDs for tracking

## Usage Examples

### Python Client
```python
import requests

# Search for failed calculations
response = requests.post(
    "http://localhost:8000/api/audit/search",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "event_type": "calculation",
        "severity": "error",
        "limit": 50
    }
)

# Get user activity
response = requests.get(
    "http://localhost:8000/api/audit/user-activity/analyst1",
    headers={"Authorization": f"Bearer {token}"}
)
```

### Monitoring Dashboard
```javascript
// Real-time security monitoring
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'audit_event') {
        updateSecurityDashboard(data);
    }
};
```

## Best Practices

### 1. Regular Review
- Monitor failed logins daily
- Review permission denials
- Check error patterns

### 2. Export and Archive
- Export logs monthly
- Archive to secure storage
- Maintain compliance records

### 3. Performance Monitoring
- Track calculation times
- Monitor cache effectiveness
- Identify bottlenecks

### 4. Security Monitoring
- Set alerts for multiple failed logins
- Monitor unusual access patterns
- Track privileged operations

## Configuration

### Environment Variables
```bash
# Audit log directory
AUDIT_LOG_DIR=/var/log/ai-dashboard/audit

# Maximum log file size (MB)
AUDIT_LOG_MAX_SIZE=100

# In-memory buffer size
AUDIT_BUFFER_SIZE=1000

# Retention days
AUDIT_RETENTION_DAYS=90
```

### Log Rotation
Logs automatically rotate when reaching size limit:
- Current: `audit_2024-01-15.log`
- Rotated: `audit_2024-01-15_143022.log`

## Troubleshooting

### Missing Logs
- Check file permissions
- Verify log directory exists
- Check disk space

### Performance Impact
- Reduce buffer size if memory constrained
- Implement async logging
- Use batch exports

### Search Performance
- Use specific date ranges
- Limit result count
- Index frequently searched fields

## Compliance Requirements

### GDPR
- User activity export available
- Right to erasure support
- Data minimization

### SOC 2
- Immutable audit trail
- Access logging
- Change tracking

### HIPAA
- PHI redaction
- Access controls
- Encryption at rest

## Future Enhancements

1. **Real-time Alerts**
   - Webhook notifications
   - Email alerts
   - SMS for critical events

2. **Advanced Analytics**
   - Anomaly detection
   - Pattern recognition
   - Predictive alerts

3. **Integration**
   - SIEM integration
   - Splunk forwarder
   - ELK stack support

4. **Visualization**
   - Audit dashboard
   - Real-time graphs
   - Heat maps