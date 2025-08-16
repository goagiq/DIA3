"""
Strategic Deception Monitoring Dashboard

Real-time dashboard for monitoring strategic deception indicators in communications.
Provides visualization, alert management, and trend analysis capabilities.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics

from loguru import logger

from src.core.error_handler import with_error_handling


@dataclass
class DashboardMetric:
    """Represents a dashboard metric."""
    metric_id: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    trend: str = "stable"  # increasing, decreasing, stable
    threshold: Optional[float] = None
    status: str = "normal"  # normal, warning, critical


@dataclass
class DeceptionAlert:
    """Represents a deception alert for the dashboard."""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    source: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeceptionTrend:
    """Represents a deception trend analysis."""
    trend_id: str
    trend_type: str
    direction: str  # increasing, decreasing, stable
    confidence: float
    description: str
    time_period: str
    data_points: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class StrategicDeceptionDashboard:
    """
    Real-time dashboard for monitoring strategic deception indicators.
    
    Features:
    - Real-time metric tracking
    - Alert management
    - Trend analysis
    - Visualization data preparation
    - Performance monitoring
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Dashboard state
        self.metrics: Dict[str, DashboardMetric] = {}
        self.alerts: List[DeceptionAlert] = []
        self.trends: List[DeceptionTrend] = []
        
        # Data storage
        self.metric_history: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=1000)  # Keep last 1000 data points
        )
        self.alert_history: deque = deque(maxlen=500)
        
        # Configuration
        self.update_interval = self.config.get('update_interval', 30)  # seconds
        self.alert_retention_days = self.config.get('alert_retention_days', 30)
        self.trend_analysis_window = self.config.get('trend_analysis_window', 24)  # hours
        
        # Dashboard status
        self.dashboard_active = False
        self.last_update = datetime.now()
        
        # Initialize default metrics
        self._initialize_default_metrics()
        
        logger.info("StrategicDeceptionDashboard initialized")
    
    def _initialize_default_metrics(self):
        """Initialize default dashboard metrics."""
        default_metrics = {
            "deception_score": {
                "name": "Overall Deception Score",
                "unit": "score",
                "threshold": 0.7
            },
            "indicators_per_hour": {
                "name": "Deception Indicators per Hour",
                "unit": "count",
                "threshold": 10
            },
            "critical_alerts": {
                "name": "Critical Alerts",
                "unit": "count",
                "threshold": 5
            },
            "pattern_confidence": {
                "name": "Pattern Confidence",
                "unit": "percentage",
                "threshold": 80
            },
            "response_time": {
                "name": "Response Time",
                "unit": "seconds",
                "threshold": 5
            }
        }
        
        for metric_id, config in default_metrics.items():
            self.metrics[metric_id] = DashboardMetric(
                metric_id=metric_id,
                metric_name=config["name"],
                value=0.0,
                unit=config["unit"],
                timestamp=datetime.now(),
                threshold=config["threshold"]
            )
    
    @with_error_handling("add_metric")
    def add_metric(self, metric_id: str, metric_name: str, value: float, unit: str, threshold: Optional[float] = None):
        """Add a new metric to the dashboard."""
        try:
            metric = DashboardMetric(
                metric_id=metric_id,
                metric_name=metric_name,
                value=value,
                unit=unit,
                timestamp=datetime.now(),
                threshold=threshold
            )
            
            self.metrics[metric_id] = metric
            self.metric_history[metric_id] = deque(maxlen=1000)
            
            logger.info(f"Added metric {metric_id}: {metric_name}")
            
        except Exception as e:
            logger.error(f"Error adding metric {metric_id}: {e}")

    @with_error_handling("update_metric")
    async def update_metric(self, metric_id: str, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Update a dashboard metric."""
        try:
            if metric_id not in self.metrics:
                logger.warning(f"Unknown metric: {metric_id}")
                return
            
            metric = self.metrics[metric_id]
            old_value = metric.value
            
            # Update metric
            metric.value = value
            metric.timestamp = datetime.now()
            
            # Calculate trend
            if old_value < value:
                metric.trend = "increasing"
            elif old_value > value:
                metric.trend = "decreasing"
            else:
                metric.trend = "stable"
            
            # Update status based on threshold
            if metric.threshold:
                if value >= metric.threshold:
                    metric.status = "critical"
                elif value >= metric.threshold * 0.8:
                    metric.status = "warning"
                else:
                    metric.status = "normal"
            
            # Store in history
            self.metric_history[metric_id].append({
                "value": value,
                "timestamp": metric.timestamp,
                "trend": metric.trend,
                "status": metric.status,
                "metadata": metadata or {}
            })
            
            logger.debug(f"Updated metric {metric_id}: {value}")
            
        except Exception as e:
            logger.error(f"Error updating metric {metric_id}: {e}")
    
    @with_error_handling("add_alert")
    async def add_alert(self, alert_type: str, severity: str, message: str, source: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a new deception alert."""
        try:
            alert = DeceptionAlert(
                alert_id=f"alert_{len(self.alerts)}_{datetime.now().timestamp()}",
                alert_type=alert_type,
                severity=severity,
                message=message,
                source=source,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            self.alerts.append(alert)
            self.alert_history.append(alert)
            
            # Clean up old alerts
            await self._cleanup_old_alerts()
            
            logger.info(f"Added alert: {alert_type} - {severity} - {message}")
            
        except Exception as e:
            logger.error(f"Error adding alert: {e}")
    
    @with_error_handling("acknowledge_alert")
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        try:
            for alert in self.alerts:
                if alert.alert_id == alert_id:
                    alert.acknowledged = True
                    logger.info(f"Acknowledged alert: {alert_id}")
                    return True
            
            logger.warning(f"Alert not found: {alert_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False
    
    @with_error_handling("resolve_alert")
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        try:
            for alert in self.alerts:
                if alert.alert_id == alert_id:
                    alert.resolved = True
                    logger.info(f"Resolved alert: {alert_id}")
                    return True
            
            logger.warning(f"Alert not found: {alert_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")
            return False
    
    @with_error_handling("analyze_trends")
    async def analyze_trends(self) -> List[DeceptionTrend]:
        """Analyze trends in deception indicators."""
        try:
            trends = []
            cutoff_time = datetime.now() - timedelta(hours=self.trend_analysis_window)
            
            for metric_id, history in self.metric_history.items():
                if not history:
                    continue
                
                # Filter recent data
                recent_data = [
                    point for point in history
                    if point["timestamp"] >= cutoff_time
                ]
                
                if len(recent_data) < 3:
                    continue
                
                # Calculate trend
                values = [point["value"] for point in recent_data]
                trend_direction = self._calculate_trend_direction(values)
                confidence = self._calculate_trend_confidence(values)
                
                trend = DeceptionTrend(
                    trend_id=f"trend_{metric_id}_{datetime.now().timestamp()}",
                    trend_type=metric_id,
                    direction=trend_direction,
                    confidence=confidence,
                    description=f"{metric_id} is {trend_direction}",
                    time_period=f"Last {self.trend_analysis_window} hours",
                    data_points=len(recent_data)
                )
                
                trends.append(trend)
            
            self.trends = trends
            logger.info(f"Analyzed {len(trends)} trends")
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return []
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values."""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression slope
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * val for i, val in enumerate(values))
        x_sq_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x_sq_sum - x_sum * x_sum)
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_trend_confidence(self, values: List[float]) -> float:
        """Calculate confidence in trend analysis."""
        if len(values) < 3:
            return 0.5
        
        # Calculate coefficient of variation
        mean_val = statistics.mean(values)
        if mean_val == 0:
            return 0.5
        
        std_dev = statistics.stdev(values)
        cv = std_dev / mean_val
        
        # Higher confidence for lower variation
        confidence = max(0.1, 1.0 - cv)
        return min(confidence, 1.0)
    
    async def _cleanup_old_alerts(self):
        """Clean up old alerts based on retention policy."""
        cutoff_time = datetime.now() - timedelta(days=self.alert_retention_days)
        
        # Remove old alerts from active list
        self.alerts = [
            alert for alert in self.alerts
            if alert.timestamp >= cutoff_time
        ]
        
        # Remove old alerts from history
        self.alert_history = deque(
            (alert for alert in self.alert_history if alert.timestamp >= cutoff_time),
            maxlen=500
        )
    
    @with_error_handling("get_dashboard_data")
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data for visualization."""
        try:
            # Update trends
            await self.analyze_trends()
            
            # Prepare metrics data
            metrics_data = {}
            for metric_id, metric in self.metrics.items():
                history = list(self.metric_history[metric_id])
                metrics_data[metric_id] = {
                    "current": {
                        "value": metric.value,
                        "unit": metric.unit,
                        "trend": metric.trend,
                        "status": metric.status,
                        "timestamp": metric.timestamp.isoformat()
                    },
                    "history": [
                        {
                            "value": point["value"],
                            "timestamp": point["timestamp"].isoformat(),
                            "trend": point["trend"],
                            "status": point["status"]
                        }
                        for point in history[-50:]  # Last 50 points
                    ]
                }
            
            # Prepare alerts data
            active_alerts = [
                {
                    "id": alert.alert_id,
                    "type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "source": alert.source,
                    "timestamp": alert.timestamp.isoformat(),
                    "acknowledged": alert.acknowledged,
                    "resolved": alert.resolved
                }
                for alert in self.alerts
                if not alert.resolved
            ]
            
            # Prepare trends data
            trends_data = [
                {
                    "id": trend.trend_id,
                    "type": trend.trend_type,
                    "direction": trend.direction,
                    "confidence": trend.confidence,
                    "description": trend.description,
                    "time_period": trend.time_period,
                    "data_points": trend.data_points
                }
                for trend in self.trends
            ]
            
            # Calculate summary statistics
            summary = {
                "total_metrics": len(self.metrics),
                "active_alerts": len([a for a in self.alerts if not a.resolved]),
                "critical_alerts": len([a for a in self.alerts if a.severity == "critical" and not a.resolved]),
                "total_trends": len(self.trends),
                "dashboard_status": "active" if self.dashboard_active else "inactive",
                "last_update": self.last_update.isoformat()
            }
            
            return {
                "summary": summary,
                "metrics": metrics_data,
                "alerts": active_alerts,
                "trends": trends_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @with_error_handling("start_dashboard")
    async def start_dashboard(self):
        """Start the dashboard monitoring."""
        if self.dashboard_active:
            logger.warning("Dashboard is already active")
            return
        
        self.dashboard_active = True
        self.last_update = datetime.now()
        logger.info("Strategic deception dashboard started")
    
    @with_error_handling("stop_dashboard")
    async def stop_dashboard(self):
        """Stop the dashboard monitoring."""
        if not self.dashboard_active:
            return
        
        self.dashboard_active = False
        logger.info("Strategic deception dashboard stopped")
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get current dashboard status."""
        return {
            "active": self.dashboard_active,
            "last_update": self.last_update.isoformat(),
            "total_metrics": len(self.metrics),
            "total_alerts": len(self.alerts),
            "total_trends": len(self.trends),
            "update_interval": self.update_interval,
            "alert_retention_days": self.alert_retention_days
        }
