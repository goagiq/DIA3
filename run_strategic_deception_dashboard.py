#!/usr/bin/env python3
"""
Strategic Deception Dashboard Runner

Simple script to run and interact with the strategic deception monitoring dashboard.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.monitoring.strategic_deception_dashboard import StrategicDeceptionDashboard
from src.agents.strategic_deception_monitoring_agent import StrategicDeceptionMonitoringAgent


async def main():
    """Main function to run the strategic deception dashboard."""
    print("🚀 Starting Strategic Deception Monitoring Dashboard")
    print("=" * 60)
    
    # Initialize dashboard
    dashboard = StrategicDeceptionDashboard()
    
    # Initialize monitoring agent
    agent = StrategicDeceptionMonitoringAgent()
    
    # Start dashboard
    await dashboard.start_dashboard()
    
    print("✅ Dashboard started successfully!")
    print("\n📊 Dashboard Status:")
    status = dashboard.get_dashboard_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Add some sample data for demonstration
    print("\n🔍 Adding sample deception indicators...")
    
    # Add sample metrics
    dashboard.add_metric("overall_deception_score", "Overall Deception Score", 0.75, "score")
    dashboard.add_metric("linguistic_indicators", "Linguistic Indicators", 12, "count")
    dashboard.add_metric("strategic_indicators", "Strategic Indicators", 8, "count")
    dashboard.add_metric("critical_alerts", "Critical Alerts", 3, "count")
    
    # Add sample alerts
    await dashboard.add_alert(
        "high_deception_score",
        "high",
        "High deception score detected",
        "sample_communication_1"
    )
    
    await dashboard.add_alert(
        "linguistic_evasion",
        "medium",
        "Linguistic evasion detected",
        "sample_communication_2"
    )
    
    # Get and display dashboard data
    print("\n📈 Current Dashboard Data:")
    dashboard_data = await dashboard.get_dashboard_data()
    
    # Display summary
    summary = dashboard_data.get("summary", {})
    print(f"\n📋 Summary:")
    print(f"   Total Metrics: {summary.get('total_metrics', 0)}")
    print(f"   Active Alerts: {summary.get('active_alerts', 0)}")
    print(f"   Critical Alerts: {summary.get('critical_alerts', 0)}")
    print(f"   Dashboard Status: {summary.get('dashboard_status', 'unknown')}")
    
    # Display metrics
    metrics = dashboard_data.get("metrics", {})
    print(f"\n📊 Metrics:")
    for metric_id, metric_data in metrics.items():
        current = metric_data.get("current", {})
        # Get metric name from dashboard metrics
        metric_name = dashboard.metrics[metric_id].metric_name if metric_id in dashboard.metrics else metric_id
        print(f"   {metric_name}: {current.get('value', 0)} {current.get('unit', '')}")
    
    # Display alerts
    alerts = dashboard_data.get("alerts", [])
    print(f"\n🚨 Active Alerts:")
    for alert in alerts:
        print(f"   [{alert['severity'].upper()}] {alert['message']}")
        print(f"      Source: {alert['source']}")
        print(f"      Time: {alert['timestamp']}")
    
    # Interactive menu
    print("\n" + "=" * 60)
    print("🎛️  Interactive Dashboard Controls")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. View dashboard data")
        print("2. Add sample alert")
        print("3. Acknowledge alerts")
        print("4. View dashboard status")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            data = await dashboard.get_dashboard_data()
            print("\n📊 Dashboard Data:")
            print(json.dumps(data, indent=2, default=str))
            
        elif choice == "2":
            alert_type = input("Alert type: ").strip()
            message = input("Alert message: ").strip()
            severity = input("Severity (low/medium/high/critical): ").strip()
            source = input("Source: ").strip()
            
            await dashboard.add_alert(alert_type, severity, message, source)
            print("✅ Alert added successfully!")
            
        elif choice == "3":
            dashboard_data = await dashboard.get_dashboard_data()
            alerts = dashboard_data.get("alerts", [])
            if not alerts:
                print("No active alerts to acknowledge.")
                continue
                
            print("\nActive Alerts:")
            for i, alert in enumerate(alerts):
                print(f"{i+1}. [{alert['severity']}] {alert['message']}")
            
            try:
                alert_choice = int(input("Enter alert number to acknowledge: ")) - 1
                if 0 <= alert_choice < len(alerts):
                    alert_id = alerts[alert_choice]['id']
                    await dashboard.acknowledge_alert(alert_id)
                    print("✅ Alert acknowledged!")
                else:
                    print("❌ Invalid alert number.")
            except ValueError:
                print("❌ Please enter a valid number.")
                
        elif choice == "4":
            status = dashboard.get_dashboard_status()
            print("\n📊 Dashboard Status:")
            for key, value in status.items():
                print(f"   {key}: {value}")
                
        elif choice == "5":
            print("\n🛑 Stopping dashboard...")
            await dashboard.stop_dashboard()
            print("✅ Dashboard stopped. Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error running dashboard: {e}")
        sys.exit(1)
