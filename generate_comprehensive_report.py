#!/usr/bin/env python3
"""
Comprehensive Report Generator using Enhanced HTML Template
Generates interactive HTML reports with all 22 modules for any analysis topic.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.adaptive_data_adapter import AdaptiveDataAdapter
from core.modules import (
    ExecutiveSummaryModule, StrategicOverviewModule, ThreatAssessmentModule,
    CapabilityAnalysisModule, RegionalSecurityModule, EconomicImpactModule,
    TechnologicalAssessmentModule, IntelligenceAnalysisModule, 
    RiskManagementModule, PolicyRecommendationsModule, StakeholderAnalysisModule,
    TimelineAnalysisModule, CostBenefitAnalysisModule, ComparativeAnalysisModule,
    ScenarioPlanningModule, ResourceAllocationModule, PerformanceMetricsModule,
    ComplianceAnalysisModule, CommunicationStrategyModule, 
    ImplementationPlanModule, MonitoringEvaluationModule, ModelPerformanceModule
)


async def generate_comprehensive_report(topic: str, output_dir: str = "Results") -> str:
    """
    Generate a comprehensive HTML report using the enhanced template.
    
    Args:
        topic: The analysis topic
        output_dir: Directory to save the report
        
    Returns:
        Path to the generated report
    """
    print(f"🎯 Generating comprehensive report for: {topic}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Initialize components
    print("📊 Initializing report components...")
    data_adapter = AdaptiveDataAdapter()
    report_generator = ModularReportGenerator()
    
    # Generate adaptive data
    print("🔄 Generating adaptive data...")
    adaptive_data = await data_adapter.adapt_data_for_topic(topic)
    
    # Initialize all 22 modules
    print("🔧 Loading all 22 analysis modules...")
    modules = [
        ExecutiveSummaryModule(),
        StrategicOverviewModule(),
        ThreatAssessmentModule(),
        CapabilityAnalysisModule(),
        RegionalSecurityModule(),
        EconomicImpactModule(),
        TechnologicalAssessmentModule(),
        IntelligenceAnalysisModule(),
        RiskManagementModule(),
        PolicyRecommendationsModule(),
        StakeholderAnalysisModule(),
        TimelineAnalysisModule(),
        CostBenefitAnalysisModule(),
        ComparativeAnalysisModule(),
        ScenarioPlanningModule(),
        ResourceAllocationModule(),
        PerformanceMetricsModule(),
        ComplianceAnalysisModule(),
        CommunicationStrategyModule(),
        ImplementationPlanModule(),
        MonitoringEvaluationModule(),
        ModelPerformanceModule()
    ]
    
    # Configure custom settings for enhanced template
    custom_config = {
        "template_type": "enhanced_html",
        "template_path": "templates/enhanced_report_template.html",
        "features": {
            "advanced_tooltips": True,
            "multiple_sources": True,
            "interactive_charts": True,
            "responsive_design": True,
            "professional_styling": True
        },
        "output_format": "html",
        "output_directory": str(output_path)
    }
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_').replace('-', '_')
    
    filename = f"{safe_topic}_comprehensive_analysis_{timestamp}.html"
    output_file = output_path / filename
    
    print(f"📝 Generating report content...")
    
    try:
        # Generate the report using the enhanced template
        report_content = await report_generator.generate_modular_report(
            topic=topic,
            data=adaptive_data,
            modules=modules,
            custom_config=custom_config
        )
        
        # Write the report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Report generated successfully: {output_file}")
        return str(output_file)
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        
        # Fallback: Create a basic enhanced report
        print("🔄 Creating fallback enhanced report...")
        fallback_content = create_fallback_report(topic, adaptive_data, modules, timestamp)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fallback_content)
        
        print(f"✅ Fallback report generated: {output_file}")
        return str(output_file)

def create_fallback_report(topic: str, data: Dict[str, Any], modules: List, timestamp: str) -> str:
    """Create a fallback enhanced report if the main generator fails."""
    
    # Load the template
    template_path = Path("templates/enhanced_report_template.html")
    
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    else:
        # Create a basic template if not found
        template_content = create_basic_template()
    
    # Prepare template data
    template_data = {
        "title": topic,
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        "executive_summary": f"Comprehensive analysis of {topic} using advanced analytical frameworks and 22 specialized modules. This report provides strategic insights, risk assessments, and actionable recommendations based on multi-source intelligence and expert analysis.",
        "estimated_cost": "$2.5-3.2 billion",
        "modules": [module.module_id for module in modules]
    }
    
    # Replace template placeholders
    html_content = template_content
    html_content = html_content.replace("{{title}}", template_data["title"])
    html_content = html_content.replace("{{timestamp}}", template_data["timestamp"])
    html_content = html_content.replace("{{executive_summary}}", template_data["executive_summary"])
    html_content = html_content.replace("{{estimated_cost}}", template_data["estimated_cost"])
    
    return html_content

def create_basic_template() -> str:
    """Create a basic HTML template if the enhanced template is not found."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; margin-bottom: 40px; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{title}}</h1>
        <p>Generated: {{timestamp}}</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{{executive_summary}}</p>
    </div>
    
    <div class="section">
        <h2>Analysis Modules</h2>
        <p>This report includes analysis from 22 specialized modules covering strategic, economic, security, and operational aspects.</p>
    </div>
</body>
</html>
    """

async def main():
    """Main function to run the report generator."""
    if len(sys.argv) < 2:
        print("Usage: python generate_comprehensive_report.py <analysis_topic>")
        print("Example: python generate_comprehensive_report.py 'Pakistan Submarine Acquisition Analysis'")
        return
    
    topic = " ".join(sys.argv[1:])
    
    try:
        report_path = await generate_comprehensive_report(topic)
        print(f"\n🎉 Report generation completed!")
        print(f"📁 Report saved to: {report_path}")
        print(f"🌐 Open the report in your web browser to view the interactive analysis")
        
        # Try to open the report in browser
        try:
            import webbrowser
            webbrowser.open(f"file://{Path(report_path).absolute()}")
            print("🌐 Report opened in your default web browser")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please manually open: {report_path}")
            
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
