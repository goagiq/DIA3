#!/usr/bin/env python3
"""
Test Forecasting Module

Unit tests for the Forecasting Module to ensure all functionality works correctly.
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.forecasting_module import ForecastingModule
from core.modules.base_module import ModuleConfig, TooltipData


class TestForecastingModule(unittest.TestCase):
    """Test cases for the Forecasting Module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.module = ForecastingModule()
        
        # Sample test data
        self.test_data = {
            'forecasting_overview': {
                'title': 'Strategic Forecasting Analysis',
                'overview': 'Comprehensive forecasting analysis for strategic planning',
                'time_horizon': '24 months',
                'confidence_level': '95%',
                'methodology': 'Monte Carlo simulation with scenario analysis',
                'key_metrics': [
                    {
                        'name': 'Market Growth Rate',
                        'value': '8.5%',
                        'description': 'Annual market growth projection',
                        'trend': 'Increasing'
                    },
                    {
                        'name': 'Technology Adoption',
                        'value': '65%',
                        'description': 'Technology adoption rate forecast',
                        'trend': 'Accelerating'
                    }
                ]
            },
            'scenario_analysis': {
                'title': 'Future Scenario Analysis',
                'overview': 'Analysis of multiple future scenarios',
                'scenarios': [
                    {
                        'name': 'Optimistic Scenario',
                        'probability': 25,
                        'description': 'High growth with favorable conditions',
                        'impact': 'High',
                        'timeline': '12-18 months',
                        'confidence': '85%',
                        'conditions': [
                            'Strong economic growth',
                            'Favorable regulatory environment',
                            'High technology adoption'
                        ]
                    },
                    {
                        'name': 'Baseline Scenario',
                        'probability': 50,
                        'description': 'Moderate growth with stable conditions',
                        'impact': 'Medium',
                        'timeline': '18-24 months',
                        'confidence': '90%',
                        'conditions': [
                            'Stable economic conditions',
                            'Moderate regulatory changes',
                            'Steady technology adoption'
                        ]
                    }
                ]
            },
            'trend_analysis': {
                'title': 'Trend Analysis',
                'overview': 'Analysis of key trends and patterns',
                'historical_data': {
                    'period': '2020-2024',
                    'data_points': '48 months',
                    'quality': 'High'
                },
                'trends': [
                    {
                        'name': 'Digital Transformation',
                        'direction': 'Increasing',
                        'description': 'Accelerating digital transformation across industries',
                        'strength': 'Strong',
                        'duration': 'Long-term',
                        'confidence': '90%',
                        'factors': [
                            'COVID-19 acceleration',
                            'Technology advancement',
                            'Competitive pressure'
                        ]
                    },
                    {
                        'name': 'Remote Work Adoption',
                        'direction': 'Stable',
                        'description': 'Stabilization of remote work patterns',
                        'strength': 'Moderate',
                        'duration': 'Medium-term',
                        'confidence': '85%',
                        'factors': [
                            'Employee preferences',
                            'Cost savings',
                            'Technology infrastructure'
                        ]
                    }
                ]
            },
            'risk_assessment': {
                'title': 'Risk Assessment',
                'overview': 'Comprehensive risk assessment and uncertainty analysis',
                'risk_factors': [
                    {
                        'name': 'Economic Uncertainty',
                        'level': 'High',
                        'probability': '30%',
                        'impact': 'Significant',
                        'mitigation': 'Diversified investment strategy'
                    },
                    {
                        'name': 'Technology Disruption',
                        'level': 'Medium',
                        'probability': '45%',
                        'impact': 'Moderate',
                        'mitigation': 'Continuous technology monitoring'
                    }
                ],
                'uncertainty_analysis': {
                    'model_uncertainty': '15%',
                    'data_uncertainty': '10%',
                    'scenario_uncertainty': '20%'
                }
            }
        }
    
    def test_module_properties(self):
        """Test basic module properties."""
        self.assertEqual(self.module.module_id, 'forecastingmodule')
        self.assertEqual(self.module.get_title(), '🔮 Forecasting & Predictive Analytics')
        self.assertTrue(self.module.is_enabled())
        self.assertEqual(self.module.get_order(), 50)
        
    def test_required_data_keys(self):
        """Test required data keys."""
        required_keys = self.module.get_required_data_keys()
        expected_keys = [
            'forecasting_overview',
            'scenario_analysis',
            'trend_analysis',
            'risk_assessment'
        ]
        self.assertEqual(set(required_keys), set(expected_keys))
    
    def test_data_validation_success(self):
        """Test successful data validation."""
        # Should not raise any exception
        self.assertTrue(self.module.validate_data(self.test_data))
    
    def test_data_validation_missing_keys(self):
        """Test data validation with missing keys."""
        incomplete_data = {
            'forecasting_overview': self.test_data['forecasting_overview']
            # Missing other required keys
        }
        
        with self.assertRaises(ValueError) as context:
            self.module.validate_data(incomplete_data)
        
        self.assertIn('Missing required data keys', str(context.exception))
    
    def test_content_generation(self):
        """Test HTML content generation."""
        content = self.module.generate_content(self.test_data)
        
        # Check basic structure
        self.assertIn('<div class="section" id="forecasting">', content)
        self.assertIn('🔮 Forecasting & Predictive Analytics', content)
        
        # Check for major sections
        self.assertIn('forecasting-overview-section', content)
        self.assertIn('scenario-section', content)
        self.assertIn('trend-analysis-section', content)
        self.assertIn('risk-assessment-section', content)
        self.assertIn('visualizations-section', content)
    
    def test_forecasting_overview_content(self):
        """Test forecasting overview section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for overview content
        self.assertIn('Strategic Forecasting Analysis', content)
        self.assertIn('24 months', content)
        self.assertIn('95%', content)
        self.assertIn('Monte Carlo simulation', content)
        self.assertIn('Market Growth Rate', content)
        self.assertIn('Technology Adoption', content)
    
    def test_scenario_analysis_content(self):
        """Test scenario analysis section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for scenario content
        self.assertIn('Future Scenario Analysis', content)
        self.assertIn('Optimistic Scenario', content)
        self.assertIn('Baseline Scenario', content)
        self.assertIn('25%', content)
        self.assertIn('50%', content)
        self.assertIn('Strong economic growth', content)
    
    def test_trend_analysis_content(self):
        """Test trend analysis section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for trend content
        self.assertIn('Trend Analysis', content)
        self.assertIn('Digital Transformation', content)
        self.assertIn('Remote Work Adoption', content)
        self.assertIn('Increasing', content)
        self.assertIn('Stable', content)
        self.assertIn('COVID-19 acceleration', content)
    
    def test_risk_assessment_content(self):
        """Test risk assessment section content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for risk content
        self.assertIn('Risk Assessment', content)
        self.assertIn('Economic Uncertainty', content)
        self.assertIn('Technology Disruption', content)
        self.assertIn('High', content)
        self.assertIn('Medium', content)
        self.assertIn('15%', content)
    
    def test_tooltip_data_initialization(self):
        """Test tooltip data initialization."""
        # Check that tooltips are properly initialized
        self.assertGreater(len(self.module.tooltip_data), 0)
        
        # Check specific tooltip keys
        expected_tooltip_keys = ['metric_0', 'scenario_0', 'trend_0', 'risk_0']
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
        self.assertIn(f'data-tooltip-{self.module.module_id}="metric_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="scenario_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="trend_0"', content)
        self.assertIn(f'data-tooltip-{self.module.module_id}="risk_0"', content)
    
    def test_chart_containers_in_content(self):
        """Test that chart containers are present in generated content."""
        content = self.module.generate_content(self.test_data)
        
        # Check for chart containers
        self.assertIn('chart-container', content)
        self.assertIn('Forecast Timeline', content)
        self.assertIn('Scenario Comparison', content)
        self.assertIn('Risk Assessment Matrix', content)
    
    def test_chart_data_generation(self):
        """Test chart data generation."""
        # Generate content to populate chart data
        self.module.generate_content(self.test_data)
        
        # Check that chart data is populated
        self.assertGreater(len(self.module.chart_data), 0)
        
        # Check for specific chart IDs
        expected_charts = [
            f'forecastTimelineChart_{self.module.module_id}',
            f'scenarioComparisonChart_{self.module.module_id}',
            f'riskMatrixChart_{self.module.module_id}'
        ]
        
        for chart_id in expected_charts:
            self.assertIn(chart_id, self.module.chart_data)
            chart_config = self.module.chart_data[chart_id]
            self.assertIn('type', chart_config)
            self.assertIn('data', chart_config)
            self.assertIn('options', chart_config)
    
    def test_probability_color_mapping(self):
        """Test probability color mapping functionality."""
        # Test various probability colors
        self.assertEqual(self.module._get_probability_color(80), 'probability-high')
        self.assertEqual(self.module._get_probability_color(50), 'probability-medium')
        self.assertEqual(self.module._get_probability_color(30), 'probability-low')
    
    def test_trend_direction_mapping(self):
        """Test trend direction mapping functionality."""
        # Test various trend directions
        self.assertEqual(self.module._get_trend_direction('increasing'), 'trend-up')
        self.assertEqual(self.module._get_trend_direction('decreasing'), 'trend-down')
        self.assertEqual(self.module._get_trend_direction('stable'), 'trend-stable')
        self.assertEqual(self.module._get_trend_direction('unknown'), 'trend-stable')
    
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
            'forecasting_overview': {},
            'scenario_analysis': {},
            'trend_analysis': {},
            'risk_assessment': {}
        }
        
        # Should not raise exception and should generate content
        content = self.module.generate_content(empty_data)
        self.assertIn('forecasting', content)
        self.assertIn('🔮 Forecasting & Predictive Analytics', content)
    
    def test_module_configuration(self):
        """Test custom module configuration."""
        custom_config = ModuleConfig(
            title="Custom Forecasting Analysis",
            description="Custom description",
            order=60,
            tooltips_enabled=False,
            charts_enabled=False
        )
        
        custom_module = ForecastingModule(custom_config)
        self.assertEqual(custom_module.get_title(), "Custom Forecasting Analysis")
        self.assertEqual(custom_module.get_description(), "Custom description")
        self.assertEqual(custom_module.get_order(), 60)
        self.assertFalse(custom_module.config.tooltips_enabled)
        self.assertFalse(custom_module.config.charts_enabled)


if __name__ == '__main__':
    print("🧪 Testing Forecasting Module")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
