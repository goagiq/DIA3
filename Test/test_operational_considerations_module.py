#!/usr/bin/env python3
"""
Test Operational Considerations Module

Unit tests for the Operational Considerations Module to ensure all functionality works correctly.
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.operational_considerations_module import OperationalConsiderationsModule
from core.modules.base_module import ModuleConfig, TooltipData


class TestOperationalConsiderationsModule(unittest.TestCase):
    """Test cases for the Operational Considerations Module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.module = OperationalConsiderationsModule()
        
        # Sample test data
        self.test_data = {
            'operational_overview': {
                'title': 'Strategic Operational Considerations',
                'overview': 'Comprehensive operational planning and readiness assessment for strategic initiatives',
                'operational_factors': [
                    {
                        'name': 'Personnel Readiness',
                        'description': 'Assessment of personnel capabilities and training',
                        'impact': 'High',
                        'priority': 'Critical'
                    },
                    {
                        'name': 'Equipment Availability',
                        'description': 'Evaluation of equipment and resource availability',
                        'impact': 'Medium',
                        'priority': 'High'
                    }
                ],
                'readiness_summary': {
                    'personnel_readiness': '85%',
                    'equipment_readiness': '78%',
                    'training_readiness': '92%',
                    'overall_readiness': '82%'
                },
                'implementation_considerations': [
                    'Ensure adequate personnel training',
                    'Maintain equipment maintenance schedules',
                    'Develop contingency plans'
                ]
            },
            'readiness_analysis': {
                'title': 'Comprehensive Readiness Analysis',
                'overview': 'Detailed analysis of personnel, equipment, and training readiness',
                'personnel_readiness': {
                    'total_personnel': '1,250',
                    'available_personnel': '1,100',
                    'qualified_personnel': '950',
                    'readiness_rate': '85%',
                    'key_gaps': 'Specialized training requirements'
                },
                'equipment_readiness': {
                    'total_equipment': '500 units',
                    'operational_equipment': '390 units',
                    'maintenance_status': 'Good',
                    'readiness_rate': '78%',
                    'critical_shortages': 'Advanced communication systems'
                },
                'training_readiness': {
                    'training_completion': '92%',
                    'certification_status': 'Current',
                    'recent_training': 'Within 6 months',
                    'readiness_rate': '92%',
                    'training_gaps': 'Advanced technical skills'
                }
            },
            'implementation_planning': {
                'title': 'Implementation Planning Framework',
                'overview': 'Comprehensive implementation planning with phases and resource requirements',
                'operational_phases': [
                    {
                        'name': 'Preparation Phase',
                        'duration': '30 days',
                        'description': 'Initial preparation and setup phase',
                        'objectives': [
                            'Establish operational infrastructure',
                            'Train key personnel',
                            'Deploy initial equipment'
                        ],
                        'resources': [
                            'Training facilities',
                            'Initial equipment',
                            'Support personnel'
                        ]
                    },
                    {
                        'name': 'Execution Phase',
                        'duration': '90 days',
                        'description': 'Main operational execution phase',
                        'objectives': [
                            'Execute primary operations',
                            'Monitor performance',
                            'Adjust as needed'
                        ],
                        'resources': [
                            'Full personnel complement',
                            'Operational equipment',
                            'Support systems'
                        ]
                    }
                ],
                'resource_requirements': {
                    'personnel': '1,250 personnel',
                    'equipment': '500 units',
                    'budget': '$50M',
                    'time': '180 days'
                },
                'timeline_considerations': [
                    'Allow for training and preparation time',
                    'Consider seasonal factors',
                    'Account for equipment delivery schedules'
                ]
            },
            'operational_risk_assessment': {
                'title': 'Operational Risk Assessment',
                'overview': 'Comprehensive assessment of operational risks and mitigation strategies',
                'operational_risks': [
                    {
                        'name': 'Personnel Shortage',
                        'level': 'High',
                        'probability': '25%',
                        'impact': 'Significant',
                        'description': 'Risk of insufficient qualified personnel'
                    },
                    {
                        'name': 'Equipment Failure',
                        'level': 'Medium',
                        'probability': '15%',
                        'impact': 'Moderate',
                        'description': 'Risk of critical equipment failure'
                    }
                ],
                'mitigation_strategies': [
                    {
                        'name': 'Enhanced Training Program',
                        'description': 'Comprehensive training program to address skill gaps',
                        'effectiveness': '85%',
                        'cost': '$5M'
                    },
                    {
                        'name': 'Equipment Redundancy',
                        'description': 'Backup equipment and systems for critical functions',
                        'effectiveness': '90%',
                        'cost': '$10M'
                    }
                ],
                'contingency_plans': [
                    {
                        'name': 'Personnel Backup Plan',
                        'description': 'Alternative personnel sources and training programs',
                        'trigger': 'Personnel shortage exceeds 20%',
                        'resources': 'Reserve personnel pool'
                    },
                    {
                        'name': 'Equipment Contingency',
                        'description': 'Alternative equipment sources and repair capabilities',
                        'trigger': 'Critical equipment failure',
                        'resources': 'Backup equipment inventory'
                    }
                ]
            }
        }
    
    def test_module_properties(self):
        """Test basic module properties."""
        self.assertEqual(self.module.module_id, 'operationalconsiderationsmodule')
        self.assertEqual(self.module.get_title(), '⚡ Operational Considerations & Readiness')
        self.assertTrue(self.module.is_enabled())
        self.assertEqual(self.module.get_order(), 60)
        
    def test_required_data_keys(self):
        """Test required data keys."""
        required_keys = self.module.get_required_data_keys()
        expected_keys = [
            'operational_overview',
            'readiness_analysis',
            'implementation_planning',
            'operational_risk_assessment'
        ]
        self.assertEqual(set(required_keys), set(expected_keys))
    
    def test_data_validation_success(self):
        """Test successful data validation."""
        # Should not raise any exception
        self.assertTrue(self.module.validate_data(self.test_data))
    
    def test_data_validation_missing_keys(self):
        """Test data validation with missing keys."""
        incomplete_data = {
            'operational_overview': self.test_data['operational_overview']
            # Missing other required keys
        }
        
        with self.assertRaises(ValueError) as context:
            self.module.validate_data(incomplete_data)
        
        self.assertIn('Missing required data keys', str(context.exception))
    
    def test_content_generation(self):
        """Test HTML content generation."""
        content = self.module.generate_content(self.test_data)
        
        # Check basic structure
        self.assertIn('<div class="section" id="operational-considerations">', content)
        self.assertIn('⚡ Operational Considerations & Readiness', content)
        
        # Check for major sections
        self.assertIn('operational-overview-section', content)
        self.assertIn('readiness-analysis-section', content)
        self.assertIn('implementation-planning-section', content)
        self.assertIn('operational-risk-assessment-section', content)
        self.assertIn('visualizations-section', content)
    
    def test_operational_overview_content(self):
        """Test operational overview section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for overview content
        self.assertIn('Strategic Operational Considerations', content)
        self.assertIn('Personnel Readiness', content)
        self.assertIn('Equipment Availability', content)
        self.assertIn('85%', content)
        self.assertIn('78%', content)
        self.assertIn('Ensure adequate personnel training', content)
    
    def test_readiness_analysis_content(self):
        """Test readiness analysis section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for readiness content
        self.assertIn('Comprehensive Readiness Analysis', content)
        self.assertIn('1,250', content)
        self.assertIn('1,100', content)
        self.assertIn('500 units', content)
        self.assertIn('390 units', content)
        self.assertIn('92%', content)
    
    def test_implementation_planning_content(self):
        """Test implementation planning section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for planning content
        self.assertIn('Implementation Planning Framework', content)
        self.assertIn('Preparation Phase', content)
        self.assertIn('Execution Phase', content)
        self.assertIn('30 days', content)
        self.assertIn('90 days', content)
        self.assertIn('$50M', content)
    
    def test_operational_risk_assessment_content(self):
        """Test operational risk assessment section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for risk content
        self.assertIn('Operational Risk Assessment', content)
        self.assertIn('Personnel Shortage', content)
        self.assertIn('Equipment Failure', content)
        self.assertIn('High', content)
        self.assertIn('Medium', content)
        self.assertIn('25%', content)
        self.assertIn('Enhanced Training Program', content)
    
    def test_tooltip_data_initialization(self):
        """Test tooltip data initialization."""
        # Check that tooltips are properly initialized
        self.assertGreater(len(self.module.tooltip_data), 0)
        
        # Check specific tooltip keys
        expected_tooltip_keys = ['factor_0', 'phase_0', 'risk_0', 'strategy_0']
        for key in expected_tooltip_keys:
            self.assertIn(key, self.module.tooltip_data)
            tooltip = self.module.tooltip_data[key]
            self.assertIsInstance(tooltip, TooltipData)
            self.assertIsNotNone(tooltip.title)
            self.assertIsNotNone(tooltip.description)
            self.assertIsNotNone(tooltip.strategic_impact)
    
    def test_tooltip_attributes_in_content(self):
        """Test that tooltip attributes are present in generated content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for tooltip data attributes
        self.assertIn(f'data-tooltip-{self.module.module_id}="factor_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="phase_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="risk_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="strategy_0"', content)
    
    def test_chart_containers_in_content(self):
        """Test that chart containers are present in generated content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for chart containers
        self.assertIn('chart-container', content)
        self.assertIn('Readiness Assessment', content)
        self.assertIn('Implementation Timeline', content)
        self.assertIn('Operational Risk Matrix', content)
    
    def test_chart_data_generation(self):
        """Test chart data generation."""
        # Generate content to populate chart data
        self.module.generate_content(self.test_data)
        
        # Check that chart data is populated
        self.assertGreater(len(self.module.chart_data), 0)
        
        # Check for specific chart IDs
        expected_charts = [
            f'readinessAssessmentChart_{self.module.module_id}',
            f'implementationTimelineChart_{self.module.module_id}',
            f'operationalRiskMatrixChart_{self.module.module_id}'
        ]
        
        for chart_id in expected_charts:
            self.assertIn(chart_id, self.module.chart_data)
            chart_config = self.module.chart_data[chart_id]
            self.assertIn('type', chart_config)
            self.assertIn('data', chart_config)
            self.assertIn('options', chart_config)
    
    def test_risk_level_color_mapping(self):
        """Test risk level color mapping functionality."""
        # Test various risk level colors
        self.assertEqual(self.module._get_risk_level_color('low'), 'risk-low')
        self.assertEqual(self.module._get_risk_level_color('medium'), 'risk-medium')
        self.assertEqual(self.module._get_risk_level_color('high'), 'risk-high')
        self.assertEqual(self.module._get_risk_level_color('critical'), 'risk-critical')
        self.assertEqual(self.module._get_risk_level_color('unknown'), 'risk-unknown')
    
    def test_empty_data_handling(self):
        """Test handling of empty or minimal data."""
        empty_data = {
            'operational_overview': {},
            'readiness_analysis': {},
            'implementation_planning': {},
            'operational_risk_assessment': {}
        }
        
        # Should not raise exception and should generate content
        content = self.module.generate_content(empty_data)
        self.assertIn('operational-considerations', content)
        self.assertIn('⚡ Operational Considerations & Readiness', content)
    
    def test_module_configuration(self):
        """Test custom module configuration."""
        custom_config = ModuleConfig(
            title="Custom Operational Analysis",
            description="Custom description",
            order=70,
            tooltips_enabled=False,
            charts_enabled=False
        )
        
        custom_module = OperationalConsiderationsModule(custom_config)
        self.assertEqual(custom_module.get_title(), "Custom Operational Analysis")
        self.assertEqual(custom_module.get_description(), "Custom description")
        self.assertEqual(custom_module.get_order(), 70)
        self.assertFalse(custom_module.config.tooltips_enabled)
        self.assertFalse(custom_module.config.charts_enabled)


if __name__ == '__main__':
    print("🧪 Testing Operational Considerations Module")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
