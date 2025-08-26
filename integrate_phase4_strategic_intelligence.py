#!/usr/bin/env python3
"""
Phase 4 Strategic Intelligence Integration Script

Demonstrates how to integrate the Enhanced StrategicIntelligenceEngine
with the existing report generation system.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import ModularReportGenerator
from src.core.adaptive_data_adapter import adaptive_data_adapter


async def generate_strategic_intelligence_report():
    """Generate a report with integrated strategic intelligence."""
    
    # Topic for strategic analysis
    topic = ("Pakistan Submarine Acquisition: Strategic Intelligence Analysis "
             "of Geopolitical Impact, Economic Implications, and Regional "
             "Security Dynamics")
    
    print("🚀 Generating Strategic Intelligence Report...")
    print(f"📋 Topic: {topic}")
    
    try:
        # Initialize the modular report generator
        generator = ModularReportGenerator()
        
        # Generate adaptive data
        print("📊 Generating adaptive data...")
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Get available modules including the new strategic intelligence module
        modules_info = generator.get_available_modules()
        all_module_ids = list(modules_info.keys())
        
        print(f"✅ Found {len(all_module_ids)} modules including strategic intelligence")
        
        # Generate the enhanced HTML report with strategic intelligence
        print("📝 Generating strategic intelligence report...")
        result = await generator.generate_modular_report(
            query=topic,
            enabled_modules=all_module_ids,
            config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True,
                "strategic_intelligence": True  # Enable strategic intelligence
            },
            output_format="html",
            title=f"Strategic Intelligence Analysis: {topic}"
        )
        
        if result.get("success"):
            print("✅ Strategic intelligence report generated successfully!")
            print(f"📁 File: {result.get('file_path')}")
            print(f"📊 Modules used: {len(result.get('modules_used', []))}")
            print(f"📏 File size: {result.get('file_size', 0)} bytes")
            
            # Open the report in browser
            import webbrowser
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                webbrowser.open(f"file://{file_path.absolute()}")
                print("🌐 Opened report in browser")
            
            return result
        else:
            print(f"❌ Error generating report: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_strategic_intelligence_components():
    """Test individual strategic intelligence components."""
    
    print("\n🔧 Testing Strategic Intelligence Components...")
    
    try:
        from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
        from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
        from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
        
        # Test Strategic Intelligence Engine
        print("📊 Testing Strategic Intelligence Engine...")
        strategic_engine = StrategicIntelligenceEngine()
        
        # Test knowledge graph query
        kg_result = await strategic_engine.query_knowledge_graph_for_intelligence(
            "Pakistan submarine acquisition", "strategic"
        )
        print(f"✅ Knowledge Graph Query: {'Success' if kg_result.get('success') else 'Failed'}")
        
        # Test historical patterns
        patterns_result = await strategic_engine.analyze_historical_patterns(
            "Pakistan submarine acquisition", "5_years"
        )
        print(f"✅ Historical Patterns: {'Success' if patterns_result.get('success') else 'Failed'}")
        
        # Test Enhanced Strategic Recommendations
        print("📋 Testing Enhanced Strategic Recommendations...")
        recommendations_engine = EnhancedStrategicRecommendations()
        
        recs_result = await recommendations_engine.generate_intelligence_driven_recommendations(
            "Pakistan submarine acquisition"
        )
        print(f"✅ Intelligence-Driven Recommendations: {len(recs_result)} generated")
        
        # Test Strategic Analytics Dashboard
        print("📈 Testing Strategic Analytics Dashboard...")
        dashboard = StrategicAnalyticsDashboard()
        
        metrics_result = await dashboard.get_strategic_metrics()
        print(f"✅ Strategic Metrics: {'Success' if metrics_result else 'Failed'}")
        
        summary_result = await dashboard.get_dashboard_summary()
        print(f"✅ Dashboard Summary: {'Success' if summary_result else 'Failed'}")
        
        print("✅ All strategic intelligence components tested successfully!")
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()


async def demonstrate_phase4_integration():
    """Demonstrate the complete Phase 4 integration."""
    
    print("\n🎯 Demonstrating Phase 4 Strategic Intelligence Integration...")
    
    try:
        # Test individual components first
        await test_strategic_intelligence_components()
        
        # Generate comprehensive report
        result = await generate_strategic_intelligence_report()
        
        if result:
            print("\n🎉 Phase 4 Integration Demonstration Completed Successfully!")
            print("📊 The integrated system provides:")
            print("   • Enhanced Strategic Intelligence Engine")
            print("   • Intelligence-driven recommendations")
            print("   • Strategic analytics dashboard")
            print("   • Risk assessment and opportunity identification")
            print("   • Cross-domain intelligence analysis")
            print("   • Historical pattern analysis")
            print("   • Predictive strategic trends")
            print("   • Interactive visualizations")
            print("   • Professional styling and layout")
            
            return True
        else:
            print("\n❌ Phase 4 Integration Demonstration Failed!")
            return False
            
    except Exception as e:
        print(f"❌ Integration demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the complete integration demonstration
    success = asyncio.run(demonstrate_phase4_integration())
    
    if success:
        print("\n🚀 Phase 4 Strategic Intelligence Integration is ready for use!")
        print("📋 Next steps:")
        print("   1. Use the strategic intelligence module in your reports")
        print("   2. Access strategic intelligence via API endpoints")
        print("   3. Customize the integration for your specific needs")
        print("   4. Monitor and optimize performance")
    else:
        print("\n❌ Integration setup failed! Please check the error messages above.")
        sys.exit(1)

