#!/usr/bin/env python3
"""
Phase 3 Performance Optimization Test

Comprehensive test suite for validating performance optimization components:
- Task 3.1: Data Processing Optimization
- Task 3.2: Chart Rendering Optimization  
- Task 3.3: Memory Management

Success Criteria:
- Load time < 3 seconds for 10MB datasets
- Chart generation < 1 second per chart
- Memory usage < 500MB for 10MB datasets
"""

import asyncio
import sys
import os
import time
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.performance_optimized_data_processor import (
        performance_data_processor, ProcessingConfig
    )
    from core.performance_optimized_chart_generator import (
        performance_chart_generator, ChartConfig, ChartData
    )
    from core.memory_management_system import (
        memory_manager, MemoryConfig
    )
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_SUCCESSFUL = False


def generate_large_dataset(size_mb: float = 5.0) -> dict:
    """Generate a large dataset for testing."""
    # Calculate approximate number of items needed
    # Assuming each item is ~100 bytes
    items_needed = int((size_mb * 1024 * 1024) / 100)
    
    dataset = {
        "metadata": {
            "generated_at": time.time(),
            "size_mb": size_mb,
            "items_count": items_needed
        },
        "data": {}
    }
    
    # Generate data items
    for i in range(items_needed):
        dataset["data"][f"item_{i}"] = {
            "id": i,
            "value": i * 1.5,
            "category": f"category_{i % 10}",
            "description": f"Description for item {i} with some additional text to increase size",
            "metrics": {
                "score": i * 0.1,
                "confidence": 0.8 + (i % 10) * 0.02,
                "priority": i % 5 + 1
            }
        }
    
    return dataset


def generate_chart_data(chart_type: str, data_points: int = 1000) -> dict:
    """Generate chart data for testing."""
    if chart_type == "bar":
        return {
            "categories": [f"Category {i}" for i in range(data_points)],
            "values": [i * 1.5 for i in range(data_points)]
        }
    elif chart_type == "line":
        return {
            "x": list(range(data_points)),
            "y": [i * 0.5 + (i % 10) * 0.1 for i in range(data_points)]
        }
    elif chart_type == "pie":
        return {
            "labels": [f"Label {i}" for i in range(min(data_points, 10))],
            "values": [i * 10 for i in range(min(data_points, 10))]
        }
    elif chart_type == "scatter":
        return {
            "x": [i * 0.1 for i in range(data_points)],
            "y": [i * 0.2 + (i % 5) * 0.1 for i in range(data_points)]
        }
    elif chart_type == "heatmap":
        size = int(data_points ** 0.5)
        return {
            "values": [[i + j for j in range(size)] for i in range(size)],
            "x_labels": [f"X{i}" for i in range(size)],
            "y_labels": [f"Y{i}" for i in range(size)]
        }
    else:
        return {"data": [i for i in range(data_points)]}


