#!/usr/bin/env python3
"""
Simple Strands test using existing tools.
"""

import asyncio
from loguru import logger

def test_strands_tools():
    """Test if Strands tools can be imported."""
    try:
        from strands_tools import calculator
        logger.info("✅ Strands tools imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Strands tools import failed: {e}")
        logger.info("💡 Try: pip install strands-agents-tools")
        return False

def test_strands_agent():
    """Test if Strands agent can be created."""
    try:
        from strands import Agent
        from strands_tools import calculator
        
        # Create agent with calculator tool
        agent = Agent(tools=[calculator])
        logger.info("✅ Strands agent created successfully with calculator tool")
        return agent
    except Exception as e:
        logger.error(f"❌ Strands agent creation failed: {e}")
        return None

async def test_agent_invocation():
    """Test if agent can be invoked with a simple calculation."""
    try:
        from strands import Agent
        from strands_tools import calculator
        
        # Create agent with calculator tool
        agent = Agent(tools=[calculator])
        
        # Test with a simple calculation
        result = await agent.invoke_async("What is 2 + 2?")
        logger.info(f"✅ Agent invocation successful: {result[:200]}...")
        return True
    except Exception as e:
        logger.error(f"❌ Agent invocation failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Simple Strands Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Import tools
    logger.info("1. Testing Strands tools import...")
    if not test_strands_tools():
        return
    
    # Test 2: Agent creation
    logger.info("2. Testing agent creation...")
    agent = test_strands_agent()
    if not agent:
        return
    
    # Test 3: Agent invocation
    logger.info("3. Testing agent invocation...")
    asyncio.run(test_agent_invocation())
    
    logger.info("✅ All tests completed!")

if __name__ == "__main__":
    main()
