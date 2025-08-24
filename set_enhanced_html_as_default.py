#!/usr/bin/env python3
"""
Set Enhanced HTML as Default Template

This script configures the modular report generator to use the enhanced HTML template
as the default for all future reports.
"""

import json
import sys
from pathlib import Path

def set_enhanced_html_as_default():
    """Set the enhanced HTML template as the default for modular reports."""
    
    # Configuration file path
    config_file = Path("src/core/config/default_template_config.json")
    
    # Create the config directory if it doesn't exist
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Default configuration
    default_config = {
        "default_template": "enhanced_html",
        "template_path": "src/core/templates/default_enhanced_html_template.html",
        "features": {
            "advanced_tooltips": True,
            "multiple_sources": True,
            "interactive_charts": True,
            "responsive_design": True,
            "professional_styling": True
        },
        "modules": {
            "all_modules_enabled": True,
            "default_modules": [
                "executive_summary",
                "strategic_overview", 
                "threat_assessment",
                "capability_analysis",
                "regional_security",
                "economic_impact",
                "technological_assessment",
                "intelligence_analysis",
                "risk_management",
                "policy_recommendations",
                "stakeholder_analysis",
                "timeline_analysis",
                "cost_benefit_analysis",
                "comparative_analysis",
                "scenario_planning",
                "resource_allocation",
                "performance_metrics",
                "compliance_analysis",
                "communication_strategy",
                "implementation_plan",
                "monitoring_evaluation",
                "model_performance"
            ]
        },
        "output": {
            "format": "html",
            "directory": "Results",
            "filename_pattern": "{topic}_enhanced_analysis_{timestamp}.html",
            "include_timestamp": True,
            "open_in_browser": True
        }
    }
    
    try:
        # Write the configuration
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print("✅ Enhanced HTML template set as default!")
        print(f"📁 Configuration saved to: {config_file}")
        print("\n📋 Default Configuration:")
        print(f"   • Template: {default_config['default_template']}")
        print(f"   • Path: {default_config['template_path']}")
        print(f"   • Modules: {len(default_config['modules']['default_modules'])} enabled")
        print(f"   • Output Format: {default_config['output']['format']}")
        print(f"   • Output Directory: {default_config['output']['directory']}")
        
        # Create a simple test script
        test_script = Path("test_enhanced_template.py")
        test_script_content = '''#!/usr/bin/env python3
"""
Test Enhanced HTML Template

This script tests the enhanced HTML template with a sample topic.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import modular_report_generator
from src.core.adaptive_data_adapter import adaptive_data_adapter

async def test_enhanced_template():
    """Test the enhanced HTML template."""
    
    topic = "Test Topic: Enhanced Template Analysis"
    
    print("🧪 Testing Enhanced HTML Template...")
    print(f"📋 Topic: {topic}")
    
    try:
        # Generate adaptive data
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Get all available modules
        modules_info = modular_report_generator.get_available_modules()
        all_module_ids = list(modules_info.keys())
        
        # Generate the enhanced HTML report
        result = await modular_report_generator.generate_modular_report(
            topic=topic,
            data=universal_data,
            enabled_modules=all_module_ids,
            report_title=f"Enhanced Test: {topic}",
            custom_config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True
            }
        )
        
        if result.get("success"):
            print("✅ Enhanced template test successful!")
            print(f"📁 File: {result.get('file_path')}")
            return True
        else:
            print(f"❌ Test failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_template())
    if success:
        print("\\n🎉 Enhanced template is working correctly!")
    else:
        print("\\n❌ Enhanced template test failed!")
        sys.exit(1)
'''
        
        with open(test_script, 'w', encoding='utf-8') as f:
            f.write(test_script_content)
        
        print(f"\n🧪 Test script created: {test_script}")
        print("   Run 'python test_enhanced_template.py' to test the enhanced template")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting default template: {e}")
        return False

if __name__ == "__main__":
    success = set_enhanced_html_as_default()
    
    if success:
        print("\n🎉 Enhanced HTML template is now the default!")
        print("📊 All future reports will use:")
        print("   • Advanced tooltips with multiple sources")
        print("   • Interactive visualizations")
        print("   • Professional styling and layout")
        print("   • All 22 analysis modules")
        print("   • Responsive design")
    else:
        print("\n❌ Failed to set enhanced template as default!")
        sys.exit(1)
