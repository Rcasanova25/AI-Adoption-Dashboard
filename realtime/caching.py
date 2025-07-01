"""
Enhanced caching system for real-time data with fallback mechanisms
"""

import asyncio
import logging
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import pickle
import gzip
from pathlib import Path

from .models import DataRecord, DataStatus

logger = logging.getLogger(__name__)

class CachePolicy(str, Enum):
    """Cache policy types"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    FIFO = "fifo"  # First In, First Out

class CacheLevel(str, Enum):
    """Cache levels for multi-tier caching"""
    MEMORY = "memory"
    DISK = "disk"
    DISTRIBUTED = "distributed"

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    expires_at: Optional[datetime] = None
    size_bytes: int = 0
    source_id: Optional[str] = None
    version: int = 1
    compressed: bool = False
    
    @property
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def age(self) -> timedelta:
        """Get age of cache entry"""
        return datetime.utcnow() - self.created_at
    
    def touch(self):
        """Update access metadata"""
        self.last_accessed = datetime.utcnow()
        self.access_count += 1

class MemoryCache:
    """In-memory cache with various eviction policies"""
    
    def __init__(
        self, 
        max_size: int = 1000,
        max_memory_mb: int = 100,
        default_ttl: Optional[timedelta] = None,
        policy: CachePolicy = CachePolicy.LRU
    ):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.default_ttl = default_ttl
        self.policy = policy
        
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: List[str] = []  # For LRU
        self._lock = asyncio.Lock()
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        async with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                return None
            
            if entry.is_expired:
                await self._remove_entry(key)
                return None
            
            # Update access metadata
            entry.touch()
            
            # Update access order for LRU
            if self.policy == CachePolicy.LRU:
                if key in self._access_order:
                    self._access_order.remove(key)
                self._access_order.append(key)
            
            # Decompress if needed
            value = entry.value
            if entry.compressed and isinstance(value, bytes):
                try:
                    value = pickle.loads(gzip.decompress(value))
                except Exception as e:
                    logger.error(f"Error decompressing cache entry {key}: {e}")
                    await self._remove_entry(key)
                    return None
            
            return value
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[timedelta] = None,
        source_id: Optional[str] = None,
        compress: bool = False
    ) -> bool:
        """Set value in cache"""
        async with self._lock:
            # Calculate TTL
            expires_at = None
            if ttl or self.default_ttl:
                expires_at = datetime.utcnow() + (ttl or self.default_ttl)
            
            # Compress value if requested
            final_value = value
            if compress:
                try:
                    serialized = pickle.dumps(value)
                    final_value = gzip.compress(serialized)
                except Exception as e:
                    logger.warning(f"Failed to compress cache entry {key}: {e}")
                    compress = False
            
            # Calculate size
            try:
                if isinstance(final_value, (str, bytes)):
                    size_bytes = len(final_value)
                else:
                    size_bytes = len(pickle.dumps(final_value))
            except Exception:
                size_bytes = 0
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=final_value,
                expires_at=expires_at,
                size_bytes=size_bytes,
                source_id=source_id,
                compressed=compress
            )
            
            # Check if we need to evict entries
            await self._ensure_capacity(size_bytes)
            
            # Store entry
            self._cache[key] = entry
            
            # Update access order
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            
            return True
    
    async def delete(self, key: str) -> bool:
        """Delete entry from cache"""
        async with self._lock:
            return await self._remove_entry(key)
    
    async def clear(self):
        """Clear all cache entries"""
        async with self._lock:
            self._cache.clear()
            self._access_order.clear()
    
    async def _remove_entry(self, key: str) -> bool:
        """Remove entry and update access order"""
        if key in self._cache:
            del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)
            return True
        return False
    
    async def _ensure_capacity(self, new_entry_size: int):
        """Ensure cache has capacity for new entry"""
        # Check size limit
        while len(self._cache) >= self.max_size:
            await self._evict_one()
        
        # Check memory limit
        current_memory = sum(entry.size_bytes for entry in self._cache.values())
        while current_memory + new_entry_size > self.max_memory_bytes and self._cache:
            await self._evict_one()
            current_memory = sum(entry.size_bytes for entry in self._cache.values())
    
    async def _evict_one(self):
        """Evict one entry based on policy"""
        if not self._cache:
            return
        
        if self.policy == CachePolicy.LRU:
            # Remove least recently used
            if self._access_order:
                key_to_remove = self._access_order[0]
                await self._remove_entry(key_to_remove)
        
        elif self.policy == CachePolicy.LFU:
            # Remove least frequently used
            min_access_count = min(entry.access_count for entry in self._cache.values())
            for key, entry in self._cache.items():
                if entry.access_count == min_access_count:
                    await self._remove_entry(key)
                    break
        
        elif self.policy == CachePolicy.TTL:
            # Remove expired entries first, then oldest
            now = datetime.utcnow()
            for key, entry in self._cache.items():
                if entry.is_expired:
                    await self._remove_entry(key)
                    return
            
            # If no expired entries, remove oldest
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].created_at)
            await self._remove_entry(oldest_key)
        
        elif self.policy == CachePolicy.FIFO:
            # Remove first inserted (oldest)
            if self._access_order:
                oldest_key = self._access_order[0]
                await self._remove_entry(oldest_key)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        async with self._lock:
            total_size = sum(entry.size_bytes for entry in self._cache.values())
            
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'memory_usage_bytes': total_size,
                'memory_usage_mb': total_size / (1024 * 1024),
                'max_memory_mb': self.max_memory_bytes / (1024 * 1024),
                'policy': self.policy.value,
                'hit_rate': getattr(self, '_hit_rate', 0.0)
            }

class DiskCache:
    """Disk-based cache for persistent storage"""
    
    def __init__(self, cache_dir: str = "cache/realtime", max_size_mb: int = 1000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
        self._metadata_file = self.cache_dir / "metadata.json"
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
        
        # Load existing metadata
        asyncio.create_task(self._load_metadata())
    
    async def _load_metadata(self):
        """Load cache metadata from disk"""
        try:
            if self._metadata_file.exists():
                with open(self._metadata_file, 'r') as f:
                    self._metadata = json.load(f)
        except Exception as e:
            logger.error(f"Error loading cache metadata: {e}")
            self._metadata = {}
    
    async def _save_metadata(self):
        """Save cache metadata to disk"""
        try:
            with open(self._metadata_file, 'w') as f:
                json.dump(self._metadata, f, default=str, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata: {e}")
    
    def _get_cache_file_path(self, key: str) -> Path:
        """Get file path for cache key"""
        # Create safe filename from key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.cache"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from disk cache"""
        async with self._lock:
            if key not in self._metadata:
                return None
            
            metadata = self._metadata[key]
            
            # Check expiration
            if metadata.get('expires_at'):
                expires_at = datetime.fromisoformat(metadata['expires_at'])
                if datetime.utcnow() > expires_at:
                    await self._remove_entry(key)
                    return None
            
            # Load from file
            cache_file = self._get_cache_file_path(key)
            if not cache_file.exists():
                await self._remove_entry(key)
                return None
            
            try:
                with open(cache_file, 'rb') as f:
                    data = f.read()
                
                # Decompress if needed
                if metadata.get('compressed', False):
                    data = gzip.decompress(data)
                
                value = pickle.loads(data)
                
                # Update access metadata
                metadata['last_accessed'] = datetime.utcnow().isoformat()
                metadata['access_count'] = metadata.get('access_count', 0) + 1
                
                return value
                
            except Exception as e:
                logger.error(f"Error reading cache file {cache_file}: {e}")
                await self._remove_entry(key)
                return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[timedelta] = None,
        source_id: Optional[str] = None,
        compress: bool = True
    ) -> bool:
        """Set value in disk cache"""
        async with self._lock:
            try:
                # Serialize value
                data = pickle.dumps(value)
                
                # Compress if requested
                if compress:
                    data = gzip.compress(data)
                
                # Calculate expiration
                expires_at = None
                if ttl:
                    expires_at = datetime.utcnow() + ttl
                
                # Ensure we have space
                await self._ensure_disk_space(len(data))
                
                # Write to file
                cache_file = self._get_cache_file_path(key)
                with open(cache_file, 'wb') as f:
                    f.write(data)
                
                # Update metadata
                self._metadata[key] = {
                    'created_at': datetime.utcnow().isoformat(),
                    'last_accessed': datetime.utcnow().isoformat(),
                    'access_count': 0,
                    'expires_at': expires_at.isoformat() if expires_at else None,
                    'size_bytes': len(data),
                    'source_id': source_id,
                    'compressed': compress,
                    'file_path': str(cache_file)
                }
                
                await self._save_metadata()
                return True
                
            except Exception as e:
                logger.error(f"Error writing cache entry {key}: {e}")
                return False
    
    async def delete(self, key: str) -> bool:
        """Delete entry from disk cache"""
        async with self._lock:
            return await self._remove_entry(key)
    
    async def _remove_entry(self, key: str) -> bool:
        """Remove entry and clean up files"""
        if key not in self._metadata:
            return False
        
        try:
            cache_file = self._get_cache_file_path(key)
            if cache_file.exists():
                cache_file.unlink()
            
            del self._metadata[key]
            await self._save_metadata()
            return True
            
        except Exception as e:
            logger.error(f"Error removing cache entry {key}: {e}")
            return False
    
    async def _ensure_disk_space(self, new_entry_size: int):
        """Ensure disk cache has space for new entry"""
        current_size = sum(
            metadata.get('size_bytes', 0) 
            for metadata in self._metadata.values()
        )
        
        # Remove old entries until we have space
        while current_size + new_entry_size > self.max_size_bytes and self._metadata:
            # Find oldest entry
            oldest_key = min(
                self._metadata.keys(),
                key=lambda k: self._metadata[k]['created_at']
            )
            
            old_size = self._metadata[oldest_key].get('size_bytes', 0)
            await self._remove_entry(oldest_key)
            current_size -= old_size
    
    async def clear(self):
        """Clear all disk cache entries"""
        async with self._lock:
            for key in list(self._metadata.keys()):
                await self._remove_entry(key)

