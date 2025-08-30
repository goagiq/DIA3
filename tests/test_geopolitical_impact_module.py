"""
Test script for Geopolitical Impact Module

Tests the functionality of the Geopolitical Impact Module including:
- Module initialization and configuration
- Content generation with sample data
- Tooltip functionality
- Chart integration
- Data validation
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.modules.geopolitical_impact_module import GeopoliticalImpactModule
from core.modules.base_module import ModuleConfig, TooltipData


def test_module_initialization():
    """Test module initialization and basic configuration."""
    print("🧪 Testing module initialization...")
    
    # Test default initialization
    module = GeopoliticalImpactModule()
    assert module.module_id == "geopoliticalimpactmodule"
    assert module.get_title() == "🌍 Geopolitical Impact Analysis"
    assert module.get_description() == "Comprehensive analysis of regional power dynamics and strategic partnerships"
    assert module.get_order() == 20
    assert module.is_enabled() == True
    assert module.config.tooltips_enabled == True
    assert module.config.charts_enabled == True
    
    print("✅ Module initialization test passed")
    
    # Test custom configuration
    custom_config = ModuleConfig(
        title="Custom Geopolitical Analysis",
        description="Custom geopolitical impact analysis",
        order=15,
        tooltips_enabled=False,
        charts_enabled=False
    )
    
    custom_module = GeopoliticalImpactModule(custom_config)
    assert custom_module.get_title() == "Custom Geopolitical Analysis"
    assert custom_module.get_description() == "Custom geopolitical impact analysis"
    assert custom_module.get_order() == 15
    assert custom_module.config.tooltips_enabled == False
    assert custom_module.config.charts_enabled == False
    
    print("✅ Custom configuration test passed")


def test_required_data_keys():
    """Test required data keys validation."""
    print("🧪 Testing required data keys...")
    
    module = GeopoliticalImpactModule()
    required_keys = module.get_required_data_keys()
    
    expected_keys = [
        'geopolitical_analysis',
        'regional_dynamics',
        'strategic_partnerships',
        'power_balance'
    ]
    
    assert set(required_keys) == set(expected_keys)
    print("✅ Required data keys test passed")


def test_data_validation():
    """Test data validation functionality."""
    print("🧪 Testing data validation...")
    
    module = GeopoliticalImpactModule()
    
    # Test with missing data
    incomplete_data = {
        'geopolitical_analysis': {},
        'regional_dynamics': {}
        # Missing strategic_partnerships and power_balance
    }
    
    try:
        module.validate_data(incomplete_data)
        assert False, "Should have raised ValueError for missing data"
    except ValueError as e:
        assert "Missing required data keys" in str(e)
        print("✅ Missing data validation test passed")
    
    # Test with complete data
    complete_data = {
        'geopolitical_analysis': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_actors': [],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'regional_dynamics': {
            'regions': [],
            'power_shifts': [],
            'conflict_areas': []
        },
        'strategic_partnerships': [],
        'power_balance': {
            'major_powers': [],
            'power_indicators': {},
            'balance_assessment': 'Test assessment'
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
    
    module = GeopoliticalImpactModule()
    
    # Sample data for testing
    test_data = {
        'geopolitical_analysis': {
            'title': 'Pakistan Submarine Acquisition Impact',
            'overview': 'Analysis of Pakistan\'s submarine acquisition and its geopolitical implications.',
            'key_actors': [
                {
                    'name': 'Pakistan',
                    'role': 'Primary Actor',
                    'influence_level': 'High'
                },
                {
                    'name': 'China',
                    'role': 'Technology Provider',
                    'influence_level': 'Very High'
                },
                {
                    'name': 'India',
                    'role': 'Regional Competitor',
                    'influence_level': 'High'
                }
            ],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'regional_dynamics': {
            'regions': [
                {
                    'name': 'South Asia',
                    'power_level': 'High',
                    'stability': 'Medium',
                    'strategic_value': 'Very High',
                    'description': 'Key region for maritime security and trade routes.'
                },
                {
                    'name': 'Indian Ocean',
                    'power_level': 'Medium',
                    'stability': 'High',
                    'strategic_value': 'Very High',
                    'description': 'Critical maritime trade route and strategic waterway.'
                }
            ],
            'power_shifts': [
                {
                    'actor': 'Pakistan',
                    'description': 'Enhanced naval capabilities through submarine acquisition',
                    'magnitude': 'High'
                },
                {
                    'actor': 'China',
                    'description': 'Increased influence in South Asian maritime security',
                    'magnitude': 'Medium'
                }
            ],
            'conflict_areas': [
                {
                    'name': 'Kashmir Dispute',
                    'intensity': 'High',
                    'description': 'Ongoing territorial dispute between India and Pakistan.'
                }
            ]
        },
        'strategic_partnerships': [
            {
                'name': 'Pakistan-China Naval Cooperation',
                'type': 'Military',
                'partners': 'Pakistan & China',
                'strength': 'High',
                'objectives': 'Enhanced naval capabilities and regional security',
                'impact': 'High',
                'description': 'Strategic partnership for naval technology transfer and joint operations.'
            },
            {
                'name': 'US-India Strategic Partnership',
                'type': 'Strategic',
                'partners': 'United States & India',
                'strength': 'Very High',
                'objectives': 'Counterbalance Chinese influence in the region',
                'impact': 'Very High',
                'description': 'Comprehensive strategic partnership including defense cooperation.'
            }
        ],
        'power_balance': {
            'major_powers': [
                {
                    'name': 'China',
                    'military_strength': 'Very High',
                    'economic_strength': 'Very High',
                    'political_influence': 'High',
                    'strategic_position': 'Very High',
                    'description': 'Rising global power with significant regional influence.'
                },
                {
                    'name': 'India',
                    'military_strength': 'High',
                    'economic_strength': 'High',
                    'political_influence': 'Medium',
                    'strategic_position': 'High',
                    'description': 'Regional power with growing global influence.'
                },
                {
                    'name': 'Pakistan',
                    'military_strength': 'Medium',
                    'economic_strength': 'Low',
                    'political_influence': 'Medium',
                    'strategic_position': 'Medium',
                    'description': 'Regional actor with strategic nuclear capabilities.'
                }
            ],
            'power_indicators': {
                'naval_capability_ratio': '1:2:3 (Pakistan:India:China)',
                'economic_influence': 'High concentration in China',
                'strategic_alliances': 'Multiple competing partnerships',
                'regional_stability': 'Medium with high volatility'
            },
            'balance_assessment': 'The regional power balance is shifting with China\'s increasing influence, India\'s growing capabilities, and Pakistan\'s strategic partnerships creating a complex triangular dynamic.'
        }
    }
    
    # Generate content
    html_content = module.generate_content(test_data)
    
    # Verify content structure
    assert '<div class="section" id="geopolitical-impact">' in html_content
    assert '🌍 Geopolitical Impact Analysis' in html_content
    assert '🗺️ Regional Dynamics Analysis' in html_content
    assert '🤝 Strategic Partnerships' in html_content
    assert '⚖️ Power Balance Analysis' in html_content
    assert '📈 Interactive Visualizations' in html_content
    
    # Verify specific content
    assert 'Pakistan Submarine Acquisition Impact' in html_content
    assert 'China' in html_content
    assert 'India' in html_content
    assert 'Pakistan' in html_content
    
    print("✅ Content generation test passed")
    
    return html_content


def test_tooltip_functionality():
    """Test tooltip initialization and functionality."""
    print("🧪 Testing tooltip functionality...")
    
    module = GeopoliticalImpactModule()
    
    # Check that tooltips were initialized
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    
    # Check specific tooltips
    assert 'geopolitical_overview' in tooltip_data
    assert 'intelligence_summary' in tooltip_data
    assert 'confidence_metrics' in tooltip_data
    assert 'high_impact_insights' in tooltip_data
    
    # Verify tooltip content
    overview_tooltip = tooltip_data['geopolitical_overview']
    assert overview_tooltip.title == "Geopolitical Overview"
    assert "Comprehensive analysis" in overview_tooltip.description
    assert overview_tooltip.confidence == 90.0
    
    print("✅ Tooltip functionality test passed")


def test_chart_integration():
    """Test chart integration functionality."""
    print("🧪 Testing chart integration...")
    
    module = GeopoliticalImpactModule()
    
    # Test with charts enabled
    assert module.config.charts_enabled == True
    
    # Test chart data generation
    test_data = {
        'geopolitical_analysis': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_actors': [],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'regional_dynamics': {
            'regions': [],
            'power_shifts': [],
            'conflict_areas': []
        },
        'strategic_partnerships': [
            {
                'name': 'Pakistan-China Partnership',
                'type': 'Military',
                'partners': 'Pakistan & China',
                'strength': 'High'
            }
        ],
        'power_balance': {
            'major_powers': [
                {
                    'name': 'China',
                    'military_strength': 'Very High',
                    'economic_strength': 'Very High',
                    'political_influence': 'High',
                    'strategic_position': 'Very High',
                    'technological_capability': 'High'
                },
                {
                    'name': 'India',
                    'military_strength': 'High',
                    'economic_strength': 'High',
                    'political_influence': 'Medium',
                    'strategic_position': 'High',
                    'technological_capability': 'Medium'
                }
            ],
            'power_indicators': {},
            'balance_assessment': 'Test assessment'
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
    
    module = GeopoliticalImpactModule()
    metadata = module.get_module_metadata()
    
    assert metadata['module_id'] == 'geopoliticalimpactmodule'
    assert metadata['title'] == '🌍 Geopolitical Impact Analysis'
    assert metadata['enabled'] == True
    assert metadata['order'] == 20
    assert 'geopolitical_analysis' in metadata['required_data_keys']
    assert metadata['tooltips_count'] > 0
    
    print("✅ Module metadata test passed")


def test_configuration_export_import():
    """Test configuration export and import functionality."""
    print("🧪 Testing configuration export/import...")
    
    module = GeopoliticalImpactModule()
    
    # Export configuration
    config = module.export_config()
    
    assert config['enabled'] == True
    assert config['title'] == '🌍 Geopolitical Impact Analysis'
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    # Import configuration
    new_config = {
        'enabled': False,
        'title': 'Modified Title',
        'description': 'Modified Description',
        'order': 25,
        'tooltips_enabled': False,
        'charts_enabled': False
    }
    
    module.import_config(new_config)
    
    assert module.config.enabled == False
    assert module.config.title == 'Modified Title'
    assert module.config.description == 'Modified Description'
    assert module.config.order == 25
    assert module.config.tooltips_enabled == False
    assert module.config.charts_enabled == False
    
    print("✅ Configuration export/import test passed")


def main():
    """Run all tests for the Geopolitical Impact Module."""
    print("🚀 Starting Geopolitical Impact Module Tests")
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
        print("✅ All Geopolitical Impact Module tests passed!")
        
        # Save generated HTML for inspection
        output_file = Path(__file__).parent.parent / 'Results' / 'test_geopolitical_impact_module.html'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geopolitical Impact Module Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric-card, .actor-card, .region-card, .partnership-card, .power-card, .conflict-card {{
            border: 1px solid #eee; padding: 15px; margin: 10px; border-radius: 5px;
        }}
        .chart-container {{ margin: 20px 0; }}
        canvas {{ max-width: 100%; }}
    </style>
</head>
<body>
    <h1>Geopolitical Impact Module Test Results</h1>
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
