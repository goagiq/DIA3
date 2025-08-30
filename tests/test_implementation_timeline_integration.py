#!/usr/bin/env python3
"""
Test Implementation Timeline Module Integration

Quick test to verify that the Implementation Timeline Module integrates correctly with the modular report generator.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator


async def test_implementation_timeline_integration():
    """Test Implementation Timeline Module integration with modular report generator."""
    print("🧪 Testing Implementation Timeline Module Integration")
    
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
                    "name": "Development Complete",
                    "date": "2024-04-15",
                    "description": "Core development work completed.",
                    "status": "In Progress",
                    "priority": "Critical",
                    "dependencies": ["Project Kickoff"]
                }
            ],
            "critical_path": ["Project Kickoff", "Development Complete"]
        },
        "progress_tracking": {
            "title": "Progress Tracking",
            "overview": "Real-time progress tracking and metrics.",
            "current_progress": 0.45,
            "progress_metrics": {
                "phases_completed": 1,
                "phases_in_progress": 1
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
                }
            ],
            "optimization_opportunities": [
                {
                    "opportunity": "Parallel Development",
                    "impact": "High",
                    "effort": "Medium",
                    "description": "Develop multiple components in parallel to reduce timeline"
                }
            ],
            "recommendations": [
                {
                    "title": "Accelerate Development",
                    "description": "Increase development team size to complete development phase faster",
                    "priority": "High",
                    "timeline": "Immediate"
                }
            ]
        }
    }
    
    try:
        # Generate report with Implementation Timeline Module
        result = await modular_report_generator.generate_modular_report(
            topic="Implementation Timeline Integration Test",
            data=sample_data,
            enabled_modules=["implementationtimelinemodule"],
            report_title="Implementation Timeline Integration Test"
        )
        
        if result.get("success"):
            print(f"✅ Report generated successfully!")
            print(f"📄 File: {result.get('filename')}")
            print(f"📁 Path: {result.get('file_path')}")
            print(f"📊 Size: {result.get('file_size')} bytes")
            
            # Check the generated file for Implementation Timeline Module content
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for Implementation Timeline Module sections
                if "Implementation Timeline Analysis" in content:
                    print("✅ Implementation Timeline Analysis section found")
                else:
                    print("❌ Implementation Timeline Analysis section missing")
                    return False
                
                if "Key Milestones" in content:
                    print("✅ Key Milestones section found")
                else:
                    print("❌ Key Milestones section missing")
                    return False
                
                if "Progress Tracking" in content:
                    print("✅ Progress Tracking section found")
                else:
                    print("❌ Progress Tracking section missing")
                    return False
                
                if "Timeline Analysis" in content:
                    print("✅ Timeline Analysis section found")
                else:
                    print("❌ Timeline Analysis section missing")
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


async def main():
    """Main test function."""
    print("🚀 Implementation Timeline Module Integration Test")
    print("=" * 60)
    
    # Run integration test
    test_passed = await test_implementation_timeline_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Integration Test Results Summary")
    print("=" * 60)
    print(f"✅ Implementation Timeline Integration: {'PASSED' if test_passed else 'FAILED'}")
    
    if test_passed:
        print("\n🎉 Implementation Timeline Module integration is working correctly!")
        return True
    else:
        print("\n❌ Implementation Timeline Module integration needs attention.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
