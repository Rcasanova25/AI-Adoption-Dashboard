"""
API Client Framework with authentication, rate limiting, and error handling
"""

import asyncio
import aiohttp
import time
import logging
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime, timedelta
import hashlib
import json
from urllib.parse import urljoin, urlparse
import ssl
from dataclasses import dataclass, field

from .models import (
    DataSourceConfig, APIResponse, AuthenticationType, 
    RateLimitConfig, RetryConfig, ConnectionPoolConfig,
    APIMethod
)

logger = logging.getLogger(__name__)

@dataclass
class RateLimiter:
    """Rate limiter implementation"""
    config: RateLimitConfig
    requests: List[float] = field(default_factory=list)
    
    def can_make_request(self) -> bool:
        """Check if a request can be made within rate limits"""
        now = time.time()
        
        # Clean old requests
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        # Check per-second limit
        recent_requests = [req_time for req_time in self.requests if now - req_time < 1]
        if len(recent_requests) >= self.config.requests_per_second:
            return False
        
        # Check per-minute limit
        if len(self.requests) >= self.config.requests_per_minute:
            return False
        
        # Check burst limit
        very_recent = [req_time for req_time in self.requests if now - req_time < 0.1]
        if len(very_recent) >= self.config.burst_limit:
            return False
        
        return True
    
    def record_request(self):
        """Record a request timestamp"""
        self.requests.append(time.time())
    
    async def wait_for_slot(self):
        """Wait until a request slot is available"""
        while not self.can_make_request():
            await asyncio.sleep(0.1)

