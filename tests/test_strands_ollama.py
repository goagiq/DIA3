#!/usr/bin/env python3
"""
Test Strands with explicit Ollama configuration.
"""

import asyncio
from loguru import logger

def test_strands_ollama():
    """Test Strands with explicit Ollama configuration."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        from strands_tools import calculator
        
        # Create Ollama model with explicit configuration
        ollama_model = OllamaModel(
            host="http://localhost:11434",
            model_id="mistral-small3.1:latest",
            temperature=0.7,
            streaming=False  # Disable streaming to avoid hanging
        )
        
        # Create agent with Ollama model and calculator tool
        agent = Agent(
            name="test_agent",
            system_prompt="You are a helpful assistant.",
            model=ollama_model,
            tools=[calculator]
        )
        
        logger.info("✅ Strands agent created successfully with Ollama model")
        return agent
    except Exception as e:
        logger.error(f"❌ Strands agent creation failed: {e}")
        return None

async def test_agent_invocation():
    """Test if agent can be invoked with Ollama."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        from strands_tools import calculator
        
        # Create Ollama model with explicit configuration
        ollama_model = OllamaModel(
            host="http://localhost:11434",
            model_id="mistral-small3.1:latest",
            temperature=0.7,
            streaming=False  # Disable streaming to avoid hanging
        )
        
        # Create agent with Ollama model and calculator tool
        agent = Agent(
            name="test_agent",
            system_prompt="You are a helpful assistant.",
            model=ollama_model,
            tools=[calculator]
        )
        
        # Test with a simple calculation
        logger.info("Testing agent invocation...")
        result = await agent.invoke_async("What is 2 + 2? Use the calculator tool if needed.")
        logger.info(f"✅ Agent invocation successful: {result[:200]}...")
        return True
    except Exception as e:
        logger.error(f"❌ Agent invocation failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Strands Ollama Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Agent creation with Ollama
    logger.info("1. Testing agent creation with Ollama...")
    agent = test_strands_ollama()
    if not agent:
        return
    
    # Test 2: Agent invocation
    logger.info("2. Testing agent invocation...")
    asyncio.run(test_agent_invocation())
    
    logger.info("✅ All tests completed!")

if __name__ == "__main__":
    main()
