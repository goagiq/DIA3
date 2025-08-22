#!/usr/bin/env python3
"""
Test script for Enhanced Fetch Service and Sequential Thinking Service

This script demonstrates the robust timeout and error handling capabilities
of the new fetch services.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_basic_fetch():
    """Test basic fetch functionality."""
    print("🧪 Testing Basic Fetch Functionality...")
    
    try:
        from src.core.fetch_service import fetch_url_safe
        
        # Test successful fetch
        result = await fetch_url_safe("https://httpbin.org/json")
        if result.success:
            print("✅ Basic fetch successful")
            print(f"   Status: {result.status_code}")
            print(f"   Response time: {result.response_time:.2f}s")
        else:
            print(f"❌ Basic fetch failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Basic fetch test failed: {e}")
        return False
    
    return True

async def test_timeout_handling():
    """Test timeout handling."""
    print("\n⏰ Testing Timeout Handling...")
    
    try:
        from src.core.fetch_service import EnhancedFetchService, FetchConfig
        
        # Create service with very short timeout
        config = FetchConfig(timeout=0.1)  # 100ms timeout
        service = EnhancedFetchService(config)
        
        # Test timeout with a slow endpoint
        result = await service.fetch_url("https://httpbin.org/delay/1")
        
        if not result.success and "timeout" in result.error_message.lower():
            print("✅ Timeout handling working correctly")
            print(f"   Error: {result.error_message}")
        else:
            print(f"❌ Timeout handling failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Timeout test failed: {e}")
        return False
    
    return True

async def test_circuit_breaker():
    """Test circuit breaker functionality."""
    print("\n🔌 Testing Circuit Breaker...")
    
    try:
        from src.core.fetch_service import EnhancedFetchService, FetchConfig
        
        # Create service with low circuit breaker threshold
        config = FetchConfig(
            circuit_breaker_threshold=2,
            circuit_breaker_timeout=10.0
        )
        service = EnhancedFetchService(config)
        
        # Try to fetch from a non-existent URL multiple times
        for i in range(3):
            result = await service.fetch_url("https://this-url-does-not-exist-12345.com")
            print(f"   Attempt {i+1}: {'Failed' if not result.success else 'Success'}")
            
            if i == 2 and "circuit breaker" in result.error_message.lower():
                print("✅ Circuit breaker working correctly")
                return True
        
        print("❌ Circuit breaker not working as expected")
        return False
        
    except Exception as e:
        print(f"❌ Circuit breaker test failed: {e}")
        return False

async def test_fallback_urls():
    """Test fallback URL functionality."""
    print("\n🔄 Testing Fallback URLs...")
    
    try:
        from src.core.fetch_service import fetch_with_fallback_safe
        
        # Test with one failing URL and one working URL
        result = await fetch_with_fallback_safe(
            primary_url="https://this-url-does-not-exist-12345.com",
            fallback_urls=["https://httpbin.org/json"]
        )
        
        if result.success:
            print("✅ Fallback URL functionality working")
            print(f"   Final URL: {result.url}")
            print(f"   Status: {result.status_code}")
        else:
            print(f"❌ Fallback URL test failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Fallback URL test failed: {e}")
        return False
    
    return True

async def test_multiple_urls():
    """Test concurrent multiple URL fetching."""
    print("\n📡 Testing Multiple URLs...")
    
    try:
        from src.core.fetch_service import fetch_multiple_urls_safe
        
        urls = [
            "https://httpbin.org/json",
            "https://httpbin.org/html",
            "https://httpbin.org/xml",
            "https://this-url-does-not-exist-12345.com"  # This will fail
        ]
        
        results = await fetch_multiple_urls_safe(urls, max_concurrent=2)
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        print(f"✅ Multiple URLs test completed")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        
        if successful > 0:
            return True
        else:
            print("❌ No URLs succeeded")
            return False
            
    except Exception as e:
        print(f"❌ Multiple URLs test failed: {e}")
        return False

async def test_sequential_thinking():
    """Test sequential thinking service."""
    print("\n🧠 Testing Sequential Thinking Service...")
    
    try:
        from src.core.sequential_thinking_service import analyze_sequential_thinking_safe
        
        # Test sequential thinking with timeout
        result = await analyze_sequential_thinking_safe(
            scenario="Test scenario for timeout handling",
            steps=3,
            iterations=5,
            urls=["https://httpbin.org/json"]
        )
        
        if result.success:
            print("✅ Sequential thinking completed successfully")
            print(f"   Steps completed: {len(result.steps_completed)}")
            print(f"   Duration: {result.total_duration:.2f}s")
            print(f"   Conclusion: {result.final_conclusion}")
        else:
            print("❌ Sequential thinking failed")
            print(f"   Errors: {result.error_messages}")
            return False
            
    except Exception as e:
        print(f"❌ Sequential thinking test failed: {e}")
        return False
    
    return True

async def test_sequential_thinking_timeout():
    """Test sequential thinking timeout handling."""
    print("\n⏰ Testing Sequential Thinking Timeout...")
    
    try:
        from src.core.sequential_thinking_service import (
            SequentialThinkingService, SequentialThinkingConfig
        )
        
        # Create service with very short timeout
        config = SequentialThinkingConfig(
            max_total_time=1.0,  # 1 second total timeout
            step_timeout=0.5     # 500ms per step
        )
        service = SequentialThinkingService(config)
        
        # Test with a scenario that should timeout
        result = await service.analyze_sequential_thinking(
            scenario="Test timeout scenario",
            steps=5,  # More steps than time allows
            iterations=10
        )
        
        if not result.success and "timed out" in result.error_messages[0].lower():
            print("✅ Sequential thinking timeout working correctly")
            print(f"   Error: {result.error_messages[0]}")
        else:
            print(f"❌ Sequential thinking timeout failed: {result.error_messages}")
            return False
            
    except Exception as e:
        print(f"❌ Sequential thinking timeout test failed: {e}")
        return False
    
    return True

async def test_service_statistics():
    """Test service statistics and monitoring."""
    print("\n📊 Testing Service Statistics...")
    
    try:
        from src.core.fetch_service import get_fetch_service
        from src.core.sequential_thinking_service import get_sequential_thinking_service
        
        # Get services
        fetch_service = await get_fetch_service()
        thinking_service = await get_sequential_thinking_service()
        
        # Get statistics
        fetch_stats = fetch_service.get_stats()
        thinking_stats = thinking_service.get_stats()
        
        print("✅ Service statistics retrieved")
        print(f"   Fetch service - Total requests: {fetch_stats['total_requests']}")
        print(f"   Fetch service - Success rate: {fetch_stats['success_rate']:.2%}")
        print(f"   Thinking service - Total processes: {thinking_stats['total_processes']}")
        print(f"   Thinking service - Success rate: {thinking_stats['success_rate']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Service statistics test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting Enhanced Fetch Service Tests")
    print("=" * 60)
    
    # Run all tests
    tests = [
        test_basic_fetch,
        test_timeout_handling,
        test_circuit_breaker,
        test_fallback_urls,
        test_multiple_urls,
        test_sequential_thinking,
        test_sequential_thinking_timeout,
        test_service_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced fetch services are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
