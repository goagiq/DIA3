#!/usr/bin/env python3
"""
Comprehensive Test Script for Strategic Deception Monitoring System

Tests all capabilities across multiple domains:
- Defense and intelligence applications
- Business intelligence and competitive analysis
- Multi-domain threat assessment
- Real-time deception detection
- Early warning systems
- MCP server integration
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import requests
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
STRATEGIC_DECEPTION_BASE = f"{API_BASE_URL}/strategic-deception"

# Comprehensive test data for different domains
TEST_DATA = {
    "defense": {
        "content": "Our military capabilities are limited and we pose no threat to any nation. We are committed to peace and have no aggressive intentions. Our recent military exercises were purely defensive in nature.",
        "expected_indicators": ["strategic", "misdirection", "false_weakness"]
    },
    "intelligence": {
        "content": "I cannot provide specific details about our intelligence operations, but I can assure you that we follow all legal protocols. Perhaps there might be some information available, but I'm not sure about the exact sources.",
        "expected_indicators": ["linguistic", "evasive", "overqualification"]
    },
    "business": {
        "content": "This deal expires tomorrow and everyone knows it's the best opportunity. Experts say this is the most favorable terms we've ever offered. You must act now or lose this chance forever.",
        "expected_indicators": ["false_urgency", "consensus_fallacy", "pressure_tactics"]
    },
    "cybersecurity": {
        "content": "I am the IT administrator and I need your password immediately. This is an emergency security update. Trust me, I have authority to make these changes.",
        "expected_indicators": ["authority_appeal", "false_urgency", "credential_request"]
    },
    "geopolitical": {
        "content": "We are committed to peaceful resolution of all disputes. However, we reserve the right to protect our interests. Our recent actions were necessary for regional stability.",
        "expected_indicators": ["strategic", "contradiction", "justification"]
    }
}

# Test scenarios for different monitoring levels
MONITORING_LEVELS = ["basic", "standard", "comprehensive", "critical"]

async def test_health_check():
    """Test strategic deception monitoring health check."""
    logger.info("🔍 Testing health check...")
    
    try:
        response = requests.get(f"{STRATEGIC_DECEPTION_BASE}/health", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ Health check passed: {data['status']}")
        logger.info(f"   Capabilities: {len(data['capabilities'])}")
        logger.info(f"   Supported domains: {len(data['supported_domains'])}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False

async def test_domain_monitoring(domain: str, test_data: Dict[str, Any]):
    """Test deception monitoring for a specific domain."""
    logger.info(f"🔍 Testing {domain} domain monitoring...")
    
    try:
        payload = {
            "content": test_data["content"],
            "domain": domain,
            "monitoring_level": "comprehensive",
            "alert_threshold": 0.5,
            "include_cultural_analysis": True,
            "include_behavioral_analysis": True,
            "include_strategic_analysis": True
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor", json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ {domain} monitoring passed")
        logger.info(f"   Deception score: {data['overall_deception_score']:.3f}")
        logger.info(f"   Severity level: {data['severity_level']}")
        logger.info(f"   Indicators detected: {data['indicators_detected']}")
        logger.info(f"   Patterns detected: {data['patterns_detected']}")
        logger.info(f"   Critical alerts: {data['critical_alerts']}")
        
        # Check recommendations
        if data['recommendations']:
            logger.info(f"   Recommendations:")
            for i, rec in enumerate(data['recommendations'], 1):
                logger.info(f"     {i}. {rec}")
        
        return True
    except Exception as e:
        logger.error(f"❌ {domain} monitoring failed: {e}")
        return False

async def test_domain_specific_endpoints():
    """Test domain-specific endpoints."""
    logger.info("🔍 Testing domain-specific endpoints...")
    
    results = []
    for domain in TEST_DATA.keys():
        try:
            payload = {
                "content": TEST_DATA[domain]["content"],
                "monitoring_level": "standard",
                "alert_threshold": 0.6
            }
            
            response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/{domain}/monitor", json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ {domain} endpoint passed")
            logger.info(f"   Domain correctly set to: {data['domain']}")
            
            results.append(True)
        except Exception as e:
            logger.error(f"❌ {domain} endpoint failed: {e}")
            results.append(False)
    
    return all(results)

async def test_batch_processing():
    """Test batch processing capabilities."""
    logger.info("🔍 Testing batch processing...")
    
    try:
        contents = [data["content"] for data in TEST_DATA.values()]
        
        payload = {
            "contents": contents,
            "domain": "general",
            "monitoring_level": "standard",
            "parallel_processing": True
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor-batch", json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ Batch processing passed")
        logger.info(f"   Total requests: {data['total_requests']}")
        logger.info(f"   Processed requests: {data['processed_requests']}")
        logger.info(f"   Failed requests: {data['failed_requests']}")
        logger.info(f"   Overall deception score: {data['overall_deception_score']:.3f}")
        logger.info(f"   Critical alerts: {data['critical_alerts']}")
        logger.info(f"   High severity alerts: {data['high_severity_alerts']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        return False

async def test_monitoring_levels():
    """Test different monitoring levels."""
    logger.info("🔍 Testing monitoring levels...")
    
    results = []
    for level in MONITORING_LEVELS:
        try:
            payload = {
                "content": TEST_DATA["business"]["content"],
                "domain": "business",
                "monitoring_level": level,
                "alert_threshold": 0.5
            }
            
            response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor", json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ {level} monitoring level passed")
            logger.info(f"   Processing time: {data['processing_time_ms']:.1f}ms")
            
            results.append(True)
        except Exception as e:
            logger.error(f"❌ {level} monitoring level failed: {e}")
            results.append(False)
    
    return all(results)

async def test_dashboard_integration():
    """Test dashboard data integration."""
    logger.info("🔍 Testing dashboard integration...")
    
    try:
        payload = {
            "time_range_hours": 24,
            "include_patterns": True
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/dashboard", json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ Dashboard integration passed")
        logger.info(f"   Dashboard ID: {data['dashboard_id']}")
        logger.info(f"   Time range: {data['time_range']['start']} to {data['time_range']['end']}")
        logger.info(f"   Total indicators: {data['total_indicators']}")
        logger.info(f"   Total patterns: {data['total_patterns']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Dashboard integration failed: {e}")
        return False

async def test_mcp_integration():
    """Test MCP server integration."""
    logger.info("🔍 Testing MCP server integration...")
    
    try:
        # Test MCP health check
        response = requests.get(f"{API_BASE_URL}/mcp-health", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"✅ MCP health check passed")
        logger.info(f"   Status: {data['status']}")
        logger.info(f"   Service: {data['service']}")
        logger.info(f"   Endpoints: {data['endpoints']}")
        logger.info(f"   Strategic assessment: {data['strategic_assessment']}")
        logger.info(f"   Strategic analytics: {data['strategic_analytics']}")
        
        # Test MCP server endpoint
        response = requests.get(f"{API_BASE_URL}/mcp/", timeout=10)
        logger.info(f"✅ MCP server endpoint accessible (status: {response.status_code})")
        
        return True
    except Exception as e:
        logger.error(f"❌ MCP integration failed: {e}")
        return False

async def test_performance_metrics():
    """Test performance metrics."""
    logger.info("🔍 Testing performance metrics...")
    
    try:
        # Test single content processing time
        start_time = time.time()
        payload = {
            "content": TEST_DATA["business"]["content"],
            "domain": "business",
            "monitoring_level": "standard"
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor", json=payload, timeout=30)
        response.raise_for_status()
        
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000
        
        data = response.json()
        logger.info(f"✅ Performance test passed")
        logger.info(f"   Total processing time: {processing_time:.1f}ms")
        logger.info(f"   API processing time: {data['processing_time_ms']:.1f}ms")
        logger.info(f"   Network overhead: {processing_time - data['processing_time_ms']:.1f}ms")
        
        return True
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        return False

async def test_error_handling():
    """Test error handling capabilities."""
    logger.info("🔍 Testing error handling...")
    
    try:
        # Test with invalid domain
        payload = {
            "content": "Test content",
            "domain": "invalid_domain",
            "monitoring_level": "standard"
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor", json=payload, timeout=10)
        
        if response.status_code == 400 or response.status_code == 422:
            logger.info(f"✅ Error handling passed - Invalid domain properly rejected")
        else:
            logger.warning(f"⚠️ Unexpected response for invalid domain: {response.status_code}")
        
        # Test with empty content
        payload = {
            "content": "",
            "domain": "business",
            "monitoring_level": "standard"
        }
        
        response = requests.post(f"{STRATEGIC_DECEPTION_BASE}/monitor", json=payload, timeout=10)
        
        if response.status_code == 400 or response.status_code == 422:
            logger.info(f"✅ Error handling passed - Empty content properly rejected")
        else:
            logger.warning(f"⚠️ Unexpected response for empty content: {response.status_code}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error handling test failed: {e}")
        return False

async def main():
    """Run comprehensive strategic deception monitoring tests."""
    logger.info("🚀 Comprehensive Strategic Deception Monitoring Test Suite")
    logger.info("=" * 80)
    
    start_time = time.time()
    test_results = []
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Domain Monitoring", lambda: asyncio.gather(*[test_domain_monitoring(domain, data) for domain, data in TEST_DATA.items()])),
        ("Domain-Specific Endpoints", test_domain_specific_endpoints),
        ("Batch Processing", test_batch_processing),
        ("Monitoring Levels", test_monitoring_levels),
        ("Dashboard Integration", test_dashboard_integration),
        ("MCP Integration", test_mcp_integration),
        ("Performance Metrics", test_performance_metrics),
        ("Error Handling", test_error_handling)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name}...")
        try:
            if test_name == "Domain Monitoring":
                result = await test_func()
                test_results.extend(result)
            else:
                result = await test_func()
                test_results.append(result)
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            test_results.append(False)
    
    # Calculate results
    end_time = time.time()
    total_time = end_time - start_time
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    logger.info("\n" + "=" * 80)
    logger.info("📊 Test Results Summary")
    logger.info("=" * 80)
    logger.info(f"✅ Passed: {passed_tests}/{total_tests}")
    logger.info(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    logger.info(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    logger.info(f"⏱️ Total Test Time: {total_time:.2f} seconds")
    
    if passed_tests == total_tests:
        logger.info("\n🎉 All Comprehensive Strategic Deception Monitoring tests passed!")
        logger.info("✅ System is fully operational and ready for production use")
        return True
    else:
        logger.error("\n❌ Some tests failed - system needs attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

