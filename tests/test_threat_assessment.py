#!/usr/bin/env python3
"""
Test script for Threat Assessment Warning Indicators Deception Analysis

This script tests the comprehensive threat assessment system including:
- Multi-domain threat assessment (defense, intelligence, business, cybersecurity, etc.)
- Linguistic deception detection
- Strategic deception identification
- Cultural deception pattern recognition
- Domain-specific threat detection
- Warning indicator generation
- Real-time threat monitoring
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any

# Test configuration
BASE_URL = "http://localhost:8004"
API_BASE = f"{BASE_URL}/threat-assessment"

# Test data for different domains
TEST_DATA = {
    "defense": {
        "content": "The strategic deployment of forces in the region indicates immediate threat assessment is required. Officials say the situation is critical and urgent action must be taken. However, we should focus on diplomatic solutions, not military escalation.",
        "domain": "defense",
        "language": "en"
    },
    "intelligence": {
        "content": "Perhaps there might be some intelligence sources indicating possible threats. I'm not sure about the exact details, but experts say we should be concerned. To be honest, the situation seems like it could be serious.",
        "domain": "intelligence",
        "language": "en"
    },
    "business": {
        "content": "The market volatility and regulatory uncertainty suggest potential business risks. Revenue growth appears to be slowing, and stakeholders are concerned about the company's strategic position.",
        "domain": "business",
        "language": "en"
    },
    "cybersecurity": {
        "content": "We've detected multiple malware infections and potential APT activity. The breach appears to be sophisticated, and we need immediate response to prevent data exfiltration.",
        "domain": "cybersecurity",
        "language": "en"
    },
    "geopolitical": {
        "content": "The geopolitical tensions in the region are escalating rapidly. International relations seem to be deteriorating, and there are concerns about potential conflicts.",
        "domain": "geopolitical",
        "language": "en"
    },
    "chinese_strategic": {
        "content": "和谐发展是重要的战略目标。我们需要和平合作来实现共赢。传统文化和历史告诉我们稳定安全的重要性。",
        "domain": "intelligence",
        "language": "zh"
    },
    "russian_strategic": {
        "content": "Безопасность и стабильность являются приоритетами. Развитие и прогресс требуют защиты и обороны. Традиции и культура важны для порядка.",
        "domain": "intelligence",
        "language": "ru"
    }
}

def test_health_check():
    """Test threat assessment service health check."""
    print("🔍 Testing threat assessment health check...")
    
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   - Total indicators: {data.get('total_indicators', 0)}")
            print(f"   - Total warnings: {data.get('total_warnings', 0)}")
            print(f"   - Total patterns: {data.get('total_patterns', 0)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_domains():
    """Test getting supported domains."""
    print("\n🔍 Testing supported domains...")
    
    try:
        response = requests.get(f"{API_BASE}/domains")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Domains retrieved: {len(data['domains'])} domains")
            for domain, description in data['descriptions'].items():
                print(f"   - {domain}: {description}")
            return True
        else:
            print(f"❌ Domains test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Domains test error: {e}")
        return False

def test_capabilities():
    """Test getting threat assessment capabilities."""
    print("\n🔍 Testing threat assessment capabilities...")
    
    try:
        response = requests.get(f"{API_BASE}/capabilities")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Capabilities retrieved:")
            print(f"   - Capabilities: {len(data['capabilities'])}")
            print(f"   - Supported data types: {len(data['supported_data_types'])}")
            print(f"   - Supported domains: {len(data['supported_domains'])}")
            print(f"   - Threat types: {len(data['threat_types'])}")
            print(f"   - Severity levels: {len(data['severity_levels'])}")
            return True
        else:
            print(f"❌ Capabilities test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Capabilities test error: {e}")
        return False

def test_single_analysis(domain: str, test_data: Dict[str, Any]):
    """Test single threat assessment analysis."""
    print(f"\n🔍 Testing {domain} domain analysis...")
    
    try:
        response = requests.post(f"{API_BASE}/analyze", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {domain} analysis completed:")
            print(f"   - Assessment ID: {data['assessment_id']}")
            print(f"   - Overall severity: {data['overall_severity']}")
            print(f"   - Confidence: {data['confidence']:.2f}")
            print(f"   - Total indicators: {data['summary']['total_indicators']}")
            print(f"   - Total warnings: {data['summary']['total_warnings']}")
            print(f"   - Total patterns: {data['summary']['total_patterns']}")
            print(f"   - Domains affected: {data['summary']['domains_affected']}")
            
            # Show some indicators
            if data['indicators']:
                print(f"   - Sample indicators:")
                for i, indicator in enumerate(data['indicators'][:3]):
                    print(f"     {i+1}. {indicator['type']} ({indicator['severity']}): {indicator['description']}")
            
            # Show recommendations
            if data['recommendations']:
                print(f"   - Recommendations:")
                for i, rec in enumerate(data['recommendations'][:3]):
                    print(f"     {i+1}. {rec}")
            
            return True
        else:
            print(f"❌ {domain} analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ {domain} analysis error: {e}")
        return False

def test_domain_specific_endpoints():
    """Test domain-specific endpoints."""
    print("\n🔍 Testing domain-specific endpoints...")
    
    domain_endpoints = {
        "defense": "/analyze-defense",
        "intelligence": "/analyze-intelligence",
        "business": "/analyze-business",
        "cybersecurity": "/analyze-cybersecurity",
        "geopolitical": "/analyze-geopolitical"
    }
    
    success_count = 0
    total_count = len(domain_endpoints)
    
    for domain, endpoint in domain_endpoints.items():
        try:
            test_data = {
                "content": TEST_DATA[domain]["content"],
                "language": TEST_DATA[domain]["language"]
            }
            
            response = requests.post(f"{API_BASE}{endpoint}", json=test_data)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {domain} endpoint: {data['overall_severity']} severity")
                success_count += 1
            else:
                print(f"❌ {domain} endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {domain} endpoint error: {e}")
    
    print(f"Domain-specific endpoints: {success_count}/{total_count} successful")
    return success_count == total_count

def test_batch_analysis():
    """Test batch threat assessment analysis."""
    print("\n🔍 Testing batch analysis...")
    
    try:
        batch_data = {
            "contents": [
                TEST_DATA["defense"]["content"],
                TEST_DATA["intelligence"]["content"],
                TEST_DATA["business"]["content"],
                TEST_DATA["cybersecurity"]["content"]
            ],
            "domain": "intelligence",
            "language": "en"
        }
        
        response = requests.post(f"{API_BASE}/analyze-batch", json=batch_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch analysis completed:")
            print(f"   - Total assessments: {data['summary']['total_assessments']}")
            print(f"   - Total indicators: {data['summary']['total_indicators']}")
            print(f"   - Total warnings: {data['summary']['total_warnings']}")
            print(f"   - Total patterns: {data['summary']['total_patterns']}")
            print(f"   - Success rate: {data['summary']['success_rate']:.2f}")
            print(f"   - Domains covered: {data['summary']['domains_covered']}")
            return True
        else:
            print(f"❌ Batch analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Batch analysis error: {e}")
        return False

def test_summary():
    """Test getting threat assessment summary."""
    print("\n🔍 Testing threat assessment summary...")
    
    try:
        response = requests.get(f"{API_BASE}/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Summary retrieved:")
            print(f"   - Total indicators: {data['total_indicators']}")
            print(f"   - Total warnings: {data['total_warnings']}")
            print(f"   - Total patterns: {data['total_patterns']}")
            print(f"   - Domains covered: {data['domains_covered']}")
            print(f"   - Severity distribution: {data['severity_distribution']}")
            return True
        else:
            print(f"❌ Summary test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Summary test error: {e}")
        return False

def test_clear_data():
    """Test clearing threat assessment data."""
    print("\n🔍 Testing clear data...")
    
    try:
        response = requests.post(f"{API_BASE}/clear-data")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Data cleared: {data['message']}")
            return True
        else:
            print(f"❌ Clear data failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Clear data error: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive threat assessment test suite."""
    print("🚀 Starting Comprehensive Threat Assessment Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    tests = [
        ("Health Check", test_health_check),
        ("Supported Domains", test_domains),
        ("Capabilities", test_capabilities),
    ]
    
    # Test individual domain analyses
    for domain, test_data in TEST_DATA.items():
        tests.append((f"{domain.title()} Analysis", 
                     lambda d=domain, td=test_data: test_single_analysis(d, td)))
    
    # Test additional functionality
    tests.extend([
        ("Domain-Specific Endpoints", test_domain_specific_endpoints),
        ("Batch Analysis", test_batch_analysis),
        ("Summary", test_summary),
        ("Clear Data", test_clear_data),
    ])
    
    # Run all tests
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Threat assessment system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the system configuration.")
    
    return passed == total

