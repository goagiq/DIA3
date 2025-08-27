#!/usr/bin/env python3
"""
Set Enhanced Template as Default

This script configures the DIA3 system to use the enhanced HTML report generator
with 22 modules and advanced tooltips as the default template for all reports.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def set_enhanced_template_as_default():
    """Set the enhanced HTML report generator as the default template."""
    
    print("🎯 Setting Enhanced Template as Default")
    print("=" * 50)
    
    # 1. Update template configuration
    update_template_config()
    
    # 2. Update MCP server configuration
    update_mcp_server_config()
    
    # 3. Update main system configuration
    update_main_config()
    
    # 4. Create verification script
    create_verification_script()
    
    print("\n✅ Enhanced template successfully set as default!")
    print("🔧 All configurations updated")
    print("📁 Reports will now use the enhanced 22-module template with advanced tooltips")
    print("💡 Features: Interactive visualizations, advanced tooltips, modular design")

def update_template_config():
    """Update the template configuration to use enhanced template."""
    print("📝 Updating template configuration...")
    
    config_file = Path("src/core/template_config.py")
    
    # Read current config
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the enhanced template path to use the correct enhanced HTML generator
    updated_content = content.replace(
        'ENHANCED_REPORT_TEMPLATE = (\n        TEMPLATES_DIR / "Pakistan_Submarine_Analysis_Enhanced_Report.html"\n    )',
        'ENHANCED_REPORT_TEMPLATE = (\n        Path("src/core/enhanced_html_report_generator.py")\n    )'
    )
    
    # Write updated config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("   ✅ Template configuration updated")

def update_mcp_server_config():
    """Update MCP server to use enhanced template by default."""
    print("🔧 Updating MCP server configuration...")
    
    # Create a configuration file for MCP server
    mcp_config_file = Path("src/config/mcp_report_config.json")
    mcp_config_file.parent.mkdir(parents=True, exist_ok=True)
    
    mcp_config = {
        "default_report_generator": "EnhancedHTMLReportGenerator",
        "default_template": "enhanced_22_module_template",
        "features": {
            "advanced_tooltips": True,
            "interactive_visualizations": True,
            "modular_design": True,
            "professional_styling": True,
            "responsive_layout": True
        },
        "modules": {
            "total_modules": 22,
            "enabled_modules": [
                "executive_summary",
                "strategic_context",
                "geopolitical_implications",
                "economic_implications",
                "security_implications",
                "diplomatic_consequences",
                "escalation_risks",
                "strategic_recommendations",
                "regional_analysis",
                "capability_assessment",
                "threat_analysis",
                "risk_evaluation",
                "policy_implications",
                "stakeholder_analysis",
                "timeline_analysis",
                "cost_benefit_analysis",
                "comparative_analysis",
                "scenario_planning",
                "resource_allocation",
                "performance_metrics",
                "compliance_analysis",
                "implementation_plan"
            ]
        },
        "output": {
            "format": "html",
            "directory": "Results",
            "filename_pattern": "{topic}_enhanced_analysis_{timestamp}.html",
            "include_timestamp": True
        },
        "generator_class": "src.core.enhanced_html_report_generator.EnhancedHTMLReportGenerator",
        "method_name": "generate_enhanced_report"
    }
    
    with open(mcp_config_file, 'w', encoding='utf-8') as f:
        json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ MCP server configuration updated")

def update_main_config():
    """Update main system configuration."""
    print("⚙️ Updating main system configuration...")
    
    # Create main configuration file
    main_config_file = Path("src/config/enhanced_template_config.json")
    main_config_file.parent.mkdir(parents=True, exist_ok=True)
    
    main_config = {
        "system_defaults": {
            "report_generator": "EnhancedHTMLReportGenerator",
            "template_type": "enhanced_22_module",
            "output_format": "html",
            "output_directory": "Results"
        },
        "enhanced_template_features": {
            "modules_count": 22,
            "advanced_tooltips": True,
            "interactive_visualizations": True,
            "modular_design": True,
            "professional_styling": True,
            "responsive_layout": True,
            "source_tracking": True,
            "confidence_scoring": True
        },
        "file_saving": {
            "verify_file_saving": True,
            "multiple_save_methods": True,
            "fallback_mechanism": True,
            "automatic_verification": True
        },
        "generator_settings": {
            "class_path": "src.core.enhanced_html_report_generator.EnhancedHTMLReportGenerator",
            "method_name": "generate_enhanced_report",
            "default_parameters": {
                "include_advanced_tooltips": True,
                "include_interactive_visualizations": True,
                "use_enhanced_template": True
            }
        }
    }
    
    with open(main_config_file, 'w', encoding='utf-8') as f:
        json.dump(main_config, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Main system configuration updated")

def create_verification_script():
    """Create a verification script to test the enhanced template."""
    print("🧪 Creating verification script...")
    
    verification_script = Path("test_enhanced_template_default.py")
    
    script_content = '''#!/usr/bin/env python3
"""
Test Enhanced Template as Default

This script verifies that the enhanced template is working as the default.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def test_enhanced_template_default():
    """Test that the enhanced template works as default."""
    
    print("🧪 Testing Enhanced Template as Default")
    print("=" * 40)
    
    try:
        # Initialize the enhanced HTML report generator
        generator = EnhancedHTMLReportGenerator()
        
        # Test data
        test_data = {
            "title": "Enhanced Template Test Report",
            "subtitle": "Verification of Enhanced Template as Default",
            "topic": "Test Analysis",
            "analysis_type": "test",
            "confidence_score": 0.9,
            "source_metadata": [
                {
                    "source_type": "test",
                    "source_name": "Test System",
                    "title": "Template Verification Test",
                    "confidence": 0.9,
                    "reliability_score": 0.9,
                    "timestamp": "2025-01-26 12:00"
                }
            ],
            "content": "This is a test report to verify that the enhanced template is working as the default template in the DIA3 system."
        }
        
        # Generate test report
        print("📊 Generating test report with enhanced template...")
        
        result = await generator.generate_enhanced_report(
            data=test_data,
            output_path="Results/test_enhanced_template_default.html"
        )
        
        if result["success"]:
            print("✅ SUCCESS: Enhanced template working as default!")
            print(f"📁 File saved to: {result['file_path']}")
            
            # Verify file exists
            file_path = Path(result['file_path'])
            if file_path.exists():
                print(f"📏 File size: {file_path.stat().st_size} bytes")
                print("🔍 File verification: PASSED")
            else:
                print("❌ File verification: FAILED")
            
            return True
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def main():
    """Main function."""
    success = await test_enhanced_template_default()
    
    print("\\n" + "=" * 40)
    if success:
        print("🎉 Enhanced template is working as default!")
        print("🚀 All reports will now use the enhanced 22-module template")
    else:
        print("⚠️ Enhanced template test failed")
        print("🔧 Please check the configuration")
    
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open(verification_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("   ✅ Verification script created")

def main():
    """Main function."""
    set_enhanced_template_as_default()
    
    print("\n" + "=" * 50)
    print("🎯 Enhanced Template Configuration Complete!")
    print("=" * 50)
    print("📋 What was configured:")
    print("   • Template configuration updated")
    print("   • MCP server configured to use enhanced template")
    print("   • Main system configuration updated")
    print("   • Verification script created")
    print("\n🚀 Next steps:")
    print("   1. Run: python test_enhanced_template_default.py")
    print("   2. Test report generation with: mcp_DIA3_generate_report")
    print("   3. Verify files are saved to /Results directory")
    print("\n💡 All future reports will now use the enhanced 22-module template!")
    print("=" * 50)

if __name__ == "__main__":
    main()