class MultiTierCache:
    """Multi-tier cache with memory and disk levels"""
    
    def __init__(
        self,
        memory_cache: Optional[MemoryCache] = None,
        disk_cache: Optional[DiskCache] = None,
        fallback_enabled: bool = True
    ):
        self.memory_cache = memory_cache or MemoryCache()
        self.disk_cache = disk_cache or DiskCache()
        self.fallback_enabled = fallback_enabled
        
        self._stats = {
            'memory_hits': 0,
            'disk_hits': 0,
            'misses': 0,
            'total_requests': 0
        }
    
    async def get(self, key: str) -> Tuple[Optional[Any], CacheLevel]:
        """Get value from cache, checking memory first then disk"""
        self._stats['total_requests'] += 1
        
        # Try memory cache first
        value = await self.memory_cache.get(key)
        if value is not None:
            self._stats['memory_hits'] += 1
            return value, CacheLevel.MEMORY
        
        # Try disk cache
        value = await self.disk_cache.get(key)
        if value is not None:
            self._stats['disk_hits'] += 1
            
            # Promote to memory cache
            await self.memory_cache.set(key, value)
            
            return value, CacheLevel.DISK
        
        # Cache miss
        self._stats['misses'] += 1
        return None, None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[timedelta] = None,
        source_id: Optional[str] = None,
        levels: List[CacheLevel] = None
    ) -> bool:
        """Set value in specified cache levels"""
        if levels is None:
            levels = [CacheLevel.MEMORY, CacheLevel.DISK]
        
        success = True
        
        if CacheLevel.MEMORY in levels:
            success &= await self.memory_cache.set(key, value, ttl, source_id)
        
        if CacheLevel.DISK in levels:
            success &= await self.disk_cache.set(key, value, ttl, source_id)
        
        return success
    
    async def delete(self, key: str) -> bool:
        """Delete from all cache levels"""
        memory_result = await self.memory_cache.delete(key)
        disk_result = await self.disk_cache.delete(key)
        return memory_result or disk_result
    
    async def clear(self):
        """Clear all cache levels"""
        await self.memory_cache.clear()
        await self.disk_cache.clear()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        memory_stats = await self.memory_cache.get_stats()
        
        total_requests = self._stats['total_requests']
        hit_rate = 0.0
        if total_requests > 0:
            total_hits = self._stats['memory_hits'] + self._stats['disk_hits']
            hit_rate = (total_hits / total_requests) * 100
        
        return {
            'total_requests': total_requests,
            'memory_hits': self._stats['memory_hits'],
            'disk_hits': self._stats['disk_hits'],
            'misses': self._stats['misses'],
            'hit_rate_percent': hit_rate,
            'memory_cache': memory_stats,
            'disk_cache': {
                'entries': len(self.disk_cache._metadata),
                'size_mb': sum(
                    m.get('size_bytes', 0) for m in self.disk_cache._metadata.values()
                ) / (1024 * 1024)
            }
        }

