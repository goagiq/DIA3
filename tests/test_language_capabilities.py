#!/usr/bin/env python3
"""
Test script for Language Capabilities Engine.

Tests the comprehensive language capabilities engine that provides strategic advantages
across multiple domains including defense, intelligence, business, and cybersecurity.
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from loguru import logger

# Test content samples
CHINESE_CONTENT = """
孙子兵法是中国古代军事理论的经典著作，体现了深刻的战略思想。
知己知彼，百战不殆。不战而屈人之兵，善之善者也。
上兵伐谋，其次伐交，其次伐兵，其下攻城。
虚虚实实，真真假假，声东击西，调虎离山。
和谐发展，和平合作，共赢未来。
"""

RUSSIAN_CONTENT = """
Война и мир - это великий роман Льва Толстого о наполеоновских войнах.
Безопасность и стабильность являются важными принципами.
Развитие и прогресс требуют модернизации.
Традиция и культура формируют историю.
Защита и оборона обеспечивают силу.
"""

ARABIC_CONTENT = """
السلام والتنمية والتعاون من المبادئ المهمة.
الأمن والاستقرار ضروريان للتقدم.
التقاليد والثقافة تشكل التاريخ.
الحماية والدفاع يضمنان القوة.
"""

ENGLISH_CONTENT = """
Strategic deception and misdirection are key principles in modern warfare.
Understanding cultural context provides significant intelligence advantages.
Language capabilities create operational advantages in multiple domains.
Business intelligence requires cultural understanding for market entry.
"""


async def test_language_capabilities_engine():
    """Test the language capabilities engine."""
    logger.info("🧪 Starting Language Capabilities Engine Tests")
    
    try:
        from src.core.language_capabilities_engine import language_capabilities_engine
        
        # Test 1: Health check
        logger.info("Test 1: Health check")
        health = await language_capabilities_engine.health_check()
        logger.info(f"Health status: {health['status']}")
        assert health['status'] in ['healthy', 'degraded'], f"Unexpected health status: {health['status']}"
        
        # Test 2: Get capabilities summary
        logger.info("Test 2: Get capabilities summary")
        summary = await language_capabilities_engine.get_capabilities_summary()
        logger.info(f"Total capabilities: {summary['total_capabilities']}")
        logger.info(f"Total advantages: {summary['total_advantages']}")
        logger.info(f"Supported languages: {summary['supported_languages']}")
        logger.info(f"Domains: {summary['domains']}")
        
        # Test 3: Analyze Chinese content
        logger.info("Test 3: Analyze Chinese content")
        chinese_result = await language_capabilities_engine.analyze_language_capabilities(
            content=CHINESE_CONTENT,
            language="zh"
        )
        logger.info(f"Chinese analysis - Language: {chinese_result['language']}")
        logger.info(f"Chinese analysis - Capabilities: {len(chinese_result['capabilities_identified'])}")
        logger.info(f"Chinese analysis - Advantages: {len(chinese_result['strategic_advantages'])}")
        
        # Test 4: Analyze Russian content
        logger.info("Test 4: Analyze Russian content")
        russian_result = await language_capabilities_engine.analyze_language_capabilities(
            content=RUSSIAN_CONTENT,
            language="ru"
        )
        logger.info(f"Russian analysis - Language: {russian_result['language']}")
        logger.info(f"Russian analysis - Capabilities: {len(russian_result['capabilities_identified'])}")
        logger.info(f"Russian analysis - Advantages: {len(russian_result['strategic_advantages'])}")
        
        # Test 5: Analyze Arabic content
        logger.info("Test 5: Analyze Arabic content")
        arabic_result = await language_capabilities_engine.analyze_language_capabilities(
            content=ARABIC_CONTENT,
            language="ar"
        )
        logger.info(f"Arabic analysis - Language: {arabic_result['language']}")
        logger.info(f"Arabic analysis - Capabilities: {len(arabic_result['capabilities_identified'])}")
        logger.info(f"Arabic analysis - Advantages: {len(arabic_result['strategic_advantages'])}")
        
        # Test 6: Auto language detection
        logger.info("Test 6: Auto language detection")
        auto_result = await language_capabilities_engine.analyze_language_capabilities(
            content=ENGLISH_CONTENT,
            language="auto"
        )
        logger.info(f"Auto detection - Language: {auto_result['language']}")
        
        logger.info("✅ All language capabilities engine tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Language capabilities engine test failed: {e}")
        return False


async def test_api_endpoints():
    """Test the API endpoints."""
    logger.info("🧪 Starting API Endpoints Tests")
    
    try:
        import httpx
        
        # Test base URL
        base_url = "http://localhost:8003"
        
        # Test 1: Health check
        logger.info("Test 1: API health check")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/language-capabilities/health")
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            health_data = response.json()
            logger.info(f"API health status: {health_data['health']['status']}")
        
        # Test 2: Get capabilities summary
        logger.info("Test 2: Get capabilities summary")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/language-capabilities/capabilities")
            assert response.status_code == 200, f"Capabilities summary failed: {response.status_code}"
            summary_data = response.json()
            logger.info(f"Total capabilities: {summary_data['summary']['total_capabilities']}")
        
        # Test 3: Analyze Chinese content via API
        logger.info("Test 3: Analyze Chinese content via API")
        async with httpx.AsyncClient() as client:
            request_data = {
                "content": CHINESE_CONTENT,
                "language": "zh"
            }
            response = await client.post(
                f"{base_url}/language-capabilities/analyze",
                json=request_data
            )
            assert response.status_code == 200, f"Chinese analysis failed: {response.status_code}"
            result_data = response.json()
            logger.info(f"Chinese analysis - Language: {result_data['language']}")
            logger.info(f"Chinese analysis - Capabilities: {len(result_data['capabilities_identified'])}")
        
        # Test 4: Defense domain analysis
        logger.info("Test 4: Defense domain analysis")
        async with httpx.AsyncClient() as client:
            request_data = {
                "content": CHINESE_CONTENT,
                "language": "zh",
                "domain": "defense"
            }
            response = await client.post(
                f"{base_url}/language-capabilities/defense/analyze",
                json=request_data
            )
            assert response.status_code == 200, f"Defense analysis failed: {response.status_code}"
            result_data = response.json()
            logger.info(f"Defense analysis - Advantages: {len(result_data['strategic_advantages'])}")
        
        # Test 5: Intelligence domain analysis
        logger.info("Test 5: Intelligence domain analysis")
        async with httpx.AsyncClient() as client:
            request_data = {
                "content": RUSSIAN_CONTENT,
                "language": "ru",
                "domain": "intelligence"
            }
            response = await client.post(
                f"{base_url}/language-capabilities/intelligence/analyze",
                json=request_data
            )
            assert response.status_code == 200, f"Intelligence analysis failed: {response.status_code}"
            result_data = response.json()
            logger.info(f"Intelligence analysis - Advantages: {len(result_data['strategic_advantages'])}")
        
        # Test 6: Business domain analysis
        logger.info("Test 6: Business domain analysis")
        async with httpx.AsyncClient() as client:
            request_data = {
                "content": ENGLISH_CONTENT,
                "language": "en",
                "domain": "business"
            }
            response = await client.post(
                f"{base_url}/language-capabilities/business/analyze",
                json=request_data
            )
            assert response.status_code == 200, f"Business analysis failed: {response.status_code}"
            result_data = response.json()
            logger.info(f"Business analysis - Advantages: {len(result_data['strategic_advantages'])}")
        
        # Test 7: Cybersecurity domain analysis
        logger.info("Test 7: Cybersecurity domain analysis")
        async with httpx.AsyncClient() as client:
            request_data = {
                "content": CHINESE_CONTENT,
                "language": "zh",
                "domain": "cybersecurity"
            }
            response = await client.post(
                f"{base_url}/language-capabilities/cybersecurity/analyze",
                json=request_data
            )
            assert response.status_code == 200, f"Cybersecurity analysis failed: {response.status_code}"
            result_data = response.json()
            logger.info(f"Cybersecurity analysis - Advantages: {len(result_data['strategic_advantages'])}")
        
        # Test 8: Get supported languages
        logger.info("Test 8: Get supported languages")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/language-capabilities/supported-languages")
            assert response.status_code == 200, f"Supported languages failed: {response.status_code}"
            languages_data = response.json()
            logger.info(f"Supported languages: {languages_data['supported_languages']}")
        
        # Test 9: Get supported domains
        logger.info("Test 9: Get supported domains")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/language-capabilities/supported-domains")
            assert response.status_code == 200, f"Supported domains failed: {response.status_code}"
            domains_data = response.json()
            logger.info(f"Supported domains: {domains_data['supported_domains']}")
        
        # Test 10: Batch analysis
        logger.info("Test 10: Batch analysis")
        async with httpx.AsyncClient() as client:
            batch_requests = [
                {"content": CHINESE_CONTENT, "language": "zh"},
                {"content": RUSSIAN_CONTENT, "language": "ru"},
                {"content": ARABIC_CONTENT, "language": "ar"}
            ]
            response = await client.post(
                f"{base_url}/language-capabilities/batch/analyze",
                json=batch_requests
            )
            assert response.status_code == 200, f"Batch analysis failed: {response.status_code}"
            batch_data = response.json()
            logger.info(f"Batch analysis - Total: {batch_data['total_requests']}")
            logger.info(f"Batch analysis - Successful: {batch_data['successful_analyses']}")
        
        logger.info("✅ All API endpoint tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ API endpoint test failed: {e}")
        return False


async def test_mcp_integration():
    """Test MCP integration."""
    logger.info("🧪 Starting MCP Integration Tests")
    
    try:
        import httpx
        
        # Test MCP server on port 8000
        mcp_url = "http://localhost:8000"
        
        # Test 1: MCP health check
        logger.info("Test 1: MCP health check")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{mcp_url}/health")
            assert response.status_code == 200, f"MCP health check failed: {response.status_code}"
            health_data = response.json()
            logger.info(f"MCP health status: {health_data.get('status', 'unknown')}")
        
        # Test 2: MCP initialize
        logger.info("Test 2: MCP initialize")
        async with httpx.AsyncClient() as client:
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "language_capabilities_test",
                        "version": "1.0.0"
                    }
                }
            }
            response = await client.post(mcp_url, json=initialize_request)
            assert response.status_code == 200, f"MCP initialize failed: {response.status_code}"
            init_data = response.json()
            logger.info(f"MCP initialize result: {init_data.get('result', {}).get('capabilities', {})}")
        
        # Test 3: MCP tools/list
        logger.info("Test 3: MCP tools/list")
        async with httpx.AsyncClient() as client:
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            response = await client.post(mcp_url, json=tools_request)
            assert response.status_code == 200, f"MCP tools/list failed: {response.status_code}"
            tools_data = response.json()
            tools = tools_data.get('result', {}).get('tools', [])
            logger.info(f"MCP tools available: {len(tools)}")
            
            # Check for language capabilities related tools
            tool_names = [tool.get('name', '') for tool in tools]
            logger.info(f"Tool names: {tool_names}")
        
        logger.info("✅ All MCP integration tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP integration test failed: {e}")
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting Comprehensive Language Capabilities Tests")
    logger.info("=" * 60)
    
    # Wait for server to start
    logger.info("⏳ Waiting 30 seconds for server to start...")
    await asyncio.sleep(30)
    
    # Run tests
    tests = [
        ("Language Capabilities Engine", test_language_capabilities_engine),
        ("API Endpoints", test_api_endpoints),
        ("MCP Integration", test_mcp_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    logger.info(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        logger.info("🎉 All tests passed! Language capabilities engine is working correctly.")
    else:
        logger.error("⚠️ Some tests failed. Please check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
