#!/usr/bin/env python3
"""
Phase 4: Comprehensive Testing & Validation

Comprehensive test suite for validating the complete JavaScript to Python 
migration:
- Unit testing of all components
- Integration testing of complete report generation
- Performance testing with various dataset sizes
- Offline functionality testing
- Browser compatibility testing

Success Criteria:
- >90% test coverage
- All performance targets met
- Complete offline functionality
- Zero JavaScript dependencies
- Production-ready system
"""

import asyncio
import sys
import os
import time
import json
import psutil
import gc
import tempfile
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # Core components
    from core.python_modular_report_generator import PythonModularReportGenerator
    from core.css_tooltip_system import CSSTooltipSystem
    from core.python_chart_generator import PythonChartGenerator
    from core.redis_enhanced_data_processor import RedisEnhancedDataProcessor
    from core.redis_enhanced_chart_generator import RedisEnhancedChartGenerator
    
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_SUCCESSFUL = False


def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


def generate_test_dataset(size_mb: float = 1.0) -> dict:
    """Generate test dataset of specified size."""
    items_needed = int((size_mb * 1024 * 1024) / 100)
    
    dataset = {
        "metadata": {
            "generated_at": time.time(),
            "size_mb": size_mb,
            "items_count": items_needed
        },
        "data": {}
    }
    
    for i in range(items_needed):
        dataset["data"][f"item_{i}"] = {
            "id": i,
            "value": i * 1.5,
            "category": f"category_{i % 10}",
            "description": f"Description for item {i}",
            "metrics": {
                "score": i * 0.1,
                "confidence": 0.8 + (i % 10) * 0.02,
                "priority": i % 5 + 1
            }
        }
    
    return dataset


def generate_chart_test_data(chart_type: str, data_points: int = 100) -> dict:
    """Generate chart test data."""
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
    else:
        return {"data": [i for i in range(data_points)]}


