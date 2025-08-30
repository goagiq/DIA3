#!/usr/bin/env python3
"""
Test script to verify pattern storage system is working correctly.
"""

import asyncio
from src.core.pattern_recognition.pattern_storage import PatternStorage


async def test_pattern_storage():
    """Test the pattern storage system."""
    print("Testing Pattern Storage System...")
    
    # Initialize pattern storage
    ps = PatternStorage()
    print("✓ Pattern storage initialized")
    
    # Test storing a pattern
    test_pattern = {
        "test_id": "test_pattern_001",
        "data": {"key": "value", "number": 42},
        "description": "Test pattern for verification"
    }
    
    result = await ps.store_pattern(
        pattern_id="test_pattern_001",
        pattern_data=test_pattern,
        pattern_type="test",
        metadata={"test": True, "created_by": "test_script"}
    )
    
    print(f"✓ Pattern stored: {result}")
    
    # Test retrieving the pattern
    retrieved = await ps.get_pattern("test_pattern_001")
    print(f"✓ Pattern retrieved: {retrieved['pattern']['pattern_id']}")
    
    # Test listing patterns
    patterns = await ps.list_patterns()
    print(f"✓ Patterns listed: {len(patterns)} patterns found")
    
    # Test pattern search
    search_results = await ps.search_patterns("test")
    print(f"✓ Pattern search: {len(search_results)} results found")
    
    print("\n🎉 All pattern storage tests passed!")


if __name__ == "__main__":
    asyncio.run(test_pattern_storage())
