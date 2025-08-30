#!/usr/bin/env python3
"""
Simple test script for Language Capabilities Engine.

Tests the core functionality without requiring the full server setup.
"""

import asyncio
import sys
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

ENGLISH_CONTENT = """
Strategic deception and misdirection are key principles in modern warfare.
Understanding cultural context provides significant intelligence advantages.
Language capabilities create operational advantages in multiple domains.
Business intelligence requires cultural understanding for market entry.
"""


async def test_language_capabilities_engine():
    """Test the language capabilities engine."""
    logger.info("🧪 Testing Language Capabilities Engine")
    
    try:
        from src.core.language_capabilities_engine import language_capabilities_engine
        
        # Test 1: Health check
        logger.info("Test 1: Health check")
        health = await language_capabilities_engine.health_check()
        logger.info(f"Health status: {health['status']}")
        
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
        
        # Test 5: Auto language detection
        logger.info("Test 5: Auto language detection")
        auto_result = await language_capabilities_engine.analyze_language_capabilities(
            content=ENGLISH_CONTENT,
            language="auto"
        )
        logger.info(f"Auto detection - Language: {auto_result['language']}")
        
        logger.info("✅ All language capabilities engine tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Language capabilities engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cultural_patterns():
    """Test cultural pattern recognition."""
    logger.info("🧪 Testing Cultural Pattern Recognition")
    
    try:
        from src.core.language_capabilities_engine import language_capabilities_engine
        
        # Test Chinese cultural patterns
        chinese_patterns = language_capabilities_engine._extract_cultural_indicators(
            CHINESE_CONTENT, "zh"
        )
        logger.info(f"Chinese cultural patterns: {chinese_patterns}")
        
        # Test Russian cultural patterns
        russian_patterns = language_capabilities_engine._extract_cultural_indicators(
            RUSSIAN_CONTENT, "ru"
        )
        logger.info(f"Russian cultural patterns: {russian_patterns}")
        
        # Test strategic patterns
        chinese_strategic = language_capabilities_engine._extract_strategic_patterns(
            CHINESE_CONTENT, "zh"
        )
        logger.info(f"Chinese strategic patterns: {chinese_strategic}")
        
        # Test deception indicators
        chinese_deception = language_capabilities_engine._extract_deception_indicators(
            CHINESE_CONTENT, "zh"
        )
        logger.info(f"Chinese deception indicators: {chinese_deception}")
        
        logger.info("✅ All cultural pattern tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Cultural pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_language_detection():
    """Test language detection functionality."""
    logger.info("🧪 Testing Language Detection")
    
    try:
        from src.core.language_capabilities_engine import language_capabilities_engine
        
        # Test Chinese detection
        chinese_detected = language_capabilities_engine._detect_language(CHINESE_CONTENT)
        logger.info(f"Chinese content detected as: {chinese_detected}")
        assert chinese_detected == "zh", f"Expected 'zh', got '{chinese_detected}'"
        
        # Test Russian detection
        russian_detected = language_capabilities_engine._detect_language(RUSSIAN_CONTENT)
        logger.info(f"Russian content detected as: {russian_detected}")
        assert russian_detected == "ru", f"Expected 'ru', got '{russian_detected}'"
        
        # Test English detection
        english_detected = language_capabilities_engine._detect_language(ENGLISH_CONTENT)
        logger.info(f"English content detected as: {english_detected}")
        assert english_detected == "en", f"Expected 'en', got '{english_detected}'"
        
        logger.info("✅ All language detection tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Language detection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting Simple Language Capabilities Tests")
    logger.info("=" * 60)
    
    # Run tests
    tests = [
        ("Language Capabilities Engine", test_language_capabilities_engine),
        ("Cultural Pattern Recognition", test_cultural_patterns),
        ("Language Detection", test_language_detection)
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
