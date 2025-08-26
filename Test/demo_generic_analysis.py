#!/usr/bin/env python3
"""
Demo: Generic Comprehensive Analysis System
Shows how to use the DIA3 system for any strategic topic.
"""

import asyncio
from Test.generic_comprehensive_analysis_system import GenericComprehensiveAnalysisSystem


async def demo_analysis():
    """Demonstrate the generic analysis system with different topics."""
    
    analyzer = GenericComprehensiveAnalysisSystem()
    
    # Example topics to analyze
    topics = [
        "Pakistan submarine acquisition",
        "China-Taiwan relations", 
        "Russia-Ukraine conflict escalation",
        "Iran nuclear program",
        "North Korea missile development",
        "Cyber warfare capabilities",
        "Space militarization",
        "Economic sanctions impact"
    ]
    
    print("🎯 DIA3 Generic Comprehensive Analysis System Demo")
    print("=" * 60)
    print("This system can analyze ANY strategic topic automatically!")
    print()
    
    # Analyze the first topic as an example
    topic = topics[0]
    print(f"📊 Analyzing: {topic}")
    print("-" * 40)
    
    result = await analyzer.analyze_topic(topic, "comprehensive")
    
    if result["success"]:
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Reports generated:")
        for report_type, path in result["report_paths"].items():
            print(f"   - {report_type}: {path}")
        
        print(f"\n📋 Analysis Summary:")
        print(f"   - Topic: {result['topic']}")
        print(f"   - Analysis Type: {result['analysis_type']}")
        print(f"   - Categories Determined: {len(result['relevant_categories'])}")
        print(f"   - Research Areas: {len(result['research_results'])}")
        
        print(f"\n🎯 Relevant Analysis Categories:")
        for i, category in enumerate(result['relevant_categories'][:10], 1):
            print(f"   {i}. {category}")
        
        if len(result['relevant_categories']) > 10:
            print(f"   ... and {len(result['relevant_categories']) - 10} more")
    
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("💡 To analyze a different topic, simply call:")
    print("   result = await analyzer.analyze_topic('Your Topic Here')")
    print()
    print("📚 Available analysis types:")
    print("   - 'comprehensive' (default)")
    print("   - 'strategic'")
    print("   - 'tactical'") 
    print("   - 'economic'")
    print()
    print("🎯 The system automatically:")
    print("   1. Researches the topic using DIA3 knowledge base")
    print("   2. Determines relevant analysis categories (from 24 available)")
    print("   3. Uses specialized agents for comprehensive analysis")
    print("   4. Generates advanced reports with tooltips and sources")


if __name__ == "__main__":
    asyncio.run(demo_analysis())

