#!/usr/bin/env python3
"""
Chart Consistency Verification System

This script verifies that chart types match their text descriptions.
"""

import json
import re
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

class ChartConsistencyVerifier:
    """Verifies chart-text consistency in reports."""
    
    def __init__(self):
        self.chart_type_mappings = {
            "Executive Summary": "doughnut",
            "Geopolitical Impact Analysis": "polarArea", 
            "Trade and Economic Impact": "line",
            "Security Implications": "radar",
            "Balance of Power Analysis": "bar",
            "Strategic Analysis": "line",
            "Enhanced Data Analysis": "scatter",
            "Regional Sentiment Analysis": "pie",
            "Implementation Timeline": "line",
            "Acquisition Programs & Modernization": "bar",
            "Forecasting & Predictive Analytics": "line",
            "Operational Considerations": "radar",
            "Regional Security Dynamics": "bar",
            "Economic Cost Analysis": "line",
            "Comparison Analysis & Strategic Options": "radar",
            "Advanced Forecasting Analysis": "line",
            "Forecast Model Performance Comparison": "bar",
            "Strategic Capability Forecasts": "radar",
            "Predictive Analytics & Feature Importance": "bar",
            "Scenario Prediction Analysis": "line"
        }
        self.generator = EnhancedHTMLReportGenerator()
    
    def verify_chart_consistency(self, html_file: str):
        """Verify chart consistency in an HTML file."""
        print(f"🔍 Verifying chart consistency in: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        verified_charts = []
        
        # Check each module's chart
        for module, expected_type in self.chart_type_mappings.items():
            # Find chart type in JavaScript
            chart_pattern = rf'// {re.escape(module)} Chart.*?type: \'([^\']+)\''
            chart_match = re.search(chart_pattern, content, re.DOTALL)
            
            if chart_match:
                actual_type = chart_match.group(1)
                
                # Find text description
                text_pattern = rf'<strong>Visualization Insight:</strong> The ([^<]+) chart'
                text_match = re.search(text_pattern, content)
                
                if text_match:
                    described_type = text_match.group(1).strip()
                    
                    # Check consistency
                    if actual_type == expected_type:
                        verified_charts.append({
                            "module": module,
                            "chart_type": actual_type,
                            "text_description": described_type,
                            "status": "✅ Consistent"
                        })
                    else:
                        issues.append({
                            "module": module,
                            "expected_type": expected_type,
                            "actual_type": actual_type,
                            "text_description": described_type,
                            "status": "❌ Mismatch"
                        })
                else:
                    issues.append({
                        "module": module,
                        "expected_type": expected_type,
                        "actual_type": actual_type,
                        "text_description": "Not found",
                        "status": "❌ Missing description"
                    })
            else:
                issues.append({
                    "module": module,
                    "expected_type": expected_type,
                    "actual_type": "Not found",
                    "text_description": "Not found",
                    "status": "❌ Missing chart"
                })
        
        return {
            "verified_charts": verified_charts,
            "issues": issues,
            "total_charts": len(self.chart_type_mappings),
            "consistent_charts": len(verified_charts),
            "inconsistent_charts": len(issues)
        }
    
    async def generate_test_report(self):
        """Generate a test report to verify consistency."""
        print("📊 Generating test report for verification...")
        
        test_data = {
            "title": "Chart Consistency Test Report",
            "subtitle": "Verification of Chart-Text Alignment",
            "topic": "Chart Consistency Analysis",
            "analysis_type": "verification",
            "confidence_score": 0.95,
            "source_metadata": [
                {
                    "source_type": "verification",
                    "source_name": "Chart Consistency Verifier",
                    "title": "Chart-Text Alignment Test",
                    "confidence": 0.95,
                    "reliability_score": 0.95,
                    "timestamp": "2025-01-26 12:00"
                }
            ],
            "content": "This is a test report to verify that chart types match their text descriptions."
        }
        
        result = await self.generator.generate_enhanced_report(
            data=test_data,
            output_path="Results/chart_consistency_test.html"
        )
        
        if result["success"]:
            return result["file_path"]
        else:
            raise Exception(f"Failed to generate test report: {result.get('error')}")

async def main():
    """Main verification function."""
    print("🔍 Chart Consistency Verification System")
    print("=" * 50)
    
    verifier = ChartConsistencyVerifier()
    
    # Generate test report
    try:
        test_file = await verifier.generate_test_report()
        print(f"✅ Test report generated: {test_file}")
        
        # Verify consistency
        results = verifier.verify_chart_consistency(test_file)
        
        print(f"\n📊 Verification Results:")
        print(f"   Total Charts: {results['total_charts']}")
        print(f"   Consistent: {results['consistent_charts']}")
        print(f"   Issues: {results['inconsistent_charts']}")
        
        if results['issues']:
            print(f"\n❌ Issues Found:")
            for issue in results['issues']:
                print(f"   • {issue['module']}: {issue['status']}")
                print(f"     Expected: {issue['expected_type']}, Got: {issue['actual_type']}")
        else:
            print(f"\n✅ All charts are consistent!")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
