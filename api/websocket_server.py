"""WebSocket server for real-time data integration.

This module provides WebSocket endpoints for real-time updates,
live market data feeds, and calculation updates.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional, Any, List
from collections import defaultdict
import random

from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from fastapi.websockets import WebSocketState

from business.financial_calculations import (
    calculate_npv,
    calculate_irr
)
from business.roi_analysis import compute_comprehensive_roi

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and message broadcasting."""
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self.client_subscriptions: Dict[WebSocket, Set[str]] = defaultdict(set)
        
    async def connect(self, websocket: WebSocket, channel: str = "general"):
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        self.active_connections[channel].add(websocket)
        self.client_subscriptions[websocket].add(channel)
        logger.info(f"Client connected to channel: {channel}")
        
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        # Remove from all channels
        for channel in list(self.client_subscriptions[websocket]):
            self.active_connections[channel].discard(websocket)
        del self.client_subscriptions[websocket]
        logger.info("Client disconnected")
        
    async def subscribe(self, websocket: WebSocket, channel: str):
        """Subscribe a client to a channel."""
        self.active_connections[channel].add(websocket)
        self.client_subscriptions[websocket].add(channel)
        await self.send_personal_message(
            {"type": "subscribed", "channel": channel},
            websocket
        )
        
    async def unsubscribe(self, websocket: WebSocket, channel: str):
        """Unsubscribe a client from a channel."""
        self.active_connections[channel].discard(websocket)
        self.client_subscriptions[websocket].discard(channel)
        await self.send_personal_message(
            {"type": "unsubscribed", "channel": channel},
            websocket
        )
        
    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        """Send a message to a specific client."""
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(message)
            
    async def broadcast_to_channel(self, message: Dict, channel: str):
        """Broadcast a message to all clients in a channel."""
        disconnected = []
        for connection in self.active_connections[channel]:
            try:
                if connection.client_state == WebSocketState.CONNECTED:
                    await connection.send_json(message)
                else:
                    disconnected.append(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
                
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
            
    async def broadcast_to_all(self, message: Dict):
        """Broadcast a message to all connected clients."""
        for channel in self.active_connections:
            await self.broadcast_to_channel(message, channel)


class MarketDataSimulator:
    """Simulates market data for demonstration purposes."""
    
    def __init__(self):
        """Initialize market data simulator."""
        self.base_rates = {
            "discount_rate": 0.10,
            "inflation_rate": 0.025,
            "market_growth": 0.08,
            "tech_index": 100.0,
            "ai_adoption_rate": 0.35
        }
        self.running = False
        
    def generate_market_update(self) -> Dict[str, Any]:
        """Generate simulated market data update."""
        # Add some random variation
        return {
            "timestamp": datetime.now().isoformat(),
            "type": "market_update",
            "data": {
                "discount_rate": self.base_rates["discount_rate"] + random.uniform(-0.005, 0.005),
                "inflation_rate": self.base_rates["inflation_rate"] + random.uniform(-0.002, 0.002),
                "market_growth": self.base_rates["market_growth"] + random.uniform(-0.01, 0.01),
                "tech_index": self.base_rates["tech_index"] * (1 + random.uniform(-0.02, 0.02)),
                "ai_adoption_rate": min(0.8, self.base_rates["ai_adoption_rate"] + random.uniform(0, 0.001))
            }
        }
        
    async def start_streaming(self, manager: ConnectionManager, interval: int = 5):
        """Start streaming market data."""
        self.running = True
        while self.running:
            try:
                update = self.generate_market_update()
                await manager.broadcast_to_channel(update, "market_data")
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Error in market data stream: {e}")
                
    def stop_streaming(self):
        """Stop streaming market data."""
        self.running = False


class CalculationUpdateService:
    """Service for real-time calculation updates."""
    
    def __init__(self, manager: ConnectionManager):
        """Initialize calculation update service."""
        self.manager = manager
        self.active_calculations: Dict[str, Dict] = {}
        
    async def start_calculation(
        self,
        calculation_id: str,
        calculation_type: str,
        parameters: Dict[str, Any],
        websocket: Optional[WebSocket] = None
    ):
        """Start a calculation and provide real-time updates."""
        self.active_calculations[calculation_id] = {
            "type": calculation_type,
            "status": "started",
            "progress": 0,
            "parameters": parameters,
            "started_at": datetime.now().isoformat()
        }
        
        # Send initial status
        update = {
            "type": "calculation_update",
            "calculation_id": calculation_id,
            "status": "started",
            "progress": 0,
            "message": f"Starting {calculation_type} calculation..."
        }
        
        if websocket:
            await self.manager.send_personal_message(update, websocket)
        else:
            await self.manager.broadcast_to_channel(update, "calculations")
            
        # Simulate calculation progress
        try:
            result = await self._perform_calculation(
                calculation_id,
                calculation_type,
                parameters,
                websocket
            )
            
            # Send completion update
            update = {
                "type": "calculation_complete",
                "calculation_id": calculation_id,
                "status": "completed",
                "result": result,
                "completed_at": datetime.now().isoformat()
            }
            
            if websocket:
                await self.manager.send_personal_message(update, websocket)
            else:
                await self.manager.broadcast_to_channel(update, "calculations")
                
        except Exception as e:
            # Send error update
            update = {
                "type": "calculation_error",
                "calculation_id": calculation_id,
                "status": "error",
                "error": str(e)
            }
            
            if websocket:
                await self.manager.send_personal_message(update, websocket)
            else:
                await self.manager.broadcast_to_channel(update, "calculations")
                
        finally:
            del self.active_calculations[calculation_id]
            
    async def _perform_calculation(
        self,
        calculation_id: str,
        calculation_type: str,
        parameters: Dict[str, Any],
        websocket: Optional[WebSocket] = None
    ) -> Dict[str, Any]:
        """Perform the actual calculation with progress updates."""
        
        # Send progress updates
        for progress in [25, 50, 75]:
            await asyncio.sleep(0.5)  # Simulate work
            update = {
                "type": "calculation_update",
                "calculation_id": calculation_id,
                "status": "processing",
                "progress": progress,
                "message": f"Processing {calculation_type}... {progress}%"
            }
            
            if websocket:
                await self.manager.send_personal_message(update, websocket)
            else:
                await self.manager.broadcast_to_channel(update, "calculations")
                
        # Perform actual calculation
        if calculation_type == "npv":
            result = calculate_npv(
                cash_flows=parameters.get("cash_flows", []),
                discount_rate=parameters.get("discount_rate", 0.1),
                initial_investment=parameters.get("initial_investment", 0)
            )
            return {"npv": result}
            
        elif calculation_type == "irr":
            result = calculate_irr(
                cash_flows=parameters.get("cash_flows", []),
                initial_investment=parameters.get("initial_investment", 0)
            )
            return {"irr": result}
            
        elif calculation_type == "comprehensive_roi":
            result = compute_comprehensive_roi(
                initial_investment=parameters.get("initial_investment", 0),
                annual_cash_flows=parameters.get("annual_cash_flows", []),
                annual_operating_costs=parameters.get("annual_operating_costs", []),
                risk_level=parameters.get("risk_level", "Medium"),
                discount_rate=parameters.get("discount_rate", 0.1)
            )
            return result
            
        else:
            raise ValueError(f"Unknown calculation type: {calculation_type}")
            
    def get_active_calculations(self) -> List[Dict]:
        """Get list of active calculations."""
        return [
            {
                "calculation_id": calc_id,
                **calc_data
            }
            for calc_id, calc_data in self.active_calculations.items()
        ]


class NotificationService:
    """Service for sending real-time notifications."""
    
    def __init__(self, manager: ConnectionManager):
        """Initialize notification service."""
        self.manager = manager
        
    async def send_notification(
        self,
        notification_type: str,
        message: str,
        level: str = "info",
        data: Optional[Dict] = None,
        channel: str = "notifications"
    ):
        """Send a notification to clients."""
        notification = {
            "type": "notification",
            "notification_type": notification_type,
            "level": level,  # info, warning, error, success
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        await self.manager.broadcast_to_channel(notification, channel)
        
    async def send_cache_update(self):
        """Send cache statistics update."""
        


# Global instances
connection_manager = ConnectionManager()
market_simulator = MarketDataSimulator()
calculation_service = CalculationUpdateService(connection_manager)
notification_service = NotificationService(connection_manager)


async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint handler."""
    await connection_manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "subscribe":
                channel = data.get("channel", "general")
                await connection_manager.subscribe(websocket, channel)
                
            elif message_type == "unsubscribe":
                channel = data.get("channel", "general")
                await connection_manager.unsubscribe(websocket, channel)
                
            elif message_type == "calculate":
                # Start a calculation with real-time updates
                calculation_id = data.get("calculation_id", str(datetime.now().timestamp()))
                calculation_type = data.get("calculation_type")
                parameters = data.get("parameters", {})
                
                asyncio.create_task(
                    calculation_service.start_calculation(
                        calculation_id,
                        calculation_type,
                        parameters,
                        websocket
                    )
                )
                
            elif message_type == "ping":
                # Respond to ping
                await connection_manager.send_personal_message(
                    {"type": "pong", "timestamp": datetime.now().isoformat()},
                    websocket
                )
                
            elif message_type == "get_active_calculations":
                # Send list of active calculations
                await connection_manager.send_personal_message(
                    {
                        "type": "active_calculations",
                        "calculations": calculation_service.get_active_calculations()
                    },
                    websocket
                )
                
            else:
                # Echo unknown messages
                await connection_manager.send_personal_message(
                    {"type": "error", "message": f"Unknown message type: {message_type}"},
                    websocket
                )
                
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket)


async def start_background_tasks():
    """Start background tasks for real-time updates."""
    # Start market data streaming
    asyncio.create_task(
        market_simulator.start_streaming(connection_manager, interval=10)
    )
    
    # Start periodic health checks
    async def health_check_loop():
        while True:
            await asyncio.sleep(60)  # Every minute
            # await notification_service.send_system_health() # Removed as per refactoring
            
    asyncio.create_task(health_check_loop())
    
    logger.info("Background tasks started")


def stop_background_tasks():
    """Stop all background tasks."""
    market_simulator.stop_streaming()
    logger.info("Background tasks stopped")