# System Monitoring Tool

## Overview
The System Monitoring tool provides comprehensive capabilities for monitoring system health, performance metrics, resource utilization, and operational status to support proactive system management and infrastructure monitoring.

## Purpose
To monitor system health, track performance metrics, detect anomalies, monitor resource utilization, and provide real-time system status information for proactive maintenance, capacity planning, and operational excellence.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **psutil** (>=5.9.0) - System and process utilities
- **GPUtil** (>=1.4.0) - GPU monitoring
- **netifaces** (>=0.11.0) - Network interface information
- **speedtest-cli** (>=2.1.0) - Internet speed testing
- **plotly** (>=5.15.0) - Interactive visualizations
- **dash** (>=2.14.0) - Interactive dashboards
- **streamlit** (>=1.28.0) - Web application framework
- **redis** (>=4.6.0) - Caching and data storage
- **influxdb** (>=5.3.0) - Time series database
- **prometheus_client** (>=0.17.0) - Prometheus metrics
- **schedule** (>=1.2.0) - Task scheduling
- **requests** (>=2.31.0) - HTTP requests
- **paramiko** (>=3.3.0) - SSH connections
- **docker** (>=6.1.0) - Docker container monitoring
- **kubernetes** (>=28.0.0) - Kubernetes monitoring

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "monitoring_config": {
      "type": "object",
      "properties": {
        "monitoring_interval": {"type": "integer"},
        "metrics_to_monitor": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["cpu", "memory", "disk", "network", "gpu", "processes", "system_load", "temperature"]
          }
        },
        "thresholds": {
          "type": "object",
          "properties": {
            "cpu_usage": {"type": "number"},
            "memory_usage": {"type": "number"},
            "disk_usage": {"type": "number"},
            "network_latency": {"type": "number"}
          }
        }
      }
    },
    "alert_config": {
      "type": "object",
      "properties": {
        "enable_alerts": {"type": "boolean"},
        "alert_channels": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["email", "slack", "webhook", "sms"]
          }
        },
        "alert_thresholds": {
          "type": "object",
          "additionalProperties": {"type": "number"}
        }
      }
    }
  },
  "required": ["monitoring_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "system_metrics": {
      "type": "object",
      "properties": {
        "cpu_metrics": {
          "type": "object",
          "properties": {
            "cpu_percent": {"type": "number"},
            "cpu_count": {"type": "integer"},
            "cpu_freq": {"type": "object"},
            "cpu_stats": {"type": "object"}
          }
        },
        "memory_metrics": {
          "type": "object",
          "properties": {
            "memory_percent": {"type": "number"},
            "memory_available": {"type": "number"},
            "memory_used": {"type": "number"},
            "memory_total": {"type": "number"}
          }
        },
        "disk_metrics": {
          "type": "object",
          "properties": {
            "disk_usage": {"type": "object"},
            "disk_io": {"type": "object"},
            "disk_partitions": {"type": "array"}
          }
        },
        "network_metrics": {
          "type": "object",
          "properties": {
            "network_io": {"type": "object"},
            "network_connections": {"type": "integer"},
            "network_interfaces": {"type": "array"}
          }
        },
        "gpu_metrics": {
          "type": "object",
          "properties": {
            "gpu_count": {"type": "integer"},
            "gpu_utilization": {"type": "array"},
            "gpu_memory": {"type": "array"},
            "gpu_temperature": {"type": "array"}
          }
        }
      }
    },
    "system_status": {
      "type": "object",
      "properties": {
        "overall_health": {"type": "string"},
        "health_score": {"type": "number"},
        "alerts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "metric": {"type": "string"},
              "value": {"type": "number"},
              "threshold": {"type": "number"},
              "severity": {"type": "string"},
              "timestamp": {"type": "string"}
            }
          }
        }
      }
    },
    "performance_analysis": {
      "type": "object",
      "properties": {
        "bottlenecks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "component": {"type": "string"},
              "issue": {"type": "string"},
              "impact": {"type": "string"},
              "recommendation": {"type": "string"}
            }
          }
        },
        "trends": {
          "type": "object",
          "properties": {
            "cpu_trend": {"type": "string"},
            "memory_trend": {"type": "string"},
            "disk_trend": {"type": "string"}
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "system_dashboard": {"type": "string"},
        "performance_charts": {"type": "string"},
        "alert_history": {"type": "string"}
      }
    },
    "monitoring_insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "insight": {"type": "string"},
          "metric": {"type": "string"},
          "value": {"type": "number"},
          "trend": {"type": "string"},
          "action_required": {"type": "boolean"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for system monitoring in seconds"
    }
  }
}
```

## Intended Use
- **System Health Monitoring**: Monitor overall system health and performance
- **Resource Utilization Tracking**: Track CPU, memory, disk, and network usage
- **Performance Analysis**: Identify bottlenecks and performance issues
- **Capacity Planning**: Monitor resource trends for capacity planning
- **Alert Management**: Set up and manage system alerts
- **Real-time Monitoring**: Provide real-time system status information

## Limitations
- Requires appropriate system permissions for monitoring
- Some metrics may not be available on all platforms
- GPU monitoring requires specific hardware and drivers
- Network monitoring may be limited by firewall settings

## Safety
- Ensure monitoring doesn't impact system performance
- Handle sensitive system information appropriately
- Respect system resource limits
- Implement proper error handling for monitoring failures

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn psutil GPUtil netifaces plotly dash streamlit
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import psutil
   import GPUtil
   import plotly.express as px
   ```

