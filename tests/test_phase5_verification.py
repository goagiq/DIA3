"""
Simple verification script for Phase 5: Model Interpretability & Explainable AI
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger


async def verify_phase5_components():
    """Verify Phase 5 components are properly implemented"""
    logger.info("🔍 Verifying Phase 5 components")
    
    try:
        # Test Model Interpretability Engine
        from src.core.interpretability.model_interpretability_engine import ModelInterpretabilityEngine
        engine = ModelInterpretabilityEngine()
        logger.info("✅ Model Interpretability Engine imported successfully")
        
        # Test Intelligence Explanations Engine
        from src.core.interpretability.intelligence_explanations import IntelligenceExplanations
        intel_engine = IntelligenceExplanations()
        logger.info("✅ Intelligence Explanations Engine imported successfully")
        
        # Test Phase 5 MCP Tools
        from src.mcp_servers.phase5_interpretability_mcp_tools import phase5_interpretability_mcp_tools
        logger.info("✅ Phase 5 MCP Tools imported successfully")
        
        # Test Phase 5 API Routes
        from src.api.routes.phase5_interpretability_routes import router
        logger.info("✅ Phase 5 API Routes imported successfully")
        
        logger.info("🎉 All Phase 5 components verified successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Phase 5 component verification failed: {e}")
        return False


async def main():
    """Main verification function"""
    logger.info("🚀 Starting Phase 5 Verification")
    
    success = await verify_phase5_components()
    
    if success:
        logger.info("✅ Phase 5 verification completed successfully!")
    else:
        logger.error("❌ Phase 5 verification failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
