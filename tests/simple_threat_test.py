#!/usr/bin/env python3
"""
Simple threat assessment test
"""

import requests
import json
import time

def test_threat_assessment():
    """Test basic threat assessment functionality."""
    base_url = "http://localhost:8004"
    
    print("🔍 Testing Threat Assessment System")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/threat-assessment/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Simple analysis
    print("\n2. Testing simple analysis...")
    test_data = {
        "content": "This is a test message with potential security implications.",
        "domain": "intelligence",
        "language": "en",
        "metadata": {"test": True}
    }
    
    try:
        response = requests.post(
            f"{base_url}/threat-assessment/analyze",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Analysis successful")
            result = response.json()
            print(f"   Assessment ID: {result.get('assessment_id', 'N/A')}")
            print(f"   Overall Severity: {result.get('overall_severity', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print(f"   Indicators: {result.get('summary', {}).get('total_indicators', 0)}")
            print(f"   Warnings: {result.get('summary', {}).get('total_warnings', 0)}")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

if __name__ == "__main__":
    print("Simple Threat Assessment Test")
    print("=" * 40)
    
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(5)
    
    success = test_threat_assessment()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Threat Assessment System is working!")
    else:
        print("❌ Threat Assessment System has issues.")
        print("Please check the server logs and configuration.")
