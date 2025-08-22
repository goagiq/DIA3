"""
Real-time Monitoring for Data.gov Integration - Phase 3
Implements live data dashboards, alert systems, and trend monitoring capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import time
from collections import deque, defaultdict
import threading
from dataclasses import dataclass, asdict
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class Alert:
    """Alert data structure."""
    id: str
    type: str
    severity: str
    message: str
    timestamp: datetime
    data: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class Metric:
    """Metric data structure."""
    name: str
    value: float
    timestamp: datetime
    unit: str = ""
    metadata: Dict[str, Any] = None

@dataclass
class Dashboard:
    """Dashboard data structure."""
    id: str
    name: str
    metrics: List[Metric]
    alerts: List[Alert]
    last_updated: datetime
    status: str = "active"

class RealTimeMonitoringEngine:
    """Real-time monitoring engine for Data.gov data analysis."""
    
    def __init__(self):
        self.dashboards = {}
        self.alerts = deque(maxlen=1000)  # Keep last 1000 alerts
        self.metrics_history = defaultdict(lambda: deque(maxlen=10000))  # Keep last 10000 metrics
        self.alert_callbacks = []
        self.monitoring_tasks = {}
        self.alert_rules = {}
        self.thresholds = {}
        self.is_running = False
        self.monitoring_thread = None
        
        # Initialize default alert rules
        self._initialize_default_rules()
        
        # Performance tracking
        self.performance_metrics = {
            "total_alerts": 0,
            "active_alerts": 0,
            "metrics_processed": 0,
            "last_alert_time": None,
            "uptime_start": datetime.now()
        }
    
    def _initialize_default_rules(self):
        """Initialize default alert rules."""
        self.alert_rules = {
            "data_freshness": {
                "enabled": True,
                "threshold": 3600,  # 1 hour
                "severity": "warning",
                "message": "Data is older than {threshold} seconds"
            },
            "api_response_time": {
                "enabled": True,
                "threshold": 30,  # 30 seconds
                "severity": "error",
                "message": "API response time exceeded {threshold} seconds"
            },
            "data_quality": {
                "enabled": True,
                "threshold": 0.8,  # 80% quality
                "severity": "warning",
                "message": "Data quality below {threshold}%"
            },
            "anomaly_detection": {
                "enabled": True,
                "threshold": 0.1,  # 10% anomaly rate
                "severity": "warning",
                "message": "Anomaly rate above {threshold}%"
            },
            "trend_change": {
                "enabled": True,
                "threshold": 0.2,  # 20% change
                "severity": "info",
                "message": "Significant trend change detected: {change}%"
            }
        }
    
    async def start_monitoring(self):
        """Start the real-time monitoring system."""
        try:
            logger.info("Starting real-time monitoring system...")
            self.is_running = True
            
            # Start monitoring thread
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            logger.info("Real-time monitoring system started successfully")
            return {"status": "success", "message": "Monitoring system started"}
            
        except Exception as e:
            logger.error(f"Error starting monitoring system: {e}")
            return {"status": "error", "message": str(e)}
    
    async def stop_monitoring(self):
        """Stop the real-time monitoring system."""
        try:
            logger.info("Stopping real-time monitoring system...")
            self.is_running = False
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            logger.info("Real-time monitoring system stopped")
            return {"status": "success", "message": "Monitoring system stopped"}
            
        except Exception as e:
            logger.error(f"Error stopping monitoring system: {e}")
            return {"status": "error", "message": str(e)}
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_running:
            try:
                # Process monitoring tasks
                for task_id, task in self.monitoring_tasks.items():
                    if task['active'] and time.time() - task['last_run'] >= task['interval']:
                        asyncio.run(self._execute_monitoring_task(task_id, task))
                
                # Update performance metrics
                self._update_performance_metrics()
                
                # Sleep for monitoring interval
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Wait longer on error
    
    async def _execute_monitoring_task(self, task_id: str, task: Dict[str, Any]):
        """Execute a monitoring task."""
        try:
            task['last_run'] = time.time()
            
            # Execute the monitoring function
            if task['function']:
                result = await task['function']()
                
                # Process results and generate alerts
                await self._process_monitoring_results(task_id, result)
                
        except Exception as e:
            logger.error(f"Error executing monitoring task {task_id}: {e}")
            await self._create_alert(
                "monitoring_error",
                "error",
                f"Monitoring task {task_id} failed: {str(e)}",
                {"task_id": task_id, "error": str(e)}
            )
    
    async def _process_monitoring_results(self, task_id: str, results: Dict[str, Any]):
        """Process monitoring results and generate alerts."""
        try:
            if results.get('status') != 'success':
                await self._create_alert(
                    "monitoring_failure",
                    "error",
                    f"Monitoring task {task_id} returned failure",
                    {"task_id": task_id, "results": results}
                )
                return
            
            # Check data freshness
            if 'last_update' in results:
                await self._check_data_freshness(results['last_update'])
            
            # Check API response time
            if 'response_time' in results:
                await self._check_api_response_time(results['response_time'])
            
            # Check data quality
            if 'data_quality' in results:
                await self._check_data_quality(results['data_quality'])
            
            # Check for anomalies
            if 'anomaly_rate' in results:
                await self._check_anomaly_rate(results['anomaly_rate'])
            
            # Check for trend changes
            if 'trend_change' in results:
                await self._check_trend_change(results['trend_change'])
            
        except Exception as e:
            logger.error(f"Error processing monitoring results: {e}")
    
    async def add_monitoring_task(self, task_id: str, function: Callable, 
                                interval: int = 300, active: bool = True) -> Dict[str, Any]:
        """Add a monitoring task."""
        try:
            self.monitoring_tasks[task_id] = {
                'function': function,
                'interval': interval,
                'active': active,
                'last_run': 0,
                'created_at': datetime.now()
            }
            
            logger.info(f"Added monitoring task: {task_id}")
            return {"status": "success", "task_id": task_id}
            
        except Exception as e:
            logger.error(f"Error adding monitoring task: {e}")
            return {"status": "error", "message": str(e)}
    
    async def remove_monitoring_task(self, task_id: str) -> Dict[str, Any]:
        """Remove a monitoring task."""
        try:
            if task_id in self.monitoring_tasks:
                del self.monitoring_tasks[task_id]
                logger.info(f"Removed monitoring task: {task_id}")
                return {"status": "success", "task_id": task_id}
            else:
                return {"status": "error", "message": f"Task {task_id} not found"}
                
        except Exception as e:
            logger.error(f"Error removing monitoring task: {e}")
            return {"status": "error", "message": str(e)}
    
    async def create_dashboard(self, dashboard_id: str, name: str) -> Dict[str, Any]:
        """Create a new dashboard."""
        try:
            dashboard = Dashboard(
                id=dashboard_id,
                name=name,
                metrics=[],
                alerts=[],
                last_updated=datetime.now()
            )
            
            self.dashboards[dashboard_id] = dashboard
            logger.info(f"Created dashboard: {dashboard_id}")
            return {"status": "success", "dashboard_id": dashboard_id}
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            return {"status": "error", "message": str(e)}
    
    async def add_metric_to_dashboard(self, dashboard_id: str, metric: Metric) -> Dict[str, Any]:
        """Add a metric to a dashboard."""
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            dashboard = self.dashboards[dashboard_id]
            dashboard.metrics.append(metric)
            dashboard.last_updated = datetime.now()
            
            # Store in history
            self.metrics_history[metric.name].append(metric)
            
            # Update performance metrics
            self.performance_metrics["metrics_processed"] += 1
            
            logger.debug(f"Added metric {metric.name} to dashboard {dashboard_id}")
            return {"status": "success", "metric_name": metric.name}
            
        except Exception as e:
            logger.error(f"Error adding metric to dashboard: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _create_alert(self, alert_type: str, severity: str, message: str, 
                          data: Dict[str, Any] = None) -> Alert:
        """Create a new alert."""
        try:
            alert = Alert(
                id=f"{alert_type}_{int(time.time())}",
                type=alert_type,
                severity=severity,
                message=message,
                timestamp=datetime.now(),
                data=data or {}
            )
            
            self.alerts.append(alert)
            
            # Add to active dashboards
            for dashboard in self.dashboards.values():
                dashboard.alerts.append(alert)
                dashboard.last_updated = datetime.now()
            
            # Update performance metrics
            self.performance_metrics["total_alerts"] += 1
            self.performance_metrics["active_alerts"] += 1
            self.performance_metrics["last_alert_time"] = datetime.now()
            
            # Trigger alert callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")
            
            logger.info(f"Created alert: {alert.id} - {message}")
            return alert
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    async def _check_data_freshness(self, last_update: datetime):
        """Check data freshness and create alert if needed."""
        try:
            rule = self.alert_rules.get("data_freshness")
            if not rule or not rule["enabled"]:
                return
            
            age_seconds = (datetime.now() - last_update).total_seconds()
            if age_seconds > rule["threshold"]:
                await self._create_alert(
                    "data_freshness",
                    rule["severity"],
                    rule["message"].format(threshold=rule["threshold"]),
                    {"age_seconds": age_seconds, "threshold": rule["threshold"]}
                )
                
        except Exception as e:
            logger.error(f"Error checking data freshness: {e}")
    
    async def _check_api_response_time(self, response_time: float):
        """Check API response time and create alert if needed."""
        try:
            rule = self.alert_rules.get("api_response_time")
            if not rule or not rule["enabled"]:
                return
            
            if response_time > rule["threshold"]:
                await self._create_alert(
                    "api_response_time",
                    rule["severity"],
                    rule["message"].format(threshold=rule["threshold"]),
                    {"response_time": response_time, "threshold": rule["threshold"]}
                )
                
        except Exception as e:
            logger.error(f"Error checking API response time: {e}")
    
    async def _check_data_quality(self, quality_score: float):
        """Check data quality and create alert if needed."""
        try:
            rule = self.alert_rules.get("data_quality")
            if not rule or not rule["enabled"]:
                return
            
            if quality_score < rule["threshold"]:
                await self._create_alert(
                    "data_quality",
                    rule["severity"],
                    rule["message"].format(threshold=rule["threshold"] * 100),
                    {"quality_score": quality_score, "threshold": rule["threshold"]}
                )
                
        except Exception as e:
            logger.error(f"Error checking data quality: {e}")
    
    async def _check_anomaly_rate(self, anomaly_rate: float):
        """Check anomaly rate and create alert if needed."""
        try:
            rule = self.alert_rules.get("anomaly_detection")
            if not rule or not rule["enabled"]:
                return
            
            if anomaly_rate > rule["threshold"]:
                await self._create_alert(
                    "anomaly_detection",
                    rule["severity"],
                    rule["message"].format(threshold=rule["threshold"] * 100),
                    {"anomaly_rate": anomaly_rate, "threshold": rule["threshold"]}
                )
                
        except Exception as e:
            logger.error(f"Error checking anomaly rate: {e}")
    
    async def _check_trend_change(self, trend_change: float):
        """Check trend change and create alert if needed."""
        try:
            rule = self.alert_rules.get("trend_change")
            if not rule or not rule["enabled"]:
                return
            
            if abs(trend_change) > rule["threshold"]:
                await self._create_alert(
                    "trend_change",
                    rule["severity"],
                    rule["message"].format(change=trend_change * 100),
                    {"trend_change": trend_change, "threshold": rule["threshold"]}
                )
                
        except Exception as e:
            logger.error(f"Error checking trend change: {e}")
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard data."""
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            dashboard = self.dashboards[dashboard_id]
            
            return {
                "status": "success",
                "dashboard": {
                    "id": dashboard.id,
                    "name": dashboard.name,
                    "status": dashboard.status,
                    "last_updated": dashboard.last_updated.isoformat(),
                    "metrics": [asdict(metric) for metric in dashboard.metrics[-50:]],  # Last 50 metrics
                    "alerts": [asdict(alert) for alert in dashboard.alerts[-20:]]  # Last 20 alerts
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_metrics_history(self, metric_name: str, limit: int = 100) -> Dict[str, Any]:
        """Get metrics history for a specific metric."""
        try:
            if metric_name not in self.metrics_history:
                return {"status": "error", "message": f"Metric {metric_name} not found"}
            
            metrics = list(self.metrics_history[metric_name])[-limit:]
            
            return {
                "status": "success",
                "metric_name": metric_name,
                "metrics": [asdict(metric) for metric in metrics],
                "count": len(metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics history: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_alerts(self, severity: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get alerts with optional filtering."""
        try:
            alerts = list(self.alerts)
            
            # Filter by severity if specified
            if severity:
                alerts = [alert for alert in alerts if alert.severity == severity]
            
            # Get recent alerts
            recent_alerts = alerts[-limit:]
            
            return {
                "status": "success",
                "alerts": [asdict(alert) for alert in recent_alerts],
                "total_alerts": len(alerts),
                "filtered_count": len(recent_alerts)
            }
            
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            return {"status": "error", "message": str(e)}
    
    async def acknowledge_alert(self, alert_id: str) -> Dict[str, Any]:
        """Acknowledge an alert."""
        try:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    logger.info(f"Acknowledged alert: {alert_id}")
                    return {"status": "success", "alert_id": alert_id}
            
            return {"status": "error", "message": f"Alert {alert_id} not found"}
            
        except Exception as e:
            logger.error(f"Error acknowledging alert: {e}")
            return {"status": "error", "message": str(e)}
    
    async def resolve_alert(self, alert_id: str) -> Dict[str, Any]:
        """Resolve an alert."""
        try:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.resolved = True
                    self.performance_metrics["active_alerts"] -= 1
                    logger.info(f"Resolved alert: {alert_id}")
                    return {"status": "success", "alert_id": alert_id}
            
            return {"status": "error", "message": f"Alert {alert_id} not found"}
            
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return {"status": "error", "message": str(e)}
    
    async def update_alert_rule(self, rule_name: str, **kwargs) -> Dict[str, Any]:
        """Update an alert rule."""
        try:
            if rule_name not in self.alert_rules:
                return {"status": "error", "message": f"Rule {rule_name} not found"}
            
            rule = self.alert_rules[rule_name]
            rule.update(kwargs)
            
            logger.info(f"Updated alert rule: {rule_name}")
            return {"status": "success", "rule_name": rule_name}
            
        except Exception as e:
            logger.error(f"Error updating alert rule: {e}")
            return {"status": "error", "message": str(e)}
    
    async def add_alert_callback(self, callback: Callable) -> Dict[str, Any]:
        """Add an alert callback function."""
        try:
            self.alert_callbacks.append(callback)
            logger.info("Added alert callback")
            return {"status": "success", "callbacks_count": len(self.alert_callbacks)}
            
        except Exception as e:
            logger.error(f"Error adding alert callback: {e}")
            return {"status": "error", "message": str(e)}
    
    def _update_performance_metrics(self):
        """Update performance metrics."""
        try:
            # Calculate uptime
            uptime = datetime.now() - self.performance_metrics["uptime_start"]
            self.performance_metrics["uptime_seconds"] = uptime.total_seconds()
            
            # Calculate alert rate
            if self.performance_metrics["last_alert_time"]:
                time_since_last_alert = (datetime.now() - self.performance_metrics["last_alert_time"]).total_seconds()
                self.performance_metrics["time_since_last_alert"] = time_since_last_alert
            
        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            return {
                "status": "success",
                "performance_metrics": self.performance_metrics.copy(),
                "monitoring_tasks": {
                    task_id: {
                        "active": task["active"],
                        "interval": task["interval"],
                        "last_run": task["last_run"],
                        "created_at": task["created_at"].isoformat()
                    }
                    for task_id, task in self.monitoring_tasks.items()
                },
                "dashboards_count": len(self.dashboards),
                "alert_rules": self.alert_rules
            }
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {"status": "error", "message": str(e)}
    
    async def export_monitoring_data(self, format: str = "json") -> Dict[str, Any]:
        """Export monitoring data."""
        try:
            if format.lower() == "json":
                export_data = {
                    "dashboards": {
                        dashboard_id: {
                            "id": dashboard.id,
                            "name": dashboard.name,
                            "status": dashboard.status,
                            "last_updated": dashboard.last_updated.isoformat(),
                            "metrics_count": len(dashboard.metrics),
                            "alerts_count": len(dashboard.alerts)
                        }
                        for dashboard_id, dashboard in self.dashboards.items()
                    },
                    "alerts": [asdict(alert) for alert in list(self.alerts)[-100:]],  # Last 100 alerts
                    "performance_metrics": self.performance_metrics,
                    "export_timestamp": datetime.now().isoformat()
                }
                
                return {
                    "status": "success",
                    "format": format,
                    "data": export_data
                }
            else:
                return {"status": "error", "message": f"Unsupported format: {format}"}
                
        except Exception as e:
            logger.error(f"Error exporting monitoring data: {e}")
            return {"status": "error", "message": str(e)}
