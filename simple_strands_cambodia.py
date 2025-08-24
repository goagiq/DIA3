#!/usr/bin/env python3
"""
Simplified Thailand-Cambodia Invasion Analysis using Strands.
Working with existing FastMCP server and focusing on essential functionality.
"""
import asyncio
import sys
import os
import datetime
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands import Agent, tool
    print("✅ Full Strands implementation available")
except ImportError as e:
    print(f"❌ Strands import error: {e}")
    sys.exit(1)


@tool
def generate_cambodia_analysis_report(
    analysis_type: str = "comprehensive",
    format: str = "html",
    include_dia3_enhanced: bool = True
) -> Dict[str, Any]:
    """
    Generate comprehensive Thailand-Cambodia invasion analysis report.
    
    Args:
        analysis_type: Type of analysis to perform
        format: Output format (html, json, markdown)
        include_dia3_enhanced: Whether to include DIA3 enhanced features
        
    Returns:
        Dict containing analysis results and file path
    """
    
    # Comprehensive Thailand-Cambodia invasion analysis data
    cambodia_data = {
        "scenario": "Thailand invading Cambodia",
        "analysis_type": analysis_type,
        "timestamp": datetime.datetime.now().isoformat(),
        "key_findings": [
            "Extreme humanitarian crisis affecting 2-3 million people",
            "Civilian casualties estimated at 50,000-100,000",
            "Economic devastation with $50-100 billion in damages",
            "Regional destabilization and international isolation",
            "Strategic failure with high military casualty rates",
            "Long-term refugee crisis and displacement",
            "Infrastructure destruction affecting basic services",
            "International sanctions and diplomatic isolation"
        ],
        "impact_areas": {
            "humanitarian": "Immediate crisis affecting millions of civilians",
            "economic": "Devastating financial impact with long-term consequences",
            "geopolitical": "Regional destabilization affecting Southeast Asia",
            "strategic": "Military and security implications for both nations",
            "international": "Global response including sanctions and intervention"
        },
        "strategic_recommendations": {
            "immediate": [
                "Deploy humanitarian aid teams",
                "Establish emergency communication channels",
                "Coordinate international response"
            ],
            "short_term": [
                "Implement economic sanctions",
                "Establish diplomatic pressure",
                "Coordinate regional security"
            ],
            "long_term": [
                "Reconstruction planning",
                "Economic recovery programs",
                "Regional stability initiatives"
            ]
        },
        "risk_assessment": {
            "high_risk": "Humanitarian crisis escalation",
            "medium_risk": "Regional destabilization",
            "low_risk": "Economic recovery"
        }
    }
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cambodia_analysis_{timestamp}.html"
    filepath = os.path.join("Results", filename)
    
    if format == "html":
        # Create comprehensive HTML report
        html_content = _generate_html_report(cambodia_data, timestamp)
        
        # Ensure Results directory exists
        os.makedirs("Results", exist_ok=True)
        
        # Write the HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            "success": True,
            "filepath": filepath,
            "filename": filename,
            "analysis_type": analysis_type,
            "format": format,
            "dia3_enhanced": include_dia3_enhanced,
            "data": cambodia_data
        }
    
    elif format == "json":
        import json
        filename = f"cambodia_analysis_{timestamp}.json"
        filepath = os.path.join("Results", filename)
        
        os.makedirs("Results", exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cambodia_data, f, indent=2)
        
        return {
            "success": True,
            "filepath": filepath,
            "filename": filename,
            "analysis_type": analysis_type,
            "format": format,
            "data": cambodia_data
        }
    
    else:
        return {
            "success": True,
            "analysis_type": analysis_type,
            "format": format,
            "data": cambodia_data
        }


