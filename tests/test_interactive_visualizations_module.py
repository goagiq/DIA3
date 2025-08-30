"""
Test script for Interactive Visualizations Module

Tests the functionality of the Interactive Visualizations Module including:
- Module initialization and configuration
- Content generation with sample data
- Tooltip functionality
- Chart integration
- Data validation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.modules.interactive_visualizations_module import InteractiveVisualizationsModule
from core.modules.base_module import ModuleConfig


def test_module_initialization():
    """Test module initialization and basic configuration."""
    print("🧪 Testing module initialization...")
    
    # Test default initialization
    module = InteractiveVisualizationsModule()
    assert module.module_id == "interactivevisualizationsmodule"
    assert module.get_title() == "📊 Interactive Visualizations"
    assert module.get_description() == "Enhanced data visualization with strategic trends analysis and interactive charts"
    assert module.get_order() == 40
    assert module.is_enabled() == True
    assert module.config.tooltips_enabled == True
    assert module.config.charts_enabled == True
    
    print("✅ Module initialization test passed")
    
    # Test custom configuration
    custom_config = ModuleConfig(
        title="Custom Interactive Visualizations",
        description="Custom interactive visualization analysis",
        order=45,
        tooltips_enabled=False,
        charts_enabled=False
    )
    
    custom_module = InteractiveVisualizationsModule(custom_config)
    assert custom_module.get_title() == "Custom Interactive Visualizations"
    assert custom_module.get_description() == "Custom interactive visualization analysis"
    assert custom_module.get_order() == 45
    assert custom_module.config.tooltips_enabled == False
    assert custom_module.config.charts_enabled == False
    
    print("✅ Custom configuration test passed")


def test_required_data_keys():
    """Test required data keys validation."""
    print("🧪 Testing required data keys...")
    
    module = InteractiveVisualizationsModule()
    required_keys = module.get_required_data_keys()
    
    expected_keys = [
        'visualization_overview',
        'strategic_trends',
        'data_metrics',
        'interactive_charts'
    ]
    
    assert set(required_keys) == set(expected_keys)
    print("✅ Required data keys test passed")


def test_data_validation():
    """Test data validation functionality."""
    print("🧪 Testing data validation...")
    
    module = InteractiveVisualizationsModule()
    
    # Test with missing data
    incomplete_data = {
        'visualization_overview': {},
        'strategic_trends': {}
        # Missing data_metrics and interactive_charts
    }
    
    try:
        module.validate_data(incomplete_data)
        assert False, "Should have raised ValueError for missing data"
    except ValueError as e:
        assert "Missing required data keys" in str(e)
        print("✅ Missing data validation test passed")
    
    # Test with complete data
    complete_data = {
        'visualization_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_visualizations': [],
            'overall_complexity': 'Medium',
            'confidence_score': 85.0
        },
        'strategic_trends': {
            'trend_categories': [
                {
                    'name': 'Technology Trends',
                    'direction': 'Increasing',
                    'strength': 'High',
                    'duration': 'Long-term',
                    'description': 'Technology trend analysis.'
                },
                {
                    'name': 'Economic Trends',
                    'direction': 'Stable',
                    'strength': 'Medium',
                    'duration': 'Medium-term',
                    'description': 'Economic trend analysis.'
                }
            ],
            'trend_indicators': [
                {
                    'name': 'Digital Transformation',
                    'current_value': '75%',
                    'trend': 'High',
                    'significance': 'High',
                    'description': 'Digital transformation indicator.'
                }
            ]
        },
        'data_metrics': {
            'performance_indicators': [
                {
                    'name': 'Data Quality',
                    'value': '90%',
                    'target': '95%',
                    'status': 'On Track',
                    'description': 'Data quality performance indicator.'
                }
            ],
            'statistical_analysis': [
                {
                    'name': 'Trend Analysis',
                    'method': 'Linear Regression',
                    'result': 'Positive Trend',
                    'confidence': '85%',
                    'description': 'Statistical trend analysis.'
                }
            ]
        },
        'interactive_charts': {
            'chart_types': [
                {
                    'name': 'Line Chart',
                    'type': 'Trend Analysis',
                    'interactivity': 'High',
                    'complexity': 'Medium',
                    'description': 'Interactive line chart for trend analysis.'
                }
            ],
            'chart_configurations': [
                {
                    'name': 'Performance Dashboard',
                    'chart_type': 'Bar Chart',
                    'data_source': 'Real-time Data',
                    'update_frequency': 'Daily',
                    'description': 'Performance dashboard configuration.'
                }
            ]
        }
    }
    
    try:
        module.validate_data(complete_data)
        print("✅ Complete data validation test passed")
    except Exception as e:
        assert False, f"Should not have raised exception: {e}"


def test_content_generation():
    """Test HTML content generation."""
    print("🧪 Testing content generation...")
    
    module = InteractiveVisualizationsModule()
    
    # Sample data for testing
    test_data = {
        'visualization_overview': {
            'title': 'Pakistan-India Interactive Visualization Analysis',
            'overview': 'Comprehensive interactive visualization analysis of Pakistan-India strategic data with enhanced chart capabilities.',
            'key_visualizations': [
                {
                    'name': 'Strategic Trends Chart',
                    'type': 'Line Chart',
                    'complexity': 'High',
                    'interactivity': 'High'
                },
                {
                    'name': 'Performance Metrics Dashboard',
                    'type': 'Bar Chart',
                    'complexity': 'Medium',
                    'interactivity': 'High'
                }
            ],
            'overall_complexity': 'High',
            'confidence_score': 88.0
        },
        'strategic_trends': {
            'trend_categories': [
                {
                    'name': 'Military Capability Trends',
                    'direction': 'Increasing',
                    'strength': 'High',
                    'duration': 'Long-term',
                    'description': 'Analysis of military capability trends in the region.'
                },
                {
                    'name': 'Economic Integration Trends',
                    'direction': 'Stable',
                    'strength': 'Medium',
                    'duration': 'Medium-term',
                    'description': 'Analysis of economic integration trends.'
                }
            ],
            'trend_indicators': [
                {
                    'name': 'Naval Capability Index',
                    'current_value': '85%',
                    'trend': 'High',
                    'significance': 'High',
                    'description': 'Naval capability trend indicator.'
                },
                {
                    'name': 'Economic Cooperation Index',
                    'current_value': '60%',
                    'trend': 'Stable',
                    'significance': 'Medium',
                    'description': 'Economic cooperation trend indicator.'
                }
            ]
        },
        'data_metrics': {
            'performance_indicators': [
                {
                    'name': 'Data Accuracy',
                    'value': '92%',
                    'target': '95%',
                    'status': 'On Track',
                    'description': 'Data accuracy performance indicator.'
                },
                {
                    'name': 'Processing Speed',
                    'value': '85%',
                    'target': '90%',
                    'status': 'Improving',
                    'description': 'Data processing speed indicator.'
                }
            ],
            'statistical_analysis': [
                {
                    'name': 'Correlation Analysis',
                    'method': 'Pearson Correlation',
                    'result': 'Strong Positive',
                    'confidence': '88%',
                    'description': 'Statistical correlation analysis.'
                }
            ]
        },
        'interactive_charts': {
            'chart_types': [
                {
                    'name': 'Strategic Trends Line Chart',
                    'type': 'Trend Analysis',
                    'interactivity': 'High',
                    'complexity': 'High',
                    'description': 'Interactive line chart for strategic trends.'
                },
                {
                    'name': 'Performance Metrics Bar Chart',
                    'type': 'Performance Analysis',
                    'interactivity': 'High',
                    'complexity': 'Medium',
                    'description': 'Interactive bar chart for performance metrics.'
                }
            ],
            'chart_configurations': [
                {
                    'name': 'Strategic Dashboard',
                    'chart_type': 'Multi-Chart Dashboard',
                    'data_source': 'Strategic Intelligence Data',
                    'update_frequency': 'Real-time',
                    'description': 'Strategic intelligence dashboard configuration.'
                }
            ]
        }
    }
    
    # Generate content
    html_content = module.generate_content(test_data)
    
    # Verify content structure
    assert '<div class="section" id="interactive-visualizations">' in html_content
    assert '📊 Interactive Visualizations' in html_content
    assert '📈 Strategic Trends Analysis' in html_content
    assert '📊 Data Metrics Analysis' in html_content
    assert '📊 Interactive Charts Analysis' in html_content
    assert '📈 Interactive Visualizations' in html_content
    
    # Verify specific content
    assert 'Pakistan-India Interactive Visualization Analysis' in html_content
    assert 'Strategic Trends Chart' in html_content
    assert 'Performance Metrics Dashboard' in html_content
    assert 'High' in html_content
    
    print("✅ Content generation test passed")
    
    return html_content


def test_tooltip_functionality():
    """Test tooltip initialization and functionality."""
    print("🧪 Testing tooltip functionality...")
    
    module = InteractiveVisualizationsModule()
    
    # Check that tooltips were initialized
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    
    # Check specific tooltips
    assert 'visualization_overview' in tooltip_data
    assert 'strategic_trends' in tooltip_data
    assert 'data_metrics' in tooltip_data
    assert 'interactive_charts' in tooltip_data
    
    # Verify tooltip content
    overview_tooltip = tooltip_data['visualization_overview']
    assert overview_tooltip.title == "Visualization Overview"
    assert "Comprehensive analysis" in overview_tooltip.description
    assert overview_tooltip.confidence == 92.0
    
    print("✅ Tooltip functionality test passed")


def test_chart_integration():
    """Test chart integration functionality."""
    print("🧪 Testing chart integration...")
    
    module = InteractiveVisualizationsModule()
    
    # Test with charts enabled
    assert module.config.charts_enabled == True
    
    # Test chart data generation
    test_data = {
        'visualization_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_visualizations': [],
            'overall_complexity': 'Medium',
            'confidence_score': 85.0
        },
        'strategic_trends': {
            'trend_indicators': [
                {
                    'name': 'Test Trend Indicator',
                    'current_value': '75%',
                    'trend': 'High',
                    'significance': 'High',
                    'description': 'Test description'
                }
            ]
        },
        'data_metrics': {
            'performance_indicators': [
                {
                    'name': 'Test Performance Indicator',
                    'value': '85%',
                    'target': '90%',
                    'status': 'On Track',
                    'description': 'Test description'
                }
            ]
        },
        'interactive_charts': {
            'chart_types': [],
            'chart_configurations': []
        }
    }
    
    # Generate content to trigger chart generation
    html_content = module.generate_content(test_data)
    
    # Verify chart elements are present
    assert 'chart-container' in html_content
    assert 'canvas' in html_content
    assert 'Chart(' in html_content
    
    print("✅ Chart integration test passed")


def test_module_metadata():
    """Test module metadata functionality."""
    print("🧪 Testing module metadata...")
    
    module = InteractiveVisualizationsModule()
    metadata = module.get_module_metadata()
    
    assert metadata['module_id'] == 'interactivevisualizationsmodule'
    assert metadata['title'] == '📊 Interactive Visualizations'
    assert metadata['enabled'] == True
    assert metadata['order'] == 40
    assert 'visualization_overview' in metadata['required_data_keys']
    assert metadata['tooltips_count'] > 0
    
    print("✅ Module metadata test passed")


def test_configuration_export_import():
    """Test configuration export and import functionality."""
    print("🧪 Testing configuration export/import...")
    
    module = InteractiveVisualizationsModule()
    
    # Export configuration
    config = module.export_config()
    
    assert config['enabled'] == True
    assert config['title'] == '📊 Interactive Visualizations'
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    # Import configuration
    new_config = {
        'enabled': False,
        'title': 'Modified Title',
        'description': 'Modified Description',
        'order': 50,
        'tooltips_enabled': False,
        'charts_enabled': False
    }
    
    module.import_config(new_config)
    
    assert module.config.enabled == False
    assert module.config.title == 'Modified Title'
    assert module.config.description == 'Modified Description'
    assert module.config.order == 50
    assert module.config.tooltips_enabled == False
    assert module.config.charts_enabled == False
    
    print("✅ Configuration export/import test passed")


def main():
    """Run all tests for the Interactive Visualizations Module."""
    print("🚀 Starting Interactive Visualizations Module Tests")
    print("=" * 60)
    
    try:
        test_module_initialization()
        test_required_data_keys()
        test_data_validation()
        html_content = test_content_generation()
        test_tooltip_functionality()
        test_chart_integration()
        test_module_metadata()
        test_configuration_export_import()
        
        print("=" * 60)
        print("✅ All Interactive Visualizations Module tests passed!")
        
        # Save generated HTML for inspection
        output_file = Path(__file__).parent.parent / 'Results' / 'test_interactive_visualizations_module.html'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Visualizations Module Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .visualization-card, .category-card, .indicator-card, .analysis-card, .type-card, .config-card {{
            border: 1px solid #eee; padding: 15px; margin: 10px; border-radius: 5px;
        }}
        .chart-container {{ margin: 20px 0; }}
        canvas {{ max-width: 100%; }}
    </style>
</head>
<body>
    <h1>Interactive Visualizations Module Test Results</h1>
    {html_content}
</body>
</html>
            """)
        
        print(f"📄 Test HTML saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
