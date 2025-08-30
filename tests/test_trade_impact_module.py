"""
Test script for Trade Impact Module

Tests the functionality of the Trade Impact Module including:
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

from core.modules.trade_impact_module import TradeImpactModule
from core.modules.base_module import ModuleConfig


def test_module_initialization():
    """Test module initialization and basic configuration."""
    print("🧪 Testing module initialization...")
    
    # Test default initialization
    module = TradeImpactModule()
    assert module.module_id == "tradeimpactmodule"
    assert module.get_title() == "📊 Trade Impact Analysis"
    assert module.get_description() == "Comprehensive analysis of trade disruptions, energy impacts, and economic implications"
    assert module.get_order() == 25
    assert module.is_enabled() == True
    assert module.config.tooltips_enabled == True
    assert module.config.charts_enabled == True
    
    print("✅ Module initialization test passed")
    
    # Test custom configuration
    custom_config = ModuleConfig(
        title="Custom Trade Analysis",
        description="Custom trade impact analysis",
        order=30,
        tooltips_enabled=False,
        charts_enabled=False
    )
    
    custom_module = TradeImpactModule(custom_config)
    assert custom_module.get_title() == "Custom Trade Analysis"
    assert custom_module.get_description() == "Custom trade impact analysis"
    assert custom_module.get_order() == 30
    assert custom_module.config.tooltips_enabled == False
    assert custom_module.config.charts_enabled == False
    
    print("✅ Custom configuration test passed")


def test_required_data_keys():
    """Test required data keys validation."""
    print("🧪 Testing required data keys...")
    
    module = TradeImpactModule()
    required_keys = module.get_required_data_keys()
    
    expected_keys = [
        'trade_analysis',
        'trade_disruptions',
        'energy_trade',
        'economic_implications'
    ]
    
    assert set(required_keys) == set(expected_keys)
    print("✅ Required data keys test passed")


def test_data_validation():
    """Test data validation functionality."""
    print("🧪 Testing data validation...")
    
    module = TradeImpactModule()
    
    # Test with missing data
    incomplete_data = {
        'trade_analysis': {},
        'trade_disruptions': {}
        # Missing energy_trade and economic_implications
    }
    
    try:
        module.validate_data(incomplete_data)
        assert False, "Should have raised ValueError for missing data"
    except ValueError as e:
        assert "Missing required data keys" in str(e)
        print("✅ Missing data validation test passed")
    
    # Test with complete data
    complete_data = {
        'trade_analysis': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_sectors': [],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'trade_disruptions': {
            'disruptions': [],
            'risk_factors': [],
            'mitigation_strategies': []
        },
        'energy_trade': {
            'energy_sectors': [],
            'price_impacts': {},
            'supply_chains': []
        },
        'economic_implications': {
            'gdp_impacts': {},
            'employment_effects': {},
            'currency_effects': {},
            'long_term_implications': 'Test implications'
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
    
    module = TradeImpactModule()
    
    # Sample data for testing
    test_data = {
        'trade_analysis': {
            'title': 'Russia-China Trade Restrictions Impact',
            'overview': 'Analysis of the impact of new trade restrictions on Russia-China bilateral trade relations.',
            'key_sectors': [
                {
                    'name': 'Energy',
                    'role': 'Primary Trade Sector',
                    'impact_level': 'Very High'
                },
                {
                    'name': 'Manufacturing',
                    'role': 'Secondary Trade Sector',
                    'impact_level': 'High'
                },
                {
                    'name': 'Technology',
                    'role': 'Emerging Trade Sector',
                    'impact_level': 'Medium'
                }
            ],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'trade_disruptions': {
            'disruptions': [
                {
                    'name': 'Supply Chain Disruption',
                    'severity': 'High',
                    'duration': '6-12 months',
                    'probability': 'High',
                    'description': 'Significant disruption to supply chains due to trade restrictions.'
                },
                {
                    'name': 'Payment System Restrictions',
                    'severity': 'Medium',
                    'duration': '3-6 months',
                    'probability': 'Medium',
                    'description': 'Restrictions on payment systems affecting trade transactions.'
                }
            ],
            'risk_factors': [
                {
                    'factor': 'Political Tensions',
                    'description': 'Ongoing political tensions between trading partners',
                    'level': 'High'
                },
                {
                    'factor': 'Economic Sanctions',
                    'description': 'Comprehensive economic sanctions affecting trade',
                    'level': 'Very High'
                }
            ],
            'mitigation_strategies': [
                {
                    'name': 'Supply Chain Diversification',
                    'effectiveness': 'High',
                    'description': 'Diversify supply chains to reduce dependency on single sources.'
                },
                {
                    'name': 'Alternative Payment Systems',
                    'effectiveness': 'Medium',
                    'description': 'Develop alternative payment systems to bypass restrictions.'
                }
            ]
        },
        'energy_trade': {
            'energy_sectors': [
                {
                    'name': 'Oil and Gas',
                    'trade_volume': 'Very High',
                    'impact_level': 'Very High',
                    'price_sensitivity': 'High',
                    'description': 'Primary energy trade sector with significant impact.'
                },
                {
                    'name': 'Nuclear Energy',
                    'trade_volume': 'Medium',
                    'impact_level': 'Medium',
                    'price_sensitivity': 'Low',
                    'description': 'Nuclear energy cooperation and technology transfer.'
                }
            ],
            'price_impacts': {
                'crude_oil': '15-20% increase',
                'natural_gas': '20-25% volatility',
                'coal': '10-15% increase',
                'nuclear_materials': '5-10% increase'
            },
            'supply_chains': [
                {
                    'name': 'Oil Pipeline Network',
                    'vulnerability': 'High',
                    'description': 'Vulnerable to geopolitical disruptions and sanctions.'
                },
                {
                    'name': 'LNG Transportation',
                    'vulnerability': 'Medium',
                    'description': 'More flexible but still vulnerable to restrictions.'
                }
            ]
        },
        'economic_implications': {
            'gdp_impacts': {
                'Russia': '-1.2% to -1.8% GDP growth impact',
                'China': '-0.3% to -0.5% GDP growth impact'
            },
            'employment_effects': {
                'manufacturing': '150,000-300,000 job losses',
                'energy_sector': '50,000-100,000 job losses',
                'technology': '25,000-50,000 job losses'
            },
            'currency_effects': {
                'Ruble': '15-20% depreciation',
                'Yuan': '5-8% appreciation',
                'Dollar': 'Temporary strengthening'
            },
            'long_term_implications': 'Long-term economic decoupling trends with significant implications for global trade patterns and economic stability.'
        }
    }
    
    # Generate content
    html_content = module.generate_content(test_data)
    
    # Verify content structure
    assert '<div class="section" id="trade-impact">' in html_content
    assert '📊 Trade Impact Analysis' in html_content
    assert '⚠️ Trade Disruption Analysis' in html_content
    assert '⚡ Energy Trade Impact Analysis' in html_content
    assert '💰 Economic Implications' in html_content
    assert '📈 Interactive Visualizations' in html_content
    
    # Verify specific content
    assert 'Russia-China Trade Restrictions Impact' in html_content
    assert 'Energy' in html_content
    assert 'Manufacturing' in html_content
    assert 'Technology' in html_content
    
    print("✅ Content generation test passed")
    
    return html_content


def test_tooltip_functionality():
    """Test tooltip initialization and functionality."""
    print("🧪 Testing tooltip functionality...")
    
    module = TradeImpactModule()
    
    # Check that tooltips were initialized
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    
    # Check specific tooltips
    assert 'trade_overview' in tooltip_data
    assert 'trade_disruptions' in tooltip_data
    assert 'energy_trade' in tooltip_data
    assert 'economic_implications' in tooltip_data
    
    # Verify tooltip content
    overview_tooltip = tooltip_data['trade_overview']
    assert overview_tooltip.title == "Trade Overview"
    assert "Comprehensive analysis" in overview_tooltip.description
    assert overview_tooltip.confidence == 90.0
    
    print("✅ Tooltip functionality test passed")


def test_chart_integration():
    """Test chart integration functionality."""
    print("🧪 Testing chart integration...")
    
    module = TradeImpactModule()
    
    # Test with charts enabled
    assert module.config.charts_enabled == True
    
    # Test chart data generation
    test_data = {
        'trade_analysis': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_sectors': [
                {
                    'name': 'Energy',
                    'trade_volume': 'Very High',
                    'impact_level': 'Very High'
                },
                {
                    'name': 'Manufacturing',
                    'trade_volume': 'High',
                    'impact_level': 'High'
                }
            ],
            'impact_level': 'High',
            'confidence_score': 85.0
        },
        'trade_disruptions': {
            'disruptions': [],
            'risk_factors': [],
            'mitigation_strategies': []
        },
        'energy_trade': {
            'energy_sectors': [],
            'price_impacts': {
                'crude_oil': '15-20% increase',
                'natural_gas': '20-25% volatility'
            },
            'supply_chains': []
        },
        'economic_implications': {
            'gdp_impacts': {},
            'employment_effects': {},
            'currency_effects': {},
            'long_term_implications': 'Test implications'
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
    
    module = TradeImpactModule()
    metadata = module.get_module_metadata()
    
    assert metadata['module_id'] == 'tradeimpactmodule'
    assert metadata['title'] == '📊 Trade Impact Analysis'
    assert metadata['enabled'] == True
    assert metadata['order'] == 25
    assert 'trade_analysis' in metadata['required_data_keys']
    assert metadata['tooltips_count'] > 0
    
    print("✅ Module metadata test passed")


def test_configuration_export_import():
    """Test configuration export and import functionality."""
    print("🧪 Testing configuration export/import...")
    
    module = TradeImpactModule()
    
    # Export configuration
    config = module.export_config()
    
    assert config['enabled'] == True
    assert config['title'] == '📊 Trade Impact Analysis'
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    # Import configuration
    new_config = {
        'enabled': False,
        'title': 'Modified Title',
        'description': 'Modified Description',
        'order': 35,
        'tooltips_enabled': False,
        'charts_enabled': False
    }
    
    module.import_config(new_config)
    
    assert module.config.enabled == False
    assert module.config.title == 'Modified Title'
    assert module.config.description == 'Modified Description'
    assert module.config.order == 35
    assert module.config.tooltips_enabled == False
    assert module.config.charts_enabled == False
    
    print("✅ Configuration export/import test passed")


def main():
    """Run all tests for the Trade Impact Module."""
    print("🚀 Starting Trade Impact Module Tests")
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
        print("✅ All Trade Impact Module tests passed!")
        
        # Save generated HTML for inspection
        output_file = Path(__file__).parent.parent / 'Results' / 'test_trade_impact_module.html'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trade Impact Module Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric-card, .sector-card, .disruption-card, .energy-sector-card, .strategy-card, .supply-chain-card {{
            border: 1px solid #eee; padding: 15px; margin: 10px; border-radius: 5px;
        }}
        .chart-container {{ margin: 20px 0; }}
        canvas {{ max-width: 100%; }}
    </style>
</head>
<body>
    <h1>Trade Impact Module Test Results</h1>
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