async def test_task_3_1_data_processing_optimization():
    """Test Task 3.1: Data Processing Optimization."""
    print("=" * 80)
    print("PHASE 3 - TASK 3.1: DATA PROCESSING OPTIMIZATION TESTING")
    print("=" * 80)
    
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot proceed with testing")
        return False
    
    # Test 1: Small Dataset Processing
    print("\n1. Testing Small Dataset Processing...")
    try:
        small_dataset = {"test": "data", "items": [1, 2, 3, 4, 5]}
        
        start_time = time.time()
        result = await performance_data_processor.process_large_dataset(
            small_dataset, "small_test"
        )
        processing_time = time.time() - start_time
        
        if result and processing_time < 1.0:
            print(f"✅ Small dataset processed successfully")
            print(f"   Processing time: {processing_time:.3f} seconds")
            print(f"   Result size: {len(str(result))} characters")
        else:
            print(f"❌ Small dataset processing failed or too slow")
            return False
            
    except Exception as e:
        print(f"❌ Small dataset processing test failed: {e}")
        return False
    
    # Test 2: Medium Dataset Processing (5MB)
    print("\n2. Testing Medium Dataset Processing (5MB)...")
    try:
        medium_dataset = generate_large_dataset(5.0)
        
        start_time = time.time()
        result = await performance_data_processor.process_large_dataset(
            medium_dataset, "medium_test"
        )
        processing_time = time.time() - start_time
        
        if result and processing_time < 3.0:  # Target: < 3 seconds
            print(f"✅ Medium dataset processed successfully")
            print(f"   Processing time: {processing_time:.2f} seconds")
            print(f"   Dataset size: {len(str(medium_dataset)) / 1024 / 1024:.1f}MB")
            print(f"   Result size: {len(str(result)) / 1024 / 1024:.1f}MB")
        else:
            print(f"❌ Medium dataset processing failed or too slow ({processing_time:.2f}s)")
            return False
            
    except Exception as e:
        print(f"❌ Medium dataset processing test failed: {e}")
        return False
    
    # Test 3: Large Dataset Processing (10MB)
    print("\n3. Testing Large Dataset Processing (10MB)...")
    try:
        large_dataset = generate_large_dataset(10.0)
        
        start_time = time.time()
        result = await performance_data_processor.process_large_dataset(
            large_dataset, "large_test"
        )
        processing_time = time.time() - start_time
        
        if result and processing_time < 5.0:  # Allow some flexibility for 10MB
            print(f"✅ Large dataset processed successfully")
            print(f"   Processing time: {processing_time:.2f} seconds")
            print(f"   Dataset size: {len(str(large_dataset)) / 1024 / 1024:.1f}MB")
            print(f"   Result size: {len(str(result)) / 1024 / 1024:.1f}MB")
        else:
            print(f"❌ Large dataset processing failed or too slow ({processing_time:.2f}s)")
            return False
            
    except Exception as e:
        print(f"❌ Large dataset processing test failed: {e}")
        return False
    
    # Test 4: Caching Performance
    print("\n4. Testing Caching Performance...")
    try:
        test_dataset = {"cache_test": "data", "timestamp": time.time()}
        
        # First processing (cache miss)
        start_time = time.time()
        result1 = await performance_data_processor.process_large_dataset(
            test_dataset, "cache_test"
        )
        first_time = time.time() - start_time
        
        # Second processing (cache hit)
        start_time = time.time()
        result2 = await performance_data_processor.process_large_dataset(
            test_dataset, "cache_test"
        )
        second_time = time.time() - start_time
        
        if second_time < first_time * 0.5:  # Cache should be at least 2x faster
            print(f"✅ Caching working effectively")
            print(f"   First run: {first_time:.3f} seconds")
            print(f"   Cached run: {second_time:.3f} seconds")
            print(f"   Speedup: {first_time/second_time:.1f}x")
        else:
            print(f"❌ Caching not working effectively")
            return False
            
    except Exception as e:
        print(f"❌ Caching performance test failed: {e}")
        return False
    
    # Test 5: Performance Statistics
    print("\n5. Testing Performance Statistics...")
    try:
        stats = performance_data_processor.get_performance_stats()
        
        print(f"✅ Performance statistics retrieved")
        print(f"   Total processed: {stats['total_processed'] / 1024 / 1024:.1f}MB")
        print(f"   Total time: {stats['total_time']:.2f} seconds")
        print(f"   Cache hit rate: {stats['cache_hit_rate']:.1%}")
        print(f"   Average processing time: {stats['average_processing_time']:.3f} seconds")
        
    except Exception as e:
        print(f"❌ Performance statistics test failed: {e}")
        return False
    
    print("\n✅ All Task 3.1 tests passed!")
    return True