### Usage

#### Basic System Monitoring
```python
import psutil
import pandas as pd
import numpy as np
from datetime import datetime
import time

class SystemMonitor:
    def __init__(self):
        """Initialize system monitor"""
        self.metrics_history = []
    
    def get_cpu_metrics(self):
        """Get CPU metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            'cpu_stats': psutil.cpu_stats()._asdict()
        }
    
    def get_memory_metrics(self):
        """Get memory metrics"""
        memory = psutil.virtual_memory()
        return {
            'memory_percent': memory.percent,
            'memory_available': memory.available,
            'memory_used': memory.used,
            'memory_total': memory.total,
            'memory_free': memory.free
        }
    
    def get_disk_metrics(self):
        """Get disk metrics"""
        disk_usage = {}
        disk_io = psutil.disk_io_counters()
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.device] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except PermissionError:
                continue
        
        return {
            'disk_usage': disk_usage,
            'disk_io': disk_io._asdict() if disk_io else {}
        }
    
    def get_network_metrics(self):
        """Get network metrics"""
        network_io = psutil.net_io_counters()
        network_connections = len(psutil.net_connections())
        
        return {
            'network_io': network_io._asdict() if network_io else {},
            'network_connections': network_connections
        }
    
    def get_system_metrics(self):
        """Get all system metrics"""
        metrics = {
            'timestamp': datetime.now(),
            'cpu': self.get_cpu_metrics(),
            'memory': self.get_memory_metrics(),
            'disk': self.get_disk_metrics(),
            'network': self.get_network_metrics()
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def monitor_continuously(self, interval=60, duration=None):
        """Monitor system continuously"""
        start_time = time.time()
        
        while True:
            try:
                metrics = self.get_system_metrics()
                print(f"CPU: {metrics['cpu']['cpu_percent']}%, "
                      f"Memory: {metrics['memory']['memory_percent']}%, "
                      f"Timestamp: {metrics['timestamp']}")
                
                if duration and (time.time() - start_time) > duration:
                    break
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("Monitoring stopped by user")
                break
            except Exception as e:
                print(f"Error during monitoring: {e}")
                time.sleep(interval)

# Usage example
monitor = SystemMonitor()
metrics = monitor.get_system_metrics()
print("System Metrics:", metrics)
```

