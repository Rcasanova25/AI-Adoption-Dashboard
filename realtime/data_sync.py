"""
Data synchronization and conflict resolution system
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
import json
import hashlib
from dataclasses import dataclass, field
from enum import Enum

from .models import DataRecord, DataChangeEvent, DataStatus

logger = logging.getLogger(__name__)

class ConflictResolutionStrategy(str, Enum):
    """Strategies for resolving data conflicts"""
    LATEST_WINS = "latest_wins"
    SOURCE_PRIORITY = "source_priority"
    MANUAL_REVIEW = "manual_review"
    MERGE_FIELDS = "merge_fields"
    CUSTOM_FUNCTION = "custom_function"

class ChangeType(str, Enum):
    """Types of data changes"""
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    MERGE = "merge"

@dataclass
class DataConflict:
    """Represents a data synchronization conflict"""
    source_id: str
    field_name: str
    local_value: Any
    remote_value: Any
    local_timestamp: datetime
    remote_timestamp: datetime
    conflict_type: str = "value_mismatch"
    resolution_strategy: Optional[ConflictResolutionStrategy] = None
    resolved: bool = False
    resolved_value: Any = None
    resolved_at: Optional[datetime] = None

@dataclass
class SyncState:
    """State of data synchronization"""
    source_id: str
    last_sync: Optional[datetime] = None
    sync_version: int = 0
    pending_changes: List[DataChangeEvent] = field(default_factory=list)
    conflicts: List[DataConflict] = field(default_factory=list)
    sync_in_progress: bool = False
    last_error: Optional[str] = None

class ChangeDetector:
    """Detects changes in data records"""
    
    def __init__(self):
        self._data_checksums: Dict[str, str] = {}
        self._field_checksums: Dict[str, Dict[str, str]] = {}
    
    def calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for data"""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(sorted_data.encode()).hexdigest()
    
    def calculate_field_checksums(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Calculate checksums for individual fields"""
        checksums = {}
        for field, value in data.items():
            value_str = json.dumps(value, sort_keys=True, default=str)
            checksums[field] = hashlib.sha256(value_str.encode()).hexdigest()
        return checksums
    
    def detect_changes(
        self, 
        source_id: str, 
        new_data: Dict[str, Any],
        old_data: Optional[Dict[str, Any]] = None
    ) -> Optional[DataChangeEvent]:
        """Detect changes in data"""
        new_checksum = self.calculate_checksum(new_data)
        old_checksum = self._data_checksums.get(source_id)
        
        # No change if checksums match
        if new_checksum == old_checksum:
            return None
        
        # Determine change type
        if old_checksum is None:
            change_type = ChangeType.INSERT
        else:
            change_type = ChangeType.UPDATE
        
        # Find changed fields
        new_field_checksums = self.calculate_field_checksums(new_data)
        old_field_checksums = self._field_checksums.get(source_id, {})
        
        changed_fields = []
        for field, new_checksum in new_field_checksums.items():
            old_field_checksum = old_field_checksums.get(field)
            if new_checksum != old_field_checksum:
                changed_fields.append(field)
        
        # Update stored checksums
        self._data_checksums[source_id] = new_checksum
        self._field_checksums[source_id] = new_field_checksums
        
        return DataChangeEvent(
            source_id=source_id,
            change_type=change_type.value,
            old_data=old_data,
            new_data=new_data,
            changed_fields=changed_fields
        )
    
    def mark_deleted(self, source_id: str) -> Optional[DataChangeEvent]:
        """Mark a source as deleted"""
        if source_id not in self._data_checksums:
            return None
        
        # Remove checksums
        del self._data_checksums[source_id]
        if source_id in self._field_checksums:
            del self._field_checksums[source_id]
        
        return DataChangeEvent(
            source_id=source_id,
            change_type=ChangeType.DELETE.value,
            old_data=None,
            new_data=None
        )

class ConflictResolver:
    """Resolves data synchronization conflicts"""
    
    def __init__(self):
        self._source_priorities: Dict[str, int] = {}
        self._custom_resolvers: Dict[str, callable] = {}
    
    def set_source_priority(self, source_id: str, priority: int):
        """Set priority for a data source (higher number = higher priority)"""
        self._source_priorities[source_id] = priority
    
    def register_custom_resolver(self, source_id: str, resolver_func: callable):
        """Register a custom conflict resolution function"""
        self._custom_resolvers[source_id] = resolver_func
    
    async def resolve_conflict(
        self, 
        conflict: DataConflict, 
        strategy: ConflictResolutionStrategy
    ) -> Any:
        """Resolve a data conflict using the specified strategy"""
        try:
            if strategy == ConflictResolutionStrategy.LATEST_WINS:
                return self._resolve_latest_wins(conflict)
            
            elif strategy == ConflictResolutionStrategy.SOURCE_PRIORITY:
                return self._resolve_source_priority(conflict)
            
            elif strategy == ConflictResolutionStrategy.MERGE_FIELDS:
                return self._resolve_merge_fields(conflict)
            
            elif strategy == ConflictResolutionStrategy.CUSTOM_FUNCTION:
                return await self._resolve_custom(conflict)
            
            elif strategy == ConflictResolutionStrategy.MANUAL_REVIEW:
                # For manual review, return None and mark for manual resolution
                return None
            
            else:
                logger.warning(f"Unknown conflict resolution strategy: {strategy}")
                return conflict.remote_value  # Default to remote value
                
        except Exception as e:
            logger.error(f"Error resolving conflict: {e}")
            return conflict.remote_value  # Fallback to remote value
    
    def _resolve_latest_wins(self, conflict: DataConflict) -> Any:
        """Resolve conflict by choosing the latest value"""
        if conflict.remote_timestamp > conflict.local_timestamp:
            return conflict.remote_value
        else:
            return conflict.local_value
    
    def _resolve_source_priority(self, conflict: DataConflict) -> Any:
        """Resolve conflict using source priority"""
        source_priority = self._source_priorities.get(conflict.source_id, 0)
        
        # For now, assume local has priority 1, remote has source priority
        if source_priority > 1:
            return conflict.remote_value
        else:
            return conflict.local_value
    
    def _resolve_merge_fields(self, conflict: DataConflict) -> Any:
        """Resolve conflict by merging field values"""
        # Simple merge strategy - combine values if both are dicts
        if isinstance(conflict.local_value, dict) and isinstance(conflict.remote_value, dict):
            merged = conflict.local_value.copy()
            merged.update(conflict.remote_value)
            return merged
        
        # For non-dict values, fall back to latest wins
        return self._resolve_latest_wins(conflict)
    
    async def _resolve_custom(self, conflict: DataConflict) -> Any:
        """Resolve conflict using custom function"""
        resolver = self._custom_resolvers.get(conflict.source_id)
        if not resolver:
            logger.warning(f"No custom resolver found for {conflict.source_id}")
            return conflict.remote_value
        
        try:
            if asyncio.iscoroutinefunction(resolver):
                return await resolver(conflict)
            else:
                return resolver(conflict)
        except Exception as e:
            logger.error(f"Custom resolver failed: {e}")
            return conflict.remote_value

class DataSynchronizer:
    """Main data synchronization manager"""
    
    def __init__(self):
        self.change_detector = ChangeDetector()
        self.conflict_resolver = ConflictResolver()
        self.sync_states: Dict[str, SyncState] = {}
        self._lock = asyncio.Lock()
        self._data_store: Dict[str, DataRecord] = {}
        
        # Default conflict resolution strategies by source
        self._default_strategies: Dict[str, ConflictResolutionStrategy] = {}
    
    def set_default_strategy(self, source_id: str, strategy: ConflictResolutionStrategy):
        """Set default conflict resolution strategy for a source"""
        self._default_strategies[source_id] = strategy
    
    async def sync_data(
        self, 
        source_id: str, 
        new_data: Dict[str, Any],
        force_update: bool = False
    ) -> Tuple[bool, List[DataConflict]]:
        """
        Synchronize data for a source
        Returns: (success, conflicts)
        """
        async with self._lock:
            sync_state = self.sync_states.setdefault(source_id, SyncState(source_id=source_id))
            
            if sync_state.sync_in_progress and not force_update:
                logger.warning(f"Sync already in progress for {source_id}")
                return False, []
            
            sync_state.sync_in_progress = True
            sync_state.last_error = None
            
            try:
                # Get current data
                current_record = self._data_store.get(source_id)
                current_data = current_record.data if current_record else None
                
                # Detect changes
                change_event = self.change_detector.detect_changes(
                    source_id, new_data, current_data
                )
                
                if not change_event and not force_update:
                    # No changes detected
                    sync_state.sync_in_progress = False
                    return True, []
                
                # Check for conflicts
                conflicts = []
                if current_data and change_event and change_event.change_type == ChangeType.UPDATE.value:
                    conflicts = await self._detect_conflicts(
                        source_id, current_data, new_data, change_event.changed_fields
                    )
                
                # Resolve conflicts
                resolved_data = new_data.copy()
                if conflicts:
                    resolved_data = await self._resolve_conflicts(source_id, conflicts, resolved_data)
                
                # Update data store
                new_record = DataRecord(
                    source_id=source_id,
                    data=resolved_data,
                    version=sync_state.sync_version + 1
                )
                
                self._data_store[source_id] = new_record
                
                # Update sync state
                sync_state.last_sync = datetime.utcnow()
                sync_state.sync_version += 1
                sync_state.sync_in_progress = False
                
                # Add to pending changes if there were unresolved conflicts
                unresolved_conflicts = [c for c in conflicts if not c.resolved]
                if change_event:
                    sync_state.pending_changes.append(change_event)
                
                return True, unresolved_conflicts
                
            except Exception as e:
                logger.error(f"Error during sync for {source_id}: {e}")
                sync_state.sync_in_progress = False
                sync_state.last_error = str(e)
                return False, []
    
    async def _detect_conflicts(
        self, 
        source_id: str, 
        local_data: Dict[str, Any],
        remote_data: Dict[str, Any],
        changed_fields: List[str]
    ) -> List[DataConflict]:
        """Detect conflicts between local and remote data"""
        conflicts = []
        
        for field in changed_fields:
            local_value = local_data.get(field)
            remote_value = remote_data.get(field)
            
            # Check if values are actually different
            if local_value != remote_value:
                conflict = DataConflict(
                    source_id=source_id,
                    field_name=field,
                    local_value=local_value,
                    remote_value=remote_value,
                    local_timestamp=datetime.utcnow(),  # Should be actual timestamp
                    remote_timestamp=datetime.utcnow()  # Should be actual timestamp
                )
                conflicts.append(conflict)
        
        return conflicts
    
    async def _resolve_conflicts(
        self, 
        source_id: str, 
        conflicts: List[DataConflict],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve all conflicts and return updated data"""
        resolved_data = data.copy()
        default_strategy = self._default_strategies.get(source_id, ConflictResolutionStrategy.LATEST_WINS)
        
        for conflict in conflicts:
            try:
                strategy = conflict.resolution_strategy or default_strategy
                resolved_value = await self.conflict_resolver.resolve_conflict(conflict, strategy)
                
                if resolved_value is not None:
                    resolved_data[conflict.field_name] = resolved_value
                    conflict.resolved = True
                    conflict.resolved_value = resolved_value
                    conflict.resolved_at = datetime.utcnow()
                
            except Exception as e:
                logger.error(f"Error resolving conflict for field {conflict.field_name}: {e}")
        
        return resolved_data
    
    async def get_sync_state(self, source_id: str) -> Optional[SyncState]:
        """Get synchronization state for a source"""
        return self.sync_states.get(source_id)
    
    async def get_data(self, source_id: str) -> Optional[DataRecord]:
        """Get synchronized data for a source"""
        async with self._lock:
            return self._data_store.get(source_id)
    
    async def get_all_data(self) -> Dict[str, DataRecord]:
        """Get all synchronized data"""
        async with self._lock:
            return self._data_store.copy()
    
    async def clear_conflicts(self, source_id: str):
        """Clear resolved conflicts for a source"""
        sync_state = self.sync_states.get(source_id)
        if sync_state:
            sync_state.conflicts = [c for c in sync_state.conflicts if not c.resolved]
    
    async def force_sync(self, source_id: str, data: Dict[str, Any]) -> bool:
        """Force synchronization without conflict detection"""
        try:
            async with self._lock:
                sync_state = self.sync_states.setdefault(source_id, SyncState(source_id=source_id))
                
                new_record = DataRecord(
                    source_id=source_id,
                    data=data,
                    version=sync_state.sync_version + 1
                )
                
                self._data_store[source_id] = new_record
                sync_state.last_sync = datetime.utcnow()
                sync_state.sync_version += 1
                
                return True
                
        except Exception as e:
            logger.error(f"Error during force sync for {source_id}: {e}")
            return False
    
    async def rollback_changes(self, source_id: str, version: int) -> bool:
        """Rollback to a specific version (basic implementation)"""
        # This would require a more sophisticated versioning system
        # For now, just log the request
        logger.info(f"Rollback requested for {source_id} to version {version}")
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics"""
        stats = {
            'total_sources': len(self.sync_states),
            'sources_with_conflicts': 0,
            'total_conflicts': 0,
            'avg_sync_frequency': 0,
            'sources_by_status': {
                'syncing': 0,
                'idle': 0,
                'error': 0
            }
        }
        
        for sync_state in self.sync_states.values():
            if sync_state.conflicts:
                stats['sources_with_conflicts'] += 1
                stats['total_conflicts'] += len(sync_state.conflicts)
            
            if sync_state.sync_in_progress:
                stats['sources_by_status']['syncing'] += 1
            elif sync_state.last_error:
                stats['sources_by_status']['error'] += 1
            else:
                stats['sources_by_status']['idle'] += 1
        
        return stats

# Global synchronizer instance
_global_synchronizer: Optional[DataSynchronizer] = None

def get_global_synchronizer() -> DataSynchronizer:
    """Get the global data synchronizer instance"""
    global _global_synchronizer
    if _global_synchronizer is None:
        _global_synchronizer = DataSynchronizer()
    return _global_synchronizer