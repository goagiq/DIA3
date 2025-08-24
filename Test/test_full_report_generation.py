#!/usr/bin/env python3
"""
Test script for full report generation with all 22 modules.
"""

import asyncio
import sys

# Add src to path
sys.path.append('src')

async def test_full_report_generation():
    """Test full report generation with all 22 modules."""
    
    print("🧪 Testing Full Report Generation with All 22 Modules")
    print("=" * 60)
    
    try:
        # Import the integrated adaptive modular report generator
        from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
        
        # Test query
        test_query = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
        
        print(f"📝 Test Query: {test_query}")
        print()
        
        # Generate report with all 22 modules
        print("🚀 Generating report with all 22 modules...")
        result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
            test_query
        )
        
        print("📊 Report Generation Results:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   File Path: {result.get('file_path', 'N/A')}")
        print(f"   Query: {result.get('query', 'N/A')}")
        print(f"   Universal Data Sections: {result.get('universal_data_sections', 0)}")
        print(f"   Integrated Adaptive Mode: {result.get('integrated_adaptive_mode', False)}")
        print(f"   Modules Generated: {result.get('modules_generated', 0)}")
        print(f"   Selected Modules: {result.get('selected_modules', [])}")
        print(f"   Module Selection Method: {result.get('module_selection_method', 'N/A')}")
        
        if result.get('error'):
            print(f"   Error: {result.get('error')}")
        
        print()
        
        # Check if all 22 modules were selected
        selected_modules = result.get('selected_modules', [])
        if len(selected_modules) == 22:
            print("✅ All 22 modules were selected!")
        else:
            print(f"⚠️ Only {len(selected_modules)} modules were selected")
            print(f"   Expected: 22, Got: {len(selected_modules)}")
        
        # Check for specific problematic modules
        problematic_modules = [
            'acquisition_programs',
            'regional_security', 
            'strategic_partnerships',
            'trade_impact',
            'escalation_timeline',
            'strategic_recommendations',
            'implementation_timeline',
            'forecasting'
        ]
        
        print("\n🔍 Checking Problematic Modules:")
        for module in problematic_modules:
            if module in selected_modules:
                print(f"   ✅ {module}: Selected")
            else:
                print(f"   ❌ {module}: Not selected")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Error testing full report generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_report_generation())
    sys.exit(0 if success else 1)
