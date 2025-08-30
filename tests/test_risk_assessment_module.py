"""
Test script for Risk Assessment Module

Tests the functionality of the Risk Assessment Module including:
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

from core.modules.risk_assessment_module import RiskAssessmentModule
from core.modules.base_module import ModuleConfig


def test_module_initialization():
    """Test module initialization and basic configuration."""
    print("🧪 Testing module initialization...")
    
    # Test default initialization
    module = RiskAssessmentModule()
    assert module.module_id == "riskassessmentmodule"
    assert module.get_title() == "⚠️ Risk Assessment Analysis"
    assert module.get_description() == "Comprehensive risk assessment with escalation probability timeline and mitigation strategies"
    assert module.get_order() == 35
    assert module.is_enabled() == True
    assert module.config.tooltips_enabled == True
    assert module.config.charts_enabled == True
    
    print("✅ Module initialization test passed")
    
    # Test custom configuration
    custom_config = ModuleConfig(
        title="Custom Risk Analysis",
        description="Custom risk assessment analysis",
        order=40,
        tooltips_enabled=False,
        charts_enabled=False
    )
    
    custom_module = RiskAssessmentModule(custom_config)
    assert custom_module.get_title() == "Custom Risk Analysis"
    assert custom_module.get_description() == "Custom risk assessment analysis"
    assert custom_module.get_order() == 40
    assert custom_module.config.tooltips_enabled == False
    assert custom_module.config.charts_enabled == False
    
    print("✅ Custom configuration test passed")


def test_required_data_keys():
    """Test required data keys validation."""
    print("🧪 Testing required data keys...")
    
    module = RiskAssessmentModule()
    required_keys = module.get_required_data_keys()
    
    expected_keys = [
        'risk_overview',
        'risk_matrix',
        'escalation_timeline',
        'mitigation_strategies'
    ]
    
    assert set(required_keys) == set(expected_keys)
    print("✅ Required data keys test passed")


def test_data_validation():
    """Test data validation functionality."""
    print("🧪 Testing data validation...")
    
    module = RiskAssessmentModule()
    
    # Test with missing data
    incomplete_data = {
        'risk_overview': {},
        'risk_matrix': {}
        # Missing escalation_timeline and mitigation_strategies
    }
    
    try:
        module.validate_data(incomplete_data)
        assert False, "Should have raised ValueError for missing data"
    except ValueError as e:
        assert "Missing required data keys" in str(e)
        print("✅ Missing data validation test passed")
    
    # Test with complete data
    complete_data = {
        'risk_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_risks': [],
            'overall_risk_level': 'Medium',
            'confidence_score': 85.0
        },
        'risk_matrix': {
            'risk_categories': [
                {
                    'name': 'Military Risk',
                    'risk_level': 'High',
                    'probability': '75%',
                    'impact': 'High',
                    'description': 'Military escalation risk in the region.'
                },
                {
                    'name': 'Economic Risk',
                    'risk_level': 'Medium',
                    'probability': '60%',
                    'impact': 'Medium',
                    'description': 'Economic disruption risk.'
                }
            ],
            'risk_assessments': [
                {
                    'name': 'Strategic Risk Assessment',
                    'risk_score': 'High (85%)',
                    'trend': 'Increasing',
                    'priority': 'High',
                    'description': 'Strategic risk assessment for the region.'
                }
            ]
        },
        'escalation_timeline': {
            'timeline_periods': [
                {
                    'name': 'Immediate (0-30 days)',
                    'duration': '30 days',
                    'risk_level': 'High',
                    'probability': '80%',
                    'description': 'Immediate escalation risk period.'
                },
                {
                    'name': 'Short-term (1-3 months)',
                    'duration': '3 months',
                    'risk_level': 'Medium',
                    'probability': '65%',
                    'description': 'Short-term escalation risk period.'
                }
            ],
            'escalation_scenarios': [
                {
                    'name': 'Military Escalation',
                    'trigger': 'Border incident',
                    'probability': '70%',
                    'impact': 'High',
                    'description': 'Military escalation scenario.'
                }
            ]
        },
        'mitigation_strategies': {
            'strategy_categories': [
                {
                    'name': 'Diplomatic Mitigation',
                    'effectiveness': 'High',
                    'cost': 'Low',
                    'timeline': 'Immediate',
                    'description': 'Diplomatic mitigation strategies.'
                },
                {
                    'name': 'Military Mitigation',
                    'effectiveness': 'Medium',
                    'cost': 'High',
                    'timeline': 'Short-term',
                    'description': 'Military mitigation strategies.'
                }
            ],
            'implementation_plans': [
                {
                    'name': 'Diplomatic Engagement Plan',
                    'priority': 'High',
                    'timeline': 'Immediate',
                    'resources': 'Medium',
                    'description': 'Diplomatic engagement implementation plan.'
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
    
    module = RiskAssessmentModule()
    
    # Sample data for testing
    test_data = {
        'risk_overview': {
            'title': 'Pakistan-India Risk Assessment Analysis',
            'overview': 'Comprehensive risk assessment of the Pakistan-India relationship and potential escalation scenarios.',
            'key_risks': [
                {
                    'name': 'Military Escalation',
                    'category': 'Military Risk',
                    'risk_level': 'High',
                    'probability': '75%'
                },
                {
                    'name': 'Economic Disruption',
                    'category': 'Economic Risk',
                    'risk_level': 'Medium',
                    'probability': '60%'
                }
            ],
            'overall_risk_level': 'High',
            'confidence_score': 85.0
        },
        'risk_matrix': {
            'risk_categories': [
                {
                    'name': 'Military Risk',
                    'risk_level': 'High',
                    'probability': '75%',
                    'impact': 'High',
                    'description': 'Military escalation risk in the region.'
                },
                {
                    'name': 'Economic Risk',
                    'risk_level': 'Medium',
                    'probability': '60%',
                    'impact': 'Medium',
                    'description': 'Economic disruption risk.'
                }
            ],
            'risk_assessments': [
                {
                    'name': 'Strategic Risk Assessment',
                    'risk_score': 'High (85%)',
                    'trend': 'Increasing',
                    'priority': 'High',
                    'description': 'Strategic risk assessment for the region.'
                }
            ]
        },
        'escalation_timeline': {
            'timeline_periods': [
                {
                    'name': 'Immediate (0-30 days)',
                    'duration': '30 days',
                    'risk_level': 'High',
                    'probability': '80%',
                    'description': 'Immediate escalation risk period.'
                },
                {
                    'name': 'Short-term (1-3 months)',
                    'duration': '3 months',
                    'risk_level': 'Medium',
                    'probability': '65%',
                    'description': 'Short-term escalation risk period.'
                }
            ],
            'escalation_scenarios': [
                {
                    'name': 'Military Escalation',
                    'trigger': 'Border incident',
                    'probability': '70%',
                    'impact': 'High',
                    'description': 'Military escalation scenario.'
                }
            ]
        },
        'mitigation_strategies': {
            'strategy_categories': [
                {
                    'name': 'Diplomatic Mitigation',
                    'effectiveness': 'High',
                    'cost': 'Low',
                    'timeline': 'Immediate',
                    'description': 'Diplomatic mitigation strategies.'
                },
                {
                    'name': 'Military Mitigation',
                    'effectiveness': 'Medium',
                    'cost': 'High',
                    'timeline': 'Short-term',
                    'description': 'Military mitigation strategies.'
                }
            ],
            'implementation_plans': [
                {
                    'name': 'Diplomatic Engagement Plan',
                    'priority': 'High',
                    'timeline': 'Immediate',
                    'resources': 'Medium',
                    'description': 'Diplomatic engagement implementation plan.'
                }
            ]
        }
    }
    
    # Generate content
    html_content = module.generate_content(test_data)
    
    # Verify content structure
    assert '<div class="section" id="risk-assessment">' in html_content
    assert '⚠️ Risk Assessment Analysis' in html_content
    assert '📊 Comprehensive Risk Matrix' in html_content
    assert '⏰ Escalation Probability Timeline' in html_content
    assert '🛡️ Mitigation Strategies' in html_content
    assert '📈 Interactive Visualizations' in html_content
    
    # Verify specific content
    assert 'Pakistan-India Risk Assessment Analysis' in html_content
    assert 'Military Escalation' in html_content
    assert 'Economic Disruption' in html_content
    assert 'High' in html_content
    
    print("✅ Content generation test passed")
    
    return html_content


def test_tooltip_functionality():
    """Test tooltip initialization and functionality."""
    print("🧪 Testing tooltip functionality...")
    
    module = RiskAssessmentModule()
    
    # Check that tooltips were initialized
    tooltip_data = module.get_tooltip_data()
    assert len(tooltip_data) > 0
    
    # Check specific tooltips
    assert 'risk_overview' in tooltip_data
    assert 'risk_matrix' in tooltip_data
    assert 'escalation_timeline' in tooltip_data
    assert 'mitigation_strategies' in tooltip_data
    
    # Verify tooltip content
    overview_tooltip = tooltip_data['risk_overview']
    assert overview_tooltip.title == "Risk Overview"
    assert "Comprehensive analysis" in overview_tooltip.description
    assert overview_tooltip.confidence == 90.0
    
    print("✅ Tooltip functionality test passed")


def test_chart_integration():
    """Test chart integration functionality."""
    print("🧪 Testing chart integration...")
    
    module = RiskAssessmentModule()
    
    # Test with charts enabled
    assert module.config.charts_enabled == True
    
    # Test chart data generation
    test_data = {
        'risk_overview': {
            'title': 'Test Analysis',
            'overview': 'Test overview',
            'key_risks': [],
            'overall_risk_level': 'Medium',
            'confidence_score': 85.0
        },
        'risk_matrix': {
            'risk_categories': [
                {
                    'name': 'Test Risk Category',
                    'risk_level': 'High',
                    'probability': '75%',
                    'impact': 'High',
                    'description': 'Test description'
                }
            ],
            'risk_assessments': []
        },
        'escalation_timeline': {
            'timeline_periods': [
                {
                    'name': 'Test Period',
                    'duration': '30 days',
                    'risk_level': 'High',
                    'probability': '80%',
                    'description': 'Test description'
                }
            ],
            'escalation_scenarios': []
        },
        'mitigation_strategies': {
            'strategy_categories': [],
            'implementation_plans': []
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
    
    module = RiskAssessmentModule()
    metadata = module.get_module_metadata()
    
    assert metadata['module_id'] == 'riskassessmentmodule'
    assert metadata['title'] == '⚠️ Risk Assessment Analysis'
    assert metadata['enabled'] == True
    assert metadata['order'] == 35
    assert 'risk_overview' in metadata['required_data_keys']
    assert metadata['tooltips_count'] > 0
    
    print("✅ Module metadata test passed")


def test_configuration_export_import():
    """Test configuration export and import functionality."""
    print("🧪 Testing configuration export/import...")
    
    module = RiskAssessmentModule()
    
    # Export configuration
    config = module.export_config()
    
    assert config['enabled'] == True
    assert config['title'] == '⚠️ Risk Assessment Analysis'
    assert config['tooltips_enabled'] == True
    assert config['charts_enabled'] == True
    
    # Import configuration
    new_config = {
        'enabled': False,
        'title': 'Modified Title',
        'description': 'Modified Description',
        'order': 45,
        'tooltips_enabled': False,
        'charts_enabled': False
    }
    
    module.import_config(new_config)
    
    assert module.config.enabled == False
    assert module.config.title == 'Modified Title'
    assert module.config.description == 'Modified Description'
    assert module.config.order == 45
    assert module.config.tooltips_enabled == False
    assert module.config.charts_enabled == False
    
    print("✅ Configuration export/import test passed")


def main():
    """Run all tests for the Risk Assessment Module."""
    print("🚀 Starting Risk Assessment Module Tests")
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
        print("✅ All Risk Assessment Module tests passed!")
        
        # Save generated HTML for inspection
        output_file = Path(__file__).parent.parent / 'Results' / 'test_risk_assessment_module.html'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Risk Assessment Module Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .risk-card, .category-card, .assessment-card, .period-card, .scenario-card, .plan-card {{
            border: 1px solid #eee; padding: 15px; margin: 10px; border-radius: 5px;
        }}
        .chart-container {{ margin: 20px 0; }}
        canvas {{ max-width: 100%; }}
    </style>
</head>
<body>
    <h1>Risk Assessment Module Test Results</h1>
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
