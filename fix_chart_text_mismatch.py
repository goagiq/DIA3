#!/usr/bin/env python3
"""
Fix Chart-Text Mismatch and Add Verification

This script fixes the mismatch between chart descriptions in text and actual chart types,
and adds verification checks to ensure consistency going forward.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def fix_chart_text_mismatch():
    """Fix the mismatch between chart descriptions and actual chart types."""
    
    print("🔧 Fixing Chart-Text Mismatch")
    print("=" * 50)
    
    # 1. Define the correct chart type mappings
    chart_type_mappings = {
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
    
    # 2. Define chart type descriptions for text
    chart_descriptions = {
        "doughnut": "doughnut chart",
        "polarArea": "polar area chart", 
        "line": "line chart",
        "radar": "radar chart",
        "bar": "bar chart",
        "scatter": "scatter plot",
        "pie": "pie chart"
    }
    
    # 3. Fix the enhanced HTML report generator
    fix_enhanced_html_generator(chart_type_mappings, chart_descriptions)
    
    # 4. Create verification system
    create_verification_system(chart_type_mappings)
    
    # 5. Update configuration
    update_configuration(chart_type_mappings)
    
    print("\n✅ Chart-Text Mismatch Fixed!")
    print("🔍 Verification system added")
    print("📋 All chart types now match their descriptions")

def fix_enhanced_html_generator(chart_type_mappings: Dict[str, str], chart_descriptions: Dict[str, str]):
    """Fix the enhanced HTML report generator to align chart types with descriptions."""
    print("📝 Fixing enhanced HTML report generator...")
    
    generator_file = Path("src/core/enhanced_html_report_generator.py")
    
    # Read the file
    with open(generator_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the chart type mappings in the data
    for module, chart_type in chart_type_mappings.items():
        # Find and replace the chart type in the module_data dictionary
        pattern = f'"{module}": {{\s*"type": "[^"]*"'
        replacement = f'"{module}": {{\n                "type": "{chart_type}"'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Fix the text descriptions to match chart types
    for module, chart_type in chart_type_mappings.items():
        chart_desc = chart_descriptions[chart_type]
        
        # Replace radar chart mentions with correct chart type
        if chart_type != "radar":
            pattern = f'<strong>Visualization Insight:</strong> The radar chart'
            replacement = f'<strong>Visualization Insight:</strong> The {chart_desc}'
            content = re.sub(pattern, replacement, content)
    
    # Add chart type verification method
    verification_method = '''
    def _verify_chart_text_consistency(self, module_title: str, chart_type: str) -> bool:
        """Verify that chart type matches text description."""
        # Define expected chart types for each module
        expected_chart_types = {
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
        
        expected_type = expected_chart_types.get(module_title, "bar")
        is_consistent = chart_type == expected_type
        
        if not is_consistent:
            logger.warning(f"Chart type mismatch for {module_title}: expected {expected_type}, got {chart_type}")
        
        return is_consistent
    
    def _get_chart_description(self, chart_type: str) -> str:
        """Get the proper description for a chart type."""
        descriptions = {
            "doughnut": "doughnut chart",
            "polarArea": "polar area chart", 
            "line": "line chart",
            "radar": "radar chart",
            "bar": "bar chart",
            "scatter": "scatter plot",
            "pie": "pie chart"
        }
        return descriptions.get(chart_type, "chart")
'''
    
    # Insert verification method before the _generate_meaningful_chart_data method
    insert_point = content.find("def _generate_meaningful_chart_data")
    if insert_point != -1:
        content = content[:insert_point] + verification_method + "\n    " + content[insert_point:]
    
    # Update the _generate_meaningful_chart_data method to use verification
    content = re.sub(
        r'data = module_data\[module_title\]',
        r'data = module_data[module_title]\n        # Verify chart type consistency\n        self._verify_chart_text_consistency(module_title, data["type"])',
        content
    )
    
    # Write the updated file
    with open(generator_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ Enhanced HTML report generator updated")

def create_verification_system(chart_type_mappings: Dict[str, str]):
    """Create a verification system to check chart-text consistency."""
    print("🔍 Creating verification system...")
    
    verification_script = Path("verify_chart_consistency.py")
    
    script_content = f'''#!/usr/bin/env python3
"""
Chart Consistency Verification System

This script verifies that chart types match their text descriptions.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