class RealtimeDataCache:
    """Specialized cache for real-time data with fallback mechanisms"""
    
    def __init__(self, multi_tier_cache: Optional[MultiTierCache] = None):
        self.cache = multi_tier_cache or MultiTierCache()
        self._fallback_data: Dict[str, DataRecord] = {}
        self._lock = asyncio.Lock()
    
    async def get_data(self, source_id: str) -> Optional[DataRecord]:
        """Get data record with fallback"""
        cache_key = f"realtime_data:{source_id}"
        
        # Try cache first
        cached_data, cache_level = await self.cache.get(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache hit for {source_id} from {cache_level}")
            return cached_data
        
        # Fallback to stored data
        async with self._lock:
            fallback_data = self._fallback_data.get(source_id)
            if fallback_data:
                logger.info(f"Using fallback data for {source_id}")
                return fallback_data
        
        return None
    
    async def set_data(
        self, 
        source_id: str, 
        data_record: DataRecord,
        ttl: Optional[timedelta] = None,
        store_fallback: bool = True
    ) -> bool:
        """Set data record in cache"""
        cache_key = f"realtime_data:{source_id}"
        
        # Store in cache
        success = await self.cache.set(
            cache_key, 
            data_record, 
            ttl=ttl,
            source_id=source_id
        )
        
        # Store as fallback
        if store_fallback:
            async with self._lock:
                self._fallback_data[source_id] = data_record
        
        return success
    
    async def invalidate_data(self, source_id: str) -> bool:
        """Invalidate cached data for a source"""
        cache_key = f"realtime_data:{source_id}"
        return await self.cache.delete(cache_key)
    
    async def get_cached_sources(self) -> List[str]:
        """Get list of sources with cached data"""
        # This would require cache key enumeration
        # For now, return fallback sources
        async with self._lock:
            return list(self._fallback_data.keys())
    
    async def cleanup_expired(self):
        """Clean up expired cache entries"""
        # Memory cache handles this automatically
        # For disk cache, we could add cleanup logic here
        pass
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return await self.cache.get_stats()

# Global cache instance
_global_cache: Optional[RealtimeDataCache] = None

def get_global_cache() -> RealtimeDataCache:
    """Get the global realtime data cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = RealtimeDataCache()
    return _global_cache