#!/usr/bin/env python3
"""
Test Regional Sentiment Module

Test script to verify that the Regional Sentiment Module works correctly.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.regional_sentiment_module import RegionalSentimentModule


async def test_regional_sentiment_module():
    """Test the Regional Sentiment Module functionality."""
    print("🧪 Testing Regional Sentiment Module")
    
    # Create module instance
    module = RegionalSentimentModule()
    
    # Test module properties
    print(f"✅ Module ID: {module.module_id}")
    print(f"✅ Module Title: {module.get_title()}")
    print(f"✅ Module Description: {module.get_description()}")
    print(f"✅ Module Order: {module.get_order()}")
    print(f"✅ Module Enabled: {module.is_enabled()}")
    
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
        # Test data validation
        print("\n🔍 Testing data validation...")
        required_keys = module.get_required_data_keys()
        print(f"✅ Required keys: {required_keys}")
        
        # Test content generation
        print("\n📝 Testing content generation...")
        content = module.generate_content(sample_data)
        
        if content:
            print("✅ Content generated successfully")
            print(f"📊 Content length: {len(content)} characters")
            
            # Check for key sections
            if "Regional Sentiment Analysis" in content:
                print("✅ Regional sentiment section found")
            else:
                print("❌ Regional sentiment section missing")
                return False
            
            if "Stakeholder Analysis" in content:
                print("✅ Stakeholder analysis section found")
            else:
                print("❌ Stakeholder analysis section missing")
                return False
            
            if "Diplomatic Implications" in content:
                print("✅ Diplomatic implications section found")
            else:
                print("❌ Diplomatic implications section missing")
                return False
            
            if "Sentiment Trends Analysis" in content:
                print("✅ Sentiment trends section found")
            else:
                print("❌ Sentiment trends section missing")
                return False
            
            if "Interactive Visualizations" in content:
                print("✅ Interactive visualizations section found")
            else:
                print("❌ Interactive visualizations section missing")
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
            
            # Save test output
            output_file = Path("Results") / "test_regional_sentiment_module.html"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Test output saved to: {output_file}")
            
            return True
        else:
            print("❌ Content generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


async def test_module_configuration():
    """Test module configuration functionality."""
    print("\n🔧 Testing module configuration...")
    
    try:
        # Test custom configuration
        custom_config = {
            "title": "Custom Regional Sentiment",
            "description": "Custom description for testing",
            "order": 30,
            "tooltips_enabled": False,
            "charts_enabled": False
        }
        
        module = RegionalSentimentModule()
        module.import_config(custom_config)
        
        print(f"✅ Custom title: {module.get_title()}")
        print(f"✅ Custom description: {module.get_description()}")
        print(f"✅ Custom order: {module.get_order()}")
        print(f"✅ Tooltips enabled: {module.config.tooltips_enabled}")
        print(f"✅ Charts enabled: {module.config.charts_enabled}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def test_empty_data():
    """Test module with empty data."""
    print("\n📭 Testing with empty data...")
    
    try:
        module = RegionalSentimentModule()
        empty_data = {}
        
        content = module.generate_content(empty_data)
        
        if content:
            print("✅ Empty data handling successful")
            return True
        else:
            print("❌ Empty data handling failed")
            return False
            
    except Exception as e:
        print(f"❌ Empty data test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Regional Sentiment Module Test Suite")
    print("=" * 50)
    
    # Run all tests
    test1_passed = await test_regional_sentiment_module()
    test2_passed = await test_module_configuration()
    test3_passed = await test_empty_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Module Functionality: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Configuration: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Empty Data Handling: {'PASSED' if test3_passed else 'FAILED'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    
    if all_passed:
        print("\n🎉 Regional Sentiment Module is working correctly!")
        return True
    else:
        print("\n❌ Regional Sentiment Module needs attention.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
