#!/usr/bin/env python3
"""
Test Acquisition Programs Module

Unit tests for the Acquisition Programs Module to ensure all functionality works correctly.
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.acquisition_programs_module import AcquisitionProgramsModule
from core.modules.base_module import ModuleConfig, TooltipData


class TestAcquisitionProgramsModule(unittest.TestCase):
    """Test cases for the Acquisition Programs Module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.module = AcquisitionProgramsModule()
        
        # Sample test data
        self.test_data = {
            'acquisition_programs': {
                'title': 'Strategic Acquisition Programs',
                'overview': 'Comprehensive acquisition programs for capability enhancement',
                'total_budget': '$2.5 Billion',
                'total_programs': 5,
                'programs': [
                    {
                        'name': 'Next-Gen Fighter Program',
                        'type': 'Air Defense',
                        'budget': '$800M',
                        'timeline': '2024-2028',
                        'status': 'Active',
                        'priority': 'High'
                    },
                    {
                        'name': 'Naval Modernization',
                        'type': 'Naval Systems',
                        'budget': '$600M',
                        'timeline': '2024-2026',
                        'status': 'At Risk',
                        'priority': 'Critical'
                    }
                ]
            },
            'modernization_initiatives': {
                'title': 'Modernization Initiatives',
                'overview': 'Key initiatives for capability modernization',
                'initiatives': [
                    {
                        'name': 'Radar System Upgrade',
                        'category': 'C4ISR',
                        'description': 'Upgrade to next-generation radar systems',
                        'impact': 'High',
                        'timeline': '18 months',
                        'cost': '$150M'
                    },
                    {
                        'name': 'Network-Centric Warfare',
                        'category': 'Information Systems',
                        'description': 'Implementation of network-centric capabilities',
                        'impact': 'Critical',
                        'timeline': '24 months',
                        'cost': '$200M'
                    }
                ]
            },
            'program_analysis': {
                'title': 'Program Risk & Dependency Analysis',
                'overview': 'Analysis of program risks and dependencies',
                'risks': [
                    {
                        'name': 'Technology Risk',
                        'level': 'High',
                        'probability': '30%',
                        'impact': 'Significant',
                        'mitigation': 'Prototype development and testing'
                    },
                    {
                        'name': 'Budget Risk',
                        'level': 'Medium',
                        'probability': '20%',
                        'impact': 'Moderate',
                        'mitigation': 'Regular budget reviews and controls'
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
                        'name': 'Technology Transfer',
                        'type': 'External',
                        'status': 'Pending',
                        'critical': False
                    }
                ]
            },
            'strategic_impact': {
                'title': 'Strategic Impact Assessment',
                'overview': 'Assessment of strategic impact and capability gaps',
                'capability_gaps': [
                    {
                        'name': 'Air Defense Capability',
                        'current_state': '45%',
                        'target_state': '85%',
                        'impact': 'Critical'
                    },
                    {
                        'name': 'Naval Power Projection',
                        'current_state': '35%',
                        'target_state': '75%',
                        'impact': 'High'
                    }
                ],
                'strategic_benefits': [
                    {
                        'name': 'Enhanced Deterrence',
                        'description': 'Improved deterrence capabilities',
                        'timeframe': '2-3 years',
                        'magnitude': 'High'
                    },
                    {
                        'name': 'Regional Stability',
                        'description': 'Contribution to regional stability',
                        'timeframe': '3-5 years',
                        'magnitude': 'Medium'
                    }
                ]
            }
        }
    
    def test_module_properties(self):
        """Test basic module properties."""
        self.assertEqual(self.module.module_id, 'acquisitionprogramsmodule')
        self.assertEqual(self.module.get_title(), '🎯 Acquisition Programs & Modernization')
        self.assertTrue(self.module.is_enabled())
        self.assertEqual(self.module.get_order(), 40)
        
    def test_required_data_keys(self):
        """Test required data keys."""
        required_keys = self.module.get_required_data_keys()
        expected_keys = [
            'acquisition_programs',
            'modernization_initiatives',
            'program_analysis',
            'strategic_impact'
        ]
        self.assertEqual(set(required_keys), set(expected_keys))
    
    def test_data_validation_success(self):
        """Test successful data validation."""
        # Should not raise any exception
        self.assertTrue(self.module.validate_data(self.test_data))
    
    def test_data_validation_missing_keys(self):
        """Test data validation with missing keys."""
        incomplete_data = {
            'acquisition_programs': self.test_data['acquisition_programs']
            # Missing other required keys
        }
        
        with self.assertRaises(ValueError) as context:
            self.module.validate_data(incomplete_data)
        
        self.assertIn('Missing required data keys', str(context.exception))
    
    def test_content_generation(self):
        """Test HTML content generation."""
        content = self.module.generate_content(self.test_data)
        
        # Check basic structure
        self.assertIn('<div class="section" id="acquisition-programs">', content)
        self.assertIn('🎯 Acquisition Programs & Modernization', content)
        
        # Check for major sections
        self.assertIn('programs-overview-section', content)
        self.assertIn('modernization-section', content)
        self.assertIn('program-analysis-section', content)
        self.assertIn('strategic-impact-section', content)
        self.assertIn('visualizations-section', content)
    
    def test_programs_overview_content(self):
        """Test programs overview section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for program overview content
        self.assertIn('Strategic Acquisition Programs', content)
        self.assertIn('$2.5 Billion', content)
        self.assertIn('Next-Gen Fighter Program', content)
        self.assertIn('Naval Modernization', content)
        self.assertIn('Air Defense', content)
        self.assertIn('Naval Systems', content)
    
    def test_modernization_initiatives_content(self):
        """Test modernization initiatives section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for modernization content
        self.assertIn('Modernization Initiatives', content)
        self.assertIn('Radar System Upgrade', content)
        self.assertIn('Network-Centric Warfare', content)
        self.assertIn('C4ISR', content)
        self.assertIn('Information Systems', content)
    
    def test_program_analysis_content(self):
        """Test program analysis section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for analysis content
        self.assertIn('Program Risk & Dependency Analysis', content)
        self.assertIn('Technology Risk', content)
        self.assertIn('Budget Risk', content)
        self.assertIn('Industrial Base Capacity', content)
        self.assertIn('Technology Transfer', content)
    
    def test_strategic_impact_content(self):
        """Test strategic impact section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for strategic impact content
        self.assertIn('Strategic Impact Assessment', content)
        self.assertIn('Air Defense Capability', content)
        self.assertIn('Naval Power Projection', content)
        self.assertIn('Enhanced Deterrence', content)
        self.assertIn('Regional Stability', content)
    
    def test_tooltip_data_initialization(self):
        """Test tooltip data initialization."""
        # Check that tooltips are properly initialized
        self.assertGreater(len(self.module.tooltip_data), 0)
        
        # Check specific tooltip keys
        expected_tooltip_keys = ['program_0', 'initiative_0', 'risk_0', 'gap_0']
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
        self.assertIn(f'data-tooltip-{self.module.module_id}="program_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="initiative_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="risk_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="gap_0"', content)
    
    def test_chart_containers_in_content(self):
        """Test that chart containers are present in generated content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for chart containers
        self.assertIn('chart-container', content)
        self.assertIn('Program Timeline Analysis', content)
        self.assertIn('Budget Allocation by Program', content)
        self.assertIn('Capability Gap Assessment', content)
    
    def test_chart_data_generation(self):
        """Test chart data generation."""
        # Generate content to populate chart data
        self.module.generate_content(self.test_data)
        
        # Check that chart data is populated
        self.assertGreater(len(self.module.chart_data), 0)
        
        # Check for specific chart IDs
        expected_charts = [
            f'programTimelineChart_{self.module.module_id}',
            f'budgetAllocationChart_{self.module.module_id}',
            f'capabilityGapChart_{self.module.module_id}'
        ]
        
        for chart_id in expected_charts:
            self.assertIn(chart_id, self.module.chart_data)
            chart_config = self.module.chart_data[chart_id]
            self.assertIn('type', chart_config)
            self.assertIn('data', chart_config)
            self.assertIn('options', chart_config)
    
    def test_status_color_mapping(self):
        """Test status color mapping functionality."""
        # Test various status colors
        self.assertEqual(self.module._get_status_color('active'), 'status-green')
        self.assertEqual(self.module._get_status_color('completed'), 'status-green')
        self.assertEqual(self.module._get_status_color('at risk'), 'status-yellow')
        self.assertEqual(self.module._get_status_color('delayed'), 'status-yellow')
        self.assertEqual(self.module._get_status_color('critical'), 'status-red')
        self.assertEqual(self.module._get_status_color('cancelled'), 'status-red')
        self.assertEqual(self.module._get_status_color('unknown'), 'status-gray')
    
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
            'acquisition_programs': {},
            'modernization_initiatives': {},
            'program_analysis': {},
            'strategic_impact': {}
        }
        
        # Should not raise exception and should generate content
        content = self.module.generate_content(empty_data)
        self.assertIn('acquisition-programs', content)
        self.assertIn('🎯 Acquisition Programs & Modernization', content)
    
    def test_module_configuration(self):
        """Test custom module configuration."""
        custom_config = ModuleConfig(
            title="Custom Acquisition Analysis",
            description="Custom description",
            order=50,
            tooltips_enabled=False,
            charts_enabled=False
        )
        
        custom_module = AcquisitionProgramsModule(custom_config)
        self.assertEqual(custom_module.get_title(), "Custom Acquisition Analysis")
        self.assertEqual(custom_module.get_description(), "Custom description")
        self.assertEqual(custom_module.get_order(), 50)
        self.assertFalse(custom_module.config.tooltips_enabled)
        self.assertFalse(custom_module.config.charts_enabled)


if __name__ == '__main__':
    print("🧪 Testing Acquisition Programs Module")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
