#!/usr/bin/env python3
"""
Comprehensive Phase 4 Integration Test

This script performs comprehensive testing of the Phase 4 integration with all 22 modules.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_all_modules():
    """Test all 22 modules for Phase 4 integration."""
    
    print("🧪 Comprehensive Phase 4 Integration Test")
    print("=" * 60)
    
    # List of all 22 modules
    all_modules = [
        "strategic_recommendations_module",
        "executive_summary_module",
        "geopolitical_impact_module",
        "trade_impact_module",
        "balance_of_power_module",
        "risk_assessment_module",
        "interactive_visualizations_module",
        "strategic_analysis_module",
        "enhanced_data_analysis_module",
        "regional_sentiment_module",
        "implementation_timeline_module",
        "acquisition_programs_module",
        "forecasting_module",
        "operational_considerations_module",
        "economic_analysis_module",
        "comparison_analysis_module",
        "advanced_forecasting_module",
        "model_performance_module",
        "strategic_capability_module",
        "predictive_analytics_module",
        "scenario_analysis_module",
        "strategic_intelligence_module"
    ]
    
    test_results = {}
    
    for module_name in all_modules:
        try:
            # Import the module
            module_path = f"src.core.modules.{module_name}"
            module_class_name = "".join(word.capitalize() for word in module_name.split('_'))
            
            # Dynamic import
            module = __import__(module_path, fromlist=[module_class_name])
            module_class = getattr(module, module_class_name)
            
            # Create instance
            instance = module_class()
            
            # Test basic functionality
            test_data = {
                "topic": "Pakistan Submarine Acquisition",
                "analysis_type": "strategic",
                "time_range": "5_years"
            }
            
            # Test content generation
            result = await instance.generate_content(test_data)
            
            # Check if Phase 4 integration is present
            phase4_integrated = False
            if isinstance(result, dict) and "metadata" in result:
                phase4_integrated = result["metadata"].get("phase4_integrated", False)
            
            test_results[module_name] = {
                "import_success": True,
                "instance_created": True,
                "content_generated": True,
                "phase4_integrated": phase4_integrated,
                "error": None
            }
            
            status = "✅ PASS" if phase4_integrated else "⚠️  PARTIAL"
            print(f"{status} {module_name}")
            
        except Exception as e:
            test_results[module_name] = {
                "import_success": False,
                "instance_created": False,
                "content_generated": False,
                "phase4_integrated": False,
                "error": str(e)
            }
            print(f"❌ FAIL {module_name}: {str(e)}")
    
    return test_results

async def test_modular_report_generator():
    """Test the modular report generator with Phase 4 integration."""
    
    print("\n🔧 Testing Modular Report Generator")
    print("=" * 40)
    
    try:
        from src.core.modular_report_generator import ModularReportGenerator
        
        # Create generator
        generator = ModularReportGenerator()
        
        # Check total modules
        total_modules = len(generator.modules)
        print(f"📊 Total registered modules: {total_modules}")
        
        # Check for strategic intelligence module
        strategic_found = "strategic_intelligence" in generator.modules
        print(f"🎯 Strategic Intelligence Module: {'✅ Found' if strategic_found else '❌ Missing'}")
        
        # Test report generation
        test_query = "Pakistan Submarine Acquisition Analysis"
        test_config = {"phase4_integration": True}
        
        result = await generator.generate_modular_report(
            query=test_query,
            config=test_config,
            output_format="html"
        )
        
        print(f"📄 Report Generation: {'✅ Success' if result.get('success') else '❌ Failed'}")
        
        return {
            "total_modules": total_modules,
            "strategic_intelligence_found": strategic_found,
            "report_generation_success": result.get('success', False),
            "error": None
        }
        
    except Exception as e:
        print(f"❌ Modular Report Generator Test Failed: {e}")
        return {
            "total_modules": 0,
            "strategic_intelligence_found": False,
            "report_generation_success": False,
            "error": str(e)
        }

async def test_phase4_capabilities():
    """Test specific Phase 4 capabilities."""
    
    print("\n🚀 Testing Phase 4 Capabilities")
    print("=" * 35)
    
    try:
        from src.core.modules.strategic_intelligence_module import StrategicIntelligenceModule
        
        # Create strategic intelligence module
        strategic_module = StrategicIntelligenceModule()
        
        # Test data
        test_data = {
            "topic": "Pakistan Submarine Acquisition",
            "analysis_type": "strategic",
            "time_range": "5_years"
        }
        
        # Test content generation
        result = await strategic_module.generate_content(test_data)
        
        # Check capabilities
        capabilities = {
            "knowledge_graph": "Knowledge Graph Intelligence" in result.get("content", ""),
            "cross_domain": "Cross-Domain Intelligence" in result.get("content", ""),
            "recommendations": "Intelligence-Driven Recommendations" in result.get("content", ""),
            "metadata": "metadata" in result and result["metadata"].get("phase4_integrated", False)
        }
        
        for capability, status in capabilities.items():
            print(f"{'✅' if status else '❌'} {capability.replace('_', ' ').title()}")
        
        return capabilities
        
    except Exception as e:
        print(f"❌ Phase 4 Capabilities Test Failed: {e}")
        return {"error": str(e)}

async def main():
    """Main test function."""
    
    print("🚀 Comprehensive Phase 4 Integration Test Suite")
    print("=" * 60)
    
    # Test 1: All modules
    print("\n📋 Test 1: Individual Module Testing")
    module_results = await test_all_modules()
    
    # Test 2: Modular report generator
    print("\n📋 Test 2: Modular Report Generator Testing")
    generator_results = await test_modular_report_generator()
    
    # Test 3: Phase 4 capabilities
    print("\n📋 Test 3: Phase 4 Capabilities Testing")
    capability_results = await test_phase4_capabilities()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    # Module summary
    total_modules = len(module_results)
    successful_modules = sum(1 for r in module_results.values() if r["import_success"])
    phase4_modules = sum(1 for r in module_results.values() if r["phase4_integrated"])
    
    print(f"📋 Module Testing:")
    print(f"   Total Modules: {total_modules}")
    print(f"   Successfully Imported: {successful_modules}/{total_modules}")
    print(f"   Phase 4 Integrated: {phase4_modules}/{total_modules}")
    
    # Generator summary
    print(f"\n🔧 Generator Testing:")
    print(f"   Total Registered Modules: {generator_results.get('total_modules', 0)}")
    print(f"   Strategic Intelligence Module: {'✅ Found' if generator_results.get('strategic_intelligence_found') else '❌ Missing'}")
    print(f"   Report Generation: {'✅ Success' if generator_results.get('report_generation_success') else '❌ Failed'}")
    
    # Capabilities summary
    if "error" not in capability_results:
        print(f"\n🚀 Phase 4 Capabilities:")
        for capability, status in capability_results.items():
            print(f"   {capability.replace('_', ' ').title()}: {'✅ Working' if status else '❌ Failed'}")
    else:
        print(f"\n🚀 Phase 4 Capabilities: ❌ {capability_results['error']}")
    
    # Overall assessment
    print(f"\n🎯 Overall Assessment:")
    if phase4_modules == total_modules and generator_results.get('report_generation_success'):
        print("   🎉 EXCELLENT: All modules successfully integrated with Phase 4!")
    elif phase4_modules >= total_modules * 0.8:
        print("   ✅ GOOD: Most modules successfully integrated with Phase 4!")
    elif phase4_modules >= total_modules * 0.5:
        print("   ⚠️  PARTIAL: Some modules successfully integrated with Phase 4!")
    else:
        print("   ❌ POOR: Most modules failed Phase 4 integration!")
    
    print(f"\n🔧 Next Steps:")
    print("   1. Generate a comprehensive report to validate integration")
    print("   2. Test the enhanced HTML report generation")
    print("   3. Verify all Phase 4 capabilities are working correctly")

if __name__ == "__main__":
    asyncio.run(main())
