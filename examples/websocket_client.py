"""Example WebSocket client for real-time data integration.

This script demonstrates how to connect to the WebSocket server
and receive real-time updates.
"""

import asyncio
import json
import logging
from datetime import datetime
import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketClient:
    """WebSocket client for real-time data."""
    
    def __init__(self, url: str = "ws://localhost:8000/ws"):
        """Initialize WebSocket client."""
        self.url = url
        self.websocket = None
        
    async def connect(self):
        """Connect to WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.url)
            logger.info(f"Connected to {self.url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
            
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected")
            
    async def subscribe(self, channel: str):
        """Subscribe to a channel."""
        message = {
            "type": "subscribe",
            "channel": channel
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Subscribed to channel: {channel}")
        
    async def unsubscribe(self, channel: str):
        """Unsubscribe from a channel."""
        message = {
            "type": "unsubscribe",
            "channel": channel
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Unsubscribed from channel: {channel}")
        
    async def request_calculation(self, calculation_type: str, parameters: dict):
        """Request a real-time calculation."""
        message = {
            "type": "calculate",
            "calculation_id": f"calc_{datetime.now().timestamp()}",
            "calculation_type": calculation_type,
            "parameters": parameters
        }
        await self.websocket.send(json.dumps(message))
        logger.info(f"Requested {calculation_type} calculation")
        
    async def listen(self):
        """Listen for messages from server."""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
        except Exception as e:
            logger.error(f"Error in listener: {e}")
            
    async def handle_message(self, data: dict):
        """Handle incoming messages."""
        msg_type = data.get("type")
        
        if msg_type == "market_update":
            logger.info(f"Market Update: {data['data']}")
            
        elif msg_type == "calculation_update":
            logger.info(f"Calculation Progress: {data['progress']}% - {data['message']}")
            
        elif msg_type == "calculation_complete":
            logger.info(f"Calculation Complete: {data['result']}")
            
        elif msg_type == "notification":
            logger.info(f"Notification [{data['level']}]: {data['message']}")
            
        elif msg_type == "cache_update":
            logger.info(f"Cache Stats: {data['stats']}")
            
        elif msg_type == "system_health":
            logger.info(f"System Health: {data['metrics']}")
            
        else:
            logger.info(f"Received: {data}")
            
    async def run_example(self):
        """Run example client interactions."""
        if not await self.connect():
            return
            
        try:
            # Subscribe to channels
            await self.subscribe("market_data")
            await self.subscribe("calculations")
            await self.subscribe("notifications")
            await self.subscribe("system")
            
            # Request some calculations
            await self.request_calculation("npv", {
                "cash_flows": [100000, 120000, 140000, 160000, 180000],
                "discount_rate": 0.10,
                "initial_investment": 500000
            })
            
            await asyncio.sleep(2)
            
            await self.request_calculation("comprehensive_roi", {
                "initial_investment": 1000000,
                "annual_cash_flows": [300000, 350000, 400000, 450000, 500000],
                "annual_operating_costs": [50000, 55000, 60000, 65000, 70000],
                "risk_level": "Medium",
                "discount_rate": 0.10
            })
            
            # Listen for messages
            await self.listen()
            
        finally:
            await self.disconnect()


async def main():
    """Main function."""
    client = WebSocketClient()
    
    # Run the example
    await client.run_example()


if __name__ == "__main__":
    asyncio.run(main())