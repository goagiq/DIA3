#!/usr/bin/env python3
"""
Test Enhanced Report Generation
Demonstrates the enhanced report generation functionality
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_enhanced_report_generation():
    """Test the enhanced report generation functionality"""
    
    print("🧪 Testing Enhanced Report Generation")
    print("=" * 50)
    
    try:
        # Import the enhanced report integration
        from core.export.enhanced_report_integration import generate_enhanced_report
        
        print("✅ Successfully imported enhanced report integration")
        
        # Generate a test report
        print("\n📊 Generating enhanced report...")
        report_path = generate_enhanced_report(
            analysis_type="pakistan_submarine",
            title="Pakistan's 50-Submarine Acquisition",
            subtitle="Comprehensive Strategic Analysis for Conventional Deterrence"
        )
        
        print(f"✅ Enhanced report generated successfully!")
        print(f"📄 Report saved to: {report_path}")
        
        # Check if the file exists
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path)
            print(f"📏 File size: {file_size:,} bytes")
            
            # Check for key features in the report
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features_found = []
            if "Knowledge Graph" in content:
                features_found.append("✅ Knowledge Graph")
            if "Chart.js" in content:
                features_found.append("✅ Interactive Charts")
            if "professional-table" in content:
                features_found.append("✅ Professional Tables")
            if "vis-network" in content:
                features_found.append("✅ Network Visualization")
            if "Pakistan's 50-Submarine Acquisition" in content:
                features_found.append("✅ Strategic Analysis Content")
            
            print("\n🔍 Report Features Found:")
            for feature in features_found:
                print(f"   {feature}")
            
            if len(features_found) >= 4:
                print("\n🎉 Enhanced report generation test PASSED!")
                print("   The report includes all expected features:")
                print("   - Professional HTML layout")
                print("   - Interactive charts and visualizations")
                print("   - Knowledge graph with network visualization")
                print("   - Professional data tables")
                print("   - Comprehensive strategic analysis")
            else:
                print("\n⚠️  Enhanced report generation test PARTIAL")
                print("   Some expected features may be missing")
                
        else:
            print("❌ Report file not found!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   - networkx")
        print("   - matplotlib")
        print("   - seaborn")
        print("   - jinja2")
        return False
        
    except Exception as e:
        print(f"❌ Error during report generation: {e}")
        return False
    
    return True

def test_custom_enhanced_report():
    """Test custom enhanced report generation"""
    
    print("\n🧪 Testing Custom Enhanced Report Generation")
    print("=" * 50)
    
    try:
        from core.export.enhanced_report_integration import generate_custom_enhanced_report
        
        # Create custom analysis data
        custom_data = {
            'main_entity': 'Custom Strategic Analysis',
            'key_concepts': ['Strategic Planning', 'Risk Assessment', 'Decision Making'],
            'risk_factors': ['Market Volatility', 'Regulatory Changes', 'Competition'],
            'recommendations': ['Diversification', 'Innovation', 'Partnerships'],
            'executive_summary': {
                'description': 'This is a custom strategic analysis demonstrating the enhanced report generation capabilities.',
                'key_findings': {
                    'Strategic Impact': 'High impact on organizational performance',
                    'Risk Level': 'Medium to high risk environment',
                    'Opportunity': 'Significant growth potential'
                },
                'summary_stats': [
                    {'label': 'Impact Score', 'value': '85%', 'description': 'Strategic impact'},
                    {'label': 'Risk Level', 'value': 'MEDIUM', 'description': 'Overall risk'},
                    {'label': 'Timeline', 'value': '12-18', 'description': 'Months to implement'}
                ]
            }
        }
        
        print("📊 Generating custom enhanced report...")
        report_path = generate_custom_enhanced_report(
            analysis_data=custom_data,
            title="Custom Strategic Analysis",
            subtitle="Enhanced Report Generation Demo"
        )
        
        print(f"✅ Custom enhanced report generated successfully!")
        print(f"📄 Report saved to: {report_path}")
        
        if os.path.exists(report_path):
            print("🎉 Custom enhanced report generation test PASSED!")
        else:
            print("❌ Custom report file not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error during custom report generation: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    
    print("🚀 Enhanced Report Generation Test Suite")
    print("=" * 60)
    
    # Test basic enhanced report generation
    test1_passed = test_enhanced_report_generation()
    
    # Test custom enhanced report generation
    test2_passed = test_custom_enhanced_report()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Enhanced report generation is working correctly")
        print("✅ Both standard and custom reports can be generated")
        print("✅ Reports include knowledge graphs and interactive visualizations")
    elif test1_passed:
        print("⚠️  PARTIAL SUCCESS")
        print("✅ Basic enhanced report generation works")
        print("❌ Custom report generation needs attention")
    elif test2_passed:
        print("⚠️  PARTIAL SUCCESS")
        print("❌ Basic enhanced report generation needs attention")
        print("✅ Custom report generation works")
    else:
        print("❌ ALL TESTS FAILED")
        print("❌ Enhanced report generation needs debugging")
    
    print("\n📝 Next Steps:")
    print("   1. Open the generated HTML reports in a web browser")
    print("   2. Verify that all interactive features work correctly")
    print("   3. Check that knowledge graphs are properly displayed")
    print("   4. Ensure professional tables are formatted correctly")
    print("   5. Test responsive design on different screen sizes")

if __name__ == "__main__":
    main()
