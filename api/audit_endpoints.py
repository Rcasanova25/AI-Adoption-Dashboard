"""Audit log API endpoints for AI Adoption Dashboard.

This module provides API endpoints for viewing and managing audit logs.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from fastapi import Depends

from utils.audit_logger import audit_logger, AuditEventType, AuditSeverity
from .endpoints import APIResponse, log_api_call
from .auth_endpoints import get_current_user, require_permission, TokenData

logger = logging.getLogger(__name__)


class AuditAPI:
    """API endpoints for audit log management."""
    
    @staticmethod
    @log_api_call("audit/search")
    def search_logs(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Search audit logs.
        
        Request:
            {
                "event_type": "calculation",  # optional
                "user": "username",  # optional
                "severity": "error",  # optional
                "start_date": "2024-01-01T00:00:00",  # optional
                "end_date": "2024-01-31T23:59:59",  # optional
                "limit": 100
            }
        """
        try:
            # Parse parameters
            event_type = None
            if request_data.get("event_type"):
                event_type = AuditEventType(request_data["event_type"])
            
            severity = None
            if request_data.get("severity"):
                severity = AuditSeverity(request_data["severity"])
            
            start_time = None
            if request_data.get("start_date"):
                start_time = datetime.fromisoformat(request_data["start_date"])
            
            end_time = None
            if request_data.get("end_date"):
                end_time = datetime.fromisoformat(request_data["end_date"])
            
            # Search logs
            entries = audit_logger.search(
                event_type=event_type,
                user=request_data.get("user"),
                start_time=start_time,
                end_time=end_time,
                severity=severity,
                limit=request_data.get("limit", 100)
            )
            
            # Convert to dict format
            results = [entry.to_dict() for entry in entries]
            
            return APIResponse.success({
                "entries": results,
                "count": len(results)
            })
            
        except ValueError as e:
            return APIResponse.error(str(e), 400)
        except Exception as e:
            logger.error(f"Audit search error: {e}")
            return APIResponse.error("Failed to search audit logs", 500)
    
    @staticmethod
    @log_api_call("audit/stats")
    def get_statistics(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get audit log statistics."""
        try:
            stats = audit_logger.get_stats()
            
            return APIResponse.success(stats)
            
        except Exception as e:
            logger.error(f"Audit stats error: {e}")
            return APIResponse.error("Failed to get audit statistics", 500)
    
    @staticmethod
    @log_api_call("audit/recent")
    def get_recent_activity(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get recent activity (last 24 hours)."""
        try:
            # Get entries from last 24 hours
            start_time = datetime.utcnow() - timedelta(days=1)
            
            entries = audit_logger.search(
                start_time=start_time,
                limit=50
            )
            
            # Group by event type
            by_type = {}
            for entry in entries:
                event_type = entry.event_type.value
                if event_type not in by_type:
                    by_type[event_type] = []
                by_type[event_type].append(entry.to_dict())
            
            return APIResponse.success({
                "recent_activity": by_type,
                "total_count": len(entries),
                "period": "last_24_hours"
            })
            
        except Exception as e:
            logger.error(f"Recent activity error: {e}")
            return APIResponse.error("Failed to get recent activity", 500)
    
    @staticmethod
    @log_api_call("audit/user-activity")
    def get_user_activity(
        username: str,
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get activity for specific user."""
        try:
            # Check permission - users can view their own activity
            if current_user and current_user.username != username:
                # Need admin permission to view other users
                if not require_permission("admin:users"):
                    return APIResponse.error("Permission denied", 403)
            
            entries = audit_logger.search(
                user=username,
                limit=100
            )
            
            # Summarize by action
            summary = {
                "total_actions": len(entries),
                "actions_by_type": {},
                "recent_actions": []
            }
            
            for entry in entries:
                action = entry.action
                if action not in summary["actions_by_type"]:
                    summary["actions_by_type"][action] = 0
                summary["actions_by_type"][action] += 1
                
                if len(summary["recent_actions"]) < 10:
                    summary["recent_actions"].append({
                        "timestamp": entry.timestamp.isoformat(),
                        "action": entry.action,
                        "event_type": entry.event_type.value
                    })
            
            return APIResponse.success({
                "username": username,
                "activity_summary": summary
            })
            
        except Exception as e:
            logger.error(f"User activity error: {e}")
            return APIResponse.error("Failed to get user activity", 500)
    
    @staticmethod
    @log_api_call("audit/export")
    def export_logs(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Export audit logs.
        
        Request:
            {
                "format": "json",  # or "csv"
                "filters": {
                    "event_type": "calculation",
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-01-31T23:59:59"
                }
            }
        """
        try:
            format = request_data.get("format", "json")
            filters = request_data.get("filters", {})
            
            # Parse filters
            if filters.get("start_date"):
                filters["start_time"] = datetime.fromisoformat(filters.pop("start_date"))
            if filters.get("end_date"):
                filters["end_time"] = datetime.fromisoformat(filters.pop("end_date"))
            if filters.get("event_type"):
                filters["event_type"] = AuditEventType(filters["event_type"])
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_logs_{timestamp}.{format}"
            
            # Export logs
            output_path = audit_logger.export_logs(
                output_file=filename,
                format=format,
                filters=filters
            )
            
            # Audit the export itself
            audit_logger.log_data_export(
                export_type="audit_logs",
                format=format,
                user=current_user.username if current_user else "anonymous",
                record_count=len(audit_logger.search(**filters))
            )
            
            return APIResponse.success({
                "filename": filename,
                "format": format,
                "message": f"Audit logs exported to {filename}"
            })
            
        except Exception as e:
            logger.error(f"Audit export error: {e}")
            return APIResponse.error("Failed to export audit logs", 500)
    
    @staticmethod
    @log_api_call("audit/calculation-history")
    def get_calculation_history(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get calculation history with performance metrics."""
        try:
            # Get calculation entries
            entries = audit_logger.search(
                event_type=AuditEventType.CALCULATION,
                limit=100
            )
            
            # Analyze performance
            calc_stats = {}
            for entry in entries:
                calc_type = entry.details.get("calculation_type")
                if calc_type not in calc_stats:
                    calc_stats[calc_type] = {
                        "count": 0,
                        "total_duration_ms": 0,
                        "cache_hits": 0,
                        "avg_duration_ms": 0
                    }
                
                stats = calc_stats[calc_type]
                stats["count"] += 1
                
                duration = entry.details.get("duration_ms", 0)
                stats["total_duration_ms"] += duration
                
                if entry.details.get("cache_hit"):
                    stats["cache_hits"] += 1
                
                stats["avg_duration_ms"] = stats["total_duration_ms"] / stats["count"]
                stats["cache_hit_rate"] = stats["cache_hits"] / stats["count"]
            
            return APIResponse.success({
                "calculation_stats": calc_stats,
                "recent_calculations": [
                    {
                        "timestamp": e.timestamp.isoformat(),
                        "type": e.details.get("calculation_type"),
                        "user": e.user,
                        "duration_ms": e.details.get("duration_ms"),
                        "cache_hit": e.details.get("cache_hit")
                    }
                    for e in entries[:10]
                ]
            })
            
        except Exception as e:
            logger.error(f"Calculation history error: {e}")
            return APIResponse.error("Failed to get calculation history", 500)
    
    @staticmethod
    @log_api_call("audit/security-events")
    def get_security_events(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get security-related events (failed logins, permission denials)."""
        try:
            # Get authentication events
            auth_entries = audit_logger.search(
                event_type=AuditEventType.AUTHENTICATION,
                limit=50
            )
            
            # Get permission check events
            perm_entries = audit_logger.search(
                event_type=AuditEventType.PERMISSION_CHECK,
                limit=50
            )
            
            # Filter for failures
            failed_logins = [
                e for e in auth_entries 
                if not e.details.get("success", True)
            ]
            
            permission_denials = [
                e for e in perm_entries 
                if not e.details.get("granted", True)
            ]
            
            # Analyze patterns
            failed_by_user = {}
            for entry in failed_logins:
                user = entry.user
                if user not in failed_by_user:
                    failed_by_user[user] = 0
                failed_by_user[user] += 1
            
            return APIResponse.success({
                "failed_login_attempts": len(failed_logins),
                "permission_denials": len(permission_denials),
                "failed_logins_by_user": failed_by_user,
                "recent_security_events": [
                    {
                        "timestamp": e.timestamp.isoformat(),
                        "type": e.event_type.value,
                        "user": e.user,
                        "action": e.action,
                        "details": e.details
                    }
                    for e in (failed_logins + permission_denials)[:20]
                ]
            })
            
        except Exception as e:
            logger.error(f"Security events error: {e}")
            return APIResponse.error("Failed to get security events", 500)


# Initialize audit API instance
audit_api = AuditAPI()