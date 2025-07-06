"""Demonstration of audit logging functionality.

This script shows how audit logging works in the AI Adoption Dashboard.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import time
import json

from utils.audit_logger import audit_logger, AuditEventType, AuditSeverity


def demonstrate_audit_logging():
    """Show various audit logging capabilities."""
    
    print("=== AI Adoption Dashboard Audit Logging Demo ===\n")
    
    # 1. Log a calculation
    print("1. Logging calculation event...")
    audit_logger.log_calculation(
        calculation_type="npv",
        parameters={
            "cash_flows_count": 5,
            "discount_rate": 0.10,
            "initial_investment": 1000000
        },
        result={"npv": 250000, "profitable": True},
        user="demo_user",
        duration_ms=45.3,
        cache_hit=False
    )
    print("✓ Calculation logged\n")
    
    # 2. Log API call
    print("2. Logging API call...")
    audit_logger.log_api_call(
        endpoint="/api/financial/irr",
        method="POST",
        user="demo_user",
        status_code=200,
        duration_ms=62.1,
        ip_address="192.168.1.100"
    )
    print("✓ API call logged\n")
    
    # 3. Log authentication events
    print("3. Logging authentication events...")
    
    # Successful login
    audit_logger.log_authentication(
        action="login",
        username="admin",
        success=True,
        ip_address="192.168.1.100"
    )
    
    # Failed login
    audit_logger.log_authentication(
        action="login",
        username="hacker",
        success=False,
        ip_address="192.168.1.200",
        details={"reason": "Invalid password"}
    )
    print("✓ Authentication events logged\n")
    
    # 4. Log permission checks
    print("4. Logging permission checks...")
    audit_logger.log_permission_check(
        user="analyst1",
        permission="write:calculations",
        granted=True,
        context="NPV calculation"
    )
    
    audit_logger.log_permission_check(
        user="viewer1",
        permission="admin:users",
        granted=False,
        context="User management access"
    )
    print("✓ Permission checks logged\n")
    
    # 5. Log data export
    print("5. Logging data export...")
    audit_logger.log_data_export(
        export_type="financial_analysis",
        format="excel",
        user="analyst1",
        record_count=150,
        file_size_bytes=524288
    )
    print("✓ Data export logged\n")
    
    # 6. Log error
    print("6. Logging error event...")
    audit_logger.log_error(
        error_type="ValueError",
        error_message="Invalid discount rate: -0.5",
        user="demo_user",
        context={
            "calculation": "npv",
            "parameters": {"discount_rate": -0.5}
        }
    )
    print("✓ Error logged\n")
    
    # 7. Search audit logs
    print("7. Searching audit logs...")
    print("\n   Recent calculation events:")
    calc_entries = audit_logger.search(
        event_type=AuditEventType.CALCULATION,
        limit=5
    )
    for entry in calc_entries:
        print(f"   - {entry.timestamp.strftime('%H:%M:%S')} "
              f"{entry.action} by {entry.user} "
              f"(duration: {entry.details.get('duration_ms', 0):.1f}ms)")
    
    print("\n   Failed authentication attempts:")
    failed_auth = audit_logger.search(
        event_type=AuditEventType.AUTHENTICATION,
        severity=AuditSeverity.WARNING,
        limit=5
    )
    for entry in failed_auth:
        print(f"   - {entry.timestamp.strftime('%H:%M:%S')} "
              f"{entry.action} for {entry.user} "
              f"from {entry.details.get('ip_address', 'unknown')}")
    
    # 8. Get statistics
    print("\n8. Audit log statistics:")
    stats = audit_logger.get_stats()
    print(f"   Total entries: {stats['summary']['total_entries']}")
    print("   Entries by type:")
    for event_type, count in stats['summary']['entries_by_type'].items():
        print(f"   - {event_type}: {count}")
    
    # 9. Export logs
    print("\n9. Exporting audit logs...")
    export_file = audit_logger.export_logs(
        output_file="audit_export_demo.json",
        format="json",
        filters={
            "start_time": datetime.utcnow() - timedelta(minutes=5)
        }
    )
    print(f"✓ Logs exported to: {export_file}")
    
    # Show exported content
    with open(export_file, 'r') as f:
        exported = json.load(f)
        print(f"   Exported {len(exported)} entries")
    
    print("\n=== Demo Complete ===")
    print("\nAudit logs provide:")
    print("- Complete activity tracking")
    print("- Security monitoring")
    print("- Performance metrics")
    print("- Compliance documentation")
    print("- Debugging capabilities")


if __name__ == "__main__":
    demonstrate_audit_logging()