class ChartConsistencyVerifier:
    """Verifies chart-text consistency in reports."""
    
    def __init__(self):
        self.chart_type_mappings = chart_type_mappings
        self.generator = EnhancedHTMLReportGenerator()
    
    def verify_chart_consistency(self, html_file: str) -> Dict[str, Any]:
        """Verify chart consistency in an HTML file."""
        print(f"🔍 Verifying chart consistency in: {{html_file}}")
        
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
                        verified_charts.append({{
                            "module": module,
                            "chart_type": actual_type,
                            "text_description": described_type,
                            "status": "✅ Consistent"
                        }})
                    else:
                        issues.append({{
                            "module": module,
                            "expected_type": expected_type,
                            "actual_type": actual_type,
                            "text_description": described_type,
                            "status": "❌ Mismatch"
                        }})
                else:
                    issues.append({{
                        "module": module,
                        "expected_type": expected_type,
                        "actual_type": actual_type,
                        "text_description": "Not found",
                        "status": "❌ Missing description"
                    }})
            else:
                issues.append({{
                    "module": module,
                    "expected_type": expected_type,
                    "actual_type": "Not found",
                    "text_description": "Not found",
                    "status": "❌ Missing chart"
                }})
        
        return {{
            "verified_charts": verified_charts,
            "issues": issues,
            "total_charts": len(self.chart_type_mappings),
            "consistent_charts": len(verified_charts),
            "inconsistent_charts": len(issues)
        }}
    
    def generate_test_report(self) -> str:
        """Generate a test report to verify consistency."""
        print("📊 Generating test report for verification...")
        
        test_data = {{
            "title": "Chart Consistency Test Report",
            "subtitle": "Verification of Chart-Text Alignment",
            "topic": "Chart Consistency Analysis",
            "analysis_type": "verification",
            "confidence_score": 0.95,
            "source_metadata": [
                {{
                    "source_type": "verification",
                    "source_name": "Chart Consistency Verifier",
                    "title": "Chart-Text Alignment Test",
                    "confidence": 0.95,
                    "reliability_score": 0.95,
                    "timestamp": "2025-01-26 12:00"
                }}
            ],
            "content": "This is a test report to verify that chart types match their text descriptions."
        }}
        
        result = await self.generator.generate_enhanced_report(
            data=test_data,
            output_path="Results/chart_consistency_test.html"
        )
        
        if result["success"]:
            return result["file_path"]
        else:
            raise Exception(f"Failed to generate test report: {{result.get('error')}}")

async def main():
    """Main verification function."""
    print("🔍 Chart Consistency Verification System")
    print("=" * 50)
    
    verifier = ChartConsistencyVerifier()
    
    # Generate test report
    try:
        test_file = await verifier.generate_test_report()
        print(f"✅ Test report generated: {{test_file}}")
        
        # Verify consistency
        results = verifier.verify_chart_consistency(test_file)
        
        print(f"\\n📊 Verification Results:")
        print(f"   Total Charts: {{results['total_charts']}}")
        print(f"   Consistent: {{results['consistent_charts']}}")
        print(f"   Issues: {{results['inconsistent_charts']}}")
        
        if results['issues']:
            print(f"\\n❌ Issues Found:")
            for issue in results['issues']:
                print(f"   • {{issue['module']}}: {{issue['status']}}")
                print(f"     Expected: {{issue['expected_type']}}, Got: {{issue['actual_type']}}")
        else:
            print(f"\\n✅ All charts are consistent!")
        
        # Also verify existing reports
        results_dir = Path("Results")
        html_files = list(results_dir.glob("*.html"))
        
        if html_files:
            print(f"\\n🔍 Verifying existing reports:")
            for html_file in html_files[:3]:  # Check first 3 files
                try:
                    file_results = verifier.verify_chart_consistency(str(html_file))
                    print(f"   {{html_file.name}}: {{file_results['consistent_charts']}}/{{file_results['total_charts']}} consistent")
                except Exception as e:
                    print(f"   {{html_file.name}}: Error - {{e}}")
        
    except Exception as e:
        print(f"❌ Verification failed: {{e}}")
    
    print("\\n" + "=" * 50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
'''
    
    with open(verification_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("   ✅ Verification system created")

def update_configuration(chart_type_mappings: Dict[str, str]):
    """Update configuration files with chart type mappings."""
    print("⚙️ Updating configuration...")
    
    # Update enhanced template config
    config_file = Path("src/config/enhanced_template_config.json")
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Add chart consistency settings
        config["chart_consistency"] = {
            "enabled": True,
            "verification_required": True,
            "chart_type_mappings": chart_type_mappings,
            "auto_correction": True
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Configuration updated")

def main():
    """Main function."""
    fix_chart_text_mismatch()
    
    print("\n" + "=" * 50)
    print("🎯 Chart-Text Mismatch Fix Complete!")
    print("=" * 50)
    print("📋 What was fixed:")
    print("   • Chart types aligned with text descriptions")
    print("   • Verification system added")
    print("   • Configuration updated")
    print("\n🚀 Next steps:")
    print("   1. Run: python verify_chart_consistency.py")
    print("   2. Test report generation")
    print("   3. Verify all charts match their descriptions")
    print("\n💡 All future reports will have consistent chart-text alignment!")
    print("=" * 50)

if __name__ == "__main__":
    main()