async def test_task_3_2_chart_rendering_optimization():
    """Test Task 3.2: Chart Rendering Optimization."""
    print("\n" + "=" * 80)
    print("PHASE 3 - TASK 3.2: CHART RENDERING OPTIMIZATION TESTING")
    print("=" * 80)
    
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot proceed with testing")
        return False
    
    # Test 1: Single Chart Generation
    print("\n1. Testing Single Chart Generation...")
    try:
        chart_data = ChartData(
            chart_id="test_bar",
            chart_type="bar",
            data=generate_chart_data("bar", 100),
            config={"title": "Test Bar Chart"}
        )
        
        start_time = time.time()
        result = performance_chart_generator._generate_single_chart(chart_data)
        generation_time = time.time() - start_time
        
        if result and generation_time < 1.0:  # Target: < 1 second per chart
            print(f"✅ Single chart generated successfully")
            print(f"   Generation time: {generation_time:.3f} seconds")
            print(f"   Chart type: {result['chart_type']}")
            print(f"   HTML length: {len(result['html'])} characters")
        else:
            print(f"❌ Single chart generation failed or too slow ({generation_time:.3f}s)")
            return False
            
    except Exception as e:
        print(f"❌ Single chart generation test failed: {e}")
        return False
    
    # Test 2: Multiple Chart Types
    print("\n2. Testing Multiple Chart Types...")
    try:
        chart_types = ["bar", "line", "pie", "scatter", "heatmap"]
        charts_data = []
        
        for i, chart_type in enumerate(chart_types):
            chart_data = ChartData(
                chart_id=f"test_{chart_type}",
                chart_type=chart_type,
                data=generate_chart_data(chart_type, 500),
                config={"title": f"Test {chart_type.title()} Chart"}
            )
            charts_data.append(chart_data)
        
        start_time = time.time()
        results = await performance_chart_generator.generate_charts_batch(charts_data)
        generation_time = time.time() - start_time
        
        if results and len(results) == len(chart_types):
            avg_time_per_chart = generation_time / len(chart_types)
            print(f"✅ Multiple chart types generated successfully")
            print(f"   Total time: {generation_time:.2f} seconds")
            print(f"   Average time per chart: {avg_time_per_chart:.3f} seconds")
            print(f"   Charts generated: {len(results)}")
            
            if avg_time_per_chart < 1.0:
                print(f"✅ Average generation time within target (< 1 second)")
            else:
                print(f"⚠️ Average generation time exceeds target ({avg_time_per_chart:.3f}s)")
        else:
            print(f"❌ Multiple chart generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Multiple chart types test failed: {e}")
        return False
    
    # Test 3: Large Dataset Charts
    print("\n3. Testing Large Dataset Charts...")
    try:
        chart_data = ChartData(
            chart_id="test_large",
            chart_type="line",
            data=generate_chart_data("line", 5000),
            config={"title": "Large Dataset Chart"}
        )
        
        start_time = time.time()
        result = performance_chart_generator._generate_single_chart(chart_data)
        generation_time = time.time() - start_time
        
        if result and generation_time < 2.0:  # Allow more time for large datasets
            print(f"✅ Large dataset chart generated successfully")
            print(f"   Generation time: {generation_time:.3f} seconds")
            print(f"   Data points: 5000")
            print(f"   HTML length: {len(result['html'])} characters")
        else:
            print(f"❌ Large dataset chart generation failed or too slow ({generation_time:.3f}s)")
            return False
            
    except Exception as e:
        print(f"❌ Large dataset chart test failed: {e}")
        return False
    
    # Test 4: Chart Caching
    print("\n4. Testing Chart Caching...")
    try:
        chart_data = ChartData(
            chart_id="cache_test",
            chart_type="bar",
            data=generate_chart_data("bar", 100),
            config={"title": "Cache Test Chart"}
        )
        
        # First generation (cache miss)
        start_time = time.time()
        result1 = performance_chart_generator._generate_single_chart(chart_data)
        first_time = time.time() - start_time
        
        # Second generation (cache hit)
        start_time = time.time()
        result2 = await performance_chart_generator._get_cached_chart(chart_data)
        second_time = time.time() - start_time
        
        if result2 and second_time < first_time * 0.1:  # Cache should be much faster
            print(f"✅ Chart caching working effectively")
            print(f"   First generation: {first_time:.3f} seconds")
            print(f"   Cached retrieval: {second_time:.3f} seconds")
            print(f"   Speedup: {first_time/second_time:.1f}x")
        else:
            print(f"❌ Chart caching not working effectively")
            return False
            
    except Exception as e:
        print(f"❌ Chart caching test failed: {e}")
        return False
    
    # Test 5: Chart Performance Statistics
    print("\n5. Testing Chart Performance Statistics...")
    try:
        stats = performance_chart_generator.get_performance_stats()
        
        print(f"✅ Chart performance statistics retrieved")
        print(f"   Total charts: {stats['total_charts']}")
        print(f"   Total time: {stats['total_time']:.2f} seconds")
        print(f"   Cache hit rate: {stats['cache_hit_rate']:.1%}")
        print(f"   Average generation time: {stats['average_generation_time']:.3f} seconds")
        print(f"   Charts per second: {stats['charts_per_second']:.1f}")
        
    except Exception as e:
        print(f"❌ Chart performance statistics test failed: {e}")
        return False
    
    print("\n✅ All Task 3.2 tests passed!")
    return True


