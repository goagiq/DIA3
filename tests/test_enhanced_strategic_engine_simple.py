#!/usr/bin/env python3
"""
Simple test for enhanced strategic analysis engine.
"""

import asyncio
from datetime import datetime


async def test_enhanced_strategic_engine():
    """Test the enhanced strategic analysis engine directly."""
    print("🔍 Testing Enhanced Strategic Analysis Engine")
    print("=" * 60)
    
    try:
        # Import the engine
        from src.core.enhanced_strategic_analysis_engine import enhanced_strategic_analysis_engine
        
        print("✅ Engine imported successfully")
        
        # Test supported domains
        domains = await enhanced_strategic_analysis_engine.get_supported_domains()
        print(f"✅ Supported domains: {domains}")
        
        # Test domain capabilities
        capabilities = await enhanced_strategic_analysis_engine.get_domain_capabilities("defense")
        print(f"✅ Defense capabilities: {capabilities['domain']}")
        
        # Test strategic analysis
        test_content = """
        Russia has announced a reduction in military spending while maintaining 
        strategic nuclear capabilities. The government claims to be withdrawing 
        troops from border regions, but intelligence sources indicate continued 
        military modernization and troop movements.
        """
        
        analysis = await enhanced_strategic_analysis_engine.analyze_strategic_content(
            content=test_content,
            domain="defense",
            language="en",
            analysis_depth="comprehensive"
        )
        
        print(f"✅ Analysis completed:")
        print(f"   - Analysis ID: {analysis.analysis_id}")
        print(f"   - Domain: {analysis.domain}")
        print(f"   - Confidence: {analysis.confidence_score:.2f}")
        print(f"   - Principles detected: {len(analysis.principles_detected)}")
        print(f"   - Strategic moves: {len(analysis.strategic_moves)}")
        print(f"   - Risk level: {analysis.risk_assessment.get('overall_risk_level', 'unknown')}")
        
        # Test history
        history = await enhanced_strategic_analysis_engine.get_analysis_history()
        print(f"✅ Analysis history: {len(history)} entries")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Enhanced Strategic Analysis Engine Test")
    print("=" * 80)
    
    asyncio.run(test_enhanced_strategic_engine())
