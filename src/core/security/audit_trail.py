"""
Audit Trail Service for Enhanced Report System.

This module provides comprehensive audit trail functionality for FedRAMP and DoD compliance,
tracking all operations, data access, and system changes.
"""

import json
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events for categorization."""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    REPORT_GENERATION = "report_generation"
    EXPORT_OPERATION = "export_operation"
    SYSTEM_CONFIGURATION = "system_configuration"
    SECURITY_EVENT = "security_event"
    ADMIN_ACTION = "admin_action"
    API_CALL = "api_call"
    MCP_TOOL_USAGE = "mcp_tool_usage"
    MONTE_CARLO_SIMULATION = "monte_carlo_simulation"
    KNOWLEDGE_GRAPH_ACCESS = "knowledge_graph_access"
    STRATEGIC_ANALYSIS = "strategic_analysis"
    RISK_ASSESSMENT = "risk_assessment"


class AuditSeverity(Enum):
    """Severity levels for audit events."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Audit event data structure."""
    event_id: str
    timestamp: datetime
    event_type: AuditEventType
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resource: Optional[str]
    action: str
    details: Dict[str, Any]
    severity: AuditSeverity
    success: bool
    error_message: Optional[str] = None
    data_classification: Optional[str] = None
    compliance_tags: List[str] = None
    
    def __post_init__(self):
        if self.compliance_tags is None:
            self.compliance_tags = []
        if self.timestamp.tzinfo is None:
            self.timestamp = self.timestamp.replace(tzinfo=timezone.utc)


