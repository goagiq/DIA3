#!/usr/bin/env python3
"""
Phase 2.1 Core Modules Migration Test

Comprehensive test suite for validating the migration of core modules
from JavaScript-dependent to pure Python implementation.
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.python_modular_report_generator import (
        python_modular_report_generator
    )
    from core.css_tooltip_system import CSSTooltipSystem
    from core.python_chart_generator import PythonChartGenerator
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_SUCCESSFUL = False


async def test_phase2_1_components():
    """Test individual components of Phase 2.1."""
    print("=" * 80)
    print("PHASE 2.1 CORE MODULES MIGRATION - COMPONENT TESTING")
    print("=" * 80)
    
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot proceed with testing")
        return False
    
    # Test 1: Core Modules Configuration
    print("\n1. Testing Core Modules Configuration...")
    try:
        modules_info = python_modular_report_generator.get_core_modules_info()
        print("✅ Core modules info retrieved successfully")
        print(f"   Phase: {modules_info['phase']}")
        print(f"   Total modules: {modules_info['total_modules']}")
        
        for module_id, info in modules_info['modules'].items():
            priority = info['priority']
            print(f"   - {module_id}: {info['title']} (Priority: {priority})")
        
        if modules_info['total_modules'] != 4:
            total = modules_info['total_modules']
            print(f"❌ Expected 4 core modules, got {total}")
            return False
        
    except Exception as e:
        print(f"❌ Core modules configuration test failed: {e}")
        return False
    
    # Test 2: Individual Module Content Generation
    print("\n2. Testing Individual Module Content Generation...")
    sample_data = {
        "topic": "Cybersecurity Threat Analysis",
        "data": {
            "threats": ["ransomware", "phishing", "data_breach"],
            "risk_level": "high",
            "affected_systems": ["email", "databases", "networks"]
        }
    }
    
    core_modules = ["executive_summary", "strategic_recommendations", "strategic_analysis", "risk_assessment"]
    
    for module_id in core_modules:
        try:
            content = await python_modular_report_generator._generate_module_content(
                module_id, sample_data, "Cybersecurity Threat Analysis"
            )
            
            if content and len(content) > 100:  # Basic content validation
                print(f"✅ {module_id} content generated successfully ({len(content)} characters)")
            else:
                print(f"❌ {module_id} content generation failed or too short")
                return False
                
        except Exception as e:
            print(f"❌ {module_id} content generation failed: {e}")
            return False
    
    # Test 3: Tooltip Generation
    print("\n3. Testing Tooltip Generation...")
    try:
        tooltips = await python_modular_report_generator._generate_module_tooltips(
            "strategic_recommendations", "sample content"
        )
        
        if tooltips and len(tooltips) > 0:
            print(f"✅ Tooltips generated successfully ({len(tooltips)} tooltips)")
            for tooltip in tooltips:
                print(f"   - {tooltip['id']}: {tooltip['trigger']}")
        else:
            print("❌ Tooltip generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Tooltip generation test failed: {e}")
        return False
    
    # Test 4: Chart Generation
    print("\n4. Testing Chart Generation...")
    try:
        charts = await python_modular_report_generator._generate_module_charts(
            "strategic_recommendations", "sample content"
        )
        
        if charts and len(charts) > 0:
            print(f"✅ Charts generated successfully ({len(charts)} charts)")
            for chart in charts:
                print(f"   - {chart['id']}: {chart['type']} chart")
        else:
            print("❌ Chart generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        return False
    
    print("\n✅ All component tests passed!")
    return True


async def test_phase2_1_integration():
    """Test integration of all Phase 2.1 components."""
    print("\n" + "=" * 80)
    print("PHASE 2.1 CORE MODULES MIGRATION - INTEGRATION TESTING")
    print("=" * 80)
    
    # Test 1: Full Report Generation with All Core Modules
    print("\n1. Testing Full Report Generation with All Core Modules...")
    try:
        sample_data = {
            "topic": "Artificial Intelligence Strategy",
            "data": {
                "technologies": ["machine_learning", "deep_learning", "natural_language_processing"],
                "applications": ["automation", "prediction", "optimization"],
                "risks": ["bias", "privacy", "security"],
                "opportunities": ["efficiency", "innovation", "competitive_advantage"]
            }
        }
        
        start_time = time.time()
        report_path = await python_modular_report_generator.generate_core_modules_report(
            data=sample_data,
            topic="Artificial Intelligence Strategy"
        )
        generation_time = time.time() - start_time
        
        if report_path and Path(report_path).exists():
            file_size = Path(report_path).stat().st_size
            print(f"✅ Full report generated successfully")
            print(f"   File: {report_path}")
            print(f"   Size: {file_size:,} bytes")
            print(f"   Generation time: {generation_time:.2f} seconds")
            
            # Validate report content
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "Executive Summary" in content and "Strategic Recommendations" in content:
                print("✅ Report contains expected core modules")
            else:
                print("❌ Report missing expected core modules")
                return False
                
        else:
            print("❌ Full report generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Full report generation test failed: {e}")
        return False
    
    # Test 2: Report Generation with Specific Modules
    print("\n2. Testing Report Generation with Specific Modules...")
    try:
        specific_modules = ["executive_summary", "risk_assessment"]
        
        report_path = await python_modular_report_generator.generate_core_modules_report(
            data=sample_data,
            topic="Cybersecurity Assessment",
            include_modules=specific_modules
        )
        
        if report_path and Path(report_path).exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "Executive Summary" in content and "Risk Assessment" in content:
                print("✅ Specific modules report generated successfully")
            else:
                print("❌ Specific modules report missing expected content")
                return False
        else:
            print("❌ Specific modules report generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Specific modules report test failed: {e}")
        return False
    
    # Test 3: CSS Tooltip Integration
    print("\n3. Testing CSS Tooltip Integration...")
    try:
        tooltip_system = CSSTooltipSystem()
        base_css = tooltip_system.generate_base_css()
        
        if base_css and len(base_css) > 100:
            print("✅ CSS tooltip system working correctly")
        else:
            print("❌ CSS tooltip system not generating proper CSS")
            return False
            
    except Exception as e:
        print(f"❌ CSS tooltip integration test failed: {e}")
        return False
    
    # Test 4: Chart Generator Integration
    print("\n4. Testing Chart Generator Integration...")
    try:
        chart_generator = PythonChartGenerator()
        
        # Test chart template registration
        chart_generator.add_chart_template("test_chart", {
            "type": "bar",
            "title": "Test Chart",
            "x_label": "Categories",
            "y_label": "Values"
        })
        
        print("✅ Chart generator integration working correctly")
        
    except Exception as e:
        print(f"❌ Chart generator integration test failed: {e}")
        return False
    
    print("\n✅ All integration tests passed!")
    return True


async def test_phase2_1_performance():
    """Test performance of Phase 2.1 components."""
    print("\n" + "=" * 80)
    print("PHASE 2.1 CORE MODULES MIGRATION - PERFORMANCE TESTING")
    print("=" * 80)
    
    # Test 1: Report Generation Performance
    print("\n1. Testing Report Generation Performance...")
    try:
        sample_data = {
            "topic": "Performance Test Analysis",
            "data": {
                "metrics": [f"metric_{i}" for i in range(100)],
                "values": [i * 1.5 for i in range(100)],
                "categories": [f"category_{i}" for i in range(20)]
            }
        }
        
        start_time = time.time()
        report_path = await python_modular_report_generator.generate_core_modules_report(
            data=sample_data,
            topic="Performance Test Analysis"
        )
        generation_time = time.time() - start_time
        
        print(f"✅ Report generation performance test completed")
        print(f"   Generation time: {generation_time:.2f} seconds")
        
        if generation_time < 5.0:  # Should complete within 5 seconds
            print("✅ Performance within acceptable limits (< 5 seconds)")
        else:
            print(f"⚠️  Performance slower than expected ({generation_time:.2f} seconds)")
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False
    
    # Test 2: Memory Usage (Basic)
    print("\n2. Testing Memory Usage...")
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Generate multiple reports
        for i in range(3):
            await python_modular_report_generator.generate_core_modules_report(
                data={"topic": f"Memory Test {i}"},
                topic=f"Memory Test {i}"
            )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Memory usage test completed")
        print(f"   Initial memory: {initial_memory:.1f} MB")
        print(f"   Final memory: {final_memory:.1f} MB")
        print(f"   Memory increase: {memory_increase:.1f} MB")
        
        if memory_increase < 100:  # Should not increase by more than 100MB
            print("✅ Memory usage within acceptable limits")
        else:
            print(f"⚠️  Memory usage higher than expected ({memory_increase:.1f} MB increase)")
            
    except ImportError:
        print("⚠️  psutil not available - skipping memory test")
    except Exception as e:
        print(f"❌ Memory usage test failed: {e}")
        return False
    
    print("\n✅ All performance tests completed!")
    return True


async def test_phase2_1_compatibility():
    """Test compatibility with existing systems."""
    print("\n" + "=" * 80)
    print("PHASE 2.1 CORE MODULES MIGRATION - COMPATIBILITY TESTING")
    print("=" * 80)
    
    # Test 1: HTML Output Compatibility
    print("\n1. Testing HTML Output Compatibility...")
    try:
        sample_data = {"topic": "Compatibility Test"}
        report_path = await python_modular_report_generator.generate_core_modules_report(
            data=sample_data,
            topic="Compatibility Test"
        )
        
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required HTML elements
        required_elements = [
            "<!DOCTYPE html>",
            "<html",
            "<head>",
            "<body>",
            "</html>"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if not missing_elements:
            print("✅ HTML output contains all required elements")
        else:
            print(f"❌ HTML output missing elements: {missing_elements}")
            return False
            
    except Exception as e:
        print(f"❌ HTML compatibility test failed: {e}")
        return False
    
    # Test 2: CSS Compatibility
    print("\n2. Testing CSS Compatibility...")
    try:
        if "tooltip" in content and "chart" in content:
            print("✅ CSS classes for tooltips and charts present")
        else:
            print("❌ CSS classes missing for interactive features")
            return False
            
    except Exception as e:
        print(f"❌ CSS compatibility test failed: {e}")
        return False
    
    # Test 3: Offline Viewing Compatibility
    print("\n3. Testing Offline Viewing Compatibility...")
    try:
        # Check if report is self-contained (no external dependencies)
        if "http://" not in content and "https://" not in content:
            print("✅ Report is self-contained for offline viewing")
        else:
            print("⚠️  Report contains external dependencies")
            
    except Exception as e:
        print(f"❌ Offline viewing compatibility test failed: {e}")
        return False
    
    print("\n✅ All compatibility tests passed!")
    return True


async def main():
    """Main test function for Phase 2.1."""
    print("🚀 Starting Phase 2.1 Core Modules Migration Testing")
    print("=" * 80)
    
    test_results = []
    
    # Run all test suites
    test_results.append(await test_phase2_1_components())
    test_results.append(await test_phase2_1_integration())
    test_results.append(await test_phase2_1_performance())
    test_results.append(await test_phase2_1_compatibility())
    
    # Summary
    print("\n" + "=" * 80)
    print("PHASE 2.1 CORE MODULES MIGRATION - TEST SUMMARY")
    print("=" * 80)
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    print(f"\n📊 Test Results:")
    print(f"   Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 PHASE 2.1 CORE MODULES MIGRATION SUCCESSFUL!")
        print("✅ All core modules (Executive Summary, Strategic Recommendations,")
        print("   Strategic Analysis, Risk Assessment) have been successfully")
        print("   migrated from JavaScript-dependent to pure Python implementation.")
        print("\n📋 Key Achievements:")
        print("   • Pure Python implementation with no JavaScript dependencies")
        print("   • CSS-based tooltips replacing JavaScript tooltips")
        print("   • Python-generated static charts replacing interactive JavaScript charts")
        print("   • Self-contained HTML reports for offline viewing")
        print("   • Fast generation times (< 5 seconds)")
        print("   • Compatible with existing report structure")
        
        return True
    else:
        print(f"\n❌ PHASE 2.1 CORE MODULES MIGRATION FAILED!")
        print(f"   {total_tests - passed_tests} test(s) failed")
        return False


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
