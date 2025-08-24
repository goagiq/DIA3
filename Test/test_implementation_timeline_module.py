#!/usr/bin/env python3
"""
Test Implementation Timeline Module

Test script to verify that the Implementation Timeline Module works correctly.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.implementation_timeline_module import ImplementationTimelineModule


async def test_implementation_timeline_module():
    """Test the Implementation Timeline Module functionality."""
    print("🧪 Testing Implementation Timeline Module")
    
    # Create module instance
    module = ImplementationTimelineModule()
    
    # Test module properties
    print(f"✅ Module ID: {module.module_id}")
    print(f"✅ Module Title: {module.get_title()}")
    print(f"✅ Module Description: {module.get_description()}")
    print(f"✅ Module Order: {module.get_order()}")
    print(f"✅ Module Enabled: {module.is_enabled()}")
    
    # Sample data for testing
    sample_data = {
        "implementation_timeline": {
            "title": "Implementation Timeline Analysis",
            "overview": "Comprehensive analysis of implementation timeline and project phases.",
            "total_duration": "22 weeks",
            "start_date": "2024-01-15",
            "end_date": "2024-06-15",
            "phases": [
                {
                    "name": "Planning Phase",
                    "duration": "4 weeks",
                    "duration_weeks": 4,
                    "status": "Completed",
                    "progress": 1.0
                },
                {
                    "name": "Development Phase",
                    "duration": "8 weeks",
                    "duration_weeks": 8,
                    "status": "In Progress",
                    "progress": 0.75
                },
                {
                    "name": "Testing Phase",
                    "duration": "6 weeks",
                    "duration_weeks": 6,
                    "status": "Not Started",
                    "progress": 0.0
                },
                {
                    "name": "Deployment Phase",
                    "duration": "4 weeks",
                    "duration_weeks": 4,
                    "status": "Not Started",
                    "progress": 0.0
                }
            ]
        },
        "key_milestones": {
            "title": "Key Milestones",
            "overview": "Critical milestones for project success.",
            "milestones": [
                {
                    "name": "Project Kickoff",
                    "date": "2024-01-15",
                    "description": "Official project start with stakeholder alignment.",
                    "status": "Completed",
                    "priority": "High",
                    "dependencies": []
                },
                {
                    "name": "Requirements Finalized",
                    "date": "2024-02-15",
                    "description": "All requirements documented and approved.",
                    "status": "Completed",
                    "priority": "High",
                    "dependencies": ["Project Kickoff"]
                },
                {
                    "name": "Development Complete",
                    "date": "2024-04-15",
                    "description": "Core development work completed.",
                    "status": "In Progress",
                    "priority": "Critical",
                    "dependencies": ["Requirements Finalized"]
                },
                {
                    "name": "Testing Complete",
                    "date": "2024-05-30",
                    "description": "All testing phases completed successfully.",
                    "status": "Not Started",
                    "priority": "High",
                    "dependencies": ["Development Complete"]
                },
                {
                    "name": "Production Deployment",
                    "date": "2024-06-15",
                    "description": "System deployed to production environment.",
                    "status": "Not Started",
                    "priority": "Critical",
                    "dependencies": ["Testing Complete"]
                }
            ],
            "critical_path": ["Project Kickoff", "Requirements Finalized", "Development Complete", "Testing Complete", "Production Deployment"]
        },
        "progress_tracking": {
            "title": "Progress Tracking",
            "overview": "Real-time progress tracking and metrics.",
            "current_progress": 0.45,
            "progress_metrics": {
                "phases_completed": 1,
                "phases_in_progress": 1,
                "phases_remaining": 2,
                "milestones_completed": 2,
                "milestones_remaining": 3
            },
            "progress_trends": [
                {
                    "period": "Week 1-4",
                    "progress": 0.18,
                    "status": "On Track",
                    "notes": "Planning phase completed successfully"
                },
                {
                    "period": "Week 5-8",
                    "progress": 0.36,
                    "status": "On Track",
                    "notes": "Development phase progressing well"
                },
                {
                    "period": "Week 9-12",
                    "progress": 0.45,
                    "status": "On Track",
                    "notes": "Development phase 75% complete"
                }
            ]
        },
        "timeline_analysis": {
            "title": "Timeline Analysis",
            "overview": "Analysis of timeline risks and optimization opportunities.",
            "risk_factors": [
                {
                    "factor": "Resource Constraints",
                    "impact": "High",
                    "probability": "Medium",
                    "mitigation": "Secure additional resources and optimize allocation"
                },
                {
                    "factor": "Technical Challenges",
                    "impact": "Medium",
                    "probability": "Low",
                    "mitigation": "Early prototyping and technical feasibility studies"
                },
                {
                    "factor": "Scope Creep",
                    "impact": "High",
                    "probability": "Medium",
                    "mitigation": "Strict change control and stakeholder management"
                }
            ],
            "optimization_opportunities": [
                {
                    "opportunity": "Parallel Development",
                    "impact": "High",
                    "effort": "Medium",
                    "description": "Develop multiple components in parallel to reduce timeline"
                },
                {
                    "opportunity": "Automated Testing",
                    "impact": "Medium",
                    "effort": "Low",
                    "description": "Implement automated testing to accelerate testing phase"
                }
            ],
            "recommendations": [
                {
                    "title": "Accelerate Development",
                    "description": "Increase development team size to complete development phase faster",
                    "priority": "High",
                    "timeline": "Immediate"
                },
                {
                    "title": "Early Testing",
                    "description": "Begin testing activities in parallel with development",
                    "priority": "Medium",
                    "timeline": "Next 2 weeks"
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
            if "Implementation Timeline Analysis" in content:
                print("✅ Implementation timeline section found")
            else:
                print("❌ Implementation timeline section missing")
                return False
            
            if "Key Milestones" in content:
                print("✅ Key milestones section found")
            else:
                print("❌ Key milestones section missing")
                return False
            
            if "Progress Tracking" in content:
                print("✅ Progress tracking section found")
            else:
                print("❌ Progress tracking section missing")
                return False
            
            if "Timeline Analysis" in content:
                print("✅ Timeline analysis section found")
            else:
                print("❌ Timeline analysis section missing")
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
            output_file = Path("Results") / "test_implementation_timeline_module.html"
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
            "title": "Custom Implementation Timeline",
            "description": "Custom description for testing",
            "order": 35,
            "tooltips_enabled": False,
            "charts_enabled": False
        }
        
        module = ImplementationTimelineModule()
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
        module = ImplementationTimelineModule()
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
    print("🚀 Implementation Timeline Module Test Suite")
    print("=" * 50)
    
    # Run all tests
    test1_passed = await test_implementation_timeline_module()
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
        print("\n🎉 Implementation Timeline Module is working correctly!")
        return True
    else:
        print("\n❌ Implementation Timeline Module needs attention.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