def test_mcp_integration():
    """Test MCP integration for threat assessment."""
    print("\n🔍 Testing MCP integration...")
    
    try:
        # Test MCP health check
        response = requests.get(f"{BASE_URL}/mcp-health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MCP server health: {data['status']}")
            print(f"   - Strategic assessment: {data.get('strategic_assessment', False)}")
            print(f"   - Strategic analytics: {data.get('strategic_analytics', False)}")
            return True
        else:
            print(f"❌ MCP health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP integration error: {e}")
        return False

if __name__ == "__main__":
    print("Threat Assessment Warning Indicators Deception Analysis Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding. Please start the server first.")
            print("   Run: .venv/Scripts/python.exe main.py")
            exit(1)
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please start the server first.")
        print("   Run: .venv/Scripts/python.exe main.py")
        exit(1)
    
    # Run comprehensive tests
    success = run_comprehensive_test()
    
    # Test MCP integration
    mcp_success = test_mcp_integration()
    
    print("\n" + "=" * 60)
    print("🎯 Final Results:")
    print(f"   - Threat Assessment Tests: {'✅ PASSED' if success else '❌ FAILED'}")
    print(f"   - MCP Integration: {'✅ PASSED' if mcp_success else '❌ FAILED'}")
    
    if success and mcp_success:
        print("\n🎉 All systems operational! Threat assessment system is ready for use.")
    else:
        print("\n⚠️ Some issues detected. Please check the system configuration.")
    
    print("\n📋 Available endpoints:")
    print(f"   - Health: {API_BASE}/health")
    print(f"   - Domains: {API_BASE}/domains")
    print(f"   - Capabilities: {API_BASE}/capabilities")
    print(f"   - Analyze: {API_BASE}/analyze")
    print(f"   - Batch: {API_BASE}/analyze-batch")
    print(f"   - Summary: {API_BASE}/summary")