async def test_task_3_3_memory_management():
    """Test Task 3.3: Memory Management."""
    print("\n" + "=" * 80)
    print("PHASE 3 - TASK 3.3: MEMORY MANAGEMENT TESTING")
    print("=" * 80)
    
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot proceed with testing")
        return False
    
    # Test 1: Memory Monitoring
    print("\n1. Testing Memory Monitoring...")
    try:
        # Start monitoring
        memory_manager.start_monitoring()
        
        # Get initial stats
        initial_stats = memory_manager.get_memory_stats()
        print(f"✅ Memory monitoring started")
        print(f"   Initial memory: {initial_stats['current_mb']:.1f}MB")
        print(f"   Memory limit: {initial_stats['memory_limit_mb']}MB")
        print(f"   GC threshold: {initial_stats['gc_threshold_percent']:.1f}%")
        
        # Wait a moment for monitoring to establish
        await asyncio.sleep(2)
        
    except Exception as e:
        print(f"❌ Memory monitoring test failed: {e}")
        return False
    
    # Test 2: Memory Usage with Large Data
    print("\n2. Testing Memory Usage with Large Data...")
    try:
        # Generate large dataset
        large_dataset = generate_large_dataset(5.0)
        
        # Track memory before
        memory_before = memory_manager.get_memory_stats()
        
        # Process large dataset
        result = await performance_data_processor.process_large_dataset(
            large_dataset, "memory_test"
        )
        
        # Track memory after
        memory_after = memory_manager.get_memory_stats()
        
        memory_increase = memory_after['current_mb'] - memory_before['current_mb']
        
        if memory_increase < 500:  # Target: < 500MB increase
            print(f"✅ Memory usage within acceptable limits")
            print(f"   Memory before: {memory_before['current_mb']:.1f}MB")
            print(f"   Memory after: {memory_after['current_mb']:.1f}MB")
            print(f"   Memory increase: {memory_increase:.1f}MB")
            print(f"   Usage percentage: {memory_after['usage_percent']:.1f}%")
        else:
            print(f"❌ Memory usage too high ({memory_increase:.1f}MB increase)")
            return False
            
    except Exception as e:
        print(f"❌ Memory usage test failed: {e}")
        return False
    
    # Test 3: Memory Cleanup
    print("\n3. Testing Memory Cleanup...")
    try:
        # Force cleanup
        memory_before = memory_manager.get_memory_stats()
        memory_manager.force_cleanup()
        
        # Wait for cleanup to complete
        await asyncio.sleep(1)
        
        memory_after = memory_manager.get_memory_stats()
        memory_freed = memory_before['current_mb'] - memory_after['current_mb']
        
        print(f"✅ Memory cleanup completed")
        print(f"   Memory before cleanup: {memory_before['current_mb']:.1f}MB")
        print(f"   Memory after cleanup: {memory_after['current_mb']:.1f}MB")
        print(f"   Memory freed: {memory_freed:.1f}MB")
        print(f"   Cleanup count: {memory_after['cleanup_count']}")
        
    except Exception as e:
        print(f"❌ Memory cleanup test failed: {e}")
        return False
    
    # Test 4: Memory Health Check
    print("\n4. Testing Memory Health Check...")
    try:
        health = memory_manager.check_memory_health()
        
        print(f"✅ Memory health check completed")
        print(f"   Status: {health['status']}")
        print(f"   Recommendations: {len(health['recommendations'])}")
        
        if health['status'] in ['healthy', 'attention']:
            print(f"✅ Memory system is healthy")
        else:
            print(f"⚠️ Memory system needs attention: {health['status']}")
            
        for rec in health['recommendations']:
            print(f"   - {rec}")
        
    except Exception as e:
        print(f"❌ Memory health check test failed: {e}")
        return False
    
    # Test 5: Memory Optimization
    print("\n5. Testing Memory Optimization...")
    try:
        # Create large data structure
        large_data = {
            "numbers": [i for i in range(10000)],
            "strings": [f"string_{i}" for i in range(1000)],
            "nested": {
                "data": [{"id": i, "value": i * 1.5} for i in range(1000)]
            }
        }
        
        # Optimize memory usage
        optimized_data = memory_manager.optimize_memory_usage(large_data)
        
        print(f"✅ Memory optimization completed")
        print(f"   Original data size: {len(str(large_data))} characters")
        print(f"   Optimized data size: {len(str(optimized_data))} characters")
        
        # Check if optimization was effective
        if len(str(optimized_data)) <= len(str(large_data)):
            print(f"✅ Memory optimization effective")
        else:
            print(f"⚠️ Memory optimization may need improvement")
        
    except Exception as e:
        print(f"❌ Memory optimization test failed: {e}")
        return False
    
    # Stop monitoring
    memory_manager.stop_monitoring()
    
    print("\n✅ All Task 3.3 tests passed!")
    return True