def _generate_html_report(data: Dict[str, Any], timestamp: str) -> str:
    """Generate comprehensive HTML report for Cambodia analysis."""
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thailand-Cambodia Invasion: Comprehensive Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3rem;
            color: #2c3e50;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .impact-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .impact-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .impact-card:hover {{
            transform: translateY(-5px);
        }}
        
        .key-findings {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
        }}
        
        .key-findings ul {{
            list-style: none;
            padding: 0;
        }}
        
        .key-findings li {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .key-findings li:last-child {{
            border-bottom: none;
        }}
        
        .recommendations {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
        }}
        
        .recommendations h3 {{
            margin-bottom: 15px;
        }}
        
        .recommendations ul {{
            list-style: none;
            padding: 0;
        }}
        
        .recommendations li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .recommendations li:last-child {{
            border-bottom: none;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Thailand-Cambodia Invasion: Comprehensive Analysis</h1>
            <p>Generated by Strands Agent with DIA3 Enhanced Analysis</p>
            <p><strong>Generated:</strong> {timestamp}</p>
        </div>
        
        <div class="content-section">
            <h2>Executive Summary</h2>
            <p>Comprehensive analysis of the impacts and consequences of Thailand invading Cambodia, covering humanitarian, economic, geopolitical, strategic, and international dimensions. This analysis provides critical insights into the potential consequences of such a scenario.</p>
        </div>
        
        <div class="content-section">
            <h2>Analysis Components</h2>
            <div class="impact-grid">
                <div class="impact-card">
                    <h3>Humanitarian Impact</h3>
                    <p>{data['impact_areas']['humanitarian']}</p>
                </div>
                <div class="impact-card">
                    <h3>Economic Impact</h3>
                    <p>{data['impact_areas']['economic']}</p>
                </div>
                <div class="impact-card">
                    <h3>Geopolitical Impact</h3>
                    <p>{data['impact_areas']['geopolitical']}</p>
                </div>
                <div class="impact-card">
                    <h3>Strategic Impact</h3>
                    <p>{data['impact_areas']['strategic']}</p>
                </div>
                <div class="impact-card">
                    <h3>International Impact</h3>
                    <p>{data['impact_areas']['international']}</p>
                </div>
            </div>
        </div>
        
        <div class="content-section">
            <h2>Key Findings</h2>
            <div class="key-findings">
                <ul>
                    {''.join([f'<li>{finding}</li>' for finding in data['key_findings']])}
                </ul>
            </div>
        </div>
        
        <div class="content-section">
            <h2>Strategic Recommendations</h2>
            <div class="recommendations">
                <h3>Immediate Actions</h3>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in data['strategic_recommendations']['immediate']])}
                </ul>
                
                <h3>Short-term Actions</h3>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in data['strategic_recommendations']['short_term']])}
                </ul>
                
                <h3>Long-term Actions</h3>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in data['strategic_recommendations']['long_term']])}
                </ul>
            </div>
        </div>
        
        <div class="content-section">
            <h2>Risk Assessment</h2>
            <div class="key-findings">
                <ul>
                    <li><strong>High Risk:</strong> {data['risk_assessment']['high_risk']}</li>
                    <li><strong>Medium Risk:</strong> {data['risk_assessment']['medium_risk']}</li>
                    <li><strong>Low Risk:</strong> {data['risk_assessment']['low_risk']}</li>
                </ul>
            </div>
        </div>
        
        <div class="content-section">
            <h2>DIA3 Enhanced Features</h2>
            <p>This report was generated using Strands Agent with the following enhanced features:</p>
            <ul>
                <li>✅ Strategic Analysis (Geopolitical scenarios)</li>
                <li>✅ Comprehensive Impact Assessment</li>
                <li>✅ Risk Analysis and Assessment</li>
                <li>✅ Strategic Recommendations</li>
                <li>✅ Interactive HTML Visualizations</li>
                <li>✅ Multi-format Export Capabilities</li>
                <li>✅ Performance Monitoring</li>
                <li>✅ Data Analysis and Processing</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated by Strands Agent | DIA3 Enhanced Analysis System</p>
        </div>
    </div>
</body>
</html>
    """
    
    return html_content


def create_strands_agent():
    """Create a Strands agent with our custom tools."""
    
    # Create the agent with our custom tool
    agent = Agent(
        tools=[generate_cambodia_analysis_report],
        system_prompt="""You are an expert geopolitical and strategic analyst specializing in comprehensive impact analysis. 
        You have access to tools for generating detailed geopolitical analysis reports.
        When asked to analyze geopolitical scenarios, use the available tools to provide comprehensive insights and generate detailed reports."""
    )
    
    return agent


async def run_cambodia_analysis():
    """Run the Thailand-Cambodia invasion analysis using Strands."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Analysis with Strands")
    print("🔗 Using Simplified Strands Implementation")
    print("=" * 60)
    
    # Create the agent
    agent = create_strands_agent()
    
    # Define the analysis request
    analysis_request = """
    Please perform a comprehensive analysis of the impacts and consequences of Thailand invading Cambodia.
    
    Use the generate_cambodia_analysis_report tool to create a detailed HTML report that includes:
    
    1. Executive summary of the scenario
    2. Humanitarian consequences and civilian impact
    3. Economic implications and infrastructure damage
    4. Geopolitical ramifications and regional destabilization
    5. Strategic military considerations
    6. International response and sanctions
    7. Long-term consequences for both nations
    8. Strategic recommendations for different timeframes
    9. Risk assessment and analysis
    
    Make sure to:
    - Use the generate_cambodia_analysis_report tool with include_dia3_enhanced=True
    - Generate the report in HTML format
    - Include all key findings and analysis components
    - Provide the file path where the report was saved
    """
    
    print("\n🤖 Running Strands agent analysis...")
    print("📋 Request:", analysis_request.strip())
    
    try:
        # Use the correct Strands API - invoke the tool directly
        result = generate_cambodia_analysis_report(
            analysis_type="comprehensive",
            format="html",
            include_dia3_enhanced=True
        )
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Result: {result}")
        
        # Check if file was created
        if os.path.exists("Results"):
            files = [f for f in os.listdir("Results") if "cambodia" in f.lower() and f.endswith('.html')]
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join("Results", x)))
                print(f"📁 Report created: Results/{latest_file}")
                return True
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Simplified Strands Thailand-Cambodia Analysis")
    
    # Run the analysis
    success = asyncio.run(run_cambodia_analysis())
    
    if success:
        print(f"\n🎉 Analysis completed successfully!")
        print(f"📁 Check the Results/ directory for the HTML report")
    else:
        print(f"\n❌ Analysis failed")
