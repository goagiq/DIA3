"""
Strategic Deception Dashboard API

FastAPI-based web interface for the strategic deception monitoring dashboard.
Provides REST endpoints for dashboard data and real-time monitoring.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from src.core.monitoring.strategic_deception_dashboard import StrategicDeceptionDashboard
from src.agents.strategic_deception_monitoring_agent import StrategicDeceptionMonitoringAgent

# Initialize FastAPI app
app = FastAPI(
    title="Strategic Deception Monitoring Dashboard",
    description="Real-time monitoring of strategic deception indicators in communications",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize dashboard and agent
dashboard = StrategicDeceptionDashboard()
agent = StrategicDeceptionMonitoringAgent()

# HTML template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategic Deception Monitoring Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.8;
        }
        .content {
            padding: 20px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #007bff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .metric-card h3 {
            margin: 0 0 10px 0;
            color: #495057;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .metric-unit {
            font-size: 0.8em;
            color: #6c757d;
        }
        .alerts-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .alert-item {
            background: white;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #dc3545;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .alert-severity {
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8em;
        }
        .alert-severity.critical { color: #dc3545; }
        .alert-severity.high { color: #fd7e14; }
        .alert-severity.medium { color: #ffc107; }
        .alert-severity.low { color: #28a745; }
        .controls {
            background: #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn:hover {
            background: #0056b3;
        }
        .btn.danger {
            background: #dc3545;
        }
        .btn.danger:hover {
            background: #c82333;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active {
            background: #28a745;
        }
        .status-inactive {
            background: #dc3545;
        }
        .refresh-info {
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Strategic Deception Monitoring</h1>
            <p>Real-time monitoring of deception indicators in communications</p>
        </div>
        
        <div class="content">
            <div class="metrics-grid" id="metrics-grid">
                <!-- Metrics will be populated here -->
            </div>
            
            <div class="alerts-section">
                <h2>🚨 Active Alerts</h2>
                <div id="alerts-container">
                    <!-- Alerts will be populated here -->
                </div>
            </div>
            
            <div class="controls">
                <h3>🎛️ Dashboard Controls</h3>
                <button class="btn" onclick="refreshDashboard()">🔄 Refresh Dashboard</button>
                <button class="btn" onclick="addSampleAlert()">➕ Add Sample Alert</button>
                <button class="btn" onclick="toggleDashboard()">⏯️ Toggle Dashboard</button>
                <button class="btn danger" onclick="clearAlerts()">🗑️ Clear Alerts</button>
                
                <div style="margin-top: 15px;">
                    <span class="status-indicator" id="status-indicator"></span>
                    <span id="status-text">Dashboard Status</span>
                </div>
            </div>
            
            <div class="refresh-info">
                Dashboard refreshes automatically every 30 seconds
            </div>
        </div>
    </div>

    <script>
        let dashboardActive = false;
        
        async function loadDashboardData() {
            try {
                const response = await fetch('/api/dashboard/data');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }
        
        function updateDashboard(data) {
            // Update metrics
            const metricsGrid = document.getElementById('metrics-grid');
            metricsGrid.innerHTML = '';
            
            if (data.metrics) {
                Object.entries(data.metrics).forEach(([id, metric]) => {
                    const metricCard = document.createElement('div');
                    metricCard.className = 'metric-card';
                    const current = metric.current || metric;
                    metricCard.innerHTML = `
                        <h3>${id}</h3>
                        <div class="metric-value">${current.value || 0}</div>
                        <div class="metric-unit">${current.unit || ''}</div>
                    `;
                    metricsGrid.appendChild(metricCard);
                });
            }
            
            // Update alerts
            const alertsContainer = document.getElementById('alerts-container');
            alertsContainer.innerHTML = '';
            
            if (data.alerts && data.alerts.length > 0) {
                data.alerts.forEach(alert => {
                    const alertItem = document.createElement('div');
                    alertItem.className = 'alert-item';
                    alertItem.innerHTML = `
                        <div class="alert-severity ${alert.severity}">${alert.severity}</div>
                        <div style="margin-top: 5px;"><strong>${alert.message}</strong></div>
                        <div style="font-size: 0.9em; color: #6c757d; margin-top: 5px;">
                            Source: ${alert.source} | Time: ${new Date(alert.timestamp).toLocaleString()}
                        </div>
                    `;
                    alertsContainer.appendChild(alertItem);
                });
            } else {
                alertsContainer.innerHTML = '<p>No active alerts</p>';
            }
            
            // Update status
            const statusIndicator = document.getElementById('status-indicator');
            const statusText = document.getElementById('status-text');
            
            if (data.summary && data.summary.dashboard_status === 'active') {
                statusIndicator.className = 'status-indicator status-active';
                statusText.textContent = 'Dashboard Active';
                dashboardActive = true;
            } else {
                statusIndicator.className = 'status-indicator status-inactive';
                statusText.textContent = 'Dashboard Inactive';
                dashboardActive = false;
            }
        }
        
        async function refreshDashboard() {
            await loadDashboardData();
        }
        
        async function addSampleAlert() {
            try {
                const response = await fetch('/api/dashboard/add-sample-alert', {
                    method: 'POST'
                });
                if (response.ok) {
                    await loadDashboardData();
                }
            } catch (error) {
                console.error('Error adding sample alert:', error);
            }
        }
        
        async function toggleDashboard() {
            try {
                const endpoint = dashboardActive ? '/api/dashboard/stop' : '/api/dashboard/start';
                const response = await fetch(endpoint, { method: 'POST' });
                if (response.ok) {
                    await loadDashboardData();
                }
            } catch (error) {
                console.error('Error toggling dashboard:', error);
            }
        }
        
        async function clearAlerts() {
            try {
                const response = await fetch('/api/dashboard/clear-alerts', { method: 'POST' });
                if (response.ok) {
                    await loadDashboardData();
                }
            } catch (error) {
                console.error('Error clearing alerts:', error);
            }
        }
        
        // Load initial data
        loadDashboardData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadDashboardData, 30000);
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Serve the main dashboard HTML page."""
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/api/dashboard/data")
async def get_dashboard_data():
    """Get current dashboard data."""
    try:
        return await dashboard.get_dashboard_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/status")