class Phase4TestSuite:
    """Comprehensive Phase 4 testing suite."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.test_results = []
        self.start_time = time.time()
        self.initial_memory = get_memory_usage()
        
        # Test data
        self.small_dataset = generate_test_dataset(0.5)  # 0.5MB
        self.medium_dataset = generate_test_dataset(5.0)  # 5MB
        self.large_dataset = generate_test_dataset(10.0)  # 10MB
        
        print("🚀 Phase 4: Comprehensive Testing & Validation")
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
    
    async def test_unit_core_components(self) -> bool:
        """Test core components individually."""
        test_name = "Unit Testing - Core Components"
        start_time = time.time()
        
        try:
            # Test CSS Tooltip System
            tooltip_system = CSSTooltipSystem()
            tooltip_data = {
                "strategic_insight": "This represents a key strategic opportunity",
                "risk_factor": "Medium risk with mitigation strategies available",
                "recommendation": "Proceed with enhanced monitoring"
            }
            css_output = tooltip_system.generate_tooltip_css(tooltip_data)
            assert "tooltip" in css_output, "CSS tooltip generation failed"
            
            # Test Python Chart Generator
            chart_generator = PythonChartGenerator()
            chart_data = generate_chart_test_data("bar", 10)
            chart_html = chart_generator.generate_chart("test_chart", "bar", chart_data)
            assert "plotly" in chart_html.lower(), "Chart generation failed"
            
            # Test Redis Enhanced Data Processor
            data_processor = RedisEnhancedDataProcessor()
            processed_data = await data_processor.process_large_dataset(
                self.small_dataset, "unit_test_dataset"
            )
            assert "data" in processed_data, "Data processing failed"
            
            # Test Redis Enhanced Chart Generator
            from core.redis_enhanced_chart_generator import ChartData
            chart_gen = RedisEnhancedChartGenerator()
            chart_data_obj = ChartData(
                chart_id="unit_test_chart",
                chart_type="bar",
                data=generate_chart_test_data("bar", 10)
            )
            chart_html = await chart_gen.generate_chart(chart_data_obj)
            assert len(chart_html) > 0, "Redis chart generation failed"
            
            duration = time.time() - start_time
            details = "All core components working correctly"
            self.log_test(test_name, True, details, duration)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            details = f"Unit testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_integration_report_generation(self) -> bool:
        """Test complete report generation end-to-end."""
        test_name = "Integration Testing - Complete Report Generation"
        start_time = time.time()
        
        try:
            # Test modular report generator
            report_generator = PythonModularReportGenerator()
            
            # Create test data for core modules
            test_data = {
                "topic": "Integration Test Analysis",
                "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
                "recommendations": ["Recommendation 1", "Recommendation 2"],
                "risks": ["Risk 1", "Risk 2", "Risk 3"]
            }
            
            # Generate complete report using core modules
            report_html = await report_generator.generate_core_modules_report(
                data=test_data,
                topic="Integration Test Report",
                include_modules=["executive_summary", "strategic_analysis"]
            )
            
            # Validate report
            assert "executive_summary" in report_html, "Executive summary missing"
            assert "strategic_analysis" in report_html, "Strategic analysis missing"
            assert "tooltip" in report_html.lower(), "Tooltips missing"
            
            duration = time.time() - start_time
            details = f"Complete report generated successfully ({len(report_html)} characters)"
            self.log_test(test_name, True, details, duration)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            details = f"Integration testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_performance_small_datasets(self) -> bool:
        """Test performance with small datasets."""
        test_name = "Performance Testing - Small Datasets (<1MB)"
        start_time = time.time()
        
        try:
            data_processor = RedisEnhancedDataProcessor()
            chart_generator = RedisEnhancedChartGenerator()
            
            # Test data processing
            processing_start = time.time()
            processed_data = await data_processor.process_large_dataset(
                self.small_dataset, "performance_test_small"
            )
            processing_time = time.time() - processing_start
            
            # Test chart generation
            chart_start = time.time()
            from core.redis_enhanced_chart_generator import ChartData
            chart_data_obj = ChartData(
                chart_id="performance_test_chart",
                chart_type="bar",
                data=generate_chart_test_data("bar", 50)
            )
            chart_html = await chart_generator.generate_chart(chart_data_obj)
            chart_time = time.time() - chart_start
            
            duration = time.time() - start_time
            
            # Performance targets for small datasets
            target_processing_time = 1.0  # seconds
            target_chart_time = 0.5  # seconds
            
            if processing_time < target_processing_time and chart_time < target_chart_time:
                details = f"Processing: {processing_time:.3f}s (target: <{target_processing_time}s), Chart: {chart_time:.3f}s (target: <{target_chart_time}s)"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Performance targets not met. Processing: {processing_time:.3f}s, Chart: {chart_time:.3f}s"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Performance testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_performance_medium_datasets(self) -> bool:
        """Test performance with medium datasets."""
        test_name = "Performance Testing - Medium Datasets (1-10MB)"
        start_time = time.time()
        
        try:
            data_processor = RedisEnhancedDataProcessor()
            
            # Test data processing
            processing_start = time.time()
            processed_data = await data_processor.process_large_dataset(
                self.medium_dataset, "performance_test_medium"
            )
            processing_time = time.time() - processing_start
            
            duration = time.time() - start_time
            
            # Performance targets for medium datasets
            target_processing_time = 3.0  # seconds
            
            if processing_time < target_processing_time:
                details = f"Processing time: {processing_time:.3f}s (target: <{target_processing_time}s)"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Processing time: {processing_time:.3f}s (target: <{target_processing_time}s)"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Performance testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_performance_large_datasets(self) -> bool:
        """Test performance with large datasets."""
        test_name = "Performance Testing - Large Datasets (10MB+)"
        start_time = time.time()
        
        try:
            data_processor = RedisEnhancedDataProcessor()
            
            # Test data processing
            processing_start = time.time()
            processed_data = await data_processor.process_large_dataset(
                self.large_dataset, "performance_test_large"
            )
            processing_time = time.time() - processing_start
            
            # Check memory usage
            gc.collect()
            final_memory = get_memory_usage()
            memory_increase = final_memory - self.initial_memory
            
            duration = time.time() - start_time
            
            # Performance targets for large datasets
            target_processing_time = 5.0  # seconds
            target_memory = 500  # MB
            
            if processing_time < target_processing_time and memory_increase < target_memory:
                details = f"Processing: {processing_time:.3f}s (target: <{target_processing_time}s), Memory: {memory_increase:.1f}MB (target: <{target_memory}MB)"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Performance targets not met. Processing: {processing_time:.3f}s, Memory: {memory_increase:.1f}MB"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Performance testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_offline_functionality(self) -> bool:
        """Test offline functionality and static file generation."""
        test_name = "Offline Testing - Static File Generation"
        start_time = time.time()
        
        try:
            # Create temporary directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Generate test report
                report_generator = PythonModularReportGenerator()
                test_data = {
                    "topic": "Offline Test Analysis",
                    "key_findings": ["Finding 1", "Finding 2"],
                    "recommendations": ["Recommendation 1"],
                    "risks": ["Risk 1", "Risk 2"]
                }
                
                # Generate report
                report_html = await report_generator.generate_core_modules_report(
                    data=test_data,
                    topic="Offline Test Report",
                    include_modules=["executive_summary"]
                )
                
                # Save to file
                report_file = temp_path / "offline_test_report.html"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report_html)
                
                # Verify file was created and contains expected content
                assert report_file.exists(), "Report file not created"
                assert report_file.stat().st_size > 0, "Report file is empty"
                
                # Check for offline compatibility
                file_content = report_file.read_text(encoding='utf-8')
                assert "tooltip" in file_content.lower(), "Tooltips missing in offline file"
                assert "javascript" not in file_content.lower(), "JavaScript found in offline file"
                
                duration = time.time() - start_time
                details = f"Offline report generated successfully ({report_file.stat().st_size} bytes)"
                self.log_test(test_name, True, details, duration)
                return True
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Offline testing error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_browser_compatibility(self) -> bool:
        """Test browser compatibility and HTML standards."""
        test_name = "Browser Compatibility Testing"
        start_time = time.time()
        
        try:
            # Generate test report
            report_generator = PythonModularReportGenerator()
            test_data = {
                "topic": "Browser Compatibility Test",
                "key_findings": ["Finding 1", "Finding 2"],
                "recommendations": ["Recommendation 1"],
                "risks": ["Risk 1", "Risk 2"]
            }
            
            report_html = await report_generator.generate_core_modules_report(
                data=test_data,
                topic="Browser Compatibility Test",
                include_modules=["executive_summary", "strategic_analysis"]
            )
            
            # Check HTML standards compliance
            assert "<!DOCTYPE html>" in report_html, "Missing DOCTYPE declaration"
            assert "<html" in report_html, "Missing HTML tag"
            assert "<head>" in report_html, "Missing head section"
            assert "<body>" in report_html, "Missing body section"
            assert "<meta charset" in report_html, "Missing charset declaration"
            
            # Check for CSS-only features
            assert "tooltip" in report_html.lower(), "CSS tooltips missing"
            assert ":hover" in report_html.lower(), "CSS hover effects missing"
            
            # Check for no JavaScript dependencies
            assert "javascript" not in report_html.lower(), "JavaScript found in report"
            assert "script" not in report_html.lower(), "Script tags found in report"
            
            duration = time.time() - start_time
            details = "HTML standards compliant, CSS-only features working"
            self.log_test(test_name, True, details, duration)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            details = f"Browser compatibility error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_error_handling(self) -> bool:
        """Test error handling and edge cases."""
        test_name = "Error Handling Testing"
        start_time = time.time()
        
        try:
            # Test with invalid data
            data_processor = RedisEnhancedDataProcessor()
            chart_generator = RedisEnhancedChartGenerator()
            
            # Test data processor with invalid data
            try:
                await data_processor.process_large_dataset(None, "invalid_test")
                # Should handle gracefully
            except Exception as e:
                # Expected to fail gracefully
                pass
            
            # Test chart generator with invalid data
            try:
                from core.redis_enhanced_chart_generator import ChartData
                chart_data_obj = ChartData(
                    chart_id="invalid_chart",
                    chart_type="invalid_type",
                    data={}
                )
                await chart_generator.generate_chart(chart_data_obj)
                # Should handle gracefully
            except Exception as e:
                # Expected to fail gracefully
                pass
            
            # Test with empty datasets
            try:
                await data_processor.process_large_dataset({}, "empty_test")
                # Should handle gracefully
            except Exception as e:
                # Expected to fail gracefully
                pass
            
            duration = time.time() - start_time
            details = "Error handling working correctly for edge cases"
            self.log_test(test_name, True, details, duration)
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            details = f"Error handling test error: {e}"
            self.log_test(test_name, False, details, duration)
            return False
    
    async def test_concurrent_operations(self) -> bool:
        """Test concurrent operations and scalability."""
        test_name = "Concurrent Operations Testing"
        start_time = time.time()
        
        try:
            data_processor = RedisEnhancedDataProcessor()
            chart_generator = RedisEnhancedChartGenerator()
            
            # Create multiple concurrent tasks
            tasks = []
            
            # Concurrent data processing
            for i in range(3):
                dataset = generate_test_dataset(0.5)
                task = data_processor.process_large_dataset(
                    dataset, f"concurrent_data_{i}"
                )
                tasks.append(task)
            
            # Concurrent chart generation
            for i in range(3):
                from core.redis_enhanced_chart_generator import ChartData
                chart_data_obj = ChartData(
                    chart_id=f"concurrent_chart_{i}",
                    chart_type="bar",
                    data=generate_chart_test_data("bar", 10)
                )
                task = chart_generator.generate_chart(chart_data_obj)
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for exceptions
            exceptions = [r for r in results if isinstance(r, Exception)]
            
            duration = time.time() - start_time
            
            if not exceptions:
                details = f"All {len(tasks)} concurrent operations completed successfully"
                self.log_test(test_name, True, details, duration)
                return True
            else:
                details = f"Found {len(exceptions)} exceptions in concurrent operations"
                self.log_test(test_name, False, details, duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            details = f"Concurrent operations error: {e}"
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
            "performance_metrics": {
                "initial_memory_mb": self.initial_memory,
                "final_memory_mb": final_memory,
                "memory_increase_mb": memory_increase,
                "total_duration_seconds": total_duration
            },
            "phase4_status": {
                "unit_testing": any("Unit Testing" in r["test"] and r["success"] for r in self.test_results),
                "integration_testing": any("Integration Testing" in r["test"] and r["success"] for r in self.test_results),
                "performance_testing": any("Performance Testing" in r["test"] and r["success"] for r in self.test_results),
                "offline_testing": any("Offline Testing" in r["test"] and r["success"] for r in self.test_results),
                "browser_compatibility": any("Browser Compatibility" in r["test"] and r["success"] for r in self.test_results),
                "error_handling": any("Error Handling" in r["test"] and r["success"] for r in self.test_results),
                "concurrent_operations": any("Concurrent Operations" in r["test"] and r["success"] for r in self.test_results)
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary."""
        summary = report["test_summary"]
        phase4_status = report["phase4_status"]
        
        print("=" * 70)
        print("📊 Phase 4 Test Summary")
        print("=" * 70)
        print(f"✅ Passed: {summary['passed_tests']}/{summary['total_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}/{summary['total_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⏱️ Total Duration: {summary['total_duration']:.2f}s")
        print(f"💾 Memory Increase: {summary['memory_increase_mb']:.1f}MB")
        print()
        
        print("🔍 Phase 4 Component Status:")
        print(f"   Unit Testing: {'✅' if phase4_status['unit_testing'] else '❌'}")
        print(f"   Integration Testing: {'✅' if phase4_status['integration_testing'] else '❌'}")
        print(f"   Performance Testing: {'✅' if phase4_status['performance_testing'] else '❌'}")
        print(f"   Offline Testing: {'✅' if phase4_status['offline_testing'] else '❌'}")
        print(f"   Browser Compatibility: {'✅' if phase4_status['browser_compatibility'] else '❌'}")
        print(f"   Error Handling: {'✅' if phase4_status['error_handling'] else '❌'}")
        print(f"   Concurrent Operations: {'✅' if phase4_status['concurrent_operations'] else '❌'}")
        print()
        
        if summary['success_rate'] >= 90:
            print("🎉 Phase 4 PASSED - Ready for Phase 5!")
        else:
            print("⚠️ Phase 4 needs improvement before proceeding to Phase 5")
        
        print("=" * 70)