#### Performance Analysis and Alerts
```python
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

class PerformanceAnalyzer:
    def __init__(self, history_size=100):
        """Initialize performance analyzer"""
        self.history_size = history_size
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.disk_history = deque(maxlen=history_size)
        self.timestamps = deque(maxlen=history_size)
    
    def add_metrics(self, metrics):
        """Add metrics to history"""
        self.timestamps.append(metrics['timestamp'])
        self.cpu_history.append(metrics['cpu']['cpu_percent'])
        self.memory_history.append(metrics['memory']['memory_percent'])
        
        # Get disk usage for main partition
        disk_usage = list(metrics['disk']['disk_usage'].values())[0]['percent']
        self.disk_history.append(disk_usage)
    
    def analyze_performance(self):
        """Analyze system performance"""
        if len(self.cpu_history) < 10:
            return {"status": "insufficient_data"}
        
        analysis = {
            'cpu_analysis': self._analyze_cpu(),
            'memory_analysis': self._analyze_memory(),
            'disk_analysis': self._analyze_disk(),
            'overall_health': self._calculate_health_score()
        }
        
        return analysis
    
    def _analyze_cpu(self):
        """Analyze CPU performance"""
        cpu_values = list(self.cpu_history)
        avg_cpu = np.mean(cpu_values)
        max_cpu = max(cpu_values)
        
        if avg_cpu > 80:
            status = "critical"
        elif avg_cpu > 60:
            status = "warning"
        else:
            status = "normal"
        
        return {
            'average_usage': avg_cpu,
            'max_usage': max_cpu,
            'status': status,
            'trend': self._calculate_trend(cpu_values)
        }
    
    def _analyze_memory(self):
        """Analyze memory performance"""
        memory_values = list(self.memory_history)
        avg_memory = np.mean(memory_values)
        max_memory = max(memory_values)
        
        if avg_memory > 85:
            status = "critical"
        elif avg_memory > 70:
            status = "warning"
        else:
            status = "normal"
        
        return {
            'average_usage': avg_memory,
            'max_usage': max_memory,
            'status': status,
            'trend': self._calculate_trend(memory_values)
        }
    
    def _analyze_disk(self):
        """Analyze disk performance"""
        disk_values = list(self.disk_history)
        avg_disk = np.mean(disk_values)
        max_disk = max(disk_values)
        
        if avg_disk > 90:
            status = "critical"
        elif avg_disk > 80:
            status = "warning"
        else:
            status = "normal"
        
        return {
            'average_usage': avg_disk,
            'max_usage': max_disk,
            'status': status,
            'trend': self._calculate_trend(disk_values)
        }
    
    def _calculate_trend(self, values):
        """Calculate trend of values"""
        if len(values) < 2:
            return "stable"
        
        recent_avg = np.mean(values[-5:])
        older_avg = np.mean(values[:5])
        
        if recent_avg > older_avg + 10:
            return "increasing"
        elif recent_avg < older_avg - 10:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_health_score(self):
        """Calculate overall system health score"""
        cpu_status = self._analyze_cpu()['status']
        memory_status = self._analyze_memory()['status']
        disk_status = self._analyze_disk()['status']
        
        status_scores = {'normal': 100, 'warning': 60, 'critical': 20}
        
        avg_score = (status_scores[cpu_status] + 
                    status_scores[memory_status] + 
                    status_scores[disk_status]) / 3
        
        if avg_score >= 80:
            health = "excellent"
        elif avg_score >= 60:
            health = "good"
        elif avg_score >= 40:
            health = "fair"
        else:
            health = "poor"
        
        return {
            'score': avg_score,
            'health': health,
            'cpu_status': cpu_status,
            'memory_status': memory_status,
            'disk_status': disk_status
        }

def visualize_performance(analyzer):
    """Visualize performance metrics"""
    if len(analyzer.cpu_history) < 5:
        print("Insufficient data for visualization")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('System Performance Monitoring', fontsize=16)
    
    # CPU Usage
    axes[0, 0].plot(analyzer.timestamps, analyzer.cpu_history, 'b-', linewidth=2)
    axes[0, 0].set_title('CPU Usage')
    axes[0, 0].set_ylabel('CPU %')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Memory Usage
    axes[0, 1].plot(analyzer.timestamps, analyzer.memory_history, 'r-', linewidth=2)
    axes[0, 1].set_title('Memory Usage')
    axes[0, 1].set_ylabel('Memory %')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Disk Usage
    axes[1, 0].plot(analyzer.timestamps, analyzer.disk_history, 'g-', linewidth=2)
    axes[1, 0].set_title('Disk Usage')
    axes[1, 0].set_ylabel('Disk %')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Performance Summary
    analysis = analyzer.analyze_performance()
    health = analysis['overall_health']
    
    summary_text = f"""
    Overall Health: {health['health'].title()} ({health['score']:.1f}/100)
    
    CPU: {analysis['cpu_analysis']['status'].title()}
    Memory: {analysis['memory_analysis']['status'].title()}
    Disk: {analysis['disk_analysis']['status'].title()}
    """
    
    axes[1, 1].text(0.1, 0.5, summary_text, transform=axes[1, 1].transAxes,
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    axes[1, 1].set_title('Performance Summary')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('system_performance.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
monitor = SystemMonitor()
analyzer = PerformanceAnalyzer()

# Collect metrics for 5 minutes
for _ in range(5):
    metrics = monitor.get_system_metrics()
    analyzer.add_metrics(metrics)
    time.sleep(60)

# Analyze and visualize
analysis = analyzer.analyze_performance()
print("Performance Analysis:", analysis)

visualize_performance(analyzer)
```

### Error Handling
- Handle permission errors for system monitoring
- Manage monitoring failures gracefully
- Implement retry mechanisms for failed metrics collection
- Validate system compatibility and requirements

### Monitoring
- Track monitoring system performance and accuracy
- Monitor alert effectiveness and false positives
- Review system health trends and patterns
- Validate performance analysis accuracy

### Best Practices
1. **Resource Management**: Ensure monitoring doesn't impact system performance
2. **Data Storage**: Use appropriate storage for historical metrics
3. **Alert Configuration**: Set up meaningful thresholds and alert channels
4. **Performance Analysis**: Regular analysis of system performance trends
5. **Capacity Planning**: Use monitoring data for capacity planning
6. **Security**: Secure monitoring data and access
7. **Documentation**: Document monitoring configurations and procedures
8. **Automation**: Automate monitoring and alert responses where possible
