#!/usr/bin/env python3
"""
Test script for the updated adaptive data adapter to verify proper data generation.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

async def test_adaptive_data_fix():
    """Test the updated adaptive data adapter."""
    
    print("🧪 Testing Updated Adaptive Data Adapter")
    print("=" * 50)
    
    try:
        # Import the adaptive data adapter
        from src.core.adaptive_data_adapter import AdaptiveDataAdapter
        
        # Create adapter instance
        adapter = AdaptiveDataAdapter()
        
        # Test query
        test_query = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
        
        print(f"📝 Test Query: {test_query}")
        print()
        
        # Test data generation for each module
        test_modules = [
            'executive_summary',
            'geopolitical_impact', 
            'balance_of_power',
            'risk_assessment',
            'strategic_recommendations',
            'acquisition_programs',
            'implementation_timeline',
            'forecasting',
            'operational_considerations',
            'regional_sentiment',
            'trade_impact',
            'regional_security',
            'economic_analysis',
            'comparison_analysis',
            'advanced_forecasting',
            'model_performance',
            'strategic_capability',
            'predictive_analytics',
            'scenario_analysis',
            'strategic_analysis',
            'enhanced_data_analysis',
            'interactive_visualizations'
        ]
        
        success_count = 0
        total_count = len(test_modules)
        
        for module_name in test_modules:
            try:
                print(f"🔍 Testing {module_name}...")
                
                # Generate data for this module
                module_data = adapter.module_data_mappings.get(module_name, {})
                customized_data = adapter._customize_module_data(
                    module_name, module_data, test_query, {}
                )
                
                # Check if data was generated
                if customized_data:
                    print(f"   ✅ {module_name}: Data generated successfully")
                    print(f"      Keys: {list(customized_data.keys())}")
                    success_count += 1
                else:
                    print(f"   ❌ {module_name}: No data generated")
                    
            except Exception as e:
                print(f"   ❌ {module_name}: Error - {str(e)}")
        
        print()
        print(f"📊 Results: {success_count}/{total_count} modules successful")
        
        if success_count == total_count:
            print("🎉 All modules have proper data generation!")
        else:
            print("⚠️ Some modules need attention")
        
        # Test the full universal data generation
        print("\n🔧 Testing Universal Data Generation...")
        universal_data = adapter.generate_universal_data(test_query, {})
        
        print(f"📋 Universal data sections: {len(universal_data)}")
        print(f"📋 Universal data keys: {list(universal_data.keys())}")
        
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
            if module in universal_data:
                data = universal_data[module]
                print(f"   ✅ {module}: Present with {len(data)} keys")
            else:
                print(f"   ❌ {module}: Missing from universal data")
        
        return success_count == total_count
        
    except Exception as e:
        print(f"❌ Error testing adaptive data adapter: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_adaptive_data_fix())
    sys.exit(0 if success else 1)
