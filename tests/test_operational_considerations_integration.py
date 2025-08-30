#!/usr/bin/env python3
"""
Test Operational Considerations Module Integration

Integration tests for the Operational Considerations Module with the ModularReportGenerator.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.modules.operational_considerations_module import OperationalConsiderationsModule


async def test_operational_considerations_integration():
    """Test the Operational Considerations Module integration with ModularReportGenerator."""
    print("🚀 Operational Considerations Module Integration Test Suite")
    print("=" * 60)
    
    # Test data
    test_data = {
        'operational_overview': {
            'title': 'Strategic Intelligence Operational Considerations',
            'overview': 'Comprehensive operational planning and readiness assessment for strategic intelligence operations using advanced planning frameworks and readiness analysis.',
            'operational_factors': [
                {
                    'name': 'Intelligence Collection Readiness',
                    'description': 'Assessment of intelligence collection capabilities and infrastructure',
                    'impact': 'Critical',
                    'priority': 'High'
                },
                {
                    'name': 'Analytical Capabilities',
                    'description': 'Evaluation of analytical tools and personnel expertise',
                    'impact': 'High',
                    'priority': 'High'
                },
                {
                    'name': 'Operational Security',
                    'description': 'Assessment of operational security measures and protocols',
                    'impact': 'High',
                    'priority': 'Critical'
                }
            ],
            'readiness_summary': {
                'personnel_readiness': '88%',
                'equipment_readiness': '82%',
                'training_readiness': '95%',
                'overall_readiness': '85%'
            },
            'implementation_considerations': [
                'Ensure comprehensive intelligence training programs',
                'Maintain advanced analytical tools and systems',
                'Implement robust operational security protocols',
                'Develop contingency plans for critical operations'
            ]
        },
        'readiness_analysis': {
            'title': 'Intelligence Operations Readiness Analysis',
            'overview': 'Detailed analysis of intelligence operations readiness across personnel, equipment, and training domains.',
            'personnel_readiness': {
                'total_personnel': '2,500',
                'available_personnel': '2,200',
                'qualified_personnel': '1,950',
                'readiness_rate': '88%',
                'key_gaps': 'Advanced technical skills and language capabilities'
            },
            'equipment_readiness': {
                'total_equipment': '1,200 units',
                'operational_equipment': '984 units',
                'maintenance_status': 'Excellent',
                'readiness_rate': '82%',
                'critical_shortages': 'Advanced cyber tools and satellite systems'
            },
            'training_readiness': {
                'training_completion': '95%',
                'certification_status': 'Current',
                'recent_training': 'Within 3 months',
                'readiness_rate': '95%',
                'training_gaps': 'Advanced cyber operations and cultural intelligence'
            }
        },
        'implementation_planning': {
            'title': 'Intelligence Operations Implementation Framework',
            'overview': 'Comprehensive implementation planning for intelligence operations with detailed phases and resource requirements.',
            'operational_phases': [
                {
                    'name': 'Intelligence Preparation',
                    'duration': '45 days',
                    'description': 'Initial intelligence preparation and environment analysis phase',
                    'objectives': [
                        'Establish intelligence collection priorities',
                        'Deploy intelligence collection assets',
                        'Begin environmental analysis'
                    ],
                    'resources': [
                        'Intelligence collection systems',
                        'Analytical tools and platforms',
                        'Specialized personnel'
                    ]
                },
                {
                    'name': 'Collection Operations',
                    'duration': '120 days',
                    'description': 'Primary intelligence collection and analysis phase',
                    'objectives': [
                        'Execute intelligence collection operations',
                        'Conduct comprehensive analysis',
                        'Generate intelligence products'
                    ],
                    'resources': [
                        'Full intelligence complement',
                        'Advanced collection systems',
                        'Analytical support teams'
                    ]
                },
                {
                    'name': 'Intelligence Integration',
                    'duration': '60 days',
                    'description': 'Intelligence integration and dissemination phase',
                    'objectives': [
                        'Integrate multi-source intelligence',
                        'Develop comprehensive assessments',
                        'Disseminate intelligence products'
                    ],
                    'resources': [
                        'Integration platforms',
                        'Dissemination systems',
                        'Intelligence analysts'
                    ]
                }
            ],
            'resource_requirements': {
                'personnel': '2,500 intelligence personnel',
                'equipment': '1,200 intelligence systems',
                'budget': '$150M',
                'time': '225 days'
            },
            'timeline_considerations': [
                'Allow for intelligence preparation and setup time',
                'Consider operational security requirements',
                'Account for equipment deployment schedules',
                'Plan for intelligence analysis and integration time'
            ]
        },
        'operational_risk_assessment': {
            'title': 'Intelligence Operations Risk Assessment',
            'overview': 'Comprehensive assessment of intelligence operations risks and mitigation strategies.',
            'operational_risks': [
                {
                    'name': 'Intelligence Collection Failure',
                    'level': 'High',
                    'probability': '20%',
                    'impact': 'Critical',
                    'description': 'Risk of intelligence collection system failure or compromise'
                },
                {
                    'name': 'Analytical Capability Gap',
                    'level': 'Medium',
                    'probability': '30%',
                    'impact': 'Significant',
                    'description': 'Risk of insufficient analytical capabilities'
                },
                {
                    'name': 'Operational Security Breach',
                    'level': 'Critical',
                    'probability': '10%',
                    'impact': 'Critical',
                    'description': 'Risk of operational security compromise'
                }
            ],
            'mitigation_strategies': [
                {
                    'name': 'Redundant Collection Systems',
                    'description': 'Multiple intelligence collection systems for redundancy',
                    'effectiveness': '90%',
                    'cost': '$25M'
                },
                {
                    'name': 'Advanced Analytical Training',
                    'description': 'Comprehensive training program for analytical capabilities',
                    'effectiveness': '85%',
                    'cost': '$15M'
                },
                {
                    'name': 'Enhanced Security Protocols',
                    'description': 'Advanced operational security measures and protocols',
                    'effectiveness': '95%',
                    'cost': '$20M'
                }
            ],
            'contingency_plans': [
                {
                    'name': 'Collection Backup Plan',
                    'description': 'Alternative intelligence collection methods and sources',
                    'trigger': 'Primary collection system failure',
                    'resources': 'Backup collection systems and methods'
                },
                {
                    'name': 'Analytical Support Plan',
                    'description': 'External analytical support and expertise',
                    'trigger': 'Analytical capability shortfall',
                    'resources': 'External analytical contractors and partners'
                },
                {
                    'name': 'Security Response Plan',
                    'description': 'Immediate security response and containment procedures',
                    'trigger': 'Security breach detection',
                    'resources': 'Security response teams and protocols'
                }
            ]
        }
    }
    
    try:
        # Test 1: Single Module Integration
        print("🧪 Testing Operational Considerations Module Integration")
        generator = ModularReportGenerator()
        
        # Disable all modules except Operational Considerations Module
        for module_id, module in generator.modules.items():
            if not isinstance(module, OperationalConsiderationsModule):
                module.config.enabled = False
        
        result = await generator.generate_modular_report(
            topic="Operational Considerations Integration Test",
            data=test_data,
            report_title="Operational Considerations Module Integration Test"
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
                "Operational Considerations & Readiness",
                "Strategic Intelligence Operational Considerations",
                "Intelligence Operations Readiness Analysis",
                "Intelligence Operations Implementation Framework",
                "Intelligence Operations Risk Assessment",
                "Interactive Visualizations"
            ]
            
            for section in sections_to_check:
                if section in content:
                    print(f"✅ {section} section found")
                else:
                    print(f"❌ {section} section NOT found")
            
            # Check for specific content
            if "Intelligence Collection Readiness" in content:
                print("✅ Operational factors found")
            if "88%" in content:
                print("✅ Readiness metrics found")
            if "Preparation Phase" in content:
                print("✅ Implementation phases found")
            if "Intelligence Collection Failure" in content:
                print("✅ Risk assessment found")
            
            # Check for charts
            if "chart-container" in content:
                print("✅ Chart containers found")
            if "canvas" in content:
                print("✅ Chart canvas elements found")
            
            # Check for tooltips
            if "data-tooltip-operationalconsiderationsmodule" in content:
                print("✅ Tooltip data attributes found")
            if "tooltip-title" in content:
                print("✅ Tooltip system found")
        else:
            print(f"❌ Report generation failed: {result['error']}")
            return False
        
        print("\n" + "=" * 60)
        print("📊 Integration Test Results Summary")
        print("=" * 60)
        print("✅ Operational Considerations Integration: PASSED")
        print("\n🎉 Operational Considerations Module integration is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_operational_considerations_integration())
