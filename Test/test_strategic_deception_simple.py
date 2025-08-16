#!/usr/bin/env python3
"""
Simple test script for Strategic Deception Monitoring System

Quick verification of basic strategic deception monitoring functionality.
"""

import asyncio
import json
import requests
from datetime import datetime
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
STRATEGIC_DECEPTION_BASE = f"{API_BASE_URL}/strategic-deception"

# Simple test data
TEST_CONTENT = "This is an immediate emergency requiring urgent action. Experts say this deal expires tomorrow. Everyone knows this is the best opportunity. Focus on the benefits, not the risks."

async def test_strategic_deception_monitoring():
    """Test basic strategic deception monitoring functionality."""
    
    logger.info("🚀 Testing Strategic Deception Monitoring System")
    logger.info("=" * 50)
    
    # Test 1: Health check
    logger.info("Testing health check...")
    try:
        response = requests.get(f"{STRATEGIC_DECEPTION_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Health check passed: {data.get('status')}")
            logger.info(f"   Capabilities: {len(data.get('capabilities', []))}")
            logger.info(f"   Supported domains: {len(data.get('supported_domains', []))}")
        else:
            logger.error(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Basic monitoring
    logger.info("Testing basic deception monitoring...")
    try:
        payload = {
            "content": TEST_CONTENT,
            "domain": "business",
            "language": "en",
            "monitoring_level": "standard",
            "include_cultural_analysis": True,
            "include_behavioral_analysis": True,
            "include_strategic_analysis": True,
            "alert_threshold": 0.7
        }
        
        response = requests.post(
            f"{STRATEGIC_DECEPTION_BASE}/monitor",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Basic monitoring passed")
            logger.info(f"   Domain: {data.get('domain')}")
            logger.info(f"   Deception score: {data.get('overall_deception_score', 0):.3f}")
            logger.info(f"   Severity level: {data.get('severity_level')}")
            logger.info(f"   Indicators detected: {data.get('indicators_detected', 0)}")
            logger.info(f"   Patterns detected: {data.get('patterns_detected', 0)}")
            logger.info(f"   Critical alerts: {data.get('critical_alerts', 0)}")
            
            # Show some indicators if detected
            indicators = data.get('indicators', [])
            if indicators:
                logger.info("   Sample indicators:")
                for i, indicator in enumerate(indicators[:3]):  # Show first 3
                    logger.info(f"     {i+1}. {indicator.get('indicator_type')} - {indicator.get('description')}")
            
            # Show recommendations
            recommendations = data.get('recommendations', [])
            if recommendations:
                logger.info("   Recommendations:")
                for i, rec in enumerate(recommendations[:2]):  # Show first 2
                    logger.info(f"     {i+1}. {rec}")
        else:
            logger.error(f"❌ Basic monitoring failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Basic monitoring failed: {e}")
        return False
    
    # Test 3: Domain-specific endpoint
    logger.info("Testing domain-specific endpoint...")
    try:
        payload = {
            "content": TEST_CONTENT,
            "language": "en",
            "monitoring_level": "standard",
            "include_cultural_analysis": True,
            "include_behavioral_analysis": True,
            "include_strategic_analysis": True,
            "alert_threshold": 0.7
        }
        
        response = requests.post(
            f"{STRATEGIC_DECEPTION_BASE}/business/monitor",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('domain') == 'business':
                logger.info("✅ Domain-specific endpoint passed")
                logger.info(f"   Domain correctly set to: {data.get('domain')}")
            else:
                logger.error(f"❌ Domain-specific endpoint failed: expected 'business', got '{data.get('domain')}'")
                return False
        else:
            logger.error(f"❌ Domain-specific endpoint failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Domain-specific endpoint failed: {e}")
        return False
    
    # Test 4: Dashboard data
    logger.info("Testing dashboard data...")
    try:
        payload = {
            "domain": None,
            "time_range_hours": 24,
            "severity_filter": None,
            "include_patterns": True
        }
        
        response = requests.post(
            f"{STRATEGIC_DECEPTION_BASE}/dashboard",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Dashboard data passed")
            logger.info(f"   Dashboard ID: {data.get('dashboard_id')}")
            logger.info(f"   Total indicators: {data.get('total_indicators')}")
            logger.info(f"   Total patterns: {data.get('total_patterns')}")
        else:
            logger.error(f"❌ Dashboard data failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Dashboard data failed: {e}")
        return False
    
    logger.info("=" * 50)
    logger.info("🎉 All Strategic Deception Monitoring tests passed!")
    return True

async def main():
    """Main test function."""
    try:
        success = await test_strategic_deception_monitoring()
        
        if success:
            logger.info("✅ Strategic Deception Monitoring System is working correctly")
            return 0
        else:
            logger.error("❌ Strategic Deception Monitoring System has issues")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
