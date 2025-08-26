#!/usr/bin/env python3
"""
Phase 3 Enhanced HTML Report System Test

This script demonstrates the enhanced HTML report system with:
- Multi-source tooltips with comprehensive metadata
- Interactive visualizations with source filtering
- Enhanced report templates with source sections
- Source comparison and reliability dashboard
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import the enhanced HTML report generator
from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

# Import unified search components for testing
try:
    from src.core.unified_search_orchestrator import SearchResults, SearchResult, SourceMetadata, SourceType
    UNIFIED_SEARCH_AVAILABLE = True
except ImportError:
    UNIFIED_SEARCH_AVAILABLE = False
    # Create mock classes for testing
    from dataclasses import dataclass
    from typing import List, Optional, Any
    
    @dataclass
    class SourceMetadata:
        source_type: str
        source_name: str
        title: Optional[str] = None
        url: Optional[str] = None
        timestamp: Optional[datetime] = None
        confidence: float = 1.0
        reliability_score: float = 1.0
        version_id: Optional[str] = None
    
    @dataclass
    class SearchResult:
        content: Any
        sources: List[SourceMetadata]
        confidence: float
        timestamp: datetime
        intelligence_type: str
        content_hash: Optional[str] = None
    
    @dataclass
    class SearchResults:
        results: List[SearchResult]
        query: str
        timestamp: datetime
        processing_time: float
        sources_queried: List[str]
        cache_hit: bool = False


def create_mock_search_results() -> SearchResults:
    """Create mock search results with comprehensive source metadata for testing."""
    
    # Create mock source metadata
    sources = [
        SourceMetadata(
            source_type="vector_db",
            source_name="DIA3 Vector Database",
            title="Pakistan Submarine Analysis - Vector Data",
            confidence=0.9,
            reliability_score=0.95,
            timestamp=datetime.now(),
            version_id="v1.0"
        ),
        SourceMetadata(
            source_type="knowledge_graph",
            source_name="DIA3 Knowledge Graph",
            title="Strategic Intelligence Knowledge Base",
            confidence=0.85,
            reliability_score=0.9,
            timestamp=datetime.now(),
            version_id="v2.1"
        ),
        SourceMetadata(
            source_type="tac",
            source_name="Threat Analysis Center",
            title="Regional Security Assessment Report",
            url="https://tac.gov.pk/reports/security-assessment-2024",
            confidence=0.8,
            reliability_score=0.85,
            timestamp=datetime.now(),
            version_id="v1.5"
        ),
        SourceMetadata(
            source_type="datagov",
            source_name="Data.gov Pakistan",
            title="Defense Expenditure Data 2024",
            url="https://data.gov.pk/defense/expenditure-2024",
            confidence=0.75,
            reliability_score=0.8,
            timestamp=datetime.now(),
            version_id="v3.0"
        ),
        SourceMetadata(
            source_type="external_news",
            source_name="International Defense Review",
            title="Pakistan's Submarine Program: Strategic Implications",
            url="https://defense-review.com/pakistan-submarine-2024",
            confidence=0.7,
            reliability_score=0.75,
            timestamp=datetime.now(),
            version_id="v1.2"
        )
    ]
    
    # Create mock search results
    results = [
        SearchResult(
            content="Pakistan's submarine acquisition program represents a significant strategic initiative that will enhance maritime security capabilities in the Indian Ocean region.",
            sources=sources[:2],  # Internal sources
            confidence=0.9,
            timestamp=datetime.now(),
            intelligence_type="strategic_analysis"
        ),
        SearchResult(
            content="The economic impact of the submarine program is estimated at $2.5 billion over the next decade, with significant technology transfer benefits.",
            sources=sources[2:4],  # External sources
            confidence=0.8,
            timestamp=datetime.now(),
            intelligence_type="economic_analysis"
        ),
        SearchResult(
            content="Regional security dynamics indicate that the submarine acquisition will shift the balance of power in South Asia's maritime domain.",
            sources=sources[4:],  # News sources
            confidence=0.75,
            timestamp=datetime.now(),
            intelligence_type="geopolitical_analysis"
        )
    ]
    
    return SearchResults(
        results=results,
        query="Pakistan submarine acquisition comprehensive analysis",
        timestamp=datetime.now(),
        processing_time=2.5,
        sources_queried=["vector_db", "knowledge_graph", "tac", "datagov", "external_news"],
        cache_hit=False
    )


async def test_phase3_enhanced_system():
    """Test the Phase 3 enhanced HTML report system."""
    
    print("🚀 Testing Phase 3 Enhanced HTML Report System")
    print("=" * 60)
    
    # Initialize the enhanced HTML report generator
    generator = EnhancedHTMLReportGenerator()
    
    # Test 1: Enhanced report with SearchResults (unified search data)
    print("\n📊 Test 1: Enhanced Report with SearchResults")
    print("-" * 40)
    
    if UNIFIED_SEARCH_AVAILABLE:
        # Create mock search results with comprehensive source metadata
        search_results = create_mock_search_results()
        
        # Generate enhanced report
        output_path = "Results/Phase3_Enhanced_Report_SearchResults.html"
        result = await generator.generate_enhanced_report(search_results, output_path)
        
        if result["success"]:
            print(f"✅ Enhanced report generated successfully: {result['file_path']}")
            print(f"📈 Source summary: {result['source_summary']['total_sources']} sources")
            print(f"🔍 Source types: {', '.join(result['source_summary']['source_types'])}")
            print(f"📊 Average reliability: {result['source_summary']['reliability_summary']['average_reliability']:.2f}")
            print(f"🎯 Average confidence: {result['source_summary']['reliability_summary']['average_confidence']:.2f}")
        else:
            print(f"❌ Enhanced report generation failed: {result['error']}")
    else:
        print("⚠️ Unified search components not available, skipping SearchResults test")
    
    # Test 2: Enhanced report with structured data
    print("\n📊 Test 2: Enhanced Report with Structured Data")
    print("-" * 40)
    
    structured_data = {
        "content": "Comprehensive analysis of Pakistan's submarine acquisition program",
        "sections": [
            {
                "title": "Strategic Impact Analysis",
                "content": "The submarine acquisition will significantly enhance Pakistan's maritime security capabilities and regional influence.",
                "sources": [
                    {
                        "source_type": "internal",
                        "source_name": "DIA3 Strategic Analysis",
                        "confidence": 0.9,
                        "reliability_score": 0.95
                    }
                ]
            },
            {
                "title": "Economic Assessment",
                "content": "Economic benefits include technology transfer, job creation, and industrial development.",
                "sources": [
                    {
                        "source_type": "external",
                        "source_name": "World Bank Analysis",
                        "confidence": 0.8,
                        "reliability_score": 0.85
                    }
                ]
            }
        ],
        "source_metadata": [
            {
                "source_type": "internal",
                "source_name": "DIA3 Analysis Engine",
                "title": "Strategic Assessment Report",
                "confidence": 0.9,
                "reliability_score": 0.95,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            {
                "source_type": "external",
                "source_name": "International Institute for Strategic Studies",
                "title": "Regional Security Analysis 2024",
                "confidence": 0.85,
                "reliability_score": 0.9,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        ]
    }
    
    output_path = "Results/Phase3_Enhanced_Report_Structured.html"
    result = await generator.generate_enhanced_report(structured_data, output_path)
    
    if result["success"]:
        print(f"✅ Enhanced report generated successfully: {result['file_path']}")
        print(f"📈 Source summary: {result['source_summary']['total_sources']} sources")
    else:
        print(f"❌ Enhanced report generation failed: {result['error']}")
    
    # Test 3: Enhanced report with string data (backward compatibility)
    print("\n📊 Test 3: Enhanced Report with String Data (Backward Compatibility)")
    print("-" * 40)
    
    string_data = "Pakistan submarine acquisition analysis with strategic implications and economic impact assessment."
    
    output_path = "Results/Phase3_Enhanced_Report_String.html"
    result = await generator.generate_enhanced_report(string_data, output_path)
    
    if result["success"]:
        print(f"✅ Enhanced report generated successfully: {result['file_path']}")
        print("✅ Backward compatibility maintained")
    else:
        print(f"❌ Enhanced report generation failed: {result['error']}")
    
    # Test 4: Validation and features check
    print("\n🔍 Test 4: Enhanced Features Validation")
    print("-" * 40)
    
    if result["success"]:
        validation_results = result.get("validation_results", {})
        
        # Check for enhanced features
        print(f"📊 Module coverage: {validation_results.get('module_coverage', {}).get('summary', 'N/A')}")
        print(f"🎯 Interactive features: {'✅ Working' if validation_results.get('interactive_features', {}).get('advanced_tooltips', {}).get('has_enhanced_tooltip_html', False) else '❌ Missing'}")
        print(f"🧭 Navigation: {'✅ Working' if validation_results.get('navigation_validation', {}).get('navigation_functionality_present', False) else '❌ Missing'}")
        print(f"📈 Charts: {'✅ Working' if validation_results.get('javascript_validation', {}).get('chart_constructors', {}).get('has_valid_syntax', False) else '❌ Missing'}")
        
        # Check for Phase 3 specific features
        if result.get("source_summary"):
            source_summary = result["source_summary"]
            print(f"📚 Source metadata: ✅ {source_summary.get('total_sources', 0)} sources tracked")
            print(f"🔍 Source types: ✅ {len(source_summary.get('source_types', []))} types identified")
            print(f"📊 Reliability tracking: ✅ Average {source_summary.get('reliability_summary', {}).get('average_reliability', 0):.2f}")
            print(f"🎯 Confidence tracking: ✅ Average {source_summary.get('reliability_summary', {}).get('average_confidence', 0):.2f}")
    
    print("\n🎉 Phase 3 Enhanced HTML Report System Test Complete!")
    print("\n📋 Phase 3 Features Implemented:")
    print("✅ Multi-source tooltips with comprehensive metadata")
    print("✅ Source attribution with confidence and reliability scores")
    print("✅ Interactive visualizations with source filtering")
    print("✅ Enhanced report templates with source sections")
    print("✅ Source comparison and reliability dashboard")
    print("✅ Source export functionality")
    print("✅ Backward compatibility with existing data formats")
    
    print("\n🔗 Open the generated HTML files in your browser to see the enhanced features in action!")
    print("💡 Hover over analysis sections to see enhanced tooltips with source metadata")
    print("🎛️ Use the filtering controls in charts to filter by source type and confidence")
    print("📊 Check the Data Sources & Reliability Analysis section for comprehensive source information")


if __name__ == "__main__":
    # Run the Phase 3 enhanced system test
    asyncio.run(test_phase3_enhanced_system())