class AuditTrailService:
    """
    Comprehensive audit trail service for FedRAMP and DoD compliance.
    
    Features:
    - Real-time event logging
    - Data classification tracking
    - Compliance tagging
    - Tamper-evident logging
    - Automated retention management
    - Search and retrieval capabilities
    """
    
    def __init__(self, audit_log_path: str = "logs/audit_trail.jsonl"):
        """
        Initialize the audit trail service.
        
        Args:
            audit_log_path: Path to the audit log file
        """
        self.audit_log_path = Path(audit_log_path)
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.session_events: Dict[str, List[AuditEvent]] = {}
        self.data_classifications = {
            "PUBLIC": "public",
            "INTERNAL": "internal", 
            "CONFIDENTIAL": "confidential",
            "SECRET": "secret",
            "TOP_SECRET": "top_secret"
        }
        
        # Initialize audit log file
        self._initialize_audit_log()
        
    def _initialize_audit_log(self):
        """Initialize the audit log file with header."""
        if not self.audit_log_path.exists():
            header = {
                "audit_log_created": datetime.now(timezone.utc).isoformat(),
                "system": "DIA3 Enhanced Report System",
                "compliance": ["FedRAMP", "DoD"],
                "version": "1.0"
            }
            with open(self.audit_log_path, 'w') as f:
                f.write(json.dumps(header) + '\n')
    
    def log_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource: Optional[str] = None,
        action: str = "",
        details: Optional[Dict[str, Any]] = None,
        severity: AuditSeverity = AuditSeverity.MEDIUM,
        success: bool = True,
        error_message: Optional[str] = None,
        data_classification: Optional[str] = None,
        compliance_tags: Optional[List[str]] = None
    ) -> str:
        """
        Log an audit event.
        
        Args:
            event_type: Type of audit event
            user_id: User identifier
            session_id: Session identifier
            ip_address: IP address of the user
            user_agent: User agent string
            resource: Resource being accessed/modified
            action: Action performed
            details: Additional event details
            severity: Event severity level
            success: Whether the operation was successful
            error_message: Error message if operation failed
            data_classification: Classification of data involved
            compliance_tags: Compliance tags for the event
            
        Returns:
            Event ID of the logged event
        """
        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc)
        
        if details is None:
            details = {}
            
        if compliance_tags is None:
            compliance_tags = []
            
        # Add compliance tags based on event type
        if event_type in [AuditEventType.DATA_ACCESS, AuditEventType.DATA_MODIFICATION]:
            compliance_tags.extend(["FedRAMP", "DoD"])
        if event_type == AuditEventType.SECURITY_EVENT:
            compliance_tags.extend(["FedRAMP", "DoD", "Security"])
            
        event = AuditEvent(
            event_id=event_id,
            timestamp=timestamp,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            resource=resource,
            action=action,
            details=details,
            severity=severity,
            success=success,
            error_message=error_message,
            data_classification=data_classification,
            compliance_tags=compliance_tags
        )
        
        # Log to file
        self._write_event_to_log(event)
        
        # Store in session events
        if session_id:
            if session_id not in self.session_events:
                self.session_events[session_id] = []
            self.session_events[session_id].append(event)
            
        # Log to system logger
        log_level = self._get_log_level(severity)
        logger.log(log_level, f"Audit Event: {event_type.value} - {action} - User: {user_id}")
        
        return event_id
    
    def _write_event_to_log(self, event: AuditEvent):
        """Write audit event to log file with tamper-evident features."""
        event_dict = asdict(event)
        event_dict['timestamp'] = event.timestamp.isoformat()
        event_dict['event_type'] = event.event_type.value
        event_dict['severity'] = event.severity.value
        
        # Add hash for tamper evidence
        event_json = json.dumps(event_dict, sort_keys=True)
        event_hash = hashlib.sha256(event_json.encode()).hexdigest()
        event_dict['event_hash'] = event_hash
        
        # Write to log file
        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps(event_dict) + '\n')
    
    def _get_log_level(self, severity: AuditSeverity) -> int:
        """Convert audit severity to logging level."""
        severity_map = {
            AuditSeverity.LOW: logging.INFO,
            AuditSeverity.MEDIUM: logging.WARNING,
            AuditSeverity.HIGH: logging.ERROR,
            AuditSeverity.CRITICAL: logging.CRITICAL
        }
        return severity_map.get(severity, logging.INFO)
    
    def log_user_login(self, user_id: str, session_id: str, ip_address: str, 
                      user_agent: str, success: bool = True, 
                      error_message: Optional[str] = None) -> str:
        """Log user login event."""
        return self.log_event(
            event_type=AuditEventType.USER_LOGIN,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            action="user_login",
            details={"login_method": "password"},
            severity=AuditSeverity.MEDIUM if success else AuditSeverity.HIGH,
            success=success,
            error_message=error_message,
            compliance_tags=["FedRAMP", "DoD", "Authentication"]
        )
    
    def log_data_access(self, user_id: str, session_id: str, resource: str,
                       data_classification: str, ip_address: Optional[str] = None) -> str:
        """Log data access event."""
        return self.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            resource=resource,
            action="data_access",
            details={"access_method": "api"},
            severity=AuditSeverity.MEDIUM,
            data_classification=data_classification,
            compliance_tags=["FedRAMP", "DoD", "DataAccess"]
        )
    
    def log_report_generation(self, user_id: str, session_id: str, report_type: str,
                            report_id: str, components: List[str]) -> str:
        """Log report generation event."""
        return self.log_event(
            event_type=AuditEventType.REPORT_GENERATION,
            user_id=user_id,
            session_id=session_id,
            resource=f"report:{report_id}",
            action="report_generation",
            details={
                "report_type": report_type,
                "report_id": report_id,
                "components": components
            },
            severity=AuditSeverity.MEDIUM,
            compliance_tags=["FedRAMP", "DoD", "Reporting"]
        )
    
    def log_export_operation(self, user_id: str, session_id: str, export_format: str,
                           report_id: str, file_size: int) -> str:
        """Log export operation event."""
        return self.log_event(
            event_type=AuditEventType.EXPORT_OPERATION,
            user_id=user_id,
            session_id=session_id,
            resource=f"export:{report_id}",
            action="export_operation",
            details={
                "export_format": export_format,
                "report_id": report_id,
                "file_size": file_size
            },
            severity=AuditSeverity.MEDIUM,
            compliance_tags=["FedRAMP", "DoD", "DataExport"]
        )
    
    def log_mcp_tool_usage(self, user_id: str, session_id: str, tool_name: str,
                          parameters: Dict[str, Any], success: bool = True) -> str:
        """Log MCP tool usage event."""
        return self.log_event(
            event_type=AuditEventType.MCP_TOOL_USAGE,
            user_id=user_id,
            session_id=session_id,
            action="mcp_tool_usage",
            details={
                "tool_name": tool_name,
                "parameters": parameters
            },
            severity=AuditSeverity.MEDIUM,
            success=success,
            compliance_tags=["FedRAMP", "DoD", "ToolUsage"]
        )
    
    def log_monte_carlo_simulation(self, user_id: str, session_id: str, 
                                 simulation_id: str, parameters: Dict[str, Any]) -> str:
        """Log Monte Carlo simulation event."""
        return self.log_event(
            event_type=AuditEventType.MONTE_CARLO_SIMULATION,
            user_id=user_id,
            session_id=session_id,
            resource=f"simulation:{simulation_id}",
            action="monte_carlo_simulation",
            details={
                "simulation_id": simulation_id,
                "parameters": parameters
            },
            severity=AuditSeverity.MEDIUM,
            compliance_tags=["FedRAMP", "DoD", "Simulation"]
        )
    
    def get_session_events(self, session_id: str) -> List[AuditEvent]:
        """Get all events for a specific session."""
        return self.session_events.get(session_id, [])
    
    def get_user_events(self, user_id: str, limit: int = 100) -> List[AuditEvent]:
        """Get recent events for a specific user."""
        events = []
        with open(self.audit_log_path, 'r') as f:
            for line in f:
                try:
                    event_data = json.loads(line)
                    if event_data.get('user_id') == user_id:
                        # Convert back to AuditEvent object
                        event = self._dict_to_audit_event(event_data)
                        events.append(event)
                        if len(events) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
        return events
    
    def _dict_to_audit_event(self, event_dict: Dict[str, Any]) -> AuditEvent:
        """Convert dictionary back to AuditEvent object."""
        return AuditEvent(
            event_id=event_dict['event_id'],
            timestamp=datetime.fromisoformat(event_dict['timestamp']),
            event_type=AuditEventType(event_dict['event_type']),
            user_id=event_dict.get('user_id'),
            session_id=event_dict.get('session_id'),
            ip_address=event_dict.get('ip_address'),
            user_agent=event_dict.get('user_agent'),
            resource=event_dict.get('resource'),
            action=event_dict['action'],
            details=event_dict['details'],
            severity=AuditSeverity(event_dict['severity']),
            success=event_dict['success'],
            error_message=event_dict.get('error_message'),
            data_classification=event_dict.get('data_classification'),
            compliance_tags=event_dict.get('compliance_tags', [])
        )
    
    def search_events(self, filters: Dict[str, Any], limit: int = 100) -> List[AuditEvent]:
        """Search audit events based on filters."""
        events = []
        with open(self.audit_log_path, 'r') as f:
            for line in f:
                try:
                    event_data = json.loads(line)
                    if self._matches_filters(event_data, filters):
                        event = self._dict_to_audit_event(event_data)
                        events.append(event)
                        if len(events) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
        return events
    
    def _matches_filters(self, event_data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if event matches the given filters."""
        for key, value in filters.items():
            if key not in event_data or event_data[key] != value:
                return False
        return True
    
    def get_audit_summary(self, start_date: Optional[datetime] = None, 
                         end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get audit summary statistics."""
        total_events = 0
        events_by_type = {}
        events_by_severity = {}
        events_by_user = {}
        
        with open(self.audit_log_path, 'r') as f:
            for line in f:
                try:
                    event_data = json.loads(line)
                    event_timestamp = datetime.fromisoformat(event_data['timestamp'])
                    
                    # Apply date filters
                    if start_date and event_timestamp < start_date:
                        continue
                    if end_date and event_timestamp > end_date:
                        continue
                    
                    total_events += 1
                    
                    # Count by type
                    event_type = event_data['event_type']
                    events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
                    
                    # Count by severity
                    severity = event_data['severity']
                    events_by_severity[severity] = events_by_severity.get(severity, 0) + 1
                    
                    # Count by user
                    user_id = event_data.get('user_id', 'unknown')
                    events_by_user[user_id] = events_by_user.get(user_id, 0) + 1
                    
                except json.JSONDecodeError:
                    continue
        
        return {
            "total_events": total_events,
            "events_by_type": events_by_type,
            "events_by_severity": events_by_severity,
            "events_by_user": events_by_user,
            "date_range": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            }
        }
    
    def cleanup_old_events(self, retention_days: int = 365):
        """Clean up audit events older than retention period."""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
        temp_file = self.audit_log_path.with_suffix('.tmp')
        
        with open(self.audit_log_path, 'r') as input_file, open(temp_file, 'w') as output_file:
            for line in input_file:
                try:
                    event_data = json.loads(line)
                    event_timestamp = datetime.fromisoformat(event_data['timestamp'])
                    if event_timestamp >= cutoff_date:
                        output_file.write(line)
                except json.JSONDecodeError:
                    continue
        
        # Replace original file with filtered file
        temp_file.replace(self.audit_log_path)
        logger.info(f"Cleaned up audit events older than {retention_days} days")


# Global audit trail service instance
audit_trail_service = AuditTrailService()
