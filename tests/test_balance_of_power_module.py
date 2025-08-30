"""
Test script for Balance of Power Module

Tests the functionality of the Balance of Power Module including:
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

from core.modules.balance_of_power_module import BalanceOfPowerModule
from core.modules.base_module import ModuleConfig


def test_module_initialization():
    """Test module initialization and basic configuration."""
    print("🧪 Testing module initialization...")
    
    # Test default initialization
    module = BalanceOfPowerModule()
    assert module.module_id == "balanceofpowermodule"
    assert module.get_title() == "⚖️ Balance of Power Analysis"
    assert module.get_description() == "Comprehensive analysis of military capabilities, strategic deterrence, and power balance"
    assert module.get_order() == 30
    assert module.is_enabled() == True
    assert module.config.tooltips_enabled == True
    assert module.config.charts_enabled == True
    
    print("✅ Module initialization test passed")
    
    # Test custom configuration
    custom_config = ModuleConfig(
        title="Custom Balance Analysis",
        description="Custom balance of power analysis",
        order=35,
        tooltips_enabled=False,
        charts_enabled=False
    )
    
    custom_module = BalanceOfPowerModule(custom_config)
    assert custom_module.get_title() == "Custom Balance Analysis"
    assert custom_module.get_description() == "Custom balance of power analysis"
    assert custom_module.get_order() == 35
    assert custom_module.config.tooltips_enabled == False
    assert custom_module.config.charts_enabled == False
    
    print("✅ Custom configuration test passed")


def test_required_data_keys():
    """Test required data keys validation."""
    print("🧪 Testing required data keys...")
    
    module = BalanceOfPowerModule()
    required_keys = module.get_required_data_keys()
    
    expected_keys = [
        'balance_overview',
        'naval_capabilities',
        'strategic_deterrence',
        'power_comparison'
    ]
    
    assert set(required_keys) == set(expected_keys)
    print("✅ Required data keys test passed")


def test_data_validation():
    """Test data validation functionality."""
    print("🧪 Testing data validation...")
    
    module = BalanceOfPowerModule()
    
    # Test with missing data
    incomplete_data = {
        'balance_overview': {},
        'naval_capabilities': {}
        # Missing strategic_deterrence and power_comparison
    }
    
    try:
        module.validate_data(incomplete_data)
        assert False, "Should have raised ValueError for missing data"
    except ValueError as e:
        assert "Missing required data keys" in str(e)
        print("✅ Missing data validation test passed")
    
    # Test with complete data
    complete_data = {
        'balance_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_actors': [],
            'balance_assessment': 'Medium',
            'confidence_score': 85.0
        },
        'naval_capabilities': {
            'surface_combatants': [
                {
                    'name': 'Pakistan Navy Destroyers',
                    'quantity': '4 vessels',
                    'quality': 'Medium',
                    'readiness': 'High',
                    'description': 'Modern destroyers with anti-ship and anti-air capabilities.'
                },
                {
                    'name': 'Indian Navy Destroyers',
                    'quantity': '11 vessels',
                    'quality': 'High',
                    'readiness': 'High',
                    'description': 'Advanced destroyers with comprehensive capabilities.'
                }
            ],
            'submarines': [
                {
                    'name': 'Pakistan Submarines',
                    'quantity': '8 submarines',
                    'type': 'Diesel-Electric',
                    'capability': 'Medium',
                    'description': 'Mix of modern and legacy submarines.'
                },
                {
                    'name': 'Indian Submarines',
                    'quantity': '15 submarines',
                    'type': 'Mixed Fleet',
                    'capability': 'High',
                    'description': 'Advanced nuclear and conventional submarines.'
                }
            ],
            'naval_aviation': [
                {
                    'name': 'Pakistan Naval Aviation',
                    'quantity': '25 aircraft',
                    'role': 'Maritime Patrol',
                    'effectiveness': 'Medium',
                    'description': 'Limited naval aviation capabilities.'
                },
                {
                    'name': 'Indian Naval Aviation',
                    'quantity': '200+ aircraft',
                    'role': 'Multi-Role',
                    'effectiveness': 'High',
                    'description': 'Comprehensive naval aviation with carrier-based aircraft.'
                }
            ],
            'amphibious_forces': [
                {
                    'name': 'Pakistan Amphibious Forces',
                    'quantity': 'Limited',
                    'capability': 'Low',
                    'readiness': 'Medium',
                    'description': 'Limited amphibious warfare capabilities.'
                },
                {
                    'name': 'Indian Amphibious Forces',
                    'quantity': 'Significant',
                    'capability': 'High',
                    'readiness': 'High',
                    'description': 'Well-developed amphibious warfare capabilities.'
                }
            ]
        },
        'strategic_deterrence': {
            'nuclear_capabilities': [
                {
                    'name': 'Pakistan Nuclear Arsenal',
                    'quantity': '150-160 warheads',
                    'reliability': 'High',
                    'survivability': 'Medium',
                    'description': 'Land-based and sea-based nuclear capabilities.'
                },
                {
                    'name': 'India Nuclear Arsenal',
                    'quantity': '150-200 warheads',
                    'reliability': 'High',
                    'survivability': 'High',
                    'description': 'Triad of nuclear delivery systems.'
                }
            ],
            'conventional_deterrence': {
                'military_balance': 'India has significant conventional advantage',
                'geographic_position': 'India has geographic advantages',
                'alliance_support': 'Both have limited external support',
                'economic_capacity': 'India has greater economic capacity'
            },
            'deterrence_index': 75.0
        },
        'power_comparison': {
            'military_balance': {
                'Pakistan': {
                    'naval_strength': 'Medium (65%)',
                    'air_power': 'Medium (60%)',
                    'ground_forces': 'Medium (70%)',
                    'nuclear_capability': 'High (85%)'
                },
                'India': {
                    'naval_strength': 'High (90%)',
                    'air_power': 'High (85%)',
                    'ground_forces': 'High (80%)',
                    'nuclear_capability': 'High (90%)'
                }
            },
            'economic_balance': {
                'Pakistan': {
                    'gdp': 'Low (25%)',
                    'defense_budget': 'Medium (40%)',
                    'industrial_capacity': 'Low (30%)',
                    'technological_development': 'Medium (50%)'
                },
                'India': {
                    'gdp': 'High (75%)',
                    'defense_budget': 'High (80%)',
                    'industrial_capacity': 'High (70%)',
                    'technological_development': 'High (75%)'
                }
            },
            'technological_balance': {
                'Pakistan': {
                    'military_technology': 'Medium (55%)',
                    'cyber_capabilities': 'Medium (50%)',
                    'space_capabilities': 'Low (30%)',
                    'research_development': 'Medium (45%)'
                },
                'India': {
                    'military_technology': 'High (80%)',
                    'cyber_capabilities': 'High (75%)',
                    'space_capabilities': 'High (85%)',
                    'research_development': 'High (80%)'
                }
            },
            'overall_assessment': 'India maintains a significant advantage in most areas of military, economic, and technological power, creating an unbalanced regional dynamic that influences strategic calculations and deterrence postures.'
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
    
    module = BalanceOfPowerModule()
    
    # Sample data for testing
    test_data = {
        'balance_overview': {
            'title': 'Pakistan-India Naval Balance Analysis',
            'overview': 'Comprehensive analysis of the naval balance between Pakistan and India in the Indian Ocean region.',
            'key_actors': [
                {
                    'name': 'Pakistan',
                    'role': 'Regional Naval Power',
                    'power_level': 'Medium'
                },
                {
                    'name': 'India',
                    'role': 'Dominant Naval Power',
                    'power_level': 'High'
                }
            ],
            'balance_assessment': 'Unbalanced',
            'confidence_score': 85.0
        },
        'naval_capabilities': {
            'surface_combatants': [
                {
                    'name': 'Pakistan Navy Destroyers',
                    'quantity': '4 vessels',
                    'quality': 'Medium',
                    'readiness': 'High',
                    'description': 'Modern destroyers with anti-ship and anti-air capabilities.'
                },
                {
                    'name': 'Indian Navy Destroyers',
                    'quantity': '11 vessels',
                    'quality': 'High',
                    'readiness': 'High',
                    'description': 'Advanced destroyers with comprehensive capabilities.'
                }
            ],
            'submarines': [
                {
                    'name': 'Pakistan Submarines',
                    'quantity': '8 submarines',
                    'type': 'Diesel-Electric',
                    'capability': 'Medium',
                    'description': 'Mix of modern and legacy submarines.'
                },
                {
                    'name': 'Indian Submarines',
                    'quantity': '15 submarines',
                    'type': 'Mixed Fleet',
                    'capability': 'High',
                    'description': 'Advanced nuclear and conventional submarines.'
                }
            ],
            'naval_aviation': [
                {
                    'name': 'Pakistan Naval Aviation',
                    'quantity': '25 aircraft',
                    'role': 'Maritime Patrol',
                    'effectiveness': 'Medium',
                    'description': 'Limited naval aviation capabilities.'
                },
                {
                    'name': 'Indian Naval Aviation',
                    'quantity': '200+ aircraft',
                    'role': 'Multi-Role',
                    'effectiveness': 'High',
                    'description': 'Comprehensive naval aviation with carrier-based aircraft.'
                }
            ],
            'amphibious_forces': [
                {
                    'name': 'Pakistan Amphibious Forces',
                    'quantity': 'Limited',
                    'capability': 'Low',
                    'readiness': 'Medium',
                    'description': 'Limited amphibious warfare capabilities.'
                },
                {
                    'name': 'Indian Amphibious Forces',
                    'quantity': 'Significant',
                    'capability': 'High',
                    'readiness': 'High',
                    'description': 'Well-developed amphibious warfare capabilities.'
                }
            ]
        },
        'strategic_deterrence': {
            'nuclear_capabilities': [
                {
                    'name': 'Pakistan Nuclear Arsenal',
                    'quantity': '150-160 warheads',
                    'reliability': 'High',
                    'survivability': 'Medium',
                    'description': 'Land-based and sea-based nuclear capabilities.'
                },
                {
                    'name': 'India Nuclear Arsenal',
                    'quantity': '150-200 warheads',
                    'reliability': 'High',
                    'survivability': 'High',
                    'description': 'Triad of nuclear delivery systems.'
                }
            ],
            'conventional_deterrence': {
                'military_balance': 'India has significant conventional advantage',
                'geographic_position': 'India has geographic advantages',
                'alliance_support': 'Both have limited external support',
                'economic_capacity': 'India has greater economic capacity'
            },
            'deterrence_index': 75.0
        },
        'power_comparison': {
            'military_balance': {
                'Pakistan': {
                    'naval_strength': 'Medium (65%)',
                    'air_power': 'Medium (60%)',
                    'ground_forces': 'Medium (70%)',
                    'nuclear_capability': 'High (85%)'
                },
                'India': {
                    'naval_strength': 'High (90%)',
                    'air_power': 'High (85%)',
                    'ground_forces': 'High (80%)',
                    'nuclear_capability': 'High (90%)'
                }
            },
            'economic_balance': {
                'Pakistan': {
                    'gdp': 'Low (25%)',
                    'defense_budget': 'Medium (40%)',
                    'industrial_capacity': 'Low (30%)',
                    'technological_development': 'Medium (50%)'
                },
                'India': {
                    'gdp': 'High (75%)',
                    'defense_budget': 'High (80%)',
                    'industrial_capacity': 'High (70%)',
                    'technological_development': 'High (75%)'
                }
            },
            'technological_balance': {
                'Pakistan': {
                    'military_technology': 'Medium (55%)',
                    'cyber_capabilities': 'Medium (50%)',
                    'space_capabilities': 'Low (30%)',
                    'research_development': 'Medium (45%)'
                },
                'India': {
                    'military_technology': 'High (80%)',
                    'cyber_capabilities': 'High (75%)',
                    'space_capabilities': 'High (85%)',
                    'research_development': 'High (80%)'
                }
            },
            'overall_assessment': 'India maintains a significant advantage in most areas of military, economic, and technological power, creating an unbalanced regional dynamic that influences strategic calculations and deterrence postures.'
        }
    }
    
    # Generate content
    html_content = module.generate_content(test_data)
    
    # Verify content structure
    assert '<div class="section" id="balance-of-power">' in html_content
    assert '⚖️ Balance of Power Analysis' in html_content
    assert '🚢 Naval Capabilities Comparison' in html_content
    assert '🛡️ Strategic Deterrence Analysis' in html_content
    assert '📊 Power Comparison Analysis' in html_content
    assert '📈 Interactive Visualizations' in html_content
    
    # Verify specific content
    assert 'Pakistan-India Naval Balance Analysis' in html_content
    assert 'Pakistan' in html_content
    assert 'India' in html_content
    assert 'Unbalanced' in html_content
    
    print("✅ Content generation test passed")
    
    return html_content


def test_tooltip_functionality():
    """Test tooltip initialization and functionality."""
    print("🧪 Testing tooltip functionality...")
    
    module = BalanceOfPowerModule()
    
    # Check that tooltips were initialized
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    
    # Check specific tooltips
    assert 'balance_overview' in tooltip_data
    assert 'naval_capabilities' in tooltip_data
    assert 'strategic_deterrence' in tooltip_data
    assert 'power_comparison' in tooltip_data
    
    # Verify tooltip content
    overview_tooltip = tooltip_data['balance_overview']
    assert overview_tooltip.title == "Balance Overview"
    assert "Comprehensive analysis" in overview_tooltip.description
    assert overview_tooltip.confidence == 92.0
    
    print("✅ Tooltip functionality test passed")


def test_chart_integration():
    """Test chart integration functionality."""
    print("🧪 Testing chart integration...")
    
    module = BalanceOfPowerModule()
    
    # Test with charts enabled
    assert module.config.charts_enabled == True
    
    # Test chart data generation
    test_data = {
        'balance_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_actors': [],
            'balance_assessment': 'Medium',
            'confidence_score': 85.0
        },
        'naval_capabilities': {
            'surface_combatants': [
                {
                    'name': 'Test Combatant',
                    'quantity': '5 vessels',
                    'quality': 'High',
                    'readiness': 'High',
                    'description': 'Test description'
                }
            ],
            'submarines': [
                {
                    'name': 'Test Submarine',
                    'quantity': '3 submarines',
                    'type': 'Nuclear',
                    'capability': 'Very High',
                    'description': 'Test description'
                }
            ],
            'naval_aviation': [],
            'amphibious_forces': []
        },
        'strategic_deterrence': {
            'nuclear_capabilities': [],
            'conventional_deterrence': {},
            'deterrence_index': 75.0
        },
        'power_comparison': {
            'military_balance': {
                'Country A': {
                    'naval_strength': 'High (85%)',
                    'air_power': 'Medium (65%)'
                },
                'Country B': {
                    'naval_strength': 'Medium (70%)',
                    'air_power': 'High (80%)'
                }
            },
            'economic_balance': {},
            'technological_balance': {},
            'overall_assessment': 'Test assessment'
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
    
    module = BalanceOfPowerModule()
    metadata = module.get_module_metadata()
    
    assert metadata['module_id'] == 'balanceofpowermodule'
    assert metadata['title'] == '⚖️ Balance of Power Analysis'
    assert metadata['enabled'] == True
    assert metadata['order'] == 30
    assert 'balance_overview' in metadata['required_data_keys']
    assert metadata['tooltips_count'] > 0
    
    print("✅ Module metadata test passed")


def test_configuration_export_import():
    """Test configuration export and import functionality."""
    print("🧪 Testing configuration export/import...")
    
    module = BalanceOfPowerModule()
    
    # Export configuration
    config = module.export_config()
    
    assert config['enabled'] == True
    assert config['title'] == '⚖️ Balance of Power Analysis'
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    # Import configuration
    new_config = {
        'enabled': False,
        'title': 'Modified Title',
        'description': 'Modified Description',
        'order': 40,
        'tooltips_enabled': False,
        'charts_enabled': False
    }
    
    module.import_config(new_config)
    
    assert module.config.enabled == False
    assert module.config.title == 'Modified Title'
    assert module.config.description == 'Modified Description'
    assert module.config.order == 40
    assert module.config.tooltips_enabled == False
    assert module.config.charts_enabled == False
    
    print("✅ Configuration export/import test passed")


def main():
    """Run all tests for the Balance of Power Module."""
    print("🚀 Starting Balance of Power Module Tests")
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
        print("✅ All Balance of Power Module tests passed!")
        
        # Save generated HTML for inspection
        output_file = Path(__file__).parent.parent / 'Results' / 'test_balance_of_power_module.html'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Balance of Power Module Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .actor-card, .combatant-card, .submarine-card, .aircraft-card, .amphibious-card, .nuclear-card {{
            border: 1px solid #eee; padding: 15px; margin: 10px; border-radius: 5px;
        }}
        .chart-container {{ margin: 20px 0; }}
        canvas {{ max-width: 100%; }}
    </style>
</head>
<body>
    <h1>Balance of Power Module Test Results</h1>
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