async def get_dashboard_status():
    """Get dashboard status."""
    try:
        return dashboard.get_dashboard_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dashboard/start")
async def start_dashboard():
    """Start the dashboard."""
    try:
        await dashboard.start_dashboard()
        return {"message": "Dashboard started successfully", "status": "active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dashboard/stop")
async def stop_dashboard():
    """Stop the dashboard."""
    try:
        await dashboard.stop_dashboard()
        return {"message": "Dashboard stopped successfully", "status": "inactive"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dashboard/add-sample-alert")
async def add_sample_alert():
    """Add a sample alert for demonstration."""
    try:
        await dashboard.add_alert(
            "sample_alert",
            "medium",
            "Sample deception indicator detected",
            "demo_source"
        )
        return {"message": "Sample alert added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dashboard/clear-alerts")
async def clear_alerts():
    """Clear all alerts."""
    try:
        dashboard.alerts.clear()
        return {"message": "All alerts cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dashboard/acknowledge-alert/{alert_id}")
async def acknowledge_alert(alert_id: str):
    """Acknowledge a specific alert."""
    try:
        await dashboard.acknowledge_alert(alert_id)
        return {"message": f"Alert {alert_id} acknowledged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze")
async def analyze_communication(request: Dict[str, Any]):
    """Analyze communication for deception indicators."""
    try:
        # This would integrate with the monitoring agent
        # For now, return a sample analysis
        return {
            "deception_score": 0.75,
            "indicators": [
                {"type": "linguistic", "confidence": 0.8, "description": "Evasive language detected"},
                {"type": "strategic", "confidence": 0.6, "description": "Misdirection pattern identified"}
            ],
            "recommendations": [
                "Monitor for additional linguistic patterns",
                "Cross-reference with historical communications"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_dashboard_server(host: str = "localhost", port: int = 8505):
    """Start the dashboard server."""
    print(f"🚀 Starting Strategic Deception Dashboard Server")
    print(f"📊 Dashboard will be available at: http://{host}:{port}")
    print(f"🔗 API documentation at: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_dashboard_server()
