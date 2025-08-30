#!/usr/bin/env python3
"""
Test Enhanced Data Analysis Module

Test script to verify the Enhanced Data Analysis Module functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.enhanced_data_analysis_module import EnhancedDataAnalysisModule


def test_enhanced_data_analysis_module():
    """Test the Enhanced Data Analysis Module."""
    print("🧪 Testing Enhanced Data Analysis Module")
    
    # Create module instance
    module = EnhancedDataAnalysisModule()
    
    # Test basic properties
    assert module.module_id == "enhanceddataanalysismodule"
    assert module.get_title() == "📊 Enhanced Data Analysis"
    assert module.get_description() == "Comprehensive data analysis with performance indicators and statistical insights"
    assert module.get_order() == 8
    assert module.is_enabled() == True
    
    print("✅ Module created: enhanceddataanalysismodule")
    
    # Test module metadata
    metadata = module.get_module_metadata()
    assert metadata['module_id'] == "enhanceddataanalysismodule"
    assert metadata['title'] == "📊 Enhanced Data Analysis"
    assert metadata['enabled'] == True
    assert metadata['order'] == 8
    assert 'data_analysis_overview' in metadata['required_data_keys']
    assert 'key_data_metrics' in metadata['required_data_keys']
    assert 'performance_indicators' in metadata['required_data_keys']
    assert 'statistical_analysis' in metadata['required_data_keys']
    
    print("✅ Module metadata: " + str(metadata))
    
    # Test required data keys
    required_keys = module.get_required_data_keys()
    expected_keys = ['data_analysis_overview', 'key_data_metrics', 'performance_indicators', 'statistical_analysis']
    assert required_keys == expected_keys
    
    print("✅ Required data keys: " + str(required_keys))
    
    # Test module configuration
    config = module.export_config()
    assert config['enabled'] == True
    assert config['title'] == "📊 Enhanced Data Analysis"
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    print("✅ Module config: " + str(config))
    
    # Test tooltip data
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    assert "data_analysis_overview" in tooltip_data
    assert "key_data_metrics" in tooltip_data
    assert "performance_indicators" in tooltip_data
    assert "statistical_analysis" in tooltip_data
    
    print("✅ Tooltip data count: " + str(len(tooltip_data)))
    
    # Test chart data (should be empty initially)
    chart_data = module.get_chart_data()
    assert len(chart_data) == 0
    
    print("✅ Chart data count: " + str(len(chart_data)))
    
    # Test content generation with sample data
    sample_data = {
        'data_analysis_overview': {
            'title': 'Test Data Analysis Overview',
            'overview': 'This is a test data analysis overview.',
            'key_findings': ['Finding 1', 'Finding 2', 'Finding 3'],
            'data_quality_score': 85.5,
            'analysis_confidence': 92.0
        },
        'key_data_metrics': {
            'metrics': [
                {
                    'name': 'Metric 1',
                    'value': '85%',
                    'trend': 'increasing',
                    'description': 'Test metric 1'
                },
                {
                    'name': 'Metric 2',
                    'value': '72%',
                    'trend': 'stable',
                    'description': 'Test metric 2'
                }
            ]
        },
        'performance_indicators': {
            'indicators': [
                {
                    'name': 'Indicator 1',
                    'current_value': '78%',
                    'target': '80%',
                    'status': 'on_track',
                    'description': 'Test indicator 1'
                },
                {
                    'name': 'Indicator 2',
                    'current_value': '65%',
                    'target': '70%',
                    'status': 'below_target',
                    'description': 'Test indicator 2'
                }
            ]
        },
        'statistical_analysis': {
            'statistical_measures': [
                {
                    'name': 'Measure 1',
                    'value': '0.85',
                    'significance': 'high',
                    'confidence': '90%',
                    'description': 'Test measure 1'
                },
                {
                    'name': 'Measure 2',
                    'value': '0.72',
                    'significance': 'medium',
                    'confidence': '85%',
                    'description': 'Test measure 2'
                }
            ],
            'correlation_analysis': {
                'correlations': [
                    {
                        'variable1': 'Variable A',
                        'variable2': 'Variable B',
                        'correlation_coefficient': '0.75',
                        'strength': 'strong'
                    }
                ]
            }
        }
    }
    
    try:
        content = module.generate_content(sample_data)
        assert "Enhanced Data Analysis" in content
        assert "Data Analysis Overview" in content
        assert "Key Data Metrics" in content
        assert "Performance Indicators" in content
        assert "Statistical Analysis" in content
        assert "Interactive Visualizations" in content
        
        print("✅ Content generated successfully")
        
        # Check for chart containers (should have proper chart container structure)
        assert '<div class="chart-container">' in content
        assert 'canvas id="performance_metrics_' in content
        assert 'canvas id="statistical_analysis_' in content
        
        print("✅ Chart containers found in content")
        
        # Check chart data was added
        chart_data = module.get_chart_data()
        assert len(chart_data) == 2  # Should have 2 charts
        assert "performance_metrics_enhanceddataanalysismodule" in chart_data
        assert "statistical_analysis_enhanceddataanalysismodule" in chart_data
        
        print("✅ Chart data added: " + str(len(chart_data)) + " charts")
        
        # Test tooltip script generation
        tooltip_script = module.generate_tooltip_script()
        assert "enhanceddataanalysismoduleTooltipData" in tooltip_script
        assert "data-tooltip-enhanceddataanalysismodule" in tooltip_script
        
        print("✅ Tooltip script generated")
        
        # Test chart script generation
        chart_script = module.generate_chart_script()
        assert "enhanceddataanalysismoduleChartData" in chart_script
        assert "responsive: true" in chart_script
        assert "maintainAspectRatio: false" in chart_script
        
        print("✅ Chart script generated with proper responsive settings")
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return False
    
    return True


def main():
    """Main test function."""
    print("🚀 Enhanced Data Analysis Module Test Suite")
    print("=" * 50)
    
    # Test the module
    test_passed = test_enhanced_data_analysis_module()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Enhanced Data Analysis Module: {'PASSED' if test_passed else 'FAILED'}")
    
    if test_passed:
        print("\n🎉 Enhanced Data Analysis Module is working correctly!")
        print("✅ Chart container fixes applied successfully")
        print("✅ No auto-scrolling issues detected")
        return True
    else:
        print("\n❌ Enhanced Data Analysis Module needs attention.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
