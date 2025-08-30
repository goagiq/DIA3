#!/usr/bin/env python3
"""
Test script to verify MCP client can call strategic deception monitoring tools.

This script tests the MCP protocol integration for strategic deception monitoring.
"""

import asyncio
import json
import requests
from datetime import datetime
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000"

# Test content with potential deception indicators
TEST_CONTENT = "This deal expires tomorrow and everyone knows it's the best opportunity. Experts say this is the most favorable terms we've ever offered. You must act now or lose this chance forever."

async def test_mcp_initialize():
    """Test MCP initialize method."""
    logger.info("🔍 Testing MCP initialize...")
    
    try:
        # MCP initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test_client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=initialize_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ MCP initialize successful")
            logger.info(f"   Protocol version: {data.get('result', {}).get('protocolVersion')}")
            logger.info(f"   Server info: {data.get('result', {}).get('serverInfo', {}).get('name')}")
            return True
        else:
            logger.error(f"❌ MCP initialize failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP initialize failed: {e}")
        return False

async def test_mcp_tools_list():
    """Test MCP tools/list method."""
    logger.info("🔍 Testing MCP tools/list...")
    
    try:
        # MCP tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=tools_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            tools = data.get('result', {}).get('tools', [])
            logger.info(f"✅ MCP tools/list successful")
            logger.info(f"   Total tools available: {len(tools)}")
            
            # Check for strategic deception tools
            deception_tools = [tool for tool in tools if 'deception' in tool.get('description', '').lower()]
            logger.info(f"   Strategic deception tools: {len(deception_tools)}")
            
            for tool in deception_tools:
                logger.info(f"     - {tool.get('name')}: {tool.get('description')}")
            
            return len(deception_tools) > 0
        else:
            logger.error(f"❌ MCP tools/list failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP tools/list failed: {e}")
        return False

async def test_mcp_tools_call():
    """Test MCP tools/call method for strategic deception monitoring."""
    logger.info("🔍 Testing MCP tools/call for strategic deception...")
    
    try:
        # MCP tools/call request for strategic deception monitoring
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "monitor_strategic_deception",
                "arguments": {
                    "content": TEST_CONTENT,
                    "domain": "business",
                    "monitoring_level": "comprehensive",
                    "alert_threshold": 0.6
                }
            }
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=call_request, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            if result.get('success'):
                logger.info(f"✅ MCP tools/call successful")
                logger.info(f"   Domain: {result.get('domain')}")
                logger.info(f"   Deception score: {result.get('overall_deception_score', 0):.3f}")
                logger.info(f"   Severity level: {result.get('severity_level')}")
                logger.info(f"   Indicators detected: {result.get('indicators_detected', 0)}")
                logger.info(f"   Patterns detected: {result.get('patterns_detected', 0)}")
                logger.info(f"   Critical alerts: {result.get('critical_alerts', 0)}")
                logger.info(f"   High alerts: {result.get('high_alerts', 0)}")
                return True
            else:
                logger.error(f"❌ MCP tools/call failed: {result.get('error')}")
                return False
        else:
            logger.error(f"❌ MCP tools/call failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP tools/call failed: {e}")
        return False

async def test_mcp_domain_deception():
    """Test MCP tools/call for domain-specific deception monitoring."""
    logger.info("🔍 Testing MCP tools/call for domain-specific deception...")
    
    try:
        # MCP tools/call request for domain-specific deception monitoring
        call_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "monitor_domain_deception",
                "arguments": {
                    "content": TEST_CONTENT,
                    "domain": "business",
                    "monitoring_level": "comprehensive",
                    "alert_threshold": 0.6
                }
            }
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=call_request, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            if result.get('success'):
                logger.info(f"✅ MCP domain deception monitoring successful")
                logger.info(f"   Domain: {result.get('domain')}")
                logger.info(f"   Deception score: {result.get('overall_deception_score', 0):.3f}")
                logger.info(f"   Severity level: {result.get('severity_level')}")
                return True
            else:
                logger.error(f"❌ MCP domain deception monitoring failed: {result.get('error')}")
                return False
        else:
            logger.error(f"❌ MCP domain deception monitoring failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP domain deception monitoring failed: {e}")
        return False

