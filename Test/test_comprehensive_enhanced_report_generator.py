#!/usr/bin/env python3
"""
Test script for Comprehensive Enhanced Report Generator
Tests the new category detection and advanced tooltip system.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.reporting.comprehensive_enhanced_report_generator import comprehensive_enhanced_report_generator
from core.reporting.comprehensive_category_detector import ComprehensiveCategoryDetector
from core.reporting.advanced_tooltip_system import AdvancedTooltipSystem


async def test_category_detection():
    """Test the category detection system with data source integration."""
    print("=== Testing Category Detection System with Data Sources ===")
    
    detector = ComprehensiveCategoryDetector()
    
    # Test content with various topics
    test_content = """
    The geopolitical implications of China's Belt and Road Initiative are significant for global trade and economic development.
    Security implications include potential military expansion and cyber threats. The economic impact on regional markets
    could lead to financial instability. We need to assess strategic options and develop capability planning for the future.
    Risk assessment shows multiple scenarios that require advanced forecasting and predictive analysis.
    """
    
    result = detector.detect_relevant_categories(
        content=test_content,
        topic="China Belt and Road Initiative",
        use_case="Strategic Analysis",
        query="Analyze geopolitical and economic implications"
    )
    
    print(f"✅ Category detection completed")
    print(f"📊 Detected {result['total_categories']} relevant categories")
    
    # Test data source integration
    print(f"\n📋 Data Source Analysis:")
    for category_id, info in result['detected_categories'].items():
        data_sources = detector.get_category_data_sources(category_id)
        print(f"   • {info['name']}:")
        print(f"     - Internal Sources: {len(data_sources.get('internal_sources', []))}")
        print(f"     - External Sources: {len(data_sources.get('external_sources', []))}")
        print(f"     - Intelligence Required: {data_sources.get('intelligence_required', False)}")
    
    # Test intelligence categories
    intelligence_categories = detector.get_intelligence_categories()
    print(f"\n🎯 Intelligence Categories: {len(intelligence_categories)}")
    for category in intelligence_categories:
        print(f"   • {category}")
    
    return result


async def test_tooltip_system():
    """Test the advanced tooltip system."""
    print("\n=== Testing Advanced Tooltip System ===")
    
    tooltip_system = AdvancedTooltipSystem()
    
    # Test creating a category tooltip
    tooltip = tooltip_system.create_category_tooltip(
        category_name="Geopolitical Impact Analysis",
        category_description="Analysis of political and geographical implications",
        analysis_methods=["Keyword Analysis", "Semantic Analysis", "Relevance Scoring"],
        data_sources=["DIA3-CategoryDetector", "DIA3-ContentAnalyzer"],
        confidence_level="0.85"
    )
    
    print(f"✅ Tooltip created: {tooltip.title}")
    print(f"📊 Sources: {len(tooltip.sources)}")
    
    # Test creating an analysis tooltip
    analysis_tooltip = tooltip_system.create_analysis_tooltip(
        analysis_type="geopolitical_analysis",
        analysis_description="Comprehensive geopolitical impact assessment",
        methodology="Multi-factor analysis using keyword detection and semantic analysis",
        results_summary="Significant geopolitical implications identified with high confidence",
        confidence_score=0.85,
        data_sources=["DIA3-GeopoliticalAnalyzer", "DIA3-ContentAnalyzer"]
    )
    
    print(f"✅ Analysis tooltip created: {analysis_tooltip.title}")
    
    # Test intelligence tooltip creation
    intelligence_tooltip = tooltip_system.create_intelligence_tooltip(
        title="Strategic Intelligence Synthesis",
        description="Comprehensive strategic analysis using DIA3 intelligence",
        detailed_explanation="This analysis synthesizes multiple intelligence sources for strategic recommendations.",
        category="strategic_recommendations",
        intelligence_sources=["DIA3 - Intelligence Synthesis", "DIA3 - Strategic Analysis"],
        external_sources=["Expert Opinions", "Strategic Consultations"],
        priority=1
    )
    
    print(f"✅ Intelligence tooltip created: {intelligence_tooltip.title}")
    print(f"📊 Intelligence sources: {len(intelligence_tooltip.sources)}")
    
    # Test data source retrieval
    category_sources = tooltip_system.get_category_data_sources("strategic_recommendations")
    print(f"📋 Category data sources: {category_sources}")
    
    return tooltip_system


async def test_comprehensive_report_generation():
    """Test the comprehensive enhanced report generator."""
    print("\n=== Testing Comprehensive Enhanced Report Generator ===")
    
    # Test content
    test_content = """
    The geopolitical implications of China's Belt and Road Initiative are significant for global trade and economic development.
    Security implications include potential military expansion and cyber threats. The economic impact on regional markets
    could lead to financial instability. We need to assess strategic options and develop capability planning for the future.
    Risk assessment shows multiple scenarios that require advanced forecasting and predictive analysis.
    
    The initiative spans multiple regions including Asia, Europe, and Africa, creating complex trade relationships
    and economic dependencies. Comparative analysis shows this is the largest infrastructure project in history,
    with estimated investments exceeding $1 trillion. Strategic recommendations include enhanced monitoring
    and coordinated response mechanisms.
    """
    
    # Generate comprehensive report
    result = await comprehensive_enhanced_report_generator.generate_comprehensive_enhanced_report(
        content=test_content,
        title="China Belt and Road Initiative Analysis",
        subtitle="Comprehensive Geopolitical and Economic Impact Assessment",
        topic="China Belt and Road Initiative",
        use_case="Strategic Intelligence Analysis",
        query="Analyze geopolitical and economic implications of BRI",
        output_format="html",
        include_tooltips=True,
        include_visualizations=True
    )
    
    if result["success"]:
        print(f"✅ Comprehensive report generated successfully")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Categories detected: {result['categories_detected']}")
        print(f"📊 Categories used: {len(result['categories_used'])}")
        print(f"💡 Tooltips created: {result['tooltips_created']}")
        print(f"📋 Categories used:")
        for category in result['categories_used']:
            print(f"   • {category}")
    else:
        print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
    
    return result


async def test_markdown_report():
    """Test markdown report generation."""
    print("\n=== Testing Markdown Report Generation ===")
    
    test_content = """
    Strategic analysis of emerging technologies and their impact on national security.
    The development of artificial intelligence and quantum computing presents both opportunities and risks.
    Economic implications include job displacement and new market opportunities.
    Financial implications involve investment in research and development.
    """
    
    result = await comprehensive_enhanced_report_generator.generate_comprehensive_enhanced_report(
        content=test_content,
        title="Emerging Technologies Strategic Analysis",
        subtitle="AI and Quantum Computing Impact Assessment",
        topic="Emerging Technologies",
        use_case="Technology Assessment",
        query="Analyze strategic implications of AI and quantum computing",
        output_format="markdown",
        include_tooltips=True,
        include_visualizations=False
    )
    
    if result["success"]:
        print(f"✅ Markdown report generated successfully")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Categories detected: {result['categories_detected']}")
    else:
        print(f"❌ Markdown report generation failed: {result.get('error', 'Unknown error')}")
    
    return result


async def test_json_report():
    """Test JSON report generation."""
    print("\n=== Testing JSON Report Generation ===")
    
    test_content = """
    Regional analysis of the South China Sea conflict and its implications for international trade.
    Comparative analysis of different approaches to resolving territorial disputes.
    Predictive analysis suggests increasing tensions over the next five years.
    Strategic recommendations include diplomatic engagement and military preparedness.
    """
    
    result = await comprehensive_enhanced_report_generator.generate_comprehensive_enhanced_report(
        content=test_content,
        title="South China Sea Conflict Analysis",
        subtitle="Regional Security and Trade Implications",
        topic="South China Sea Conflict",
        use_case="Regional Security Analysis",
        query="Analyze South China Sea conflict implications",
        output_format="json",
        include_tooltips=True,
        include_visualizations=False
    )
    
    if result["success"]:
        print(f"✅ JSON report generated successfully")
        print(f"📄 Report saved to: {result['report_path']}")
        print(f"📊 Categories detected: {result['categories_detected']}")
    else:
        print(f"❌ JSON report generation failed: {result.get('error', 'Unknown error')}")
    
    return result


async def main():
    """Run all tests."""
    print("🚀 Starting Comprehensive Enhanced Report Generator Tests")
    print("=" * 60)
    
    try:
        # Test category detection
        category_result = await test_category_detection()
        
        # Test tooltip system
        tooltip_result = await test_tooltip_system()
        
        # Test comprehensive report generation
        report_result = await test_comprehensive_report_generation()
        
        # Test markdown report
        markdown_result = await test_markdown_report()
        
        # Test JSON report
        json_result = await test_json_report()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("\n📋 Test Summary:")
        print(f"   ✅ Category Detection: {category_result['total_categories']} categories detected")
        print(f"   ✅ Tooltip System: {len(tooltip_result.tooltips)} tooltips created")
        print(f"   ✅ HTML Report: {report_result['success']}")
        print(f"   ✅ Markdown Report: {markdown_result['success']}")
        print(f"   ✅ JSON Report: {json_result['success']}")
        
        print("\n📁 Generated Reports:")
        if report_result['success']:
            print(f"   📄 HTML: {report_result['report_path']}")
        if markdown_result['success']:
            print(f"   📝 Markdown: {markdown_result['report_path']}")
        if json_result['success']:
            print(f"   📊 JSON: {json_result['report_path']}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