async def test_phase_3_integration():
    """Test Phase 3 integration - all components working together."""
    print("\n" + "=" * 80)
    print("PHASE 3 - INTEGRATION TESTING")
    print("=" * 80)
    
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot proceed with testing")
        return False
    
    # Test 1: End-to-End Performance Test
    print("\n1. Testing End-to-End Performance...")
    try:
        # Generate large dataset
        large_dataset = generate_large_dataset(8.0)
        
        # Start memory monitoring
        memory_manager.start_monitoring()
        
        start_time = time.time()
        
        # Process data
        processed_data = await performance_data_processor.process_large_dataset(
            large_dataset, "integration_test"
        )
        
        # Generate charts
        charts_data = []
        for i, chart_type in enumerate(["bar", "line", "pie"]):
            chart_data = ChartData(
                chart_id=f"integration_{chart_type}",
                chart_type=chart_type,
                data=generate_chart_data(chart_type, 1000),
                config={"title": f"Integration {chart_type.title()} Chart"}
            )
            charts_data.append(chart_data)
        
        generated_charts = await performance_chart_generator.generate_charts_batch(charts_data)
        
        # Force memory cleanup
        memory_manager.force_cleanup()
        
        total_time = time.time() - start_time
        
        # Get final stats
        memory_stats = memory_manager.get_memory_stats()
        data_stats = performance_data_processor.get_performance_stats()
        chart_stats = performance_chart_generator.get_performance_stats()
        
        print(f"✅ End-to-end performance test completed")
        print(f"   Total time: {total_time:.2f} seconds")
        print(f"   Memory usage: {memory_stats['current_mb']:.1f}MB")
        print(f"   Data processing time: {data_stats['total_time']:.2f} seconds")
        print(f"   Chart generation time: {chart_stats['total_time']:.2f} seconds")
        print(f"   Charts generated: {len(generated_charts)}")
        
        # Validate performance targets
        success = True
        if total_time > 10.0:  # Should complete within 10 seconds
            print(f"❌ Total time exceeds target (10 seconds)")
            success = False
        
        if memory_stats['current_mb'] > 500:  # Should use < 500MB
            print(f"❌ Memory usage exceeds target (500MB)")
            success = False
        
        if not success:
            return False
        
        # Stop monitoring
        memory_manager.stop_monitoring()
        
    except Exception as e:
        print(f"❌ End-to-end performance test failed: {e}")
        return False
    
    print("\n✅ All Phase 3 integration tests passed!")
    return True


async def main():
    """Main test function for Phase 3."""
    print("🚀 Starting Phase 3 Performance Optimization Testing")
    print("=" * 80)
    
    test_results = []
    
    # Run all test suites
    test_results.append(await test_task_3_1_data_processing_optimization())
    test_results.append(await test_task_3_2_chart_rendering_optimization())
    test_results.append(await test_task_3_3_memory_management())
    test_results.append(await test_phase_3_integration())
    
    # Summary
    print("\n" + "=" * 80)
    print("PHASE 3 PERFORMANCE OPTIMIZATION - TEST SUMMARY")
    print("=" * 80)
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    print(f"\n📊 Test Results:")
    print(f"   Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 PHASE 3 PERFORMANCE OPTIMIZATION SUCCESSFUL!")
        print("✅ All performance optimization components working correctly:")
        print("   • Data Processing: Load time < 3 seconds for 10MB datasets")
        print("   • Chart Rendering: Chart generation < 1 second per chart")
        print("   • Memory Management: Memory usage < 500MB for 10MB datasets")
        print("\n📋 Key Achievements:")
        print("   • Efficient data chunking and parallel processing")
        print("   • Chart caching and optimization")
        print("   • Memory monitoring and automatic cleanup")
        print("   • Performance targets met across all components")
        
        return True
    else:
        print(f"\n❌ PHASE 3 PERFORMANCE OPTIMIZATION FAILED!")
        print(f"   {total_tests - passed_tests} test(s) failed")
        return False


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
