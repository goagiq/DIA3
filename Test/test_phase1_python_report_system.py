"""
Test Phase 1: Python Report System Foundation

Tests the three core components:
1. Python Report Generator
2. CSS Tooltip System  
3. Python Chart Generator

Validates that all components work together without JavaScript dependencies.
"""

import asyncio
import sys
from pathlib import Path
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.python_report_generator import PythonReportGenerator, ReportConfig, ModuleData
from core.css_tooltip_system import CSSTooltipSystem, TooltipData, TooltipStyle
from core.python_chart_generator import PythonChartGenerator, ChartConfig, ChartData

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_phase1_components():
    """Test all Phase 1 components individually and together."""
    
    print("🚀 Testing Phase 1: Python Report System Foundation")
    print("=" * 60)
    
    # Test 1: CSS Tooltip System
    print("\n📋 Test 1: CSS Tooltip System")
    print("-" * 30)
    
    try:
        tooltip_system = CSSTooltipSystem()
        print("✅ CSS Tooltip System initialized")
        
        # Test tooltip data creation
        tooltip_data = TooltipData(
            title="Strategic Analysis",
            description="This analysis provides insights into strategic positioning.",
            source="DIA3 Analysis Engine",
            strategic_impact="High impact on decision making",
            recommendations="Consider implementing recommended actions",
            confidence="85%"
        )
        print("✅ Tooltip data created")
        
        # Test CSS generation
        modules_data = [{
            'id': 'test_module',
            'tooltip_data': {
                'test_tooltip': {
                    'title': 'Strategic Analysis',
                    'description': 'This analysis provides insights into strategic positioning.',
                    'position': 'top'
                }
            }
        }]
        
        css = tooltip_system.generate_css(modules_data)
        print(f"✅ CSS generated ({len(css)} characters)")
        
        # Test tooltip HTML creation
        tooltip_html = tooltip_system.create_tooltip_html(
            "test-tooltip", 
            tooltip_data, 
            "Strategic Analysis"
        )
        print(f"✅ Tooltip HTML created ({len(tooltip_html)} characters)")
        
    except Exception as e:
        print(f"❌ CSS Tooltip System test failed: {e}")
        return False
    
    # Test 2: Python Chart Generator
    print("\n📊 Test 2: Python Chart Generator")
    print("-" * 30)
    
    try:
        chart_generator = PythonChartGenerator()
        print("✅ Python Chart Generator initialized")
        
        # Test sample data creation
        sample_data = chart_generator.create_sample_data('line')
        print("✅ Sample chart data created")
        
        # Test chart configuration
        chart_config = ChartConfig(
            chart_type="line",
            title="Sample Line Chart",
            x_label="Time",
            y_label="Value"
        )
        print("✅ Chart configuration created")
        
        # Test chart data structure
        chart_data = ChartData(
            chart_id="test_chart",
            config=chart_config,
            data=sample_data
        )
        print("✅ Chart data structure created")
        
        # Test chart HTML generation
        chart_html = await chart_generator._generate_single_chart(chart_data)
        print(f"✅ Chart HTML generated ({len(chart_html)} characters)")
        
    except Exception as e:
        print(f"❌ Python Chart Generator test failed: {e}")
        return False
    
    # Test 3: Python Report Generator
    print("\n📄 Test 3: Python Report Generator")
    print("-" * 30)
    
    try:
        report_generator = PythonReportGenerator()
        print("✅ Python Report Generator initialized")
        
        # Test report configuration
        config = ReportConfig(
            title="Phase 1 Test Report",
            description="Testing the Python report system foundation",
            author="DIA3 Test System",
            version="1.0.0"
        )
        print("✅ Report configuration created")
        
        # Test module data creation
        module_data = [
            ModuleData(
                module_id="executive_summary",
                title="Executive Summary",
                content="This is a test executive summary module for Phase 1 validation.",
                tooltip_data={
                    "summary_tooltip": {
                        "title": "Executive Summary",
                        "description": "High-level overview of the analysis",
                        "position": "top"
                    }
                },
                chart_data={
                    "trend_chart": {
                        "type": "line",
                        "title": "Trend Analysis",
                        "data": sample_data
                    }
                }
            ),
            ModuleData(
                module_id="strategic_analysis",
                title="Strategic Analysis",
                content="This module contains strategic analysis with tooltips and charts.",
                tooltip_data={
                    "strategic_tooltip": {
                        "title": "Strategic Impact",
                        "description": "Analysis of strategic implications",
                        "position": "bottom"
                    }
                },
                chart_data={
                    "performance_chart": {
                        "type": "bar",
                        "title": "Performance Metrics",
                        "data": chart_generator.create_sample_data('bar')
                    }
                }
            )
        ]
        print("✅ Module data created")
        
        # Initialize components
        report_generator.initialize_components(tooltip_system, chart_generator)
        print("✅ Components initialized")
        
        # Test report generation
        result = await report_generator.generate_report(module_data, config)
        
        if result['success']:
            print(f"✅ Report generated successfully")
            print(f"   - Output: {result['output_path']}")
            print(f"   - Generation time: {result['generation_time_seconds']:.2f}s")
            print(f"   - File size: {result['file_size_bytes']:,} bytes")
            print(f"   - Modules processed: {result['modules_processed']}")
            print(f"   - Tooltips included: {result['tooltips_included']}")
            print(f"   - Charts included: {result['charts_included']}")
        else:
            print(f"❌ Report generation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Python Report Generator test failed: {e}")
        return False
    
    # Test 4: Integration Test
    print("\n🔗 Test 4: Integration Test")
    print("-" * 30)
    
    try:
        # Test that all components work together
        print("✅ All components initialized successfully")
        
        # Test generator info
        generator_info = report_generator.get_generator_info()
        print(f"✅ Generator info retrieved: {generator_info['name']} v{generator_info['version']}")
        
        # Test tooltip system info
        tooltip_info = tooltip_system.get_tooltip_styles_info()
        print(f"✅ Tooltip styles available: {len(tooltip_info['available_styles'])}")
        
        # Test chart generator info
        chart_info = chart_generator.get_chart_generator_info()
        print(f"✅ Chart types supported: {len(chart_info['supported_chart_types'])}")
        
        # Verify no JavaScript dependencies
        assert not generator_info['javascript_required'], "JavaScript should not be required"
        assert 'No JavaScript required' in tooltip_info['features'], "Tooltips should not require JavaScript"
        assert 'No JavaScript dependencies' in chart_info['features'], "Charts should not require JavaScript"
        
        print("✅ No JavaScript dependencies confirmed")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    
    print("\n🎉 Phase 1 Tests Completed Successfully!")
    print("=" * 60)
    print("✅ All foundation components working")
    print("✅ CSS tooltips functional")
    print("✅ Python charts generating")
    print("✅ Report generation working")
    print("✅ No JavaScript dependencies")
    print("✅ Ready for Phase 2: Module Migration")
    
    return True


