#!/usr/bin/env python3
"""
Test Regional Sentiment Module Integration

Test script to verify that the Regional Sentiment Module integrates correctly with the modular report generator.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator


async def test_regional_sentiment_integration():
    """Test Regional Sentiment Module integration with modular report generator."""
    print("🧪 Testing Regional Sentiment Module Integration")
    
    # Sample data for testing
    sample_data = {
        "regional_sentiment": {
            "title": "Regional Sentiment Analysis",
            "overview": "Comprehensive analysis of regional sentiment trends across key geopolitical regions.",
            "overall_sentiment": "Positive",
            "confidence_score": 0.85,
            "key_regions": [
                {
                    "name": "South Asia",
                    "sentiment": "Positive",
                    "confidence": 0.82,
                    "sentiment_score": 75
                },
                {
                    "name": "Southeast Asia",
                    "sentiment": "Neutral",
                    "confidence": 0.78,
                    "sentiment_score": 65
                },
                {
                    "name": "Middle East",
                    "sentiment": "Negative",
                    "confidence": 0.71,
                    "sentiment_score": 45
                }
            ]
        },
        "stakeholder_analysis": {
            "title": "Stakeholder Analysis",
            "overview": "Analysis of key stakeholders and their influence on regional sentiment.",
            "stakeholders": [
                {
                    "name": "Government Officials",
                    "type": "Political",
                    "sentiment": "Positive",
                    "influence_level": "High",
                    "influence_score": 85
                },
                {
                    "name": "Business Leaders",
                    "type": "Economic",
                    "sentiment": "Neutral",
                    "influence_level": "Medium",
                    "influence_score": 70
                },
                {
                    "name": "Civil Society",
                    "type": "Social",
                    "sentiment": "Positive",
                    "influence_level": "Medium",
                    "influence_score": 60
                }
            ],
            "impact_assessment": {
                "primary_impact": "Regional cooperation enhancement",
                "secondary_impact": "Economic integration",
                "risk_level": "Low"
            }
        },
        "diplomatic_implications": [
            {
                "title": "Enhanced Regional Cooperation",
                "implication": "Positive sentiment trends suggest opportunities for enhanced regional cooperation and diplomatic engagement.",
                "impact_level": "High",
                "timeline": "6-12 months",
                "confidence": 0.80
            },
            {
                "title": "Trade Agreement Prospects",
                "implication": "Favorable stakeholder sentiment indicates potential for new trade agreements and economic partnerships.",
                "impact_level": "Medium",
                "timeline": "12-18 months",
                "confidence": 0.75
            }
        ],
        "sentiment_trends": {
            "title": "Sentiment Trends Analysis",
            "overview": "Analysis of sentiment trends over the past 6 months shows overall positive trajectory.",
            "time_period": "Last 6 months",
            "trends": [
                {
                    "period": "January",
                    "positive_sentiment": 65,
                    "neutral_sentiment": 25,
                    "negative_sentiment": 10
                },
                {
                    "period": "February",
                    "positive_sentiment": 68,
                    "neutral_sentiment": 24,
                    "negative_sentiment": 8
                },
                {
                    "period": "March",
                    "positive_sentiment": 72,
                    "neutral_sentiment": 22,
                    "negative_sentiment": 6
                },
                {
                    "period": "April",
                    "positive_sentiment": 75,
                    "neutral_sentiment": 20,
                    "negative_sentiment": 5
                },
                {
                    "period": "May",
                    "positive_sentiment": 78,
                    "neutral_sentiment": 18,
                    "negative_sentiment": 4
                },
                {
                    "period": "June",
                    "positive_sentiment": 80,
                    "neutral_sentiment": 16,
                    "negative_sentiment": 4
                }
            ]
        }
    }
    
    try:
        # Generate report with Regional Sentiment Module
        result = await modular_report_generator.generate_modular_report(
            topic="Regional Sentiment Integration Test",
            data=sample_data,
            enabled_modules=["regionalsentimentmodule"],
            report_title="Regional Sentiment Integration Test"
        )
        
        if result.get("success"):
            print(f"✅ Report generated successfully!")
            print(f"📄 File: {result.get('filename')}")
            print(f"📁 Path: {result.get('file_path')}")
            print(f"📊 Size: {result.get('file_size')} bytes")
            
            # Check the generated file for Regional Sentiment Module content
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for Regional Sentiment Module sections
                if "Regional Sentiment Analysis" in content:
                    print("✅ Regional Sentiment Analysis section found")
                else:
                    print("❌ Regional Sentiment Analysis section missing")
                    return False
                
                if "Stakeholder Analysis" in content:
                    print("✅ Stakeholder Analysis section found")
                else:
                    print("❌ Stakeholder Analysis section missing")
                    return False
                
                if "Diplomatic Implications" in content:
                    print("✅ Diplomatic Implications section found")
                else:
                    print("❌ Diplomatic Implications section missing")
                    return False
                
                if "Sentiment Trends Analysis" in content:
                    print("✅ Sentiment Trends Analysis section found")
                else:
                    print("❌ Sentiment Trends Analysis section missing")
                    return False
                
                if "Interactive Visualizations" in content:
                    print("✅ Interactive Visualizations section found")
                else:
                    print("❌ Interactive Visualizations section missing")
                    return False
                
                # Check for chart containers
                if "chart-container" in content:
                    print("✅ Chart containers found")
                else:
                    print("❌ Chart containers missing")
                    return False
                
                # Check for tooltips
                if "data-tooltip" in content:
                    print("✅ Tooltip system found")
                else:
                    print("❌ Tooltip system missing")
                    return False
                
                return True
            else:
                print("❌ Generated file not found")
                return False
        else:
            print(f"❌ Report generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


async def test_multiple_modules_integration():
    """Test Regional Sentiment Module with other modules."""
    print("\n🧪 Testing Multiple Modules Integration")
    
    # Sample data for multiple modules
    sample_data = {
        "regional_sentiment": {
            "title": "Regional Sentiment Analysis",
            "overview": "Comprehensive analysis of regional sentiment trends.",
            "overall_sentiment": "Positive",
            "confidence_score": 0.85,
            "key_regions": [
                {
                    "name": "South Asia",
                    "sentiment": "Positive",
                    "confidence": 0.82,
                    "sentiment_score": 75
                }
            ]
        },
        "stakeholder_analysis": {
            "title": "Stakeholder Analysis",
            "overview": "Analysis of key stakeholders.",
            "stakeholders": [
                {
                    "name": "Government Officials",
                    "type": "Political",
                    "sentiment": "Positive",
                    "influence_level": "High",
                    "influence_score": 85
                }
            ]
        },
        "diplomatic_implications": [
            {
                "title": "Enhanced Regional Cooperation",
                "implication": "Positive sentiment trends suggest opportunities.",
                "impact_level": "High",
                "timeline": "6-12 months",
                "confidence": 0.80
            }
        ],
        "sentiment_trends": {
            "title": "Sentiment Trends Analysis",
            "overview": "Analysis of sentiment trends.",
            "time_period": "Last 6 months",
            "trends": [
                {
                    "period": "January",
                    "positive_sentiment": 65,
                    "neutral_sentiment": 25,
                    "negative_sentiment": 10
                }
            ]
        },
        "strategic_analysis": {
            "title": "Strategic Analysis",
            "overview": "Strategic analysis overview.",
            "key_components": ["Component 1", "Component 2"],
            "confidence_level": 0.85
        },
        "strategic_insights": {
            "title": "Strategic Insights",
            "insights": ["Insight 1", "Insight 2"],
            "categories": {"category1": "Category 1"}
        },
        "geopolitical_impact": {
            "title": "Geopolitical Impact",
            "regional_impact": {"Region 1": "Impact 1"},
            "global_implications": ["Implication 1"]
        },
        "strategic_implications": ["Implication 1", "Implication 2"]
    }
    
    try:
        # Generate report with multiple modules
        result = await modular_report_generator.generate_modular_report(
            topic="Multiple Modules Integration Test",
            data=sample_data,
            enabled_modules=["regionalsentimentmodule", "strategicanalysismodule"],
            report_title="Multiple Modules Integration Test"
        )
        
        if result.get("success"):
            print(f"✅ Multi-module report generated successfully!")
            print(f"📄 File: {result.get('filename')}")
            print(f"📁 Path: {result.get('file_path')}")
            print(f"📊 Size: {result.get('file_size')} bytes")
            
            # Check the generated file
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for both modules
                if "Regional Sentiment Analysis" in content and "Strategic Analysis" in content:
                    print("✅ Both modules found in report")
                    return True
                else:
                    print("❌ Not all modules found in report")
                    return False
            else:
                print("❌ Generated file not found")
                return False
        else:
            print(f"❌ Multi-module report generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error during multi-module testing: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Regional Sentiment Module Integration Test Suite")
    print("=" * 60)
    
    # Run integration tests
    test1_passed = await test_regional_sentiment_integration()
    test2_passed = await test_multiple_modules_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Integration Test Results Summary")
    print("=" * 60)
    print(f"✅ Single Module Integration: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Multiple Modules Integration: {'PASSED' if test2_passed else 'FAILED'}")
    
    all_passed = test1_passed and test2_passed
    
    if all_passed:
        print("\n🎉 Regional Sentiment Module integration is working correctly!")
        return True
    else:
        print("\n❌ Regional Sentiment Module integration needs attention.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
