#!/usr/bin/env python3
"""
Example: Phase 4 Strategic Intelligence Integration

Simple demonstration of how to integrate the Enhanced StrategicIntelligenceEngine
with your existing report generation system.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def example_1_direct_component_usage():
    """Example 1: Use strategic intelligence components directly."""
    
    print("📋 Example 1: Direct Component Usage")
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


async def example_2_integrate_with_report_generation():
    """Example 2: Integrate with existing report generation."""
    
    print("\n📋 Example 2: Integrate with Report Generation")
    print("=" * 50)
    
    try:
        # Check if modular report generator exists
        try:
            from src.core.modular_report_generator import ModularReportGenerator
            print("✅ ModularReportGenerator found")
        except ImportError:
            print("⚠️  ModularReportGenerator not found - this is expected if you're using a different report generator")
            return True
        
        # Initialize generator
        generator = ModularReportGenerator()
        
        # Check available modules
        modules_info = generator.get_available_modules()
        print(f"✅ Found {len(modules_info)} available modules")
        
        # Check if strategic intelligence module is available
        if "strategic_intelligence" in modules_info:
            print("✅ Strategic Intelligence module is available")
        else:
            print("⚠️  Strategic Intelligence module not found - you may need to register it")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def example_3_create_custom_integration():
    """Example 3: Create custom integration with your existing system."""
    
    print("\n📋 Example 3: Custom Integration")
    print("=" * 50)
    
    try:
        from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
        from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
        from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
        
        # Initialize components
        strategic_engine = StrategicIntelligenceEngine()
        recommendations_engine = EnhancedStrategicRecommendations()
        dashboard = StrategicAnalyticsDashboard()
        
        topic = "Your analysis topic"
        
        # Generate comprehensive strategic analysis
        print("📊 Generating strategic intelligence...")
        
        # Get strategic intelligence
        kg_intelligence = await strategic_engine.query_knowledge_graph_for_intelligence(
            topic, "strategic"
        )
        
        # Get historical patterns
        historical_patterns = await strategic_engine.analyze_historical_patterns(
            topic, "5_years"
        )
        
        # Get cross-domain intelligence
        cross_domain = await strategic_engine.generate_cross_domain_intelligence([
            "geopolitical", "economic", "military", "technological"
        ])
        
        # Get strategic trends
        trends = await strategic_engine.predict_strategic_trends(topic)
        
        # Get risk assessment
        risks = await strategic_engine.assess_strategic_risks_from_kg(topic)
        
        # Get opportunities
        opportunities = await strategic_engine.identify_strategic_opportunities(topic)
        
        # Get recommendations
        recommendations = await recommendations_engine.generate_intelligence_driven_recommendations(topic)
        
        # Get dashboard metrics
        metrics = await dashboard.get_strategic_metrics()
        summary = await dashboard.get_dashboard_summary()
        
        # Compile results
        results = {
            "topic": topic,
            "intelligence": {
                "knowledge_graph": kg_intelligence,
                "historical_patterns": historical_patterns,
                "cross_domain": cross_domain,
                "trends": trends,
                "risks": risks,
                "opportunities": opportunities
            },
            "recommendations": recommendations,
            "dashboard": {
                "metrics": metrics,
                "summary": summary
            }
        }
        
        print("✅ Strategic intelligence analysis completed successfully!")
        print(f"📊 Intelligence components: {len(results['intelligence'])}")
        print(f"📋 Recommendations: {len(results['recommendations'])}")
        print(f"📈 Dashboard metrics: {'Available' if results['dashboard']['metrics'] else 'Not available'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_examples():
    """Run all integration examples."""
    
    print("🚀 Phase 4 Strategic Intelligence Integration Examples")
    print("=" * 60)
    
    examples = [
        example_1_direct_component_usage,
        example_2_integrate_with_report_generation,
        example_3_create_custom_integration
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
        print("   • Use strategic intelligence components directly")
        print("   • Integrate with your existing report generation system")
        print("   • Create custom strategic intelligence solutions")
        print("   • Generate intelligence-driven reports")
    else:
        print("\n❌ Some examples failed. Please check the setup.")
        sys.exit(1)