class APIClient:
    """Advanced API client with authentication, rate limiting, and error handling"""
    
    def __init__(self, config: DataSourceConfig, session: Optional[aiohttp.ClientSession] = None):
        self.config = config
        self.session = session
        self.rate_limiter = RateLimiter(config.rate_limit)
        self._auth_headers = {}
        self._setup_authentication()
        
    def _setup_authentication(self):
        """Setup authentication headers based on config"""
        creds = self.config.credentials
        
        if creds.auth_type == AuthenticationType.API_KEY:
            if creds.api_key:
                self._auth_headers['X-API-Key'] = creds.api_key
                
        elif creds.auth_type == AuthenticationType.BEARER_TOKEN:
            if creds.bearer_token:
                self._auth_headers['Authorization'] = f'Bearer {creds.bearer_token}'
                
        elif creds.auth_type == AuthenticationType.BASIC_AUTH:
            if creds.username and creds.password:
                import base64
                credentials = base64.b64encode(f"{creds.username}:{creds.password}".encode()).decode()
                self._auth_headers['Authorization'] = f'Basic {credentials}'
        
        # Add custom headers
        if creds.custom_headers:
            self._auth_headers.update(creds.custom_headers)
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get complete headers including auth"""
        headers = {
            'User-Agent': 'AI-Dashboard/1.0',
            'Content-Type': 'application/json'
        }
        headers.update(self._auth_headers)
        
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    async def _make_request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> APIResponse:
        """Make HTTP request with retry logic"""
        retry_config = self.config.retry_config
        last_exception = None
        
        for attempt in range(retry_config.max_attempts):
            try:
                # Wait for rate limit
                await self.rate_limiter.wait_for_slot()
                
                start_time = time.time()
                
                # Make the request
                async with self.session.request(
                    method,
                    url,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                    **kwargs
                ) as response:
                    response_time = time.time() - start_time
                    self.rate_limiter.record_request()
                    
                    # Read response data
                    try:
                        if response.content_type == 'application/json':
                            data = await response.json()
                        else:
                            data = await response.text()
                    except Exception as e:
                        logger.warning(f"Failed to parse response data: {e}")
                        data = None
                    
                    api_response = APIResponse(
                        source_id=self.config.source_id,
                        status_code=response.status,
                        data=data,
                        headers=dict(response.headers),
                        response_time=response_time
                    )
                    
                    # Check if successful
                    if api_response.is_success:
                        return api_response
                    else:
                        # Log non-success status
                        logger.warning(
                            f"API request failed with status {response.status} for {self.config.source_id}"
                        )
                        api_response.error = f"HTTP {response.status}"
                        if attempt == retry_config.max_attempts - 1:
                            return api_response
                        
            except asyncio.TimeoutError:
                last_exception = "Request timeout"
                logger.warning(f"Request timeout for {self.config.source_id}, attempt {attempt + 1}")
                
            except aiohttp.ClientError as e:
                last_exception = str(e)
                logger.warning(f"Client error for {self.config.source_id}, attempt {attempt + 1}: {e}")
                
            except Exception as e:
                last_exception = str(e)
                logger.error(f"Unexpected error for {self.config.source_id}, attempt {attempt + 1}: {e}")
            
            # Calculate retry delay
            if attempt < retry_config.max_attempts - 1:
                delay = min(
                    retry_config.initial_delay * (retry_config.exponential_base ** attempt),
                    retry_config.max_delay
                )
                
                if retry_config.jitter:
                    import random
                    delay *= (0.5 + random.random() * 0.5)  # Add 0-50% jitter
                
                await asyncio.sleep(delay)
        
        # All retries failed
        return APIResponse(
            source_id=self.config.source_id,
            status_code=0,
            error=last_exception or "All retries failed",
            response_time=0.0
        )
    
    async def get(self, endpoint: Optional[str] = None, params: Optional[Dict] = None) -> APIResponse:
        """Make GET request"""
        url = self._build_url(endpoint)
        headers = self._get_headers()
        
        return await self._make_request_with_retry(
            'GET',
            url,
            headers=headers,
            params=params
        )
    
    async def post(
        self, 
        endpoint: Optional[str] = None, 
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> APIResponse:
        """Make POST request"""
        url = self._build_url(endpoint)
        headers = self._get_headers()
        
        kwargs = {'headers': headers}
        if json_data:
            kwargs['json'] = json_data
        elif data:
            kwargs['data'] = data
            
        return await self._make_request_with_retry('POST', url, **kwargs)
    
    def _build_url(self, endpoint: Optional[str] = None) -> str:
        """Build complete URL"""
        base_url = self.config.base_url or ""
        if endpoint:
            return urljoin(base_url, endpoint)
        elif self.config.endpoint:
            return urljoin(base_url, self.config.endpoint)
        else:
            return base_url
    
    async def health_check(self) -> bool:
        """Perform health check on the API"""
        try:
            response = await self.get()
            return response.is_success
        except Exception as e:
            logger.error(f"Health check failed for {self.config.source_id}: {e}")
            return False

class APIConnectionPool:
    """Manages a pool of API connections"""
    
    def __init__(self, pool_config: Optional[ConnectionPoolConfig] = None):
        self.config = pool_config or ConnectionPoolConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.clients: Dict[str, APIClient] = {}
        self._lock = asyncio.Lock()
        
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def start(self):
        """Start the connection pool"""
        if self.session is None:
            # Setup SSL context
            ssl_context = ssl.create_default_context()
            if not self.config.enable_ssl_verification:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            
            # Create connector
            connector = aiohttp.TCPConnector(
                limit=self.config.max_connections,
                limit_per_host=self.config.max_connections_per_host,
                keepalive_timeout=self.config.keepalive_timeout,
                ssl=ssl_context
            )
            
            # Create session
            timeout = aiohttp.ClientTimeout(
                total=self.config.connection_timeout,
                sock_read=self.config.read_timeout
            )
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )
    
    async def close(self):
        """Close all connections"""
        if self.session:
            await self.session.close()
            self.session = None
        self.clients.clear()
    
    async def get_client(self, config: DataSourceConfig) -> APIClient:
        """Get or create an API client for the given configuration"""
        async with self._lock:
            if config.source_id not in self.clients:
                if self.session is None:
                    await self.start()
                
                self.clients[config.source_id] = APIClient(config, self.session)
            
            return self.clients[config.source_id]
    
    async def remove_client(self, source_id: str):
        """Remove a client from the pool"""
        async with self._lock:
            if source_id in self.clients:
                del self.clients[source_id]
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all clients"""
        results = {}
        tasks = []
        
        for source_id, client in self.clients.items():
            tasks.append(self._health_check_client(source_id, client))
        
        if tasks:
            health_results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, (source_id, _) in enumerate(self.clients.items()):
                result = health_results[i]
                results[source_id] = result if isinstance(result, bool) else False
        
        return results
    
    async def _health_check_client(self, source_id: str, client: APIClient) -> bool:
        """Health check a single client"""
        try:
            return await client.health_check()
        except Exception as e:
            logger.error(f"Health check failed for {source_id}: {e}")
            return False

# Global connection pool instance
_global_pool: Optional[APIConnectionPool] = None

async def get_global_pool() -> APIConnectionPool:
    """Get the global connection pool instance"""
    global _global_pool
    if _global_pool is None:
        _global_pool = APIConnectionPool()
        await _global_pool.start()
    return _global_pool

async def cleanup_global_pool():
    """Cleanup the global connection pool"""
    global _global_pool
    if _global_pool:
        await _global_pool.close()
        _global_pool = None