"""
Dark Web Threat Detection Demo

This script demonstrates the comprehensive dark web threat detection system
that combines pattern recognition, anomaly detection, and Monte Carlo simulation
for identifying emerging threats and assessing their probability.
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.dark_web_threat_detector import DarkWebThreatDetector


def generate_sample_dark_web_data() -> List[Dict[str, Any]]:
    """Generate sample dark web data for demonstration"""
    
    # Sample data sources with realistic dark web content
    data_sources = [
        {
            "name": "Dark Web Forum Alpha",
            "type": "dark_web_forums",
            "data": [
                {
                    "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "content": "New zero-day exploit for Windows 11 available. Contact for details and pricing.",
                    "metadata": {"author": "hacker_pro", "thread_id": "12345"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
                    "content": "Large database dump from major retailer. Contains 2M customer records with credit cards.",
                    "metadata": {"author": "data_leaker", "thread_id": "12346"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
                    "content": "Ransomware-as-a-Service platform now accepting new affiliates. 70% profit share.",
                    "metadata": {"author": "ransom_ops", "thread_id": "12347"}
                }
            ]
        },
        {
            "name": "Telegram Threat Channel",
            "type": "telegram_channels",
            "data": [
                {
                    "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                    "content": "APT group targeting financial institutions in Europe. Using new supply chain attack method.",
                    "metadata": {"channel": "threat_intel", "message_id": "789"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
                    "content": "Nation-state actors selling zero-day exploits to highest bidder. Government targets only.",
                    "metadata": {"channel": "threat_intel", "message_id": "790"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
                    "content": "Social engineering campaign targeting healthcare workers. Phishing emails with COVID-19 theme.",
                    "metadata": {"channel": "threat_intel", "message_id": "791"}
                }
            ]
        },
        {
            "name": "Paste Site Monitor",
            "type": "paste_sites",
            "data": [
                {
                    "timestamp": (datetime.now() - timedelta(hours=30)).isoformat(),
                    "content": "Dumped credentials from major tech company. 50K employee accounts with passwords.",
                    "metadata": {"site": "pastebin", "paste_id": "abc123"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
                    "content": "Backdoor trojan source code. Easy to modify and deploy. Includes keylogger functionality.",
                    "metadata": {"site": "pastebin", "paste_id": "def456"}
                }
            ]
        },
        {
            "name": "Dark Web Marketplace",
            "type": "marketplaces",
            "data": [
                {
                    "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
                    "content": "Selling: Advanced persistent threat toolkit. Includes custom malware and C2 infrastructure.",
                    "metadata": {"vendor": "apt_seller", "price": "50000", "currency": "BTC"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=10)).isoformat(),
                    "content": "Buying: Zero-day exploits for popular software. Paying top dollar for quality vulnerabilities.",
                    "metadata": {"buyer": "exploit_hunter", "budget": "100000", "currency": "BTC"}
                }
            ]
        },
        {
            "name": "IRC Threat Channel",
            "type": "irc_channels",
            "data": [
                {
                    "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(),
                    "content": "Insider threat opportunity. Looking for employees at major corporations willing to sell access.",
                    "metadata": {"channel": "#insider_threats", "nick": "recruiter"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=9)).isoformat(),
                    "content": "Supply chain attack successful. Compromised software update mechanism. Multiple targets affected.",
                    "metadata": {"channel": "#supply_chain", "nick": "supply_hacker"}
                }
            ]
        }
    ]
    
    return data_sources


async def demonstrate_threat_detection():
    """Demonstrate the dark web threat detection system"""
    
    print("=" * 80)
    print("DARK WEB THREAT DETECTION SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize the threat detector
    print("Initializing Dark Web Threat Detector...")
    detector = DarkWebThreatDetector()
    print("✓ Threat detector initialized successfully")
    print()
    
    # Generate sample data
    print("Generating sample dark web data...")
    data_sources = generate_sample_dark_web_data()
    print(f"✓ Generated {len(data_sources)} data sources with realistic threat content")
    print()
    
    # Perform threat detection
    print("Performing comprehensive threat detection analysis...")
    print("This includes:")
    print("  - Pattern recognition analysis")
    print("  - Anomaly detection")
    print("  - Monte Carlo simulation for probability assessment")
    print()
    
    start_time = datetime.now()
    detection_result = await detector.detect_emerging_threats(data_sources)
    end_time = datetime.now()
    
    analysis_duration = (end_time - start_time).total_seconds()
    print(f"✓ Analysis completed in {analysis_duration:.2f} seconds")
    print()
    
    # Display results
    if "error" in detection_result:
        print(f"❌ Analysis failed: {detection_result['error']}")
        return
    
    # Display summary
    summary = detection_result.get("summary", {})
    print("ANALYSIS SUMMARY")
    print("-" * 40)
    print(f"Total threats detected: {summary.get('total_threats_detected', 0)}")
    print(f"High-risk threats: {summary.get('high_risk_threats', 0)}")
    print(f"Average confidence: {summary.get('average_confidence', 0.0):.3f}")
    print(f"Anomaly score: {summary.get('anomaly_score', 0.0):.3f}")
    print()
    
    # Display detected threats
    threats = detection_result.get("threats", [])
    if threats:
        print("DETECTED THREATS")
        print("-" * 40)
        
        for i, threat in enumerate(threats, 1):
            print(f"Threat {i}:")
            print(f"  Type: {threat.get('threat_type', 'Unknown')}")
            print(f"  Description: {threat.get('description', 'No description')}")
            print(f"  Source: {threat.get('source', 'Unknown')}")
            print(f"  Severity: {threat.get('severity_level', 'Unknown')}")
            print(f"  Confidence: {threat.get('confidence_score', 0.0):.3f}")
            print(f"  Probability: {threat.get('probability', 0.0):.3f}")
            print(f"  Impact Score: {threat.get('impact_score', 0.0):.3f}")
            print(f"  Indicators: {', '.join(threat.get('indicators', []))}")
            print()
    
    # Display threat assessments
    assessments = detection_result.get("assessments", {})
    if assessments:
        print("THREAT ASSESSMENTS")
        print("-" * 40)
        
        for threat_id, assessment in assessments.items():
            print(f"Assessment for Threat {threat_id[:8]}...:")
            print(f"  Risk Score: {assessment.get('risk_score', 0.0):.3f}")
            print(f"  Confidence Interval: {assessment.get('confidence_interval', [0.0, 0.0])}")
            print(f"  Timeline Estimate: {assessment.get('timeline_estimate', 'Unknown')}")
            print(f"  Early Warning Indicators:")
            for indicator in assessment.get('early_warning_indicators', [])[:3]:  # Show first 3
                print(f"    - {indicator}")
            print(f"  Recommended Actions:")
            for action in assessment.get('recommended_actions', [])[:3]:  # Show first 3
                print(f"    - {action}")
            print()
    
    # Display recommendations
    recommendations = detection_result.get("recommendations", [])
    if recommendations:
        print("OVERALL RECOMMENDATIONS")
        print("-" * 40)
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i}. {recommendation}")
        print()
    
    # Display methodology
    methodology = detection_result.get("methodology", {})
    if methodology:
        print("ANALYSIS METHODOLOGY")
        print("-" * 40)
        for method, description in methodology.items():
            print(f"• {method.replace('_', ' ').title()}: {description}")
        print()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"Results/dark_web_threat_detection_results_{timestamp}.json"
    
    # Ensure Results directory exists
    os.makedirs("Results", exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(detection_result, f, indent=2, default=str)
    
    print(f"✓ Results saved to: {results_file}")
    print()
    
    # Generate markdown report
    markdown_file = f"Results/dark_web_threat_detection_report_{timestamp}.md"
    generate_markdown_report(detection_result, markdown_file)
    print(f"✓ Markdown report saved to: {markdown_file}")
    print()
    
    print("=" * 80)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("=" * 80)


def generate_markdown_report(detection_result: Dict[str, Any], filename: str):
    """Generate a comprehensive markdown report from detection results"""
    
    with open(filename, 'w') as f:
        f.write("# Dark Web Threat Detection Analysis Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        summary = detection_result.get("summary", {})
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Threats Detected:** {summary.get('total_threats_detected', 0)}\n")
        f.write(f"- **High-Risk Threats:** {summary.get('high_risk_threats', 0)}\n")
        f.write(f"- **Average Confidence:** {summary.get('average_confidence', 0.0):.3f}\n")
        f.write(f"- **Anomaly Score:** {summary.get('anomaly_score', 0.0):.3f}\n\n")
        
        # Threats
        threats = detection_result.get("threats", [])
        if threats:
            f.write("## Detected Threats\n\n")
            for i, threat in enumerate(threats, 1):
                f.write(f"### Threat {i}\n\n")
                f.write(f"- **Type:** {threat.get('threat_type', 'Unknown')}\n")
                f.write(f"- **Description:** {threat.get('description', 'No description')}\n")
                f.write(f"- **Source:** {threat.get('source', 'Unknown')}\n")
                f.write(f"- **Severity:** {threat.get('severity_level', 'Unknown')}\n")
                f.write(f"- **Confidence:** {threat.get('confidence_score', 0.0):.3f}\n")
                f.write(f"- **Probability:** {threat.get('probability', 0.0):.3f}\n")
                f.write(f"- **Impact Score:** {threat.get('impact_score', 0.0):.3f}\n")
                f.write(f"- **Indicators:** {', '.join(threat.get('indicators', []))}\n\n")
        
        # Assessments
        assessments = detection_result.get("assessments", {})
        if assessments:
            f.write("## Threat Assessments\n\n")
            for threat_id, assessment in assessments.items():
                f.write(f"### Assessment for Threat {threat_id[:8]}...\n\n")
                f.write(f"- **Risk Score:** {assessment.get('risk_score', 0.0):.3f}\n")
                f.write(f"- **Confidence Interval:** {assessment.get('confidence_interval', [0.0, 0.0])}\n")
                f.write(f"- **Timeline Estimate:** {assessment.get('timeline_estimate', 'Unknown')}\n\n")
                
                f.write("**Early Warning Indicators:**\n")
                for indicator in assessment.get('early_warning_indicators', []):
                    f.write(f"- {indicator}\n")
                f.write("\n")
                
                f.write("**Recommended Actions:**\n")
                for action in assessment.get('recommended_actions', []):
                    f.write(f"- {action}\n")
                f.write("\n")
        
        # Recommendations
        recommendations = detection_result.get("recommendations", [])
        if recommendations:
            f.write("## Overall Recommendations\n\n")
            for i, recommendation in enumerate(recommendations, 1):
                f.write(f"{i}. {recommendation}\n")
            f.write("\n")
        
        # Methodology
        methodology = detection_result.get("methodology", {})
        if methodology:
            f.write("## Analysis Methodology\n\n")
            for method, description in methodology.items():
                f.write(f"### {method.replace('_', ' ').title()}\n")
                f.write(f"{description}\n\n")


async def demonstrate_real_time_monitoring():
    """Demonstrate real-time monitoring capabilities"""
    
    print("=" * 80)
    print("REAL-TIME DARK WEB MONITORING DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize the threat detector
    detector = DarkWebThreatDetector()
    
    # Generate sample data
    data_sources = generate_sample_dark_web_data()
    
    print("Starting real-time monitoring (will run for 30 seconds)...")
    print("Press Ctrl+C to stop monitoring early")
    print()
    
    try:
        # Start monitoring with 10-second intervals
        monitoring_task = asyncio.create_task(
            detector.start_real_time_monitoring(data_sources, monitoring_interval=10)
        )
        
        # Let it run for 30 seconds
        await asyncio.sleep(30)
        
        # Cancel the monitoring task
        monitoring_task.cancel()
        
        try:
            monitoring_result = await monitoring_task
            print("Monitoring Results:")
            print(f"  Monitoring ID: {monitoring_result.get('monitoring_id', 'Unknown')}")
            print(f"  Status: {monitoring_result.get('status', 'Unknown')}")
            print(f"  Data Sources: {monitoring_result.get('data_sources', 0)}")
            print(f"  Monitoring Cycles: {len(monitoring_result.get('results', []))}")
            
            # Show last few results
            results = monitoring_result.get('results', [])
            if results:
                print("\nLast 3 Monitoring Cycles:")
                for result in results[-3:]:
                    print(f"  {result.get('timestamp', 'Unknown')}: "
                          f"{result.get('threats_detected', 0)} threats, "
                          f"{result.get('high_risk_count', 0)} high-risk")
            
        except asyncio.CancelledError:
            print("Monitoring was cancelled")
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    print("\nReal-time monitoring demonstration completed")


async def main():
    """Main demonstration function"""
    
    print("Dark Web Threat Detection System - Comprehensive Demonstration")
    print("This demonstration showcases:")
    print("1. Pattern recognition for threat identification")
    print("2. Anomaly detection for emerging threats")
    print("3. Monte Carlo simulation for probability assessment")
    print("4. Real-time monitoring capabilities")
    print()
    
    # Run the main threat detection demonstration
    await demonstrate_threat_detection()
    
    print("\n" + "=" * 80)
    print("Would you like to see the real-time monitoring demonstration? (y/n): ", end="")
    
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            await demonstrate_real_time_monitoring()
    except KeyboardInterrupt:
        print("\nDemonstration stopped by user")
    
    print("\nThank you for using the Dark Web Threat Detection System!")


if __name__ == "__main__":
    asyncio.run(main())
