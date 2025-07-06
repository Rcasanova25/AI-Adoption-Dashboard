"""Audit logging module for AI Adoption Dashboard.

This module provides comprehensive audit logging for all calculations,
API calls, and user actions for compliance and debugging.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum
import threading
from collections import deque
import uuid
import hashlib


class AuditEventType(Enum):
    """Types of audit events."""
    CALCULATION = "calculation"
    API_CALL = "api_call"
    USER_ACTION = "user_action"
    AUTHENTICATION = "authentication"
    DATA_EXPORT = "data_export"
    REPORT_GENERATION = "report_generation"
    PERMISSION_CHECK = "permission_check"
    ERROR = "error"
    SYSTEM = "system"


class AuditSeverity(Enum):
    """Severity levels for audit events."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditEntry:
    """Represents a single audit log entry."""
    
    def __init__(
        self,
        event_type: AuditEventType,
        action: str,
        user: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: AuditSeverity = AuditSeverity.INFO,
        correlation_id: Optional[str] = None
    ):
        """Initialize audit entry."""
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.event_type = event_type
        self.action = action
        self.user = user or "system"
        self.details = details or {}
        self.severity = severity
        self.correlation_id = correlation_id or self.id
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type.value,
            "action": self.action,
            "user": self.user,
            "details": self.details,
            "severity": self.severity.value,
            "correlation_id": self.correlation_id
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class AuditLogger:
    """Main audit logging class."""
    
    def __init__(
        self,
        log_dir: str = "audit_logs",
        max_memory_entries: int = 1000,
        rotation_size_mb: int = 100
    ):
        """Initialize audit logger."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.max_memory_entries = max_memory_entries
        self.rotation_size_mb = rotation_size_mb
        
        # In-memory buffer for recent entries
        self.memory_buffer = deque(maxlen=max_memory_entries)
        self.buffer_lock = threading.Lock()
        
        # Setup file logging
        self.current_log_file = self._get_current_log_file()
        self.file_logger = self._setup_file_logger()
        
        # Statistics
        self.stats = {
            "total_entries": 0,
            "entries_by_type": {},
            "entries_by_severity": {},
            "entries_by_user": {}
        }
        
    def _get_current_log_file(self) -> Path:
        """Get current log file path."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"audit_{date_str}.log"
    
    def _setup_file_logger(self) -> logging.Logger:
        """Setup file logger."""
        logger = logging.getLogger("audit_file_logger")
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        logger.handlers = []
        
        # Add file handler
        handler = logging.FileHandler(self.current_log_file, mode='a')
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        
        return logger
    
    def _rotate_log_if_needed(self):
        """Check and rotate log file if it exceeds size limit."""
        if self.current_log_file.exists():
            size_mb = self.current_log_file.stat().st_size / (1024 * 1024)
            if size_mb >= self.rotation_size_mb:
                # Rotate file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = self.current_log_file.stem + f"_{timestamp}.log"
                self.current_log_file.rename(self.log_dir / new_name)
                
                # Setup new logger
                self.current_log_file = self._get_current_log_file()
                self.file_logger = self._setup_file_logger()
    
    def _update_stats(self, entry: AuditEntry):
        """Update statistics."""
        self.stats["total_entries"] += 1
        
        # By type
        event_type = entry.event_type.value
        self.stats["entries_by_type"][event_type] = \
            self.stats["entries_by_type"].get(event_type, 0) + 1
        
        # By severity
        severity = entry.severity.value
        self.stats["entries_by_severity"][severity] = \
            self.stats["entries_by_severity"].get(severity, 0) + 1
        
        # By user
        user = entry.user
        self.stats["entries_by_user"][user] = \
            self.stats["entries_by_user"].get(user, 0) + 1
    
    def log(self, entry: AuditEntry):
        """Log an audit entry."""
        # Add to memory buffer
        with self.buffer_lock:
            self.memory_buffer.append(entry)
        
        # Write to file
        self._rotate_log_if_needed()
        self.file_logger.info(entry.to_json())
        
        # Update stats
        self._update_stats(entry)
    
    def log_calculation(
        self,
        calculation_type: str,
        parameters: Dict[str, Any],
        result: Any,
        user: str,
        duration_ms: Optional[float] = None,
        cache_hit: bool = False
    ):
        """Log a calculation event."""
        details = {
            "calculation_type": calculation_type,
            "parameters": self._sanitize_parameters(parameters),
            "result_summary": self._summarize_result(result),
            "duration_ms": duration_ms,
            "cache_hit": cache_hit
        }
        
        entry = AuditEntry(
            event_type=AuditEventType.CALCULATION,
            action=f"calculate_{calculation_type}",
            user=user,
            details=details
        )
        
        self.log(entry)
    
    def log_api_call(
        self,
        endpoint: str,
        method: str,
        user: str,
        status_code: int,
        duration_ms: Optional[float] = None,
        ip_address: Optional[str] = None
    ):
        """Log an API call."""
        details = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "ip_address": ip_address
        }
        
        severity = AuditSeverity.INFO
        if status_code >= 500:
            severity = AuditSeverity.ERROR
        elif status_code >= 400:
            severity = AuditSeverity.WARNING
        
        entry = AuditEntry(
            event_type=AuditEventType.API_CALL,
            action=f"{method} {endpoint}",
            user=user,
            details=details,
            severity=severity
        )
        
        self.log(entry)
    
    def log_authentication(
        self,
        action: str,
        username: str,
        success: bool,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log authentication event."""
        event_details = {
            "action": action,
            "success": success,
            "ip_address": ip_address
        }
        if details:
            event_details.update(details)
        
        severity = AuditSeverity.INFO if success else AuditSeverity.WARNING
        
        entry = AuditEntry(
            event_type=AuditEventType.AUTHENTICATION,
            action=action,
            user=username,
            details=event_details,
            severity=severity
        )
        
        self.log(entry)
    
    def log_data_export(
        self,
        export_type: str,
        format: str,
        user: str,
        record_count: int,
        file_size_bytes: Optional[int] = None
    ):
        """Log data export event."""
        details = {
            "export_type": export_type,
            "format": format,
            "record_count": record_count,
            "file_size_bytes": file_size_bytes
        }
        
        entry = AuditEntry(
            event_type=AuditEventType.DATA_EXPORT,
            action=f"export_{export_type}",
            user=user,
            details=details
        )
        
        self.log(entry)
    
    def log_permission_check(
        self,
        user: str,
        permission: str,
        granted: bool,
        context: Optional[str] = None
    ):
        """Log permission check."""
        details = {
            "permission": permission,
            "granted": granted,
            "context": context
        }
        
        entry = AuditEntry(
            event_type=AuditEventType.PERMISSION_CHECK,
            action=f"check_{permission}",
            user=user,
            details=details,
            severity=AuditSeverity.INFO if granted else AuditSeverity.WARNING
        )
        
        self.log(entry)
    
    def log_error(
        self,
        error_type: str,
        error_message: str,
        user: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log error event."""
        details = {
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {}
        }
        
        entry = AuditEntry(
            event_type=AuditEventType.ERROR,
            action="error_occurred",
            user=user,
            details=details,
            severity=AuditSeverity.ERROR
        )
        
        self.log(entry)
    
    def _sanitize_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize sensitive parameters."""
        sanitized = {}
        sensitive_keys = ["password", "token", "secret", "key", "api_key"]
        
        for key, value in parameters.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                # Hash sensitive values
                if isinstance(value, str):
                    sanitized[key] = hashlib.sha256(value.encode()).hexdigest()[:16] + "..."
                else:
                    sanitized[key] = "***REDACTED***"
            else:
                sanitized[key] = value
                
        return sanitized
    
    def _summarize_result(self, result: Any) -> Dict[str, Any]:
        """Create summary of calculation result."""
        if isinstance(result, dict):
            return {
                "type": "dict",
                "keys": list(result.keys()),
                "sample": str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
            }
        elif isinstance(result, (list, tuple)):
            return {
                "type": type(result).__name__,
                "length": len(result),
                "sample": str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
            }
        else:
            return {
                "type": type(result).__name__,
                "value": str(result)
            }
    
    def search(
        self,
        event_type: Optional[AuditEventType] = None,
        user: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        severity: Optional[AuditSeverity] = None,
        limit: int = 100
    ) -> List[AuditEntry]:
        """Search audit logs."""
        results = []
        
        # Search in memory buffer first
        with self.buffer_lock:
            for entry in reversed(self.memory_buffer):
                if event_type and entry.event_type != event_type:
                    continue
                if user and entry.user != user:
                    continue
                if severity and entry.severity != severity:
                    continue
                if start_time and entry.timestamp < start_time:
                    continue
                if end_time and entry.timestamp > end_time:
                    continue
                    
                results.append(entry)
                if len(results) >= limit:
                    return results
        
        # If need more, search in files
        # (Implementation would read from log files)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audit statistics."""
        return {
            "summary": self.stats,
            "recent_entries": len(self.memory_buffer),
            "log_files": len(list(self.log_dir.glob("*.log")))
        }
    
    def export_logs(
        self,
        output_file: str,
        format: str = "json",
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Export audit logs to file."""
        entries = self.search(**filters) if filters else list(self.memory_buffer)
        
        output_path = Path(output_file)
        
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(
                    [entry.to_dict() for entry in entries],
                    f,
                    indent=2,
                    default=str
                )
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                if entries:
                    writer = csv.DictWriter(f, fieldnames=entries[0].to_dict().keys())
                    writer.writeheader()
                    for entry in entries:
                        writer.writerow(entry.to_dict())
        
        return str(output_path)


# Global audit logger instance
audit_logger = AuditLogger()


# Decorator for automatic audit logging
def audit_calculation(calculation_type: str):
    """Decorator to automatically audit calculations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                # Extract user from context if available
                user = kwargs.get('user', 'system')
                
                audit_logger.log_calculation(
                    calculation_type=calculation_type,
                    parameters=kwargs,
                    result=result,
                    user=user,
                    duration_ms=duration_ms
                )
                
                return result
                
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                
                audit_logger.log_error(
                    error_type=type(e).__name__,
                    error_message=str(e),
                    context={
                        "calculation_type": calculation_type,
                        "parameters": kwargs,
                        "duration_ms": duration_ms
                    }
                )
                
                raise
                
        return wrapper
    return decorator