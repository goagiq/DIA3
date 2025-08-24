#!/usr/bin/env python3
"""
Debug script for data extraction issue.
"""

import sys
sys.path.append('src')

from src.core.adaptive_data_adapter import AdaptiveDataAdapter
from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator

def debug_data_extraction():
    """Debug the data extraction process."""
    
    print("🔍 Debugging Data Extraction")
    print("=" * 40)
    
    # Generate universal data
    adapter = AdaptiveDataAdapter()
    data = adapter.generate_universal_data('Pakistan Submarine Acquisition Analysis', {})
    
    print(f"📋 Universal data sections: {len(data)}")
    print(f"📋 Universal data keys: {list(data.keys())}")
    
    # Check executive summary data
    if 'executive_summary' in data:
        exec_data = data['executive_summary']
        print(f"\n📊 Executive Summary Data:")
        print(f"   Type: {type(exec_data)}")
        print(f"   Keys: {list(exec_data.keys())}")
        
        if 'executive_summary' in exec_data:
            inner_exec = exec_data['executive_summary']
            print(f"   Inner executive_summary type: {type(inner_exec)}")
            print(f"   Inner executive_summary keys: {list(inner_exec.keys()) if isinstance(inner_exec, dict) else 'N/A'}")
    
    # Test extraction
    print(f"\n🔧 Testing Data Extraction:")
    extracted = integrated_adaptive_modular_report_generator._extract_module_data(
        data, ['executive_summary']
    )
    
    print(f"   Extracted keys: {list(extracted.keys())}")
    
    if 'executive_summary' in extracted:
        exec_extracted = extracted['executive_summary']
        print(f"   Extracted executive_summary type: {type(exec_extracted)}")
        print(f"   Extracted executive_summary value: {exec_extracted}")

if __name__ == "__main__":
    debug_data_extraction()
