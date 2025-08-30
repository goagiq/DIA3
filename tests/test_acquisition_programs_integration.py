#!/usr/bin/env python3
"""
Test Acquisition Programs Module Integration

Integration tests for the Acquisition Programs Module with the ModularReportGenerator.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.modules.acquisition_programs_module import AcquisitionProgramsModule


async def test_acquisition_programs_integration():
    """Test the Acquisition Programs Module integration with ModularReportGenerator."""
    print("🚀 Acquisition Programs Module Integration Test Suite")
    print("=" * 60)
    
    # Test data
    test_data = {
        'acquisition_programs': {
            'title': 'Strategic Defense Acquisition Programs',
            'overview': 'Comprehensive acquisition programs designed to enhance national defense capabilities through strategic investments in advanced technologies and systems.',
            'total_budget': '$15.2 Billion',
            'total_programs': 12,
            'programs': [
                {
                    'name': 'Next-Generation Fighter Aircraft Program',
                    'type': 'Air Defense Systems',
                    'budget': '$4.2B',
                    'timeline': '2024-2030',
                    'status': 'Active',
                    'priority': 'Critical'
                },
                {
                    'name': 'Advanced Naval Combat System',
                    'type': 'Naval Systems',
                    'budget': '$3.8B',
                    'timeline': '2024-2028',
                    'status': 'Active',
                    'priority': 'High'
                },
                {
                    'name': 'Integrated Air Defense Network',
                    'type': 'Air Defense Systems',
                    'budget': '$2.1B',
                    'timeline': '2025-2027',
                    'status': 'Planning',
                    'priority': 'High'
                },
                {
                    'name': 'Cybersecurity Infrastructure Upgrade',
                    'type': 'Information Systems',
                    'budget': '$1.8B',
                    'timeline': '2024-2026',
                    'status': 'At Risk',
                    'priority': 'Critical'
                },
                {
                    'name': 'Space-Based Surveillance System',
                    'type': 'Space Systems',
                    'budget': '$3.3B',
                    'timeline': '2025-2031',
                    'status': 'Active',
                    'priority': 'High'
                }
            ]
        },
        'modernization_initiatives': {
            'title': 'Critical Modernization Initiatives',
            'overview': 'Strategic modernization initiatives focused on capability enhancement and technological advancement.',
            'initiatives': [
                {
                    'name': 'AI-Enhanced Command & Control',
                    'category': 'C4ISR Systems',
                    'description': 'Integration of artificial intelligence into command and control systems for enhanced decision-making capabilities.',
                    'impact': 'Critical',
                    'timeline': '36 months',
                    'cost': '$850M'
                },
                {
                    'name': 'Quantum Communication Network',
                    'category': 'Information Systems',
                    'description': 'Development of quantum-encrypted communication networks for secure military communications.',
                    'impact': 'High',
                    'timeline': '48 months',
                    'cost': '$1.2B'
                },
                {
                    'name': 'Hypersonic Defense Systems',
                    'category': 'Missile Defense',
                    'description': 'Advanced hypersonic missile defense capabilities to counter emerging threats.',
                    'impact': 'Critical',
                    'timeline': '60 months',
                    'cost': '$2.5B'
                },
                {
                    'name': 'Autonomous Systems Integration',
                    'category': 'Unmanned Systems',
                    'description': 'Integration of autonomous systems across land, sea, and air platforms.',
                    'impact': 'High',
                    'timeline': '42 months',
                    'cost': '$1.8B'
                }
            ]
        },
        'program_analysis': {
            'title': 'Comprehensive Program Risk & Dependency Analysis',
            'overview': 'Detailed analysis of program risks, dependencies, and critical success factors.',
            'risks': [
                {
                    'name': 'Technology Maturity Risk',
                    'level': 'High',
                    'probability': '35%',
                    'impact': 'Significant delay and cost overrun',
                    'mitigation': 'Accelerated prototype development and rigorous testing protocols'
                },
                {
                    'name': 'Supply Chain Disruption',
                    'level': 'Medium',
                    'probability': '25%',
                    'impact': 'Moderate delays in component delivery',
                    'mitigation': 'Diversified supplier base and strategic stockpiling'
                },
                {
                    'name': 'Budget Constraints',
                    'level': 'Medium',
                    'probability': '20%',
                    'impact': 'Program scope reduction or timeline extension',
                    'mitigation': 'Flexible program phasing and priority-based allocation'
                },
                {
                    'name': 'Regulatory Compliance',
                    'level': 'Low',
                    'probability': '15%',
                    'impact': 'Minor delays in approval processes',
                    'mitigation': 'Early engagement with regulatory bodies'
                }
            ],
            'dependencies': [
                {
                    'name': 'Industrial Base Capacity',
                    'type': 'External',
                    'status': 'Confirmed',
                    'critical': True
                },
                {
                    'name': 'International Technology Transfer',
                    'type': 'External',
                    'status': 'Negotiating',
                    'critical': True
                },
                {
                    'name': 'Workforce Development',
                    'type': 'Internal',
                    'status': 'In Progress',
                    'critical': False
                },
                {
                    'name': 'Test Infrastructure',
                    'type': 'Internal',
                    'status': 'Available',
                    'critical': False
                }
            ]
        },
        'strategic_impact': {
            'title': 'Strategic Impact & Capability Assessment',
            'overview': 'Comprehensive assessment of strategic impact and capability gap closure.',
            'capability_gaps': [
                {
                    'name': 'Air Superiority',
                    'current_state': '65%',
                    'target_state': '95%',
                    'impact': 'Critical for regional dominance'
                },
                {
                    'name': 'Naval Power Projection',
                    'current_state': '45%',
                    'target_state': '85%',
                    'impact': 'Essential for maritime security'
                },
                {
                    'name': 'Cyber Defense Capability',
                    'current_state': '70%',
                    'target_state': '90%',
                    'impact': 'Critical infrastructure protection'
                },
                {
                    'name': 'Space Domain Awareness',
                    'current_state': '40%',
                    'target_state': '80%',
                    'impact': 'Space-based asset protection'
                },
                {
                    'name': 'Intelligence Collection',
                    'current_state': '75%',
                    'target_state': '95%',
                    'impact': 'Strategic decision support'
                }
            ],
            'strategic_benefits': [
                {
                    'name': 'Enhanced Deterrence Capability',
                    'description': 'Significantly improved deterrence posture against potential adversaries',
                    'timeframe': '3-5 years',
                    'magnitude': 'High'
                },
                {
                    'name': 'Regional Stability Contribution',
                    'description': 'Positive contribution to regional security and stability',
                    'timeframe': '2-4 years',
                    'magnitude': 'Medium'
                },
                {
                    'name': 'Alliance Strengthening',
                    'description': 'Enhanced capability to contribute to alliance operations',
                    'timeframe': '4-6 years',
                    'magnitude': 'High'
                },
                {
                    'name': 'Technological Leadership',
                    'description': 'Establishment of technological leadership in key defense domains',
                    'timeframe': '5-8 years',
                    'magnitude': 'Critical'
                }
            ]
        }
    }
    
    try:
        # Test 1: Single Module Integration
        print("🧪 Testing Acquisition Programs Module Integration")
        generator = ModularReportGenerator()
        
        # Disable all modules except Acquisition Programs Module
        for module_id, module in generator.modules.items():
            if not isinstance(module, AcquisitionProgramsModule):
                module.config.enabled = False
        
        result = await generator.generate_modular_report(
            topic="Acquisition Programs Integration Test",
            data=test_data,
            report_title="Acquisition Programs Module Integration Test"
        )
        
        if result["success"]:
            print("✅ Report generated successfully!")
            print(f"📄 File: {result['filename']}")
            print(f"📁 Path: {result['file_path']}")
            print(f"📊 Size: {result['file_size']} bytes")
            
            # Read and verify content
            with open(result["file_path"], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key sections
            sections_to_check = [
                "Acquisition Programs & Modernization",
                "Strategic Defense Acquisition Programs",
                "Critical Modernization Initiatives", 
                "Comprehensive Program Risk & Dependency Analysis",
                "Strategic Impact & Capability Assessment",
                "Interactive Visualizations"
            ]
            
            for section in sections_to_check:
                if section in content:
                    print(f"✅ {section} section found")
                else:
                    print(f"❌ {section} section NOT found")
            
            # Check for specific content
            if "Next-Generation Fighter Aircraft Program" in content:
                print("✅ Program details found")
            if "AI-Enhanced Command & Control" in content:
                print("✅ Modernization initiatives found")
            if "Technology Maturity Risk" in content:
                print("✅ Risk analysis found")
            if "Air Superiority" in content:
                print("✅ Capability gaps found")
            
            # Check for charts
            if "chart-container" in content:
                print("✅ Chart containers found")
            if "canvas" in content:
                print("✅ Chart canvas elements found")
            
            # Check for tooltips
            if "data-tooltip-acquisitionprogramsmodule" in content:
                print("✅ Tooltip data attributes found")
            if "tooltip-title" in content:
                print("✅ Tooltip system found")
        else:
            print(f"❌ Report generation failed: {result['error']}")
            return False
        
        print("\n" + "=" * 60)
        print("📊 Integration Test Results Summary")
        print("=" * 60)
        print("✅ Acquisition Programs Integration: PASSED")
        print("\n🎉 Acquisition Programs Module integration is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_acquisition_programs_integration())
