#!/usr/bin/env python3
"""
Test enhanced strategic analysis engine initialization.
"""

import asyncio


async def test_engine_init():
    """Test engine initialization."""
    print("🔍 Testing Enhanced Strategic Analysis Engine Initialization")
    print("=" * 60)
    
    try:
        # Import and test engine
        from src.core.enhanced_strategic_analysis_engine import enhanced_strategic_analysis_engine
        
        print("✅ Engine imported successfully")
        print(f"✅ Engine type: {type(enhanced_strategic_analysis_engine)}")
        
        # Test basic functionality
        if hasattr(enhanced_strategic_analysis_engine, 'get_supported_domains'):
            print("✅ get_supported_domains method exists")
            
            # Test the method
            domains = await enhanced_strategic_analysis_engine.get_supported_domains()
            print(f"✅ Supported domains: {domains}")
        else:
            print("❌ get_supported_domains method not found")
        
        if hasattr(enhanced_strategic_analysis_engine, 'analyze_strategic_content'):
            print("✅ analyze_strategic_content method exists")
        else:
            print("❌ analyze_strategic_content method not found")
        
        print("\n🎉 Engine initialization test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Enhanced Strategic Analysis Engine Initialization Test")
    print("=" * 80)
    
    asyncio.run(test_engine_init())
