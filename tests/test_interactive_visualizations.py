#!/usr/bin/env python3
"""
Comprehensive test for interactive visualizations in enhanced HTML reports
"""

import re
import json
from pathlib import Path

def test_html_file(file_path):
    """Test a single HTML file for interactive visualization features."""
    print(f"\n🔍 Testing: {file_path}")
    print("-" * 60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic file info
        print(f"📊 File size: {len(content)} bytes")
        
        # Test 1: External libraries
        libraries = {
            'Chart.js': 'https://cdn.jsdelivr.net/npm/chart.js',
            'D3.js': 'https://d3js.org/d3.v7.min.js',
            'Plotly.js': 'https://cdn.jsdelivr.net/npm/plotly.js-dist@2.27.0/plotly.min.js'
        }
        
        print("\n📚 External Libraries:")
        for lib_name, lib_url in libraries.items():
            if lib_url in content:
                print(f"  ✅ {lib_name}")
            else:
                print(f"  ❌ {lib_name}")
        
        # Test 2: Chart containers and canvas elements
        canvas_count = content.count('<canvas')
        chart_container_count = content.count('chart-container')
        
        print(f"\n🎨 Chart Elements:")
        print(f"  📊 Canvas elements: {canvas_count}")
        print(f"  📦 Chart containers: {chart_container_count}")
        
        # Test 3: JavaScript Chart constructor calls
        chart_calls = re.findall(r'const.*Chart.*=.*new Chart\(.*?\);', content, re.DOTALL)
        print(f"\n⚡ Chart Constructor Calls:")
        print(f"  🔢 Total calls: {len(chart_calls)}")
        
        # Test 4: Variable name validation
        invalid_vars = [call for call in chart_calls if 'section-' in call]
        valid_vars = [call for call in chart_calls if 'section_' in call]
        
        print(f"  ❌ Invalid variable names (with hyphens): {len(invalid_vars)}")
        print(f"  ✅ Valid variable names (with underscores): {len(valid_vars)}")
        
        if invalid_vars:
            print(f"  ⚠️  First invalid call: {invalid_vars[0][:100]}...")
        if valid_vars:
            print(f"  ✅ First valid call: {valid_vars[0][:100]}...")
        
        # Test 5: Chart data validation
        chart_data_count = content.count('"datasets":')
        chart_labels_count = content.count('"labels":')
        
        print(f"\n📈 Chart Data:")
        print(f"  🏷️  Labels found: {chart_labels_count}")
        print(f"  📊 Datasets found: {chart_data_count}")
        
        # Test 6: Advanced tooltips
        tooltip_features = {
            'Enhanced tooltip HTML': 'enhanced-tooltip',
            'Tooltip JavaScript data': 'tooltipData',
            'Tooltip functions': 'showTooltip',
            'Multiple sources': '📚',
            'Internal DIA3 sources': 'Source: DIA3 -',
            'External sources': 'Source: ',
            'Autoscroll prevention': 'scroll-behavior: auto'
        }
        
        print(f"\n💡 Advanced Tooltips:")
        for feature_name, feature_check in tooltip_features.items():
            if feature_check in content:
                print(f"  ✅ {feature_name}")
            else:
                print(f"  ❌ {feature_name}")
        
        # Test 7: JavaScript syntax validation
        js_syntax_issues = []
        
        # Check for common JavaScript syntax errors
        if 'const section-' in content:
            js_syntax_issues.append("Invalid variable names with hyphens")
        
        if 'getElementById(\'section-1Chart\')' in content and 'section_1ChartCtx' in content:
            js_syntax_issues.append("Mismatch between element ID and variable name")
        
        print(f"\n🔧 JavaScript Syntax:")
        if js_syntax_issues:
            for issue in js_syntax_issues:
                print(f"  ❌ {issue}")
        else:
            print(f"  ✅ No syntax issues detected")
        
        # Test 8: Interactive features
        interactive_features = {
            'Mouse event listeners': 'addEventListener',
            'Hover effects': 'mouseenter',
            'Smooth scrolling': 'scrollIntoView',
            'Chart.js configuration': 'Chart.defaults'
        }
        
        print(f"\n🖱️ Interactive Features:")
        for feature_name, feature_check in interactive_features.items():
            if feature_check in content:
                print(f"  ✅ {feature_name}")
            else:
                print(f"  ❌ {feature_name}")
        
        # Overall assessment
        print(f"\n📋 Overall Assessment:")
        if len(chart_calls) > 0 and len(invalid_vars) == 0 and len(valid_vars) > 0:
            print(f"  🎉 EXCELLENT: Interactive visualizations should work properly!")
        elif len(chart_calls) > 0 and len(invalid_vars) > 0:
            print(f"  ⚠️  WARNING: Charts may not render due to JavaScript syntax errors")
        elif len(chart_calls) == 0:
            print(f"  ❌ ERROR: No interactive charts found")
        else:
            print(f"  🤔 UNKNOWN: Mixed results, manual testing recommended")
        
        return len(invalid_vars) == 0 and len(valid_vars) > 0
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False

def main():
    """Test all recent HTML files."""
    print("🚀 Comprehensive Interactive Visualization Test")
    print("=" * 70)
    
    # Find recent HTML files
    results_dir = Path("Results")
    html_files = list(results_dir.glob("*.html"))
    
    # Sort by modification time (most recent first)
    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Test the 5 most recent files
    recent_files = html_files[:5]
    
    print(f"📁 Found {len(html_files)} HTML files, testing {len(recent_files)} most recent:")
    
    working_files = []
    for file_path in recent_files:
        if test_html_file(file_path):
            working_files.append(file_path)
    
    print(f"\n🎯 Summary:")
    print(f"  📊 Files tested: {len(recent_files)}")
    print(f"  ✅ Working files: {len(working_files)}")
    print(f"  ❌ Non-working files: {len(recent_files) - len(working_files)}")
    
    if working_files:
        print(f"\n🎉 Recommended files to open in browser:")
        for file_path in working_files[:3]:  # Show top 3
            print(f"  📄 {file_path}")
    
    print(f"\n💡 To test interactivity:")
    print(f"  1. Open a working file in your browser")
    print(f"  2. Hover over sections to see advanced tooltips")
    print(f"  3. Check that charts render properly")
    print(f"  4. Verify no JavaScript errors in browser console")

if __name__ == "__main__":
    main()
