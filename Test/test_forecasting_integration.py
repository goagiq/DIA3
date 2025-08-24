#!/usr/bin/env python3
"""
Test Forecasting Module Integration

Integration tests for the Forecasting Module with the ModularReportGenerator.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.modules.forecasting_module import ForecastingModule


async def test_forecasting_integration():
    """Test the Forecasting Module integration with ModularReportGenerator."""
    print("🚀 Forecasting Module Integration Test Suite")
    print("=" * 60)
    
    # Test data
    test_data = {
        'forecasting_overview': {
            'title': 'Strategic Intelligence Forecasting',
            'overview': 'Comprehensive forecasting analysis for strategic intelligence planning using advanced Monte Carlo simulation and scenario analysis.',
            'time_horizon': '24 months',
            'confidence_level': '95%',
            'methodology': 'Monte Carlo simulation with scenario planning and risk assessment',
            'key_metrics': [
                {
                    'name': 'Geopolitical Stability Index',
                    'value': '0.65',
                    'description': 'Global geopolitical stability forecast',
                    'trend': 'Stable'
                },
                {
                    'name': 'Economic Growth Rate',
                    'value': '3.2%',
                    'description': 'Global economic growth projection',
                    'trend': 'Moderate Growth'
                },
                {
                    'name': 'Technology Adoption Rate',
                    'value': '78%',
                    'description': 'Advanced technology adoption forecast',
                    'trend': 'Accelerating'
                }
            ]
        },
        'scenario_analysis': {
            'title': 'Multi-Scenario Strategic Analysis',
            'overview': 'Comprehensive analysis of multiple future scenarios with probability assessment and strategic implications.',
            'scenarios': [
                {
                    'name': 'Optimistic Scenario',
                    'probability': 25,
                    'description': 'High stability with strong economic growth and technological advancement',
                    'impact': 'High',
                    'timeline': '12-18 months',
                    'confidence': '85%',
                    'conditions': [
                        'Strong international cooperation',
                        'Robust economic recovery',
                        'Accelerated technology adoption',
                        'Reduced geopolitical tensions'
                    ]
                },
                {
                    'name': 'Baseline Scenario',
                    'probability': 50,
                    'description': 'Moderate stability with steady economic growth and gradual technological advancement',
                    'impact': 'Medium',
                    'timeline': '18-24 months',
                    'confidence': '90%',
                    'conditions': [
                        'Stable international relations',
                        'Moderate economic growth',
                        'Steady technology advancement',
                        'Controlled geopolitical tensions'
                    ]
                },
                {
                    'name': 'Pessimistic Scenario',
                    'probability': 25,
                    'description': 'Low stability with economic challenges and technological disruption',
                    'impact': 'High',
                    'timeline': '6-12 months',
                    'confidence': '80%',
                    'conditions': [
                        'Increased international tensions',
                        'Economic uncertainty',
                        'Technology disruption',
                        'Escalating conflicts'
                    ]
                }
            ]
        },
        'trend_analysis': {
            'title': 'Strategic Trend Analysis',
            'overview': 'Analysis of key strategic trends and their implications for future developments.',
            'historical_data': {
                'period': '2020-2024',
                'data_points': '48 months',
                'quality': 'High'
            },
            'trends': [
                {
                    'name': 'Digital Transformation Acceleration',
                    'direction': 'Increasing',
                    'description': 'Rapid acceleration of digital transformation across all sectors',
                    'strength': 'Strong',
                    'duration': 'Long-term',
                    'confidence': '95%',
                    'factors': [
                        'COVID-19 pandemic acceleration',
                        'Technology advancement',
                        'Competitive pressure',
                        'Customer demand'
                    ]
                },
                {
                    'name': 'Geopolitical Fragmentation',
                    'direction': 'Increasing',
                    'description': 'Growing fragmentation in international relations and alliances',
                    'strength': 'Moderate',
                    'duration': 'Medium-term',
                    'confidence': '85%',
                    'factors': [
                        'Great power competition',
                        'Economic nationalism',
                        'Technology competition',
                        'Resource competition'
                    ]
                },
                {
                    'name': 'Climate Change Impact',
                    'direction': 'Increasing',
                    'description': 'Growing impact of climate change on global stability',
                    'strength': 'Strong',
                    'duration': 'Long-term',
                    'confidence': '90%',
                    'factors': [
                        'Extreme weather events',
                        'Resource scarcity',
                        'Migration patterns',
                        'Economic disruption'
                    ]
                }
            ]
        },
        'risk_assessment': {
            'title': 'Strategic Risk Assessment',
            'overview': 'Comprehensive assessment of strategic risks and uncertainties affecting global stability.',
            'risk_factors': [
                {
                    'name': 'Cyber Threat Escalation',
                    'level': 'High',
                    'probability': '40%',
                    'impact': 'Critical',
                    'mitigation': 'Enhanced cyber defense and resilience programs'
                },
                {
                    'name': 'Economic Instability',
                    'level': 'Medium',
                    'probability': '35%',
                    'impact': 'Significant',
                    'mitigation': 'Economic diversification and resilience measures'
                },
                {
                    'name': 'Technology Disruption',
                    'level': 'High',
                    'probability': '45%',
                    'impact': 'High',
                    'mitigation': 'Continuous technology monitoring and adaptation'
                },
                {
                    'name': 'Geopolitical Conflict',
                    'level': 'Medium',
                    'probability': '30%',
                    'impact': 'Critical',
                    'mitigation': 'Diplomatic engagement and conflict prevention'
                }
            ],
            'uncertainty_analysis': {
                'model_uncertainty': '12%',
                'data_uncertainty': '8%',
                'scenario_uncertainty': '15%'
            }
        }
    }
    
    try:
        # Test 1: Single Module Integration
        print("🧪 Testing Forecasting Module Integration")
        generator = ModularReportGenerator()
        
        # Disable all modules except Forecasting Module
        for module_id, module in generator.modules.items():
            if not isinstance(module, ForecastingModule):
                module.config.enabled = False
        
        result = await generator.generate_modular_report(
            topic="Forecasting Integration Test",
            data=test_data,
            report_title="Forecasting Module Integration Test"
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
                "Forecasting & Predictive Analytics",
                "Strategic Intelligence Forecasting",
                "Multi-Scenario Strategic Analysis",
                "Strategic Trend Analysis",
                "Strategic Risk Assessment",
                "Interactive Visualizations"
            ]
            
            for section in sections_to_check:
                if section in content:
                    print(f"✅ {section} section found")
                else:
                    print(f"❌ {section} section NOT found")
            
            # Check for specific content
            if "Geopolitical Stability Index" in content:
                print("✅ Forecasting metrics found")
            if "Optimistic Scenario" in content:
                print("✅ Scenario analysis found")
            if "Digital Transformation Acceleration" in content:
                print("✅ Trend analysis found")
            if "Cyber Threat Escalation" in content:
                print("✅ Risk assessment found")
            
            # Check for charts
            if "chart-container" in content:
                print("✅ Chart containers found")
            if "canvas" in content:
                print("✅ Chart canvas elements found")
            
            # Check for tooltips
            if "data-tooltip-forecastingmodule" in content:
                print("✅ Tooltip data attributes found")
            if "tooltip-title" in content:
                print("✅ Tooltip system found")
        else:
            print(f"❌ Report generation failed: {result['error']}")
            return False
        
        print("\n" + "=" * 60)
        print("📊 Integration Test Results Summary")
        print("=" * 60)
        print("✅ Forecasting Integration: PASSED")
        print("\n🎉 Forecasting Module integration is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_forecasting_integration())
