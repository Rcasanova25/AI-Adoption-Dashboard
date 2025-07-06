# Real-Time Data Integration Features

## Overview

The AI Adoption Dashboard now includes comprehensive real-time data integration capabilities through WebSocket connections. This enables live market data feeds, real-time calculation updates, and instant notifications.

## Key Features

### 1. WebSocket Server
- **Endpoint**: `ws://localhost:8000/ws`
- **Channels**: Multiple subscription channels for different data types
- **Bi-directional**: Send requests and receive updates in real-time

### 2. Live Market Data
- Simulated market data updates every 10 seconds
- Includes:
  - Discount rates
  - Inflation rates
  - Market growth indices
  - Technology sector performance
  - AI adoption rates

### 3. Real-Time Calculations
- Progress updates during long-running calculations
- Live status notifications
- Automatic result delivery upon completion
- Error handling with immediate feedback

### 4. System Monitoring
- Cache performance statistics
- Active connection count
- System health metrics
- Real-time notifications

## Getting Started

### 1. Start the API Server
```bash
python -m api.app
```

The server will automatically:
- Initialize WebSocket endpoints
- Start background tasks for market data
- Begin system monitoring

### 2. Connect via WebSocket

#### Python Client Example
```python
import asyncio
import websockets
import json

async def connect():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Subscribe to market data
        await websocket.send(json.dumps({
            "type": "subscribe",
            "channel": "market_data"
        }))
        
        # Listen for updates
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(connect())
```

#### JavaScript Client Example
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
    console.log('Update:', data);
};
```

### 3. Use the Real-Time Dashboard
Open `examples/realtime_dashboard.html` in a web browser to see a full-featured monitoring dashboard.

## Available Channels

### market_data
Real-time market updates including:
- Economic indicators
- Technology sector indices
- AI adoption metrics

### calculations
Track calculation progress:
- Status updates (started, processing, completed)
- Progress percentage
- Results delivery

### notifications
System-wide notifications:
- Important events
- Warnings and alerts
- Success confirmations

### system
System health and performance:
- Cache statistics
- Connection metrics
- Overall system status

## Message Types

### Client to Server

#### Subscribe
```json
{
    "type": "subscribe",
    "channel": "market_data"
}
```

#### Request Calculation
```json
{
    "type": "calculate",
    "calculation_id": "unique_id",
    "calculation_type": "npv",
    "parameters": {
        "cash_flows": [100000, 120000, 140000],
        "discount_rate": 0.10,
        "initial_investment": 300000
    }
}
```

#### Ping
```json
{
    "type": "ping"
}
```

### Server to Client

#### Market Update
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

#### Calculation Progress
```json
{
    "type": "calculation_update",
    "calculation_id": "calc_123",
    "status": "processing",
    "progress": 75,
    "message": "Processing npv... 75%"
}
```

#### Notification
```json
{
    "type": "notification",
    "notification_type": "info",
    "level": "info",
    "message": "System update completed",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Use Cases

### 1. Live Financial Monitoring
Monitor real-time changes in financial metrics:
- Track NPV as market rates change
- Update ROI calculations with live data
- Adjust risk assessments dynamically

### 2. Interactive Dashboards
Build responsive user interfaces:
- Real-time chart updates
- Live calculation results
- Instant error feedback

### 3. Automated Alerts
Set up notifications for:
- Calculation completions
- Threshold breaches
- System events

### 4. Performance Monitoring
Track system performance:
- Cache hit rates
- Calculation times
- Active user counts

## Advanced Features

### Connection Management
The `ConnectionManager` class handles:
- Multiple client connections
- Channel subscriptions
- Message broadcasting
- Automatic cleanup

### Market Data Simulation
The `MarketDataSimulator` provides:
- Realistic market fluctuations
- Configurable update intervals
- Multiple data points

### Calculation Service
The `CalculationUpdateService` offers:
- Asynchronous calculation execution
- Progress tracking
- Result caching integration

### Notification System
The `NotificationService` enables:
- Multi-level notifications
- Channel-based broadcasting
- System-wide alerts

## Best Practices

1. **Connection Handling**
   - Implement reconnection logic
   - Handle connection errors gracefully
   - Clean up subscriptions on disconnect

2. **Message Processing**
   - Validate incoming messages
   - Handle unknown message types
   - Log errors appropriately

3. **Performance**
   - Limit subscription channels to needed data
   - Implement client-side throttling if needed
   - Cache results when appropriate

4. **Security** (Future Enhancement)
   - Implement authentication tokens
   - Use WSS (WebSocket Secure) in production
   - Validate all client inputs

## Troubleshooting

### Connection Issues
- Ensure the API server is running
- Check firewall settings
- Verify WebSocket URL

### No Updates Received
- Confirm channel subscription
- Check message format
- Review server logs

### Performance Problems
- Monitor active connections
- Check system resources
- Review calculation complexity

## Future Enhancements

1. **Authentication & Authorization**
   - JWT token support
   - Role-based access control
   - Secure WebSocket connections

2. **Data Persistence**
   - Store historical market data
   - Cache calculation results
   - Replay capabilities

3. **Advanced Analytics**
   - Real-time trend analysis
   - Predictive calculations
   - Alert thresholds

4. **Scalability**
   - Redis pub/sub integration
   - Horizontal scaling support
   - Load balancing

## Example Applications

See the `examples` directory for:
- `websocket_client.py`: Python WebSocket client
- `realtime_dashboard.html`: Interactive web dashboard

These examples demonstrate best practices for implementing real-time features in your applications.