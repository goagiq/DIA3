#!/usr/bin/env python3
"""
Test script for enhanced charts and tooltips with professional styling and MCP tool identification.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import the enhanced HTML report generator
from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator


class EnhancedChartAndTooltipTester:
    """Test class for enhanced charts and tooltips."""
    
    def __init__(self):
        self.generator = EnhancedHTMLReportGenerator()
        
    def test_enhanced_chart_generation(self):
        """Test enhanced chart generation with professional styling."""
        print("🎨 Testing Enhanced Chart Generation...")
        
        # Test different chart types
        chart_types = [
            "Executive Summary",
            "Geopolitical Impact Analysis", 
            "Trade and Economic Impact",
            "Balance of Power Analysis",
            "Strategic Analysis"
        ]
        
        for module_title in chart_types:
            print(f"\n📊 Testing chart for: {module_title}")
            
            # Generate chart data
            chart_data = self.generator._generate_meaningful_chart_data(1, module_title)
            
            # Verify chart configuration
            assert "type" in chart_data, f"Chart data missing type for {module_title}"
            assert "data" in chart_data, f"Chart data missing data for {module_title}"
            assert "options" in chart_data, f"Chart data missing options for {module_title}"
            
            # Check for professional styling
            options = chart_data["options"]
            assert "plugins" in options, f"Chart options missing plugins for {module_title}"
            assert "tooltip" in options["plugins"], f"Chart missing tooltip configuration for {module_title}"
            
            # Verify tooltip styling
            tooltip = options["plugins"]["tooltip"]
            assert tooltip.get("backgroundColor") == "rgba(0,0,0,0.8)", f"Tooltip missing professional background for {module_title}"
            assert tooltip.get("cornerRadius") == 8, f"Tooltip missing rounded corners for {module_title}"
            
            print(f"✅ {module_title}: {chart_data['type']} chart with professional styling")
        
        print("\n🎨 Enhanced chart generation test completed successfully!")
    
    def test_mcp_tool_identification(self):
        """Test MCP tool identification in tooltips."""
        print("\n🔧 Testing MCP Tool Identification...")
        
        # Test data with different source types
        test_data = {
            "source_metadata": [
                {
                    "source_type": "fetch",
                    "source_name": "Strategic Studies Institute",
                    "title": "Test Analysis Report",
                    "confidence": 0.8,
                    "reliability_score": 0.85,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "tac",
                    "source_name": "Defense Intelligence Database", 
                    "title": "Test Assessment",
                    "confidence": 0.75,
                    "reliability_score": 0.8,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "govdata",
                    "source_name": "Government Data Repository",
                    "title": "Test Official Data",
                    "confidence": 0.9,
                    "reliability_score": 0.95,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "vector_db",
                    "source_name": "DIA3 Vector Database",
                    "title": "Test Intelligence Analysis",
                    "confidence": 0.85,
                    "reliability_score": 0.9,
                    "timestamp": datetime.now()
                }
            ]
        }
        
        # Test tooltip generation for a module
        module_title = "Executive Summary"
        module_config = None
        
        tooltip_info = self.generator._generate_enhanced_module_tooltip_info(
            module_title, module_config, test_data
        )
        
        # Verify MCP tool identification
        sources = tooltip_info["sources"]
        mcp_tools_found = set()
        
        for source in sources:
            if "mcp_tool" in source:
                mcp_tools_found.add(source["mcp_tool"])
                print(f"✅ Found MCP tool: {source['mcp_tool']} for {source['source_name']}")
        
        # Verify we have the expected MCP tools
        expected_tools = {"Fetch", "TAC", "GovData", "DIA3"}
        assert mcp_tools_found.issuperset(expected_tools), f"Missing expected MCP tools. Found: {mcp_tools_found}"
        
        print(f"\n🔧 MCP tool identification test completed! Found tools: {mcp_tools_found}")
    
    def test_enhanced_tooltip_display(self):
        """Test enhanced tooltip display with MCP tool badges."""
        print("\n💡 Testing Enhanced Tooltip Display...")
        
        # Create sample tooltip data
        tooltip_data = {
            "section-1": {
                "title": "Executive Summary",
                "content": "Comprehensive analysis with enhanced insights.",
                "sources": [
                    {
                        "source_type": "mcp_fetch",
                        "source_name": "Strategic Studies Institute",
                        "title": "Analysis Report",
                        "confidence": 0.8,
                        "reliability_score": 0.85,
                        "is_internal": False,
                        "mcp_tool": "Fetch",
                        "timestamp": "2025-01-26 10:30"
                    },
                    {
                        "source_type": "mcp_tac",
                        "source_name": "Defense Intelligence Database",
                        "title": "Assessment",
                        "confidence": 0.75,
                        "reliability_score": 0.8,
                        "is_internal": False,
                        "mcp_tool": "TAC",
                        "timestamp": "2025-01-26 10:30"
                    },
                    {
                        "source_type": "internal",
                        "source_name": "DIA3 Analysis Engine",
                        "title": "Intelligence Analysis",
                        "confidence": 0.85,
                        "reliability_score": 0.9,
                        "is_internal": True,
                        "mcp_tool": "DIA3",
                        "timestamp": "2025-01-26 10:30"
                    }
                ]
            }
        }
        
        # Generate tooltip JavaScript
        tooltip_js = self.generator._generate_advanced_tooltips_js({"tooltip_data": tooltip_data})
        
        # Verify MCP tool badges are included
        assert "mcp-tool-badge" in tooltip_js, "Tooltip JavaScript missing MCP tool badges"
        assert "mcpIconMap" in tooltip_js, "Tooltip JavaScript missing MCP icon mapping"
        
        # Verify different MCP tool icons
        mcp_icons = ["🌐", "📊", "🏛️", "🔒"]
        for icon in mcp_icons:
            assert icon in tooltip_js, f"Tooltip JavaScript missing MCP icon: {icon}"
        
        print("✅ Enhanced tooltip display test completed successfully!")
    
    async def generate_sample_report(self):
        """Generate a sample report with enhanced charts and tooltips."""
        print("\n📄 Generating Sample Report with Enhanced Features...")
        
        # Sample data for the report
        sample_data = {
            "title": "Enhanced Charts and Tooltips Demo",
            "subtitle": "Professional styling and MCP tool identification",
            "topic": "Strategic Intelligence Analysis",
            "analysis_type": "strategic_intelligence",
            "confidence_score": 0.85,
            "source_metadata": [
                {
                    "source_type": "fetch",
                    "source_name": "Strategic Studies Institute",
                    "title": "Strategic Analysis Report",
                    "confidence": 0.8,
                    "reliability_score": 0.85,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "tac",
                    "source_name": "Defense Intelligence Database",
                    "title": "Intelligence Assessment",
                    "confidence": 0.75,
                    "reliability_score": 0.8,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "govdata",
                    "source_name": "Government Data Repository",
                    "title": "Official Strategic Data",
                    "confidence": 0.9,
                    "reliability_score": 0.95,
                    "timestamp": datetime.now()
                }
            ],
            "knowledge_graph_data": {
                "entities": ["Strategic Analysis", "Intelligence", "Security"],
                "relationships": [("Strategic Analysis", "influences", "Security")]
            },
            "vector_insights": {
                "similar_patterns": ["Historical strategic initiatives", "Regional security dynamics"],
                "confidence": 0.82
            }
        }
        
        # Generate the report
        output_path = Path("Results/enhanced_charts_and_tooltips_demo.html")
        output_path.parent.mkdir(exist_ok=True)
        
        try:
            # Generate the enhanced report
            result = await self.generator.generate_enhanced_report(sample_data, str(output_path))
            
            if result.get("success", False):
                print(f"✅ Sample report generated successfully: {output_path}")
                print(f"📊 Chart types included: {result.get('chart_types', [])}")
                print(f"🔧 MCP tools identified: {result.get('mcp_tools', [])}")
                return output_path
            else:
                print(f"❌ Failed to generate sample report: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating sample report: {e}")
            return None


async def main():
    """Main test function."""
    print("🚀 Enhanced Charts and Tooltips Test Suite")
    print("=" * 50)
    
    tester = EnhancedChartAndTooltipTester()
    
    # Run tests
    try:
        # Test enhanced chart generation
        tester.test_enhanced_chart_generation()
        
        # Test MCP tool identification
        tester.test_mcp_tool_identification()
        
        # Test enhanced tooltip display
        tester.test_enhanced_tooltip_display()
        
        # Generate sample report
        report_path = await tester.generate_sample_report()
        
        if report_path:
            print(f"\n🎉 All tests completed successfully!")
            print(f"📄 Sample report available at: {report_path}")
            print("\n✨ Enhanced Features Summary:")
            print("   • Professional chart styling with gradients and rounded corners")
            print("   • Multiple chart types: line, bar, radar, doughnut, pie, polarArea, scatter")
            print("   • MCP tool identification: Fetch, TAC, GovData, DIA3")
            print("   • Enhanced tooltips with MCP tool badges and icons")
            print("   • Improved color schemes and typography")
        else:
            print("\n❌ Sample report generation failed")
            
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
