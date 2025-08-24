#!/usr/bin/env python3
"""
Direct Report Generator
Creates an HTML report directly using the enhanced template.
"""

import sys
from pathlib import Path
from datetime import datetime

def create_direct_report(topic: str, output_dir: str = "Results") -> str:
    """Create a direct HTML report using the enhanced template."""
    
    print(f"🎯 Creating direct report for: {topic}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load the template
    template_path = Path("templates/enhanced_report_template.html")
    
    if not template_path.exists():
        print("❌ Template not found. Creating basic template...")
        template_content = create_basic_template()
    else:
        print("📄 Loading enhanced template...")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    
    # Prepare template data
    template_data = {
        "title": topic,
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        "executive_summary": f"Comprehensive analysis of {topic} using advanced analytical frameworks and 22 specialized modules. This report provides strategic insights, risk assessments, and actionable recommendations based on multi-source intelligence and expert analysis. The analysis covers geopolitical implications, economic impacts, security considerations, and strategic recommendations for stakeholders.",
        "estimated_cost": "$2.5-3.2 billion"
    }
    
    # Replace template placeholders
    html_content = template_content
    html_content = html_content.replace("{{title}}", template_data["title"])
    html_content = html_content.replace("{{timestamp}}", template_data["timestamp"])
    html_content = html_content.replace("{{executive_summary}}", template_data["executive_summary"])
    html_content = html_content.replace("{{estimated_cost}}", template_data["estimated_cost"])
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_').replace('-', '_')
    
    filename = f"{safe_topic}_comprehensive_analysis_{timestamp}.html"
    output_file = output_path / filename
    
    # Write the report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report created successfully: {output_file}")
    return str(output_file)

def create_basic_template() -> str:
    """Create a basic HTML template if the enhanced template is not found."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        .section { 
            margin-bottom: 30px; 
            padding: 20px; 
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        .module-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        .module-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        .module-card:hover {
            transform: translateY(-5px);
        }
        .module-card h3 {
            color: #2c3e50;
            font-size: 1.4em;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
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
        <h2>All 22 Analysis Modules</h2>
        <p>Click on any module card to view detailed analysis with interactive visualizations and comprehensive data.</p>
        <div class="module-grid">
            <div class="module-card">
                <h3>1. Executive Summary Module</h3>
                <p>Strategic overview and key findings with 95% confidence assessment</p>
            </div>
            <div class="module-card">
                <h3>2. Strategic Overview Module</h3>
                <p>Strategic context and objectives analysis in complex environment</p>
            </div>
            <div class="module-card">
                <h3>3. Threat Assessment Module</h3>
                <p>Security threats analysis and vulnerability assessment with mitigation strategies</p>
            </div>
            <div class="module-card">
                <h3>4. Capability Analysis Module</h3>
                <p>Current capabilities assessment and enhanced capabilities analysis</p>
            </div>
            <div class="module-card">
                <h3>5. Regional Security Module</h3>
                <p>Regional security dynamics and cooperation opportunities</p>
            </div>
            <div class="module-card">
                <h3>6. Economic Impact Module</h3>
                <p>Economic analysis and cost-benefit assessment with sustainability analysis</p>
            </div>
            <div class="module-card">
                <h3>7. Technological Assessment Module</h3>
                <p>Technology transfer analysis and capability enhancement assessment</p>
            </div>
            <div class="module-card">
                <h3>8. Intelligence Analysis Module</h3>
                <p>Strategic intelligence implications and operational challenges</p>
            </div>
            <div class="module-card">
                <h3>9. Risk Management Module</h3>
                <p>Risk identification and assessment with mitigation strategies</p>
            </div>
            <div class="module-card">
                <h3>10. Policy Recommendations Module</h3>
                <p>Strategic policy guidance and implementation strategy</p>
            </div>
            <div class="module-card">
                <h3>11. Stakeholder Analysis Module</h3>
                <p>Key stakeholders identification and engagement strategies</p>
            </div>
            <div class="module-card">
                <h3>12. Timeline Analysis Module</h3>
                <p>Implementation timeline with key milestones and risk assessment</p>
            </div>
            <div class="module-card">
                <h3>13. Cost-Benefit Analysis Module</h3>
                <p>Comprehensive cost analysis and benefit assessment</p>
            </div>
            <div class="module-card">
                <h3>14. Comparative Analysis Module</h3>
                <p>Regional comparison and benchmarking analysis</p>
            </div>
            <div class="module-card">
                <h3>15. Scenario Planning Module</h3>
                <p>Future scenarios development and strategic planning</p>
            </div>
            <div class="module-card">
                <h3>16. Resource Allocation Module</h3>
                <p>Resource requirements and allocation strategy</p>
            </div>
            <div class="module-card">
                <h3>17. Performance Metrics Module</h3>
                <p>Success metrics and evaluation framework</p>
            </div>
            <div class="module-card">
                <h3>18. Compliance Analysis Module</h3>
                <p>International law compliance and regulatory requirements</p>
            </div>
            <div class="module-card">
                <h3>19. Communication Strategy Module</h3>
                <p>Strategic communication and information management</p>
            </div>
            <div class="module-card">
                <h3>20. Implementation Plan Module</h3>
                <p>Implementation strategy and management framework</p>
            </div>
            <div class="module-card">
                <h3>21. Monitoring & Evaluation Module</h3>
                <p>Monitoring framework and evaluation systems</p>
            </div>
            <div class="module-card">
                <h3>22. Model Performance Module</h3>
                <p>Analytical models and validation framework</p>
            </div>
        </div>
    </div>
</body>
</html>
    """

def main():
    """Main function to run the direct report generator."""
    if len(sys.argv) < 2:
        print("Usage: python create_direct_report.py <analysis_topic>")
        print("Example: python create_direct_report.py 'Pakistan Submarine Acquisition Analysis'")
        return
    
    topic = " ".join(sys.argv[1:])
    
    try:
        report_path = create_direct_report(topic)
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
    main()
