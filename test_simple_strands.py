#!/usr/bin/env python3
"""
Simple test to check Strands and Ollama integration.
"""

import asyncio
from loguru import logger

def test_strands_import():
    """Test if Strands can be imported."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        logger.info("✅ Strands imports successful")
        return True
    except ImportError as e:
        logger.error(f"❌ Strands import failed: {e}")
        return False

def test_ollama_model_creation():
    """Test if Ollama model can be created."""
    try:
        from strands.models.ollama import OllamaModel
        
        # Create Ollama model
        ollama_model = OllamaModel(
            host="http://localhost:11434",
            model_id="mistral-small3.1:latest"
        )
        logger.info("✅ Ollama model created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Ollama model creation failed: {e}")
        return False

def test_agent_creation():
    """Test if agent can be created."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        
        # Create Ollama model
        ollama_model = OllamaModel(
            host="http://localhost:11434",
            model_id="mistral-small3.1:latest"
        )
        
        # Create agent
        agent = Agent(
            name="test_agent",
            system_prompt="You are a helpful assistant.",
            model=ollama_model
        )
        logger.info("✅ Agent created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Agent creation failed: {e}")
        return False

async def test_agent_invocation():
    """Test if agent can be invoked."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        
        # Create Ollama model
        ollama_model = OllamaModel(
            host="http://localhost:11434",
            model_id="mistral-small3.1:latest"
        )
        
        # Create agent
        agent = Agent(
            name="test_agent",
            system_prompt="You are a helpful assistant.",
            model=ollama_model
        )
        
        # Test invocation
        result = await agent.invoke_async("Hello, how are you?")
        logger.info(f"✅ Agent invocation successful: {result[:100]}...")
        return True
    except Exception as e:
        logger.error(f"❌ Agent invocation failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Simple Strands Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Import
    logger.info("1. Testing Strands import...")
    if not test_strands_import():
        return
    
    # Test 2: Ollama model creation
    logger.info("2. Testing Ollama model creation...")
    if not test_ollama_model_creation():
        return
    
    # Test 3: Agent creation
    logger.info("3. Testing agent creation...")
    if not test_agent_creation():
        return
    
    # Test 4: Agent invocation
    logger.info("4. Testing agent invocation...")
    asyncio.run(test_agent_invocation())
    
    logger.info("✅ All tests completed!")

if __name__ == "__main__":
    main()
