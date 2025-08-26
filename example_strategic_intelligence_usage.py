#!/usr/bin/env python3
"""
Example: Using Phase 4 Strategic Intelligence Integration

This script demonstrates how to integrate the Enhanced StrategicIntelligenceEngine
with your existing report generation system.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def example_1_generate_strategic_report():
    """Example 1: Generate a report with strategic intelligence."""
    
    print("📋 Example 1: Generate Strategic Intelligence Report")
    print("=" * 50)
    
    try:
        from src.core.modular_report_generator import ModularReportGenerator
        
        # Initialize generator
        generator = ModularReportGenerator()
        
        # Generate report with strategic intelligence
        result = await generator.generate_modular_report(
            query="Pakistan submarine acquisition strategic analysis",
            enabled_modules=["strategic_intelligence"],
            config={"strategic_intelligence": True},
            output_format="html"
        )
        
        if result.get("success"):
            print(f"✅ Report generated: {result.get('file_path')}")
            return True
        else:
            print(f"❌ Failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def example_2_use_strategic_intelligence_api():
    """Example 2: Use strategic intelligence via API."""
    
    print("\n📋 Example 2: Strategic Intelligence API Usage")
    print("=" * 50)
    
    try:
        import requests
        
        # Generate strategic intelligence analysis
        response = requests.post(
            "http://localhost:8000/strategic-intelligence/analyze",
            json={
                "topic": "Pakistan submarine acquisition",
                "analysis_depth": "comprehensive",
                "include_recommendations": True,
                "include_dashboard": True
            }
        )
        
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Strategic Intelligence Score: {analysis['results'].get('overall_score', 0)}")
            print(f"✅ Risk Level: {analysis['results'].get('risk_level', 'unknown')}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def example_3_integrate_with_existing_reports():
    """Example 3: Add strategic intelligence to existing reports."""
    
    print("\n📋 Example 3: Integrate with Existing Reports")
    print("=" * 50)
    
    try:
        from src.core.modular_report_generator import ModularReportGenerator
        
        # Initialize generator
        generator = ModularReportGenerator()
        
        # Include strategic intelligence with other modules
        result = await generator.generate_modular_report(
            query="Your analysis topic",
            enabled_modules=[
                "executive_summary",
                "strategic_intelligence",  # Add strategic intelligence
                "geopolitical_impact",
                "risk_assessment",
                "strategic_recommendations"
            ],
            config={
                "enhanced_template": True,
                "strategic_intelligence": True
            }
        )
        
        if result.get("success"):
            print(f"✅ Enhanced report generated: {result.get('file_path')}")
            return True
        else:
            print(f"❌ Failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def example_4_direct_component_usage():
    """Example 4: Use strategic intelligence components directly."""
    
    print("\n📋 Example 4: Direct Component Usage")
    print("=" * 50)
    
    try:
        from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
        from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
        from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
        
        # Initialize components
        strategic_engine = StrategicIntelligenceEngine()
        recommendations_engine = EnhancedStrategicRecommendations()
        dashboard = StrategicAnalyticsDashboard()
        
        topic = "Pakistan submarine acquisition"
        
        # Use strategic intelligence engine
        kg_intelligence = await strategic_engine.query_knowledge_graph_for_intelligence(
            topic, "strategic"
        )
        print(f"✅ Knowledge Graph Intelligence: {'Success' if kg_intelligence.get('success') else 'Failed'}")
        
        # Use recommendations engine
        recommendations = await recommendations_engine.generate_intelligence_driven_recommendations(topic)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        # Use dashboard
        metrics = await dashboard.get_strategic_metrics()
        print(f"✅ Strategic Metrics: {'Success' if metrics else 'Failed'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def run_all_examples():
    """Run all integration examples."""
    
    print("🚀 Phase 4 Strategic Intelligence Integration Examples")
    print("=" * 60)
    
    examples = [
        example_1_generate_strategic_report,
        example_2_use_strategic_intelligence_api,
        example_3_integrate_with_existing_reports,
        example_4_direct_component_usage
    ]
    
    results = []
    
    for i, example_func in enumerate(examples, 1):
        print(f"\n🎯 Running Example {i}...")
        try:
            result = await example_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Example {i} failed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Integration Examples Summary")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"Example {i}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\nOverall: {success_count}/{total_count} examples passed")
    
    if success_count == total_count:
        print("\n🎉 All examples passed! Phase 4 integration is working correctly.")
    else:
        print(f"\n⚠️  {total_count - success_count} examples failed. Check the errors above.")
    
    return success_count == total_count


if __name__ == "__main__":
    # Run all examples
    success = asyncio.run(run_all_examples())
    
    if success:
        print("\n🚀 Phase 4 Strategic Intelligence Integration is ready!")
        print("📋 You can now:")
        print("   • Generate strategic intelligence reports")
        print("   • Use the API endpoints")
        print("   • Integrate with existing reports")
        print("   • Use components directly")
    else:
        print("\n❌ Some examples failed. Please check the setup.")
        sys.exit(1)