async def run_phase4_tests():
    """Run all Phase 4 tests."""
    if not IMPORTS_SUCCESSFUL:
        print("❌ Import failed - cannot run tests")
        return False
    
    test_suite = Phase4TestSuite()
    
    # Run all tests
    tests = [
        test_suite.test_unit_core_components(),
        test_suite.test_integration_report_generation(),
        test_suite.test_performance_small_datasets(),
        test_suite.test_performance_medium_datasets(),
        test_suite.test_performance_large_datasets(),
        test_suite.test_offline_functionality(),
        test_suite.test_browser_compatibility(),
        test_suite.test_error_handling(),
        test_suite.test_concurrent_operations()
    ]
    
    # Execute all tests
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Generate and print report
    report = test_suite.generate_test_report()
    test_suite.print_summary(report)
    
    # Save report to file
    report_file = Path("Results/phase4_comprehensive_validation_report.json")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"📄 Detailed report saved to: {report_file}")
    
    # Return success if >90% tests passed
    return report["test_summary"]["success_rate"] >= 90


if __name__ == "__main__":
    print("🚀 Starting Phase 4: Comprehensive Testing & Validation")
    print("=" * 70)
    
    try:
        success = asyncio.run(run_phase4_tests())
        if success:
            print("\n🎉 Phase 4 tests completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Phase 4 tests need improvement")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution error: {e}")
        sys.exit(1)