async def test_performance():
    """Test performance with larger datasets."""
    
    print("\n⚡ Performance Test")
    print("-" * 30)
    
    try:
        # Create larger dataset
        large_modules = []
        for i in range(10):  # 10 modules
            module_data = ModuleData(
                module_id=f"module_{i}",
                title=f"Test Module {i}",
                content=f"This is test module {i} with substantial content. " * 10,  # Larger content
                tooltip_data={
                    f"tooltip_{i}": {
                        "title": f"Tooltip {i}",
                        "description": "Detailed tooltip information" * 5,
                        "position": "top"
                    }
                },
                chart_data={
                    f"chart_{i}": {
                        "type": "line",
                        "title": f"Chart {i}",
                        "data": {
                            'x': list(range(1, 101)),  # 100 data points
                            'y': [j * 2 + i for j in range(1, 101)]
                        }
                    }
                }
            )
            large_modules.append(module_data)
        
        # Test generation time
        import time
        start_time = time.time()
        
        report_generator = PythonReportGenerator()
        tooltip_system = CSSTooltipSystem()
        chart_generator = PythonChartGenerator()
        
        report_generator.initialize_components(tooltip_system, chart_generator)
        
        config = ReportConfig(
            title="Performance Test Report",
            description="Testing performance with larger datasets"
        )
        
        result = await report_generator.generate_report(large_modules, config)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        if result['success']:
            print(f"✅ Performance test completed")
            print(f"   - Total time: {total_time:.2f}s")
            print(f"   - Generation time: {result['generation_time_seconds']:.2f}s")
            print(f"   - File size: {result['file_size_bytes']:,} bytes")
            print(f"   - Modules: {result['modules_processed']}")
            
            # Performance criteria
            if total_time < 10:  # Should complete in under 10 seconds
                print("✅ Performance criteria met (< 10s)")
            else:
                print("⚠️ Performance slower than expected (> 10s)")
                
        else:
            print(f"❌ Performance test failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False
    
    return True


async def main():
    """Run all Phase 1 tests."""
    
    print("🧪 Phase 1: Python Report System Testing")
    print("Testing foundation components for JavaScript to Python migration")
    print("=" * 80)
    
    # Run component tests
    component_success = await test_phase1_components()
    
    if component_success:
        # Run performance test
        performance_success = await test_performance()
        
        if performance_success:
            print("\n🎯 Phase 1 Status: READY FOR PHASE 2")
            print("All foundation components are working correctly.")
            print("Ready to proceed with module migration.")
        else:
            print("\n⚠️ Phase 1 Status: PERFORMANCE ISSUES")
            print("Components work but performance needs optimization.")
    else:
        print("\n❌ Phase 1 Status: FAILED")
        print("Foundation components have issues that need to be resolved.")
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
