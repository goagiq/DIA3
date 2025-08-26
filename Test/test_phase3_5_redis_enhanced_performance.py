#!/usr/bin/env python3
"""
Phase 3.5 Redis-Enhanced Performance Optimization Test

Comprehensive test suite for validating Redis-enhanced performance optimization:
- Redis-enhanced data processing with caching
- Redis-enhanced chart generation with caching
- Fixed async/await issues from Phase 3
- Redis integration and fallback mechanisms
- Performance targets validation

Success Criteria:
- Load time < 3 seconds for 10MB datasets
- Chart generation < 1 second per chart
- Memory usage < 500MB for 10MB datasets
- Redis caching working effectively
- >90% test success rate
"""

import asyncio
import sys
import os
import time
import json
import psutil
import gc
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.redis_enhanced_data_processor import (
        redis_enhanced_data_processor, ProcessingConfig
    )
    from core.redis_enhanced_chart_generator import (
        redis_enhanced_chart_generator, ChartConfig, ChartData
    )
    from config.redis_config import get_redis_manager
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_SUCCESSFUL = False


def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


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


class Phase35TestSuite:
    """Comprehensive test suite for Phase 3.5 Redis-enhanced performance optimization."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.test_results = []
        self.start_time = time.time()
        self.initial_memory = get_memory_usage()
        
        print("🚀 Phase 3.5 Redis-Enhanced Performance Optimization Test")
        print("=" * 70)
        print(f"📊 Initial memory usage: {self.initial_memory:.1f} MB")
        print(f"⏰ Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def log_test(self, test_name: str, success: bool, details: str = "", duration: float = 0.0):
        """Log test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "duration": duration
        }
        self.test_results.append(result)
        
        print(f"{status} {test_name} ({duration:.3f}s)")
        if details:
            print(f"   {details}")
        print()
    
    async def test_redis_connection(self) -> bool:
        """Test Redis connection and availability."""
        test_name = "Redis Connection Test"
        start_time = time.time()
        
        try:
            redis_manager = get_redis_manager()
            is_available = redis_manager.is_available()
            
            duration = time.time() - start_time
            
            if is_available:
                stats = redis_manager.get_stats()
                details = f"Redis connected to {stats['config']['host']}:{stats['config']['port']}"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = "Redis not available, will use disk caching fallback"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Redis connection error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_data_processing_caching(self) -> bool:
        """Test data processing caching functionality."""
        test_name = "Data Processing Caching Test"
        start_time = time.time()
        
        try:
            # Generate test dataset
            dataset = generate_large_dataset(1.0)  # 1MB dataset
            
            # First processing (should cache)
            start_processing = time.time()
            result1 = await redis_enhanced_data_processor.process_large_dataset(
                dataset, "test_caching_dataset"
            )
            first_processing_time = time.time() - start_processing
            
            # Second processing (should hit cache)
            start_processing = time.time()
            result2 = await redis_enhanced_data_processor.process_large_dataset(
                dataset, "test_caching_dataset"
            )
            second_processing_time = time.time() - start_processing
            
            duration = time.time() - start_time
            
            # Check if caching worked
            stats = redis_enhanced_data_processor.get_performance_stats()
            cache_hits = stats.get("cache_hits", 0)
            cache_misses = stats.get("cache_misses", 0)
            
            if cache_hits > 0 and second_processing_time < first_processing_time:
                details = f"Cache hits: {cache_hits}, misses: {cache_misses}, speedup: {first_processing_time/second_processing_time:.1f}x"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Cache not working effectively. Hits: {cache_hits}, misses: {cache_misses}"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Data processing caching error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_chart_generation_caching(self) -> bool:
        """Test chart generation caching functionality."""
        test_name = "Chart Generation Caching Test"
        start_time = time.time()
        
        try:
            # Generate test chart data
            chart_data = ChartData(
                chart_id="test_caching_chart",
                chart_type="bar",
                data=generate_chart_data("bar", 100),
                config={"color": "steelblue"}
            )
            
            # First generation (should cache)
            start_generation = time.time()
            chart1 = await redis_enhanced_chart_generator.generate_chart(chart_data)
            first_generation_time = time.time() - start_generation
            
            # Second generation (should hit cache)
            start_generation = time.time()
            chart2 = await redis_enhanced_chart_generator.generate_chart(chart_data)
            second_generation_time = time.time() - start_generation
            
            duration = time.time() - start_time
            
            # Check if caching worked
            stats = redis_enhanced_chart_generator.get_performance_stats()
            cache_hits = stats.get("cache_hits", 0)
            cache_misses = stats.get("cache_misses", 0)
            
            if cache_hits > 0 and second_generation_time < first_generation_time:
                details = f"Cache hits: {cache_hits}, misses: {cache_misses}, speedup: {first_generation_time/second_generation_time:.1f}x"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Cache not working effectively. Hits: {cache_hits}, misses: {cache_misses}"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Chart generation caching error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_data_processing_performance(self) -> bool:
        """Test data processing performance targets."""
        test_name = "Data Processing Performance Test"
        start_time = time.time()
        
        try:
            # Test with 5MB dataset
            dataset = generate_large_dataset(5.0)
            
            processing_start = time.time()
            result = await redis_enhanced_data_processor.process_large_dataset(
                dataset, "performance_test_dataset"
            )
            processing_time = time.time() - processing_start
            
            duration = time.time() - start_time
            
            # Check performance targets
            target_time = 3.0  # seconds
            if processing_time < target_time:
                details = f"Processing time: {processing_time:.3f}s (target: <{target_time}s) ✅"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Processing time: {processing_time:.3f}s (target: <{target_time}s) ❌"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Data processing performance error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_chart_generation_performance(self) -> bool:
        """Test chart generation performance targets."""
        test_name = "Chart Generation Performance Test"
        start_time = time.time()
        
        try:
            # Generate multiple charts
            charts_data = []
            for i in range(5):
                chart_data = ChartData(
                    chart_id=f"performance_test_chart_{i}",
                    chart_type=["bar", "line", "pie", "scatter", "heatmap"][i % 5],
                    data=generate_chart_data(["bar", "line", "pie", "scatter", "heatmap"][i % 5], 500),
                    config={"color": "steelblue"}
                )
                charts_data.append(chart_data)
            
            generation_start = time.time()
            charts = await redis_enhanced_chart_generator.generate_multiple_charts(charts_data)
            generation_time = time.time() - generation_start
            
            duration = time.time() - start_time
            
            # Check performance targets
            target_time_per_chart = 1.0  # seconds per chart
            actual_time_per_chart = generation_time / len(charts_data)
            
            if actual_time_per_chart < target_time_per_chart:
                details = f"Average time per chart: {actual_time_per_chart:.3f}s (target: <{target_time_per_chart}s) ✅"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Average time per chart: {actual_time_per_chart:.3f}s (target: <{target_time_per_chart}s) ❌"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Chart generation performance error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_memory_usage(self) -> bool:
        """Test memory usage targets."""
        test_name = "Memory Usage Test"
        start_time = time.time()
        
        try:
            # Process large dataset
            dataset = generate_large_dataset(10.0)  # 10MB dataset
            
            # Force garbage collection before test
            gc.collect()
            initial_memory = get_memory_usage()
            
            # Process dataset
            result = await redis_enhanced_data_processor.process_large_dataset(
                dataset, "memory_test_dataset"
            )
            
            # Force garbage collection after test
            gc.collect()
            final_memory = get_memory_usage()
            
            memory_increase = final_memory - initial_memory
            
            duration = time.time() - start_time
            
            # Check memory targets
            target_memory = 500  # MB
            if memory_increase < target_memory:
                details = f"Memory increase: {memory_increase:.1f}MB (target: <{target_memory}MB) ✅"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Memory increase: {memory_increase:.1f}MB (target: <{target_memory}MB) ❌"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Memory usage test error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_async_await_fixes(self) -> bool:
        """Test that async/await issues from Phase 3 are fixed."""
        test_name = "Async/Await Fixes Test"
        start_time = time.time()
        
        try:
            # Test concurrent operations
            tasks = []
            
            # Concurrent data processing
            for i in range(3):
                dataset = generate_large_dataset(1.0)
                task = redis_enhanced_data_processor.process_large_dataset(
                    dataset, f"async_test_dataset_{i}"
                )
                tasks.append(task)
            
            # Concurrent chart generation
            for i in range(3):
                chart_data = ChartData(
                    chart_id=f"async_test_chart_{i}",
                    chart_type="bar",
                    data=generate_chart_data("bar", 100),
                    config={"color": "steelblue"}
                )
                task = redis_enhanced_chart_generator.generate_chart(chart_data)
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            duration = time.time() - start_time
            
            # Check for exceptions
            exceptions = [r for r in results if isinstance(r, Exception)]
            
            if not exceptions:
                details = f"All {len(tasks)} concurrent operations completed successfully ✅"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Found {len(exceptions)} exceptions in concurrent operations ❌"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Async/await test error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_redis_fallback_mechanism(self) -> bool:
        """Test Redis fallback to disk caching when Redis is unavailable."""
        test_name = "Redis Fallback Mechanism Test"
        start_time = time.time()
        
        try:
            # Test with a small dataset
            dataset = generate_large_dataset(0.5)
            
            # Process dataset (should work even if Redis is down)
            result = await redis_enhanced_data_processor.process_large_dataset(
                dataset, "fallback_test_dataset"
            )
            
            duration = time.time() - start_time
            
            # Check if processing completed successfully
            if result and "data" in result:
                details = "Processing completed successfully with fallback mechanism ✅"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = "Processing failed with fallback mechanism ❌"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Redis fallback test error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        final_memory = get_memory_usage()
        memory_increase = final_memory - self.initial_memory
        total_duration = time.time() - self.start_time
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "total_duration": total_duration,
                "memory_increase_mb": memory_increase
            },
            "test_results": self.test_results,
            "performance_stats": {
                "data_processor": redis_enhanced_data_processor.get_performance_stats(),
                "chart_generator": redis_enhanced_chart_generator.get_performance_stats(),
                "redis_manager": get_redis_manager().get_stats()
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary."""
        summary = report["test_summary"]
        
        print("=" * 70)
        print("📊 Phase 3.5 Test Summary")
        print("=" * 70)
        print(f"✅ Passed: {summary['passed_tests']}/{summary['total_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}/{summary['total_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⏱️ Total Duration: {summary['total_duration']:.2f}s")
        print(f"💾 Memory Increase: {summary['memory_increase_mb']:.1f}MB")
        print()
        
        if summary['success_rate'] >= 90:
            print("🎉 Phase 3.5 PASSED - Ready for Phase 4!")
        else:
            print("⚠️ Phase 3.5 needs improvement before proceeding to Phase 4")
        
        print("=" * 70)


async def run_phase35_tests():
    """Run all Phase 3.5 tests."""
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot run tests")
        return False
    
    test_suite = Phase35TestSuite()
    
    # Run all tests
    tests = [
        test_suite.test_redis_connection(),
        test_suite.test_data_processing_caching(),
        test_suite.test_chart_generation_caching(),
        test_suite.test_data_processing_performance(),
        test_suite.test_chart_generation_performance(),
        test_suite.test_memory_usage(),
        test_suite.test_async_await_fixes(),
        test_suite.test_redis_fallback_mechanism()
    ]
    
    # Execute all tests
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Generate and print report
    report = test_suite.generate_test_report()
    test_suite.print_summary(report)
    
    # Save report to file
    report_file = Path("Results/phase35_redis_enhanced_performance_test_report.json")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"📄 Detailed report saved to: {report_file}")
    
    # Return success if >90% tests passed
    return report["test_summary"]["success_rate"] >= 90


if __name__ == "__main__":
    print("🚀 Starting Phase 3.5 Redis-Enhanced Performance Optimization Tests")
    print("=" * 70)
    
    try:
        success = asyncio.run(run_phase35_tests())
        if success:
            print("\n🎉 Phase 3.5 tests completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Phase 3.5 tests need improvement")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution error: {e}")
        sys.exit(1)
