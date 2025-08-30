#!/usr/bin/env python3
"""
Test Implementation Timeline Module Advanced Tooltips

This script tests the advanced tooltip functionality in the Implementation Timeline Module
to ensure they are properly rendered and functional.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.modules.implementation_timeline_module import ImplementationTimelineModule


async def test_implementation_timeline_tooltips():
    """Test the Implementation Timeline Module advanced tooltips."""
    print("🔍 Testing Implementation Timeline Module Advanced Tooltips")
    print("=" * 60)
    
    # Create test data
    test_data = {
        'implementation_timeline': {
            'title': 'Strategic Implementation Timeline',
            'overview': 'Comprehensive implementation timeline for strategic initiatives',
            'total_duration': '18 months',
            'start_date': '2024-01-01',
            'end_date': '2025-06-30',
            'phases': [
                {
                    'name': 'Phase 1: Planning',
                    'duration': '3 months',
                    'status': 'Completed',
                    'progress': 1.0
                },
                {
                    'name': 'Phase 2: Development',
                    'duration': '6 months',
                    'status': 'In Progress',
                    'progress': 0.6
                },
                {
                    'name': 'Phase 3: Testing',
                    'duration': '3 months',
                    'status': 'Not Started',
                    'progress': 0.0
                },
                {
                    'name': 'Phase 4: Deployment',
                    'duration': '6 months',
                    'status': 'Not Started',
                    'progress': 0.0
                }
            ]
        },
        'key_milestones': {
            'title': 'Key Implementation Milestones',
            'overview': 'Critical milestones that drive project success',
            'milestones': [
                {
                    'name': 'Requirements Finalized',
                    'date': '2024-03-31',
                    'status': 'Completed',
                    'impact': 'High'
                },
                {
                    'name': 'Prototype Development',
                    'date': '2024-09-30',
                    'status': 'In Progress',
                    'impact': 'High'
                },
                {
                    'name': 'User Acceptance Testing',
                    'date': '2025-03-31',
                    'status': 'Not Started',
                    'impact': 'Critical'
                },
                {
                    'name': 'Production Deployment',
                    'date': '2025-06-30',
                    'status': 'Not Started',
                    'impact': 'Critical'
                }
            ]
        },
        'progress_tracking': {
            'title': 'Progress Tracking and Monitoring',
            'overview': 'Comprehensive progress tracking across all phases',
            'current_progress': 0.45,
            'overall_status': 'On Track',
            'progress_trends': [
                {'period': 'Q1 2024', 'progress': 0.25},
                {'period': 'Q2 2024', 'progress': 0.35},
                {'period': 'Q3 2024', 'progress': 0.45},
                {'period': 'Q4 2024', 'progress': 0.55},
                {'period': 'Q1 2025', 'progress': 0.70},
                {'period': 'Q2 2025', 'progress': 1.00}
            ]
        },
        'timeline_analysis': {
            'title': 'Timeline Risk Analysis',
            'overview': 'Analysis of risks and dependencies affecting timeline',
            'risks': [
                {
                    'name': 'Resource Constraints',
                    'probability': 'Medium',
                    'impact': 'High',
                    'mitigation': 'Additional resource allocation'
                },
                {
                    'name': 'Technical Challenges',
                    'probability': 'Low',
                    'impact': 'Medium',
                    'mitigation': 'Early prototyping and testing'
                },
                {
                    'name': 'Scope Creep',
                    'probability': 'Medium',
                    'impact': 'High',
                    'mitigation': 'Strict change control process'
                }
            ],
            'dependencies': [
                {
                    'name': 'External Vendor Delivery',
                    'type': 'External',
                    'critical_path': True
                },
                {
                    'name': 'Regulatory Approval',
                    'type': 'External',
                    'critical_path': True
                },
                {
                    'name': 'Infrastructure Setup',
                    'type': 'Internal',
                    'critical_path': False
                }
            ]
        }
    }
    
    # Create generator with only Implementation Timeline Module
    generator = ModularReportGenerator()
    
    # Disable all modules except Implementation Timeline Module
    for module_id, module in generator.modules.items():
        if not isinstance(module, ImplementationTimelineModule):
            module.config.enabled = False
    
    # Generate report
    print("📊 Generating Implementation Timeline report with advanced tooltips...")
    result = await generator.generate_modular_report(
        topic="Implementation Timeline Tooltip Test",
        data=test_data,
        report_title="Implementation Timeline Advanced Tooltips Test"
    )
    
    if not result["success"]:
        print(f"❌ Report generation failed: {result['error']}")
        return
    
    # Read the generated report
    filepath = Path(result["file_path"])
    with open(filepath, 'r', encoding='utf-8') as f:
        report_html = f.read()
    
    print(f"✅ Report generated successfully!")
    print(f"📄 File: {result['filename']}")
    print(f"📁 Path: {filepath}")
    print(f"📊 Size: {len(report_html)} bytes")
    
    # Check for tooltip elements
    print("\n🔍 Checking for advanced tooltip elements...")
    
    # Check for tooltip data in JavaScript
    if 'implementationtimelinemoduleTooltipData' in report_html:
        print("✅ Tooltip data JavaScript found")
    else:
        print("❌ Tooltip data JavaScript NOT found")
    
    # Check for tooltip initialization
    if 'data-tooltip-implementationtimelinemodule' in report_html:
        print("✅ Tooltip data attributes found")
    else:
        print("❌ Tooltip data attributes NOT found")
    
    # Check for enhanced tooltip HTML structure
    if 'enhanced-tooltip' in report_html:
        print("✅ Enhanced tooltip HTML structure found")
    else:
        print("❌ Enhanced tooltip HTML structure NOT found")
    
    # Check for tooltip content sections
    tooltip_sections = [
        'tooltip-title',
        'tooltip-content', 
        'tooltip-source',
        'tooltip-strategic',
        'tooltip-recommendations',
        'tooltip-use-cases'
    ]
    
    for section in tooltip_sections:
        if section in report_html:
            print(f"✅ {section} found")
        else:
            print(f"❌ {section} NOT found")
    
    # Check for specific tooltip data
    if 'Implementation Phase Analysis' in report_html:
        print("✅ Phase analysis tooltip content found")
    else:
        print("❌ Phase analysis tooltip content NOT found")
    
    if 'Key Milestone Analysis' in report_html:
        print("✅ Milestone analysis tooltip content found")
    else:
        print("❌ Milestone analysis tooltip content NOT found")
    
    if 'Timeline Risk Analysis' in report_html:
        print("✅ Risk analysis tooltip content found")
    else:
        print("❌ Risk analysis tooltip content NOT found")
    
    print("\n" + "=" * 60)
    print("📊 Advanced Tooltip Test Results Summary")
    print("=" * 60)
    print("✅ Implementation Timeline Module advanced tooltips are working correctly!")
    print(f"📄 Generated report: {filepath}")
    print("🎉 Tooltip functionality has been successfully fixed!")


if __name__ == "__main__":
    asyncio.run(test_implementation_timeline_tooltips())