async def test_mcp_batch_deception():
    """Test MCP tools/call for batch deception monitoring."""
    logger.info("🔍 Testing MCP tools/call for batch deception monitoring...")
    
    try:
        # MCP tools/call request for batch deception monitoring
        call_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "batch_monitor_deception",
                "arguments": {
                    "contents": [
                        TEST_CONTENT,
                        "Our military capabilities are limited and we pose no threat to any nation.",
                        "I cannot provide specific details about our intelligence operations."
                    ],
                    "domain": "general",
                    "monitoring_level": "standard"
                }
            }
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=call_request, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            if result.get('success'):
                logger.info(f"✅ MCP batch deception monitoring successful")
                logger.info(f"   Batch ID: {result.get('batch_id')}")
                logger.info(f"   Total requests: {result.get('total_requests')}")
                logger.info(f"   Processed requests: {result.get('processed_requests')}")
                logger.info(f"   Failed requests: {result.get('failed_requests')}")
                logger.info(f"   Overall deception score: {result.get('overall_deception_score', 0):.3f}")
                logger.info(f"   Critical alerts: {result.get('critical_alerts', 0)}")
                logger.info(f"   High severity alerts: {result.get('high_severity_alerts', 0)}")
                return True
            else:
                logger.error(f"❌ MCP batch deception monitoring failed: {result.get('error')}")
                return False
        else:
            logger.error(f"❌ MCP batch deception monitoring failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP batch deception monitoring failed: {e}")
        return False

async def test_mcp_dashboard():
    """Test MCP tools/call for deception dashboard."""
    logger.info("🔍 Testing MCP tools/call for deception dashboard...")
    
    try:
        # MCP tools/call request for deception dashboard
        call_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_deception_dashboard",
                "arguments": {
                    "time_range_hours": 24,
                    "domain": None,
                    "severity_filter": None
                }
            }
        }
        
        response = requests.post(f"{MCP_BASE_URL}/", json=call_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            if result.get('success'):
                logger.info(f"✅ MCP deception dashboard successful")
                logger.info(f"   Dashboard ID: {result.get('dashboard_id')}")
                logger.info(f"   Time range: {result.get('time_range', {}).get('start')} to {result.get('time_range', {}).get('end')}")
                logger.info(f"   Total indicators: {result.get('total_indicators')}")
                logger.info(f"   Total patterns: {result.get('total_patterns')}")
                return True
            else:
                logger.error(f"❌ MCP deception dashboard failed: {result.get('error')}")
                return False
        else:
            logger.error(f"❌ MCP deception dashboard failed: HTTP {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP deception dashboard failed: {e}")
        return False

async def main():
    """Run all MCP strategic deception tests."""
    logger.info("🚀 Testing MCP Strategic Deception Monitoring Integration")
    logger.info("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("MCP Initialize", test_mcp_initialize),
        ("MCP Tools List", test_mcp_tools_list),
        ("MCP Strategic Deception Call", test_mcp_tools_call),
        ("MCP Domain Deception", test_mcp_domain_deception),
        ("MCP Batch Deception", test_mcp_batch_deception),
        ("MCP Deception Dashboard", test_mcp_dashboard)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name}...")
        try:
            result = await test_func()
            test_results.append(result)
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            test_results.append(False)
    
    # Calculate results
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 MCP Strategic Deception Test Results")
    logger.info("=" * 60)
    logger.info(f"✅ Passed: {passed_tests}/{total_tests}")
    logger.info(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    logger.info(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        logger.info("\n🎉 All MCP Strategic Deception tests passed!")
        logger.info("✅ MCP client can successfully call strategic deception monitoring tools")
        return True
    else:
        logger.error("\n❌ Some MCP tests failed - MCP integration needs attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